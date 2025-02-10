import requests
from llama_index.core.tools import ToolMetadata, BaseTool
from llama_index.core.base.response.schema import Response
from .tool_output import ToolOutput

class WebSearchTool(BaseTool):
    def __init__(self, api_key):
        self.api_key = api_key
        self._metadata = ToolMetadata(
            name='web_search',
            description='Useful for searching the web for up-to-date information.'
        )
        self.endpoint = 'https://api.bing.microsoft.com/v7.0/search' # do google instead

    @property
    def metadata(self) -> ToolMetadata:
        return self._metadata

    def __call__(self, input: str) -> ToolOutput:
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        params = {"q": input, "textDecorations": True, "textFormat": "HTML"}
        response = requests.get(
            self.endpoint,
            headers=headers,
            params=params
        )
        if response.status_code == 200:
            search_results = response.json()
            snippets = []
            for web_page in search_results.get('webPages', {}).get('value', []):
                snippets.append(web_page.get('snippet', ''))
            output = "\n".join(snippets)
            output_response = Response(response=output)
            return ToolOutput(raw_output=output_response)
        else:
            error_message = f"Web search failed with status code {response.status_code}"
            output_response = Response(response=error_message)
            return ToolOutput(raw_output=output_response)