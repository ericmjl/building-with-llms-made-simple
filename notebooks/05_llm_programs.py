# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "llamabot[all]==0.12.8",
#     "marimo",
#     "pyprojroot==0.3.0",
#     "rich==13.9.4",
#     "pydantic==2.10.6",
#     "building-with-llms-made-simple",
# ]
#
# [tool.uv.sources]
# building-with-llms-made-simple = { path = "../", editable = true }
# ///

import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
    # Part 5: LLM Programs

    In this notebook, we'll explore how to build more complex LLM-powered programs.
    We'll start with a self-guided exercise to build a structured git commit message generator.

    ## Exercise: Build a Git Commit Message Generator

    In this exercise, you'll build a program that generates structured git commit messages
    following the Conventional Commits specification. You'll learn how to:

    1. Define structured data models using Pydantic
    2. Create a StructuredBot for generating commit messages
    3. Add custom formatting methods
    4. Handle complex nested data structures

    ### The Conventional Commits Format

    The Conventional Commits specification provides a standardized way to write commit messages.
    A commit message should include:

    1. `type`: The kind of change (feat, fix, docs, etc.)
    2. `scope`: The part of the codebase affected (optional)
    3. `description`: A short, imperative description
    4. `body`: A longer explanation (optional)
    5. `breaking_changes`: Any breaking changes (optional)

    ### Your Task

    Your task is to build a commit message generator that:

    1. Takes a git diff as input
    2. Analyzes the changes
    3. Generates a structured commit message
    4. Formats it according to the Conventional Commits specification

    You'll implement this in several steps:

    1. Create a basic `GitCommitMessage` model
    2. Add a `format` method
    3. Create a StructuredBot
    4. Test with sample git diffs
    5. Enhance with additional features (emojis, detailed file changes, etc.)

    ### Getting Started

    First, let's import the necessary packages and set up our environment.
    """
    )
    return


@app.cell
def _():
    from typing import List, Optional

    import llamabot as lmb
    from pydantic import BaseModel, Field
    from rich import print

    return BaseModel, Field, List, Optional, lmb, print


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Step 1: Create the Basic Model

    Create a `GitCommitMessage` model with the following fields:
    - `type`: The kind of change (feat, fix, docs, etc.)
    - `scope`: The part of the codebase affected (optional)
    - `description`: A short, imperative description
    - `body`: A longer explanation (optional)
    - `breaking_changes`: Any breaking changes (optional)

    Add a `format` method that formats the message according to the Conventional Commits specification.
    """
    )
    return


@app.cell
def _():
    # Your code here!
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Step 2: Create the StructuredBot

    Create a StructuredBot that uses your `GitCommitMessage` model.
    The bot should:
    - Take a git diff as input
    - Analyze the changes
    - Generate a structured commit message
    - Return an instance of your model

    You'll need to:
    1. Create a system prompt that explains the task
    2. Create a user prompt template for the git diff
    3. Initialize the StructuredBot with your model
    """
    )
    return


@app.cell
def _():
    # Your code here!
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Step 3: Test with a Sample Git Diff

    Let's test your commit message generator with a sample git diff.
    Here's a simple diff to work with:
    """
    )
    return


@app.cell
def _():
    # Sample git diff
    git_diff = """
    diff --git a/src/main.py b/src/main.py
    index abc123..def456 100644
    --- a/src/main.py
    +++ b/src/main.py
    @@ -1,5 +1,7 @@
     def main():
    -    print("Hello, World!")
    +    print("Hello, World!")
    +    print("This is a new feature")
    +    print("Added more functionality")
     """
    return (git_diff,)


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Step 4: Enhance Your Model

    Now that you have a basic working version, try enhancing your model with additional features:

    1. Add emojis based on the commit type (e.g., ✨ for feat, 🐛 for fix)
    2. Add support for detailed file changes
    3. Add multiple formatting options (conventional, markdown, short)
    4. Add validation for commit types and scopes

    Choose one or more enhancements to implement.
    """
    )
    return


@app.cell
def _():
    # Your code here!
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Step 5: Reflection

    Take a moment to reflect on what you've built:

    1. What challenges did you face?
    2. How did you solve them?
    3. What improvements could you make?
    4. How could you use this in a real project?

    Share your thoughts with your peers and discuss potential improvements.
    """
    )
    return


if __name__ == "__main__":
    app.run()
