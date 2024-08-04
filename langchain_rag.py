from rag.embedding import GenericTextLoader, TextSplitter, OpenAIEmbedder

from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from utilities.general import environment_reader


environment = environment_reader(env_file='./.env')


if __name__ == '__main__':

    SOURCE_DOCUMENT = r'C:\Users\marko\Downloads\Sports And Remedial Massage Therapy ( PDFDrive ).pdf'
    DOCUMENT_TYPE = 'pdf'

    text_loader = GenericTextLoader(
        source_document=SOURCE_DOCUMENT,
        document_type=DOCUMENT_TYPE
    )
    text_loader.read_document()
    document = text_loader.get_document()
    print(len(document))

    splitter = TextSplitter(document=document)
    splitter.split_document()
    converted_document = splitter.get_converted_document()
    print(len(converted_document))

    embedding = OpenAIEmbedder(pieces_of_text=converted_document)
    embedding.embed()

    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI()

    query = """Provide me with a detailed insight on how to perform
        sport massage of the deltoidus muscle? Limit your answer to
        768 characters.
    """
    chain = PromptTemplate.from_template(template=query) | llm
    result = chain.invoke(input={})
    print(result.content)

    vectorstore = PineconeVectorStore(
        index_name=environment["PINECONE_PROJECT_INDEX"], embedding=embeddings
    )

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    retrival_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(), 
        combine_docs_chain=combine_docs_chain
    )
    result = retrival_chain.invoke(input={"input": query})
    print(result['answer'])



    
 
