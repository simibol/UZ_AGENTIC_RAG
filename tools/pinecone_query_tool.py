import string
from llama_index.core.tools import ToolMetadata, BaseTool
from llama_index.core.base.response.schema import Response
from .tool_output import ToolOutput

class PineconeQueryTool(BaseTool):
    def __init__(self, pinecone_index, embedding_model, namespace):
        self.pinecone_index = pinecone_index
        self.embedding_model = embedding_model
        self.namespace = namespace
        self._metadata = ToolMetadata(
            name='pinecone_query',
            description='Useful for querying the Pinecone vector store for relevant information.'
        )

    @property
    def metadata(self) -> ToolMetadata:
        return self._metadata

    def __call__(self, input: str) -> ToolOutput:
        # Extract and preprocess the query
        query = self.extract_query(input)

        # Generate the embedding for the query
        query_embedding = self.embedding_model.get_query_embedding(query)

        # Perform a similarity search in Pinecone
        query_response = self.pinecone_index.query(
            vector=query_embedding,
            top_k=10,  # Increased from 5 for better results
            namespace=self.namespace,
            include_metadata=True
        )

        # Extract text snippets from the query response
        retrieved_texts = []
        if 'matches' in query_response and query_response['matches']:
            for match in query_response['matches']:
                metadata = match['metadata']
                text = metadata.get('content') or metadata.get('text', '')
                if text:
                    print(f"Match Score: {match['score']}")
                    print(f"Retrieved Text Snippet: {text[:200]}...")
                    retrieved_texts.append(text)
                else:
                    print("No 'content' or 'text' key found in metadata.")
        else:
            print("No matches found in Pinecone.")
            retrieved_texts.append("No relevant information found in the Pinecone database.")

        # Combine the retrieved texts
        context = "\n\n".join(retrieved_texts)

        # Create a Response object
        output_response = Response(response=context)
        return ToolOutput(raw_output=output_response)

    def extract_query(self, input: str) -> str:
        if 'about' in input.lower():
            query = input.lower().split('about', 1)[1].strip()
        else:
            query = input.lower()

        query = query.translate(str.maketrans('', '', string.punctuation))
        query = query.replace("'s", "")
        return query.strip()