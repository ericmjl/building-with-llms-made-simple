# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "llamabot[all]==0.12.11",
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Building with LLMs Made Simple

    A tutorial by Eric J. Ma
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Preface

    Welcome! I put this tutorial together to share what I know about building using LLMs.
    It is designed to be accessible to Pythonistas of a wide range of experiences.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Learning Goals

    By the end of this tutorial, you will be able to:

    1. **Build LLM-powered Python applications** using SimpleBot and StructuredBot
       for both free-form text generation and type-safe structured outputs,
    2. **Create RAG systems** that combine document retrieval with conversation memory
       for knowledge-based question answering,
    3. **Evaluate and improve LLM performance** through human-in-the-loop feedback
       and in-context learning techniques,
    4. **Develop autonomous agents** that can execute complex workflows using custom tools
       and external integrations.

    Moreover, I think an important concept we'll learn is that LLMs can be injected **surgically** into our applications to create magical experiences.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Prerequisites

    1. You should be able to write Python code.
    2. You should have `uv` installed on your system. Best done by the official shell script one-liner on the [`uv` installation page](https://docs.astral.sh/uv/getting-started/installation/).
    3. You should be able to run `uvx marimo edit --sandbox /path/to/some/notebook.py` to run the Marimo notebooks.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Questions and Support

    If you have questions while working through this tutorial, please use the [GitHub Discussions board](https://github.com/ericmjl/building-with-llms-made-simple/discussions) for this repository. This helps create a searchable knowledge base for other learners and allows the community to help each other.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## AI Coding Policy

    No policies needed!

    I expect you to be using AI assistance actively,
    [but to do so autodidactically](https://ericmjl.github.io/blog/2025/6/7/principles-for-using-ai-autodidactically/).
    The goal is for you to master AI assistance as a tool for convenience
    while maintaining the discipline to flex your learning muscles.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Technical Logistics

    By this point, you should have followed the installation instructions for Ollama
    and should have also downloaded a few of the smaller-sized LLMs
    that are designed to fit within 16GB RAM systems on CPU.

    However, if for whatever reason you have not done so, do not fret!
    I have deployed Ollama on Modal (see [this repo](https://github.com/ericmjl/ollama-on-modal) for instructions on how you can do so too).
    The kind folks at Modal have also given me enough credits to spend for June and July
    that can support usage at this tutorial.
    To access this endpoint, try this code below:
    """
    )
    return


@app.cell
def _():
    import llamabot as lmb

    bot = lmb.SimpleBot(
        "You are a helpful assistant.",
        model_name="ollama_chat/mistral-small3.2",
        api_base="https://ericmjl--ollama-service-ollamaservice-server.modal.run",
    )

    bot("Hey there!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The models that I have downloaded here are:

    - `deepseek-r1`
    - `gemma2:2b`
    - `gemma3:27b`
    - `llama3:27b`
    - `llama3-gradient:latest`
    - `llama3.2:latest`
    - `mistral-small:24b`
    - `mistral-small3.1:latest`
    - `mistral-small3.2:latest`
    - `qwen3:30b`

    I will keep the endpoints alive during the two tutorial days and during the sprints. Please feel free to switch over to the endpoint and use any of the larger models at any point during the conference.
    """
    )
    return


if __name__ == "__main__":
    app.run()
