# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "anthropic==0.54.0",
#     "llamabot[all]==0.12.8",
#     "marimo",
#     "requests==2.32.4",
# ]
# ///

import marimo

__generated_with = "0.14.6"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import llamabot as lmb

    return lmb, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Building Autonomous Agents

    Using LlamaBot, you can build agents that autonomously execute workflows on your behalf.
    In some ways, the bots you have already built (the `StructuredBot`s, for example),
    are "autonomous" in a sense -- you can use them to fill in pydantic models
    like a human fills out a form.

    But could we take autonomy further?

    That's what this notebook is all about.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Tools

    Merely being able to fill a form
    might not be sufficiently satisfying definition for an "agent".
    Instead, we may want an agent to take actions,
    in particular, the two general activities of:

    1. Querying the external world for information, and
    2. Modifying state of the external world

    Within LlamaBot, we have a `tool` decorator
    that makes Python functions available to `AgentBot`.
    For those in the know, MCP server access is on the way!

    The `tool` decorator modifies a function
    by parsing its function signature and docstring
    and adding a `.json_schema attribute to it.
    It is this JSON schema that gets passed into an LLM,
    which will then decide whether, given the current context,
    it should call on a function or not,
    using the JSON schema to anchor its outputs.

    Let's see an example of the `@tool` decorator in action.
    """
    )
    return


@app.cell
def _(lmb):
    @lmb.tool
    def add(num1: int, num2: int):
        """Add two integers, num1 and num2"""
        return num1 + num2

    add.json_schema
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    This information makes it possible for an LLM to decide,
    "Hey maybe to solve this problem at hand, I should call on a tool
    with arguments XYZ to solve the problem."
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## LlamaBot's AgentBot

    LlamaBot comes with an `AgentBot` for which you can provide tools that it calls.
    `AgentBot` is, by default, prompted to solve the problem that is given to it
    by either solving it within the LLM's own "reasoning" (in quotation marks -- more on that in Q&A if you desire)
    or by calling on other tools that we provide it to use.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""Let's examine one of the tools that are built in to LlamaBot's library of tools, `search_internet_and_summarize`:"""
    )
    return


@app.cell
def _():
    from llamabot.components.tools import search_internet_and_summarize

    search_internet_and_summarize.json_schema
    return (search_internet_and_summarize,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Tools are just regular functions,
    but when decorated with `@lmb.tool`,
    we automatically add in a JSON schema attribute to the function itself.
    We can use `search_internet_and_summarize` to launch internet queries via Duckduckgo.
    It will use `gpt-4.1` (by default) to generate summaries of pages that it encounters.
    However, you can use the environment variable, `LMB_INTERNET_SUMMARIZER_MODEL`,
    to set the model that is used for summarization.
    """
    )
    return


@app.cell
def _(search_internet_and_summarize):
    results = search_internet_and_summarize(
        "reviews of taylor switf'ts latest album",
        max_results=20,
    )
    return (results,)


@app.cell
def _(results):
    results
    return


@app.cell
def _(mo):
    mo.md(r"""We're now going to see it in action with `AgentBot`:""")
    return


@app.cell
def _(lmb, search_internet_and_summarize):
    internet_search_agent = lmb.AgentBot(
        tools=[search_internet_and_summarize],
    )
    return (internet_search_agent,)


@app.cell
def _(internet_search_agent):
    SHE_response = internet_search_agent(
        "reviews of S.H.E's (taiwanese girl band's) last album that they ever released"
    )

    SHE_response
    return (SHE_response,)


@app.cell
def _(SHE_response):
    print(SHE_response.content)
    return


@app.cell
def _(mo):
    mo.md(
        r"""Now, I'd like for you to build a tool that a AgentBot can try to call on. For this tool, let's call it a filesystem read tool. It accepts a file path and attempts to read it into memory. (To simplify things, assume that it reads in plain text files.)"""
    )
    return


@app.cell
def _(lmb):
    import requests
    import tempfile
    from pathlib import Path
    from urllib.parse import urlparse

    @lmb.tool
    def download_file(url: str) -> str:
        """Download a file to a temp directory and save it to disk. We guarantee that the file will remain on disk after calling on this function. This function returns the absolute path on which it was downloaded to."""

        try:
            # Get the filename from URL, or use a default name
            parsed_url = urlparse(url)
            filename = Path(parsed_url.path).name
            if not filename:
                filename = "downloaded_file"

            # Create a temporary directory that won't be automatically cleaned up
            temp_dir = Path(tempfile.mkdtemp())
            file_path = temp_dir / filename

            # Download the file
            response = requests.get(url)
            response.raise_for_status()  # Raises an exception for bad status codes

            # Write to disk
            file_path.write_bytes(response.content)

            return str(file_path.absolute())

        except Exception as e:
            return f"Error downloading file: {str(e)}"

    return Path, download_file


@app.cell
def _(Path, lmb):
    @lmb.tool
    def read_file(file_path: str, lines: int = None):
        """Read file, which is assumed to be plain text, into memory. If `lines` is specified, the first `lines` lines will be read, treating it effectively as peeking into the file.

        :param file_path: String path to the file of interest.
        :param lines: Optional number of lines to read from the beginning of the file. If None, reads entire file.
        """
        path = Path(file_path)
        content = path.read_text()

        # If lines parameter is specified, return only the first N lines
        if lines is not None:
            content_lines = content.splitlines()
            return "\n".join(content_lines[:lines])

        return content

    return (read_file,)


@app.cell
def _(mo):
    mo.md(
        r"""
    We're now going to pair it with a built-in tool that is inspired by [HuggingFace's SmolAgents](https://github.com/huggingface/smolagents),
    `write_and_execute_code`.
    """
    )
    return


@app.cell
def _():
    from llamabot.components.tools import write_and_execute_script

    return (write_and_execute_script,)


@app.cell
def _(mo):
    mo.md(
        r"""Now, I want you to create an AgentBot that does data analysis on an arbitrary CSV file, and pass it [this CSV file](https://gist.githubusercontent.com/ericmjl/8512beab991966a3f3321cd59d7d131e/raw/6b326c788c0b307850b559be15548d86f889f409/historial_temperature_data.csv), when calling on it."""
    )
    return


@app.cell
def _(download_file, lmb, read_file, write_and_execute_script):
    @lmb.prompt("system")
    def analysis_bot_sysprompt():
        """You are a data analysis expert specializing in CSV file analysis. Your goal is to help users understand their data through comprehensive analysis and visualization.

        When given a data analysis task, follow this approach:
        1. First, download or read the data file to understand its structure
        2. Examine the data: column names, data types, size, and sample rows
        3. Perform exploratory data analysis including summary statistics
        4. Create meaningful visualizations to reveal patterns and insights
        5. Provide clear, actionable insights based on your findings

        You have access to these tools:
        - download_file: Download files from URLs to analyze
        - read_file: Read files from disk (useful for peeking at large files)
        - write_and_execute_script: Write and run Python code for analysis

        Always write clean, well-commented Python code. Use popular libraries like pandas, matplotlib, seaborn, and numpy for analysis. Explain your findings in clear, non-technical language that anyone can understand.

        Do your work autonomously, don't ask the user any questions."""

    analysis_bot = lmb.AgentBot(
        system_prompt=analysis_bot_sysprompt(),
        tools=[write_and_execute_script, read_file, download_file],
    )

    analysis_bot(
        "help me analyze this file https://gist.githubusercontent.com/ericmjl/8512beab991966a3f3321cd59d7d131e/raw/6b326c788c0b307850b559be15548d86f889f409/historial_temperature_data.csv"
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
