import time
from pathlib import Path
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI, OpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from pinecone import Pinecone, ServerlessSpec  
from utilities.general import environment_reader
from langchain.chains import create_history_aware_retriever
from langchain_core.messages import AIMessage, HumanMessage

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

        self._embedder = OpenAIEmbeddings(openai_api_key=self.OPENAI_API_KEY)

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

class FAISSEmbedder(GenericEmbedder):

    def __init__(self, 
                 pieces_of_text: list[str], 
                 local_database: str = None,
                 database_name: str = None) -> None:
        super().__init__(pieces_of_text)
        self.local_database = local_database
        self.database_name = database_name

    def _initialize_embedder(self):

        self._embedder = OpenAIEmbeddings(openai_api_key=self.OPENAI_API_KEY)
    
    def _create_vector_database(self):
        self._vector_store = FAISS.from_documents(
            self.pieces_of_texts,
            self._embedder
        )

    def create_vector_database(self):

        self._initialize_embedder()
        self._create_vector_database()

    def save_vector_database(self):
        self._vector_store.save_local(
            folder_path=self.local_database,
            index_name=self.database_name
        )

    def get_vector_store(self):

        return FAISS.load_local(
            self.local_database, 
            index_name=self.database_name, 
            embeddings=self._embedder,
            allow_dangerous_deserialization=True
        )
    

class Rag:

    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI()
    vector_store = PineconeVectorStore(
        index_name=environment["PINECONE_PROJECT_INDEX"], embedding=embeddings
    )

    query = """Provide me with a detailed insight on how to perform
        sport massage of the gluteus maximus muscle. Split your answer 
        into paragraphs of 192 characters. Mark the end of each 
        paragraph with two line brakes `\n\n`. It is very important to 
        split your answer into paragraphs. Do not put all sentences 
        together, and always use `\n\n` to end the paragraph.
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
            self._instantiate_augmented_chain()
            self._raw_output = self._augmented_chain.invoke(
                input={"input": self.query}
            )
            self._output = self._raw_output['answer']
    
        else: 
            self._instantiate_chain()
            self._raw_output = self._chain.invoke(input={})
            self._output = self._raw_output.content
    
    def get_output(self):
        
        assert self._output is not None

        return self._output


class RAGChatBot:

    llm = OpenAI()

    system_prompt = (
        "You are an expert in massage therapy. I will ask you questions"
        "how to do a specific massage. Provide me with a detailed answer"
        "on how to perform that specific massage. Split your answer" 
        "into paragraphs of 192 characters. Mark the end of each" 
        "paragraph with two line brakes `\n\n`. It is very important to "
        "split your answer into paragraphs. Do not put all sentences" 
        "together, and always use `\n\n` to end the paragraph."
        "Use the following information to answer the question." 
        "If you don't know the answer, say that you don't know."
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    context_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    context_prompt = ChatPromptTemplate.from_messages([
        ("system", context_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])
     
    def __init__(self, vector_database) -> None:
        self.vector_database = vector_database
        self.history = []
        self._documents_chain = None
        self._retrieval_chain = None
        self._raw_output = None
        self._response = None
        self._history_aware_retriever = None

    def _initialize_retriever(self):
        self._history_aware_retriever = create_history_aware_retriever(
            self.llm, self.vector_database.as_retriever(), self.context_prompt
        )

    def _initialize_documents_chain(self):
        self._documents_chain = create_stuff_documents_chain(
            llm=self.llm, prompt=self.prompt
        )


    def _initialize_retrieval_chain(self):
        self._retrieval_chain = create_retrieval_chain(
            self._history_aware_retriever,
            self._documents_chain
        )
    
    def _invoke_chain(self, user_input: str = None):
        self._raw_output = self._retrieval_chain.invoke(
            {"input": user_input, "chat_history": self.history}
        )
    
    def _extract_response(self):

        assert self._raw_output is not None, 'No raw response.'

        self._response = self._raw_output['answer']

    def start_chat(self):
        self._initialize_documents_chain()
        self._initialize_retriever()
        self._initialize_retrieval_chain()
        print('>>> I am a massage therapy expert')
        while True:
            user_input = input(
                '>>> Please ask me a question, or type Q to exit? '
            )
            if user_input.upper() != 'Q':
                self._invoke_chain(user_input=user_input)
                self._extract_response()
                self.history.extend([
                    HumanMessage(content=user_input),
                    AIMessage(content=self._response) 
                ])
                print(self._response)
            else:
                print('>>> Thank you for approaching me. I wish you a nice day')
                break
     






