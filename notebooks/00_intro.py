# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.14.0"
app = marimo.App(width="full")


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

    1. Build Python program that use Large Language Model APIs as part of the mix,
    2. Define "Structured Generation" and its utility
    3. More here...

    More over, I think an important concept we'll learn is that LLMs can be injected **surgically** into our applications to create magical experiences.
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
    ## AI Coding Policy

    No policies needed!

    I expect you to be using AI assistance actively,
    [but to do so autodidactically](https://ericmjl.github.io/blog/2025/6/7/principles-for-using-ai-autodidactically/).
    The goal is for you to master AI assistance as a tool for convenience
    while maintaining the discipline to flex your learning muscles.
    """
    )
    return


if __name__ == "__main__":
    app.run()
