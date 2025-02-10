from llama_index.agent.openai import OpenAIAgent

def create_web_search_agent(llm, web_search_tool):
    web_search_agent = OpenAIAgent.from_tools(
        tools=[web_search_tool],
        llm=llm,
        verbose=True,
        system_prompt="""\
You are a Web Search Agent specialized in finding information on the internet.
Please use the web search tool to retrieve information.
""",
    )
    return web_search_agent