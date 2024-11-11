from dotenv import load_dotenv

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore


def get_llm():
    load_dotenv('.env', override=True)
    return AzureChatOpenAI(azure_deployment="gpt-4o-mini", api_version="2024-08-01-preview")

def get_embedding():
    load_dotenv('.env', override=True)
    return AzureOpenAIEmbeddings(azure_deployment="text-embedding-ada-002", api_version="2023-05-15")


if __name__ == '__main__':
    # Test LLM
    llm = get_llm()
    prompt = PromptTemplate.from_template("How to say {input} in {output_language}:\n")

    chain = prompt | llm
    output = chain.invoke(
        {
            "output_language": "German",
            "input": "I love programming.",
        }
    )

    print(output.content)

    # Test embedding model
    embeddings = get_embedding()
    text = "LangChain is the framework for building context-aware reasoning applications"

    vectorstore = InMemoryVectorStore.from_texts(
        [text],
        embedding=embeddings,
    )

    # Use the vectorstore as a retriever
    retriever = vectorstore.as_retriever()

    # Retrieve the most similar text
    retrieved_documents = retriever.invoke("What is LangChain?")

    # show the retrieved document's content
    print(retrieved_documents[0].page_content)
