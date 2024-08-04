import time
from pathlib import Path
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import PromptTemplate
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from pinecone import Pinecone, ServerlessSpec  
from utilities.general import environment_reader


environment = environment_reader(env_file='./.env')

class GenericTextLoader:

    OPENAI_API_KEY = environment['OPENAI_API_KEY']

    def __init__(self, source_document: str, document_type: str) -> None:
        self.source_document = Path(source_document)
        self.document_type = document_type
        self._document_loader = None
        self._document = None
        self._processed_document: list[str] = None

    def _initiate_loader(self):

        if self.document_type == 'txt':
            self._document_loader = TextLoader(file_path=self.source_document)
        
        if self.document_type == 'pdf':
            self._document_loader = PyMuPDFLoader(file_path=self.source_document)

    def read_document(self):

        assert self.source_document is not None, 'No document to read.'
        assert self.document_type is not None, 'No document type.'

        self._initiate_loader()
        self._document = self._document_loader.load()

    def get_document(self) -> list[str]:

        assert self._document is not None, 'No document to return.'

        return self._document


class TextSplitter:

    def __init__(self, chunk_size: int = 384, document: list[str] = None) -> None:
        self.chunk_size = chunk_size
        self.document = document
        self._splitter = None
        self._converted_document = None

    def _instantiate_splitter(self):
        self._splitter = RecursiveCharacterTextSplitter(
            separators=['\n'],
            chunk_size=self.chunk_size, 
            chunk_overlap=0
        )
    def _split_document(self):
        self._converted_document = self._splitter.split_documents(
            self.document
        )

    def split_document(self):
        
        assert len(self.document) > 0, 'Document size 0'
        
        self._instantiate_splitter()
        self._split_document()

    def get_converted_document(self):

        assert self._converted_document is not None, 'No split document.'
    
        return self._converted_document
    

class GenericEmbedder:

    OPENAI_API_KEY = environment['OPENAI_API_KEY']
    PINECONE_PROJECT_INDEX = environment['PINECONE_PROJECT_INDEX']

    def __init__(self, pieces_of_text: list[str]) -> None:
        self.pieces_of_texts = pieces_of_text
        self._embedder = None
        self._vector_store = None

class OpenAIEmbedder(GenericEmbedder):

    PINECONE_API_KEY = environment['PINECONE_API_KEY']

    def __init__(self, pieces_of_text: list[str]) -> None:
        super().__init__(pieces_of_text)

    def _initialize_embedder(self):

        self._embedder = OpenAIEmbeddings(
            openai_api_key=self.OPENAI_API_KEY
        )

    def _initialize_vector_store(self):

        pc = Pinecone(api_key=self.PINECONE_API_KEY)  
        spec = ServerlessSpec(cloud='aws', region='us-east-1')  
        # check for and delete index if already exists  
        index_name = 'massage-bot'  
        if index_name in pc.list_indexes().names():  
            pc.delete_index(index_name)  
        # create a new index  
        pc.create_index(  
            index_name,  
            dimension=1536,  # dimensionality of text-embedding-ada-002  
            metric='dotproduct',  
            spec=spec  
        )  
        # Ensure that the index is initialized.
        while not pc.describe_index(index_name).status['ready']:  
            time.sleep(1) 

        self._vector_store = PineconeVectorStore(
            index_name=self.PINECONE_PROJECT_INDEX, 
            embedding=self._embedder
        )

    def _embed(self):
        self._vector_store.add_documents(self.pieces_of_texts)

    def embed(self):

        self._initialize_embedder()
        self._initialize_vector_store()
        self._embed()


class Rag:

    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI()
    vector_store = PineconeVectorStore(
        index_name=environment["PINECONE_PROJECT_INDEX"], embedding=embeddings
    )

    query = """Provide me with a detailed insight on how to perform
        sport massage of the deltoid muscle? Limit your answer to
        768 characters.
    """

    def __init__(self, augmented: bool = False) -> None:
        self.augmented = augmented
        self._chain = None
        self._augmented_chain = None
        self._raw_output = None
        self._output = None

    def _instantiate_chain(self):
        self._chain = \
            PromptTemplate.from_template(template=self.query) | self.llm
        
    def _instantiate_augmented_chain(self):
        combine_docs_chain = create_stuff_documents_chain(
            self.llm, hub.pull("langchain-ai/retrieval-qa-chat")
        )
        self._augmented_chain = create_retrieval_chain(
            retriever=self.vector_store.as_retriever(), 
            combine_docs_chain=combine_docs_chain
        )

    def invoke_chain(self):

        if self.augmented:
            self._raw_output = self._augmented_chain.invoke(
                input={"input": self.query}
            )
            self._output = self._raw_output['answer']
    
        else: 
            self._raw_output = self._chain.invoke(input={})
            self._output = self._raw_output.content
    
    def get_output(self):
        
        assert self._output is not None

        return self._output






