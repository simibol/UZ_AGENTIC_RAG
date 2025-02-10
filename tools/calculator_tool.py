import math
from llama_index.core.tools import ToolMetadata, BaseTool
from llama_index.core.base.response.schema import Response
from .tool_output import ToolOutput

class CalculatorTool(BaseTool):
    def __init__(self):
        self._metadata = ToolMetadata(
            name='calculator',
            description='Useful for performing mathematical calculations.'
        )

    @property
    def metadata(self) -> ToolMetadata:
        return self._metadata

    def __call__(self, expression: str) -> ToolOutput:
        try:
            # Safe evaluation using restricted namespace
            result = eval(expression, {"__builtins__": None}, vars(math))
            output_response = Response(response=str(result))
            return ToolOutput(raw_output=output_response)
        except Exception as e:
            output_response = Response(response=f"Error in calculation: {e}")
            return ToolOutput(raw_output=output_response)