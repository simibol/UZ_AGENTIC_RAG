from llama_index.core.base.response.schema import Response

class ToolOutput:
    def __init__(self, raw_output: Response):
        self.raw_output = raw_output