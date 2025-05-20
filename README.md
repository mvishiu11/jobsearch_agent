## Quick overview

This repository hosts a **multi-agent CAMEL-AI workforce** that

1. collects a candidate’s preferences via a Human-in-the-Loop tool,
2. queries LinkUp for ranked Python-developer jobs,
3. gathers interview-prep resources from the open web,
4. produces a 14-day study plan in Markdown, and
5. spawns an *Embodied* agent that converts the Markdown to HTML and serves it at `http://127.0.0.1:5000`.

All agents run locally with one command (`poetry run app`) and rely only on OpenAI API keys, LinkUp API keys, and Brave API keys.

---

## Installation

```bash
git clone https://github.com/your-org/jobsearch.git
cd jobsearch
poetry install
```

> **Key packages**
>
> * `camel-ai 0.2.59` – multi-agent framework with EmbodiedAgent & Workforce ([docs.camel-ai.org][1])
> * `markdown 3.8` – converts the coach’s Markdown (tables support) to HTML ([python-markdown.github.io][2])
> * `flask 3.1` – lightweight server; runs happily in a background thread ([Stack Overflow][3])
> * `humanlayer 0.7.7` – Human-as-tool bridge for preference capture ([humanlayer.dev][4])
> * `linkup-sdk 0.2.5` – low-latency job-search API (`depth="standard"` is fastest) ([docs.linkup.so][5])

Note: This might take a while to install due to dependencies of CamelAI including such packages as `triton`.

---

## Environment

Create a `.env` in the project root:

```dotenv
OPENAI_API_KEY=sk-...        # All keys are required, no fallback is provided
LINKUP_API_KEY=...
BRAVE_API_KEY=...
MODEL_PLATFORM=openai        # defaults shown here, you can skip those
MODEL_TYPE=gpt_4o_mini
```

The Pydantic settings loader auto-detects these variables at runtime.

---

## ▶️ Running the pipeline

```bash
poetry run app
```

* The **PreferenceAgent** asks six questions through HumanLayer; answer in the console.
* The **JobSearchAgent** calls LinkUp (`depth="standard"`, 12 s timeout) and returns 3-5 jobs ranked by salary DESC. ([docs.linkup.so][5])
* The **WebAgent** fetches top interview resources with a Brave search wrapper, via a Brave search tool from official CamelAI toolkit.
* The **PlannerAgent** plans the 14-day study schedule and creates a Markdown of the full workforce run.
* Finally, **WebPresenterAgent** writes `app.py` and boots Flask in a separate thread.

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) for the styled HTML summary.

---

## Project structure

```
jobsearch/
├── jobsearch_app/
│   ├── agents.py          # factory functions for mentor/recruiter/…
│   ├── tools.py           # strict JSON-schema FunctionTools
│   ├── human.py           # HumanLayer wrapper
│   ├── web_agent.py       # EmbodiedAgent that generates Flask code
│   ├── workflow.py        # builds Workforce & kicks everything off
│   └── config.py          # .env → Pydantic Settings
├── README.md
├── .env                   # Put your OpenAI, Linkup, and Brave API keys here
└── pyproject.toml
```

---

## 🛠️ Common problems & fixes

| Symptom                                                         | Likely cause                                                                                                                             | Fix                                                                                                                                                                                                                                                                                                                                                |
| --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mentor repeats questions indefinitely**                 | Too small model,<br />incapable of adequate reasoning or prompt not strict enough.                                                      | I have tried a lot of things to make this work, but sometimes it just doesn't.<br />Best way to make this work is to just Ctrl+C and run again.                                                                                                                                                                                                    |
| LinkUp call hangs > 30 s                                        | Using `depth="deep"` or no timeout. Alternatively too small model, <br />incapable of adequate reasoning or prompt not strict enough. | Switch to `depth="standard"` (fast, €0.005/call) and pass `timeout=12`. ([docs.linkup.so][5]) <br />However sometimes this just never ends, even on `depth="standard"` due to multiple calls to the tool by the model, <br />caused  most likely by a similar case as in the problem above.  <br />In such a case, Ctrl+C and run again. |
| Workforce spawns extra agents with `search_brave` and crashes | CAMEL auto-spawns workers on task failure                                                                                                | Disable with `new_worker_agent_kwargs={"tools": []}` (already set). ([docs.camel-ai.org][1])                                                                                                                                                                                                                                                     |
| Output varies run-to-run                                        | OpenAI model stochasticity                                                                                                               | Pin `MODEL_TYPE=gpt_4o_mini` and set `temperature=0.3` in `ChatGPTConfig` if determinism is required. <br />In my case, this is minor, so I did not address this specifically.                                                                                                                                                               |

---

[1]: https://docs.camel-ai.org
[2]: https://python-markdown.github.io/extensions/tables
[3]: https://stackoverflow.com/questions/31264826/start-a-flask-application-in-separate-thread
[4]: https://www.humanlayer.dev/docs/core/human-as-tool
[5]: https://docs.linkup.so/pages/documentation/get-started/concepts
