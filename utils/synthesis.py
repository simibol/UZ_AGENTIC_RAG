def synthesize_responses(query, agent_responses, llm, history=[]):
    context = agent_responses.get('document', '')
    web_info = agent_responses.get('web', '')
    calc_info = agent_responses.get('calculator', '')
    conversation = ''
    for turn in history:
        conversation += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"

    # Handle context length
    MAX_CONTEXT_LENGTH = 1500  # Adjust based on model limits
    if len(context) > MAX_CONTEXT_LENGTH:
        context = context[:MAX_CONTEXT_LENGTH] + '...'

    synthesis_prompt = f"""\
    {conversation}
    You are an AI assistant tasked with providing detailed answers based solely on the provided context. Do not include any information not present in the context.

    Context:
    {context}

    Question:
    {query}

    Please provide a comprehensive answer using only the information from the context above.
    """

    if web_info:
        synthesis_prompt += f"\n\nAdditional Information from Web Search:\n{web_info}"

    synthesis_response = llm.complete(prompt=synthesis_prompt)
    return synthesis_response.response if hasattr(synthesis_response, 'response') else str(synthesis_response)