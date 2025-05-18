from camel.agents import EmbodiedAgent
from flask import Flask, render_template_string
import markdown
from threading import Thread
import textwrap

_HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Job-Search Summary</title>
    <link href="https://cdn.simplecss.org/simple.min.css" rel="stylesheet">
</head>
<body>
  <header><h1>Job-Search & Interview Plan</h1></header>

  <section id="result">
    {{ result|safe }}
  </section>
</body>
</html>
"""


class WebPresenterAgent(EmbodiedAgent):
    role = "Front-End Presenter"
    task = "Serve summary via Flask"

    def __init__(self, summary_data: dict, model=None):
        super().__init__(system_message="Render HTML", model=model)
        self.data = summary_data
        self.app = Flask(__name__)
        self._register_routes()

    def _register_routes(self):
        @self.app.route("/")
        def index():
            """
            Render the Job-Search & Interview Plan summary.
            """
            result = markdown.markdown(self.data, extensions=["tables"])
            return render_template_string(
                _HTML_TEMPLATE,
                result=textwrap.indent(result, "  "),
            )

    def run(self):
        Thread(target=self.app.run, kwargs={"debug": False}).start()
