from config import openai_api_key, pinecone_index, pinecone_namespace, web_search_api_key
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from tools.pinecone_query_tool import PineconeQueryTool
from tools.web_search_tool import WebSearchTool
from tools.calculator_tool import CalculatorTool
from agents.document_agent import create_document_agent
from agents.web_search_agent import create_web_search_agent
from agents.calculator_agent import create_calculator_agent
from agents.master_agent import create_master_agent
from utils.analyze_query import analyze_query
from utils.synthesis import synthesize_responses
from database import Database  # Import database module

def master_agent_chat(query, llm, pinecone_query_tool, web_search_agent, calculator_agent, db, conversation_id):
    agent_responses = {}
    
    # Analyze the query to determine which agents to use
    agents_to_use = analyze_query(query)
    
    # Store the user query in the database
    db.add_message(conversation_id, sender='user', message_text=query)
    
    # Document Retrieval
    if agents_to_use['document']:
        tool_output = pinecone_query_tool(query)
        context = tool_output.raw_output.response
        agent_responses['document'] = context
    else:
        agent_responses['document'] = ''
    
    # Web Search
    if agents_to_use['web_search']:
        web_response = web_search_agent.chat(query)
        agent_responses['web'] = web_response.response
    else:
        agent_responses['web'] = ''
    
    # Calculator
    if agents_to_use['calculator']:
        calc_response = calculator_agent.chat(query)
        agent_responses['calculator'] = calc_response.response
    else:
        agent_responses['calculator'] = ''
    
    # Synthesize responses
    combined_response = synthesize_responses(query, agent_responses, llm)
    
    # Store assistant's response in the database
    db.add_message(conversation_id, sender='assistant', message_text=combined_response)
    
    return combined_response

def chat_loop(master_agent, llm, pinecone_query_tool, web_search_agent, calculator_agent):
    print("Welcome to the AI assistant. Type 'exit' to quit.")
    history = []
    
    # Initialize the database
    db = Database()
    user_id = "user_1"  # Example user identifier
    conversation_id = db.create_conversation(user_id)
    
    try:
        while True:
            query = input("You: ")
            if query.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            agent_response = master_agent_chat(
                query, 
                llm, 
                pinecone_query_tool, 
                web_search_agent, 
                calculator_agent, 
                db, 
                conversation_id
            )
            print("AI Assistant:", agent_response)
            history.append({'assistant': agent_response})
    finally:
        db.close()

if __name__ == "__main__":
    embedding_model = OpenAIEmbedding()
    llm = OpenAI(
        model='gpt-3.5-turbo',
        openai_api_key=openai_api_key,
        temperature=0.0,
    )

    pinecone_query_tool = PineconeQueryTool(
        pinecone_index=pinecone_index,
        embedding_model=embedding_model,
        namespace=pinecone_namespace
    )

    web_search_tool = WebSearchTool(api_key=web_search_api_key)
    calculator_tool = CalculatorTool()

    document_agent = create_document_agent(llm, pinecone_query_tool)
    web_search_agent = create_web_search_agent(llm, web_search_tool)
    calculator_agent = create_calculator_agent(llm, calculator_tool)
    master_agent = create_master_agent(llm)

    chat_loop(master_agent, llm, pinecone_query_tool, web_search_agent, calculator_agent)