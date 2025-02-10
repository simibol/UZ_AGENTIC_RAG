from llama_index.agent.openai import OpenAIAgent

def create_master_agent(llm):
    master_agent = OpenAIAgent.from_llm(
        llm=llm,
        verbose=True,
    )
    master_agent.system_prompt = """\
You are the Master Agent responsible for coordinating specialized agents to answer user queries.
Analyze the user's query, decide which agents can provide useful information, and synthesize their outputs to generate a comprehensive and accurate final response.
Ensure the final answer is well-organized and directly addresses the user's needs.
"""
    return master_agent