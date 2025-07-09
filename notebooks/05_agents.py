# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = [
#     "anthropic==0.54.0",
#     "llamabot[all]==0.12.11",
#     "marimo",
#     "requests==2.32.4",
#     "torch>=2.5.1; (platform_system != 'Darwin' or platform_machine != 'x86_64')",
#     "torch==2.2.2; platform_system == 'Darwin' and platform_machine == 'x86_64'",
# ]
# ///

import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


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
    Consider a scenario where you want to research a topic by searching the internet.
    A simple bot would require you to specify exact search terms and manually review results.
    An autonomous agent, however, can decide what to search for,
    how many results to examine, and synthesize findings across multiple queries.

    That's what this notebook is all about.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## What makes an agent autonomous?

    Merely being able to fill a form
    isn't a satisfying definition for an "agent".
    Instead, we want an agent to take actions on our behalf,
    in particular, the two general activities of:

    1. Querying the external world for information, and
    2. Modifying state of the external world

    This is where **tools** come in.
    Within LlamaBot, we have a `tool` decorator
    that makes Python functions available to `AgentBot`.
    For those in the know, MCP server access is on the way!

    The `tool` decorator modifies a function
    by parsing its function signature and docstring
    and adding a `.json_schema` attribute to it.
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
        ## How AgentBot works

        `AgentBot` is LlamaBot's autonomous agent that can execute sequences of tools to accomplish complex tasks.
        Think of it as a problem-solving assistant that can break down your request into steps
        and use the right tools for each step.

        Here's how it operates under the hood:

        - **Tool-based execution**: AgentBot maintains an inventory of available tools (functions decorated with `@lmb.tool`) and
decides which ones to call based on your request
        - **Planning workflow**: It follows a structured approach: Plan → Validate → Execute → Reflect → Finish, ensuring each step
moves toward your goal
        - **Iterative problem-solving**: If one approach doesn't work, it can revise its plan and try different tools or strategies (up
to 10 iterations by default)
        - **Concurrent execution**: When multiple tools can run simultaneously, AgentBot executes them in parallel for efficiency
        - **Smart termination**: It knows when to stop working by using the built-in `respond_to_user` tool to deliver final answers

        The JSON schema information from each tool makes it possible for an LLM to decide,
        "Hey maybe to solve this problem at hand, I should call on a tool
        with arguments XYZ to solve the problem."

        `AgentBot` is, by default, prompted to solve the problem that is given to it
        by either solving it within the LLM's own reasoning
        or by calling on other tools that we provide it to use.

        The beauty of this approach is that you don't need to specify *how* to solve a problem —
        you just describe *what* you want accomplished,
        and AgentBot figures out the sequence of tool calls needed to get there.
        """  # noqa: E501
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Tools in action

        Now that we understand how AgentBot works, let's examine some concrete tools.
        We'll start with one of the built-in tools in LlamaBot's library: `search_internet_and_summarize`.
        """
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
    we automatically add a JSON schema attribute to the function itself.
    We can use `search_internet_and_summarize` to launch internet queries via DuckDuckGo.
    It will use `gpt-4.1` (by default) to generate summaries of pages that it encounters.
    However, you can use the environment variable `LMB_INTERNET_SUMMARIZER_MODEL`
    to set the model that is used for summarization.
    """
    )
    return


@app.cell
def _(search_internet_and_summarize):
    results = search_internet_and_summarize(
        "reviews of taylor swift's latest album",
        max_results=20,
    )
    return (results,)


@app.cell
def _(results):
    results
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Now let's see how AgentBot autonomously uses this tool.
        We'll create an AgentBot with access to the search tool
        and give it a research task to demonstrate its autonomous decision-making.
        """
    )
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
        r"""
        ## Building custom tools

        Let's build something more ambitious: an agent that can autonomously analyze CSV files.
        Here's what we want to accomplish:

        - Accept a file (either a local path or a URL to a publicly accessible CSV)
        - Take a peek at the file structure to understand what it contains
        - Autonomously write Python code to perform basic data analysis
        - Execute that code and provide insights

        To make this work, we need to create two custom tools:

        1. **`download_file`**: Handle internet CSV files by downloading them locally
        2. **`read_file`**: Read files from disk (useful for peeking at file structure)

        Combined with LlamaBot's built-in `write_and_execute_script` tool,
        these should give our agent everything it needs to generate analysis scripts autonomously.

        Let's start by building these tools:
        """
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
        """Download a file to a temp directory and save it to disk.
        We guarantee that the file will remain on disk after calling on this function.
        This function returns the absolute path on which it was downloaded to.
        """

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
        """Read file, which is assumed to be plain text, into memory.
        If `lines` is specified, the first `lines` lines will be read,
        treating it effectively as peeking into the file.

        :param file_path: String path to the file of interest.
        :param lines: Optional number of lines to read from the beginning of the file.
                     If None, reads entire file.
        """
        path = Path(file_path)
        content = path.read_text()

        # If lines parameter is specified, return only the first N lines
        if lines is not None:
            content_lines = content.splitlines()
            return "\n".join(content_lines[:lines])

        return content

    return (read_file,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Now for the third tool in our data analysis toolkit:
        LlamaBot's built-in `write_and_execute_script` tool.
        This tool is inspired by [HuggingFace's SmolAgents](https://github.com/huggingface/smolagents)
        and allows our agent to autonomously write and execute Python code.

        Combined with our file handling tools, this gives our agent the ability to:

        - Download or read CSV files
        - Analyze the file structure
        - Write custom analysis code
        - Execute that code and return results

        Let's examine this tool:
        """
    )
    return


@app.cell
def _():
    from llamabot.components.tools import write_and_execute_script

    return (write_and_execute_script,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Putting it all together: A data analysis agent

        Now, I want you to create an AgentBot that does data analysis on an arbitrary
        CSV file.
        You'll pass it [this CSV file](https://gist.githubusercontent.com/ericmjl/8512beab991966a3f3321cd59d7d131e/raw/6b326c788c0b307850b559be15548d86f889f409/historial_temperature_data.csv)
        when calling on it.
        This will demonstrate how multiple tools can work together autonomously.
        """
    )
    return


@app.cell
def _(download_file, lmb, read_file, write_and_execute_script):
    @lmb.prompt("system")
    def analysis_bot_sysprompt():
        """You are a data analysis expert specializing in CSV file analysis.
        Your goal is to help users understand their data through comprehensive analysis
        and visualization.

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

        Always write clean, well-commented Python code.
        Use popular libraries like pandas, matplotlib, seaborn, and numpy for analysis.
        Explain your findings in clear, non-technical language that anyone can
        understand.

        Do your work autonomously, don't ask the user any questions."""

    analysis_bot = lmb.AgentBot(
        system_prompt=analysis_bot_sysprompt(),
        tools=[write_and_execute_script, read_file, download_file],
    )

    analysis_bot(
        "help me analyze this file "
        "https://gist.githubusercontent.com/ericmjl/8512beab991966a3f3321cd59d7d131e/raw/"
        "6b326c788c0b307850b559be15548d86f889f409/historial_temperature_data.csv"
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
