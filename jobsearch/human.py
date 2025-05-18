from humanlayer import HumanLayer
from camel.toolkits import FunctionTool

_hl = HumanLayer(verbose=True)
_raw_contact_human = _hl.human_as_tool()

_HUMAN_SCHEMA = {
    "type": "function",
    "function": {
        "name": "contact_human",
        "description": (
            "Ask the human one clear question and wait for the answer. "
            "Return the answer as plain text."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "A single concise question."
                }
            },
            "required": ["question"],
            "additionalProperties": False
        }
    }
}

human_tool = FunctionTool(
    _raw_contact_human,
    openai_tool_schema=_HUMAN_SCHEMA
)
