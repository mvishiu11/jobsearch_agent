"""
Embodied agent that converts a Markdown summary into HTML,
writes a Flask `app.py`, then runs it on http://127.0.0.1:5000.
"""

from __future__ import annotations
from camel.agents import EmbodiedAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from camel.generators import SystemMessageGenerator

_SYSTEM_MSG = SystemMessageGenerator().from_dict(
    meta_dict=dict(role="Front-End Presenter",
                   task="Write Flask code that renders Markdown → HTML and run it"),
    role_tuple=("Front-End Presenter", RoleType.EMBODIMENT),
)


class WebPresenterAgent(EmbodiedAgent):
    """
    Embodied agent that spins up the Flask server and serves the Markdown.
    Also writes the Flask and HTML files.

    Args:
        markdown_doc (str): Markdown content to serve.
        model (Model, optional): Model to use for the agent.
    """

    def __init__(self, markdown_doc: str, model=None):
        super().__init__(
            system_message=_SYSTEM_MSG,
            model=model,
            code_interpreter=None,
            tool_agents=None,
        )
        self.markdown_doc = markdown_doc

    def get_init_message(self) -> BaseMessage:
        """
        Encapsulates the initial message for the agent.

        Returns:
            BaseMessage: Initial message for the agent.
        """
        content = (
            "Here is the full Markdown to serve as a web-page:\n"
            "```markdown\n"
            f"{self.markdown_doc}\n"
            "```\n\n"
            "Write *exactly one* Python script called **app.py** that:\n"
            "1. `import markdown, textwrap, flask`.\n"
            "2. Converts the Markdown string above to HTML with "
            "`markdown.markdown(..., extensions=['tables'])`.\n"
            "3. Uses simple, well-known stylesheet.\n"
            "4. Uses Flask + Jinja2 (`|safe`) to serve that HTML at route `/`.\n"
            "5. Starts the server on `127.0.0.1`, port 5000 **in a background "
            "thread** so the code returns immediately.\n"
            "6. After starting, `print('🌐 http://127.0.0.1:5000')`.\n"
            "Respond **only** with the Python code block that writes and runs "
            "the server, then print `###RUN_COMPLETE###` on a new line. "
            "NO explanations, no markdown fencing around RUN_COMPLETE."
        )
        return BaseMessage.make_user_message(role_name="user", content=content)
