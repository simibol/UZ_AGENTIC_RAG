from llama_index.agent.openai import OpenAIAgent

def create_document_agent(llm, pinecone_query_tool):
    document_agent = OpenAIAgent.from_tools(
        tools=[pinecone_query_tool],
        llm=llm,
        verbose=True,
        system_prompt="""\
You are a Document Retrieval Agent specialized in answering questions using information stored in our Pinecone vector store.
Please use the provided tool to retrieve information and generate an answer.
""",
    )
    return document_agent