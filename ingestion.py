import os

import pinecone
from langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

import pinecone


def ingest_doc() ->None:
    pinecone.init(api_key=os.environ['PINECONE_API_KEY'], environment=os.environ['PINECONE_ENVIRONMENT_REGION'])
    loader = ReadTheDocsLoader(path='langchain-docs/python.langchain.com/en/latest')
    raw_documents = loader.load()
    print(f"Loaded {len(raw_documents)} documents")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50,separators=[
        "\n\n","\n"," ",""])
    documents = text_splitter.split_documents(raw_documents)
    print(f'Total Chunks: {len(documents)}')

    for doc in documents:
        old_path = doc.metadata["source"]
        new_url = old_path.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    print(f'Going to insert: {len(documents)} to Pinecone')
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(documents, embeddings, index_name ="langchain-doc-index")

    print("Saved in Pinecone")


if __name__ == "__main__":
    ingest_doc()