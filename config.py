import os
from dotenv import load_dotenv
import openai
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

# Retrieve environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
pinecone_api_key = os.getenv('PINECONE_API_KEY')
pinecone_environment = os.getenv('PINECONE_ENVIRONMENT')
pinecone_index_name = os.getenv('PINECONE_INDEX')
pinecone_namespace = os.getenv('PINECONE_NAMESPACE')
web_search_api_key = os.getenv('WEB_API_KEY')

# Validate environment variables
if not all([openai_api_key, pinecone_api_key, pinecone_environment, pinecone_index_name, pinecone_namespace, web_search_api_key]):
    raise EnvironmentError("All API keys and environment variables must be set.")

# Initialize OpenAI
openai.api_key = openai_api_key

# Initialize Pinecone
pc = Pinecone(
    api_key=pinecone_api_key,
    environment=pinecone_environment
)

# Check if the index exists; if not, create it
if pinecone_index_name not in pc.list_indexes().names():
    pc.create_index(
        name=pinecone_index_name,
        dimension=1536,
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

# Connect to the index
pinecone_index = pc.Index(pinecone_index_name)