from pathlib import Path

# from langchain_community.document_loaders import  GoogleSpeechToTextLoader , TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

import warnings

warnings.filterwarnings("ignore")

load_dotenv()


def handleChatsEmbeddings(content, cov_name: str) -> dict:

    # Create chats directory if it doesn't exist
    Path("chats").mkdir(exist_ok=True)

    # Write
    chat_path = Path("chats") / cov_name

    split = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splied = split.split_text(content)
    print("splied done")

    embeding = MistralAIEmbeddings(model="mistral-embed", max_retries=5, timeout=120)

    chat_db_path = f"chats/{cov_name}"
    vectors = Chroma.from_texts(
        collection_name=cov_name,
        texts=splied,
        embedding=embeding,
        persist_directory=chat_db_path,
        ids=[f"doc_{i}" for i in range(len(splied))],
    )

    return {"message": "Embeddings created", "chat_db_path": chat_db_path}


def handelChatRetirvalSummery(cov_name: str, query: str):
    chat_db_path = f"chats/{cov_name}"

    vectordb = Chroma(
        persist_directory=chat_db_path,
        collection_name=cov_name,
        embedding_function=MistralAIEmbeddings(),
    )
    print(chat_db_path)
    retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 5})

    results = retriever.invoke(query)
    return results


if __name__ == "__main__":
    # with open('jk.text', 'r') as file:
    #     content = file.read()
    #     print(content[:300])
    # handleChatsEmbeddings("name is anirban , age is 20","new")
    info = handelChatRetirvalSummery("new", "name")
    print(info)
