from llama_index.agent.openai import OpenAIAgent

def create_calculator_agent(llm, calculator_tool):
    calculator_agent = OpenAIAgent.from_tools(
        tools=[calculator_tool],
        llm=llm,
        verbose=True,
        system_prompt="""\
You are a Calculator Agent specialized in performing mathematical calculations.
""",
    )
    return calculator_agent