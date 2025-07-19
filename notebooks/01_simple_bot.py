# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = [
#     "llamabot[all]==0.12.11",
#     "marimo",
#     "pyprojroot==0.3.0",
#     "rich==13.9.4",
#     "torch>=2.5.1; (platform_system != 'Darwin' or platform_machine != 'x86_64')",
#     "torch==2.2.2; platform_system == 'Darwin' and platform_machine == 'x86_64'",
# ]
# ///

import marimo

__generated_with = "0.14.12"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Introduction to LLM APIs with SimpleBot

    In this notebook, we'll learn how to interact with LLMs using LlamaBot's `SimpleBot` interface.
    We'll start with basic interactions and build up to creating a paper abstract generator.
    This notebook should take us no more than 15 minutes to complete within the tutorial setting as a class.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Creating Your First SimpleBot

    Let's start by creating a simple bot and understanding the basic components of an LLM interaction.

    LLM interactions are, for the vast majority of applications, controlled by an API call.
    The absolute basics of this API call are that it needs structured with the following components:

    - A system prompt, which sets the language model's persona across API calls (it is kept constant)
    - A model name specifying which language model
    - A user prompt, which sets the specific interaction that a user wants to have with the LM

    Let's see it in action.
    """
    )
    return


@app.cell
def _():
    import llamabot as lmb
    from rich import print

    bot = lmb.SimpleBot(
        system_prompt="You are a helpful assistant who provides concise, accurate responses.",
        model_name="ollama_chat/llama3.2",
        temperature=0.0,
    )
    return bot, lmb


@app.cell
def _(bot):
    response = bot("Aloha!")
    return (response,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""And this is the anatomy of a `response` object:""")
    return


@app.cell
def _(response):
    response.role, response.content
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    A `response` object has two attributes, a `role` and the message `conent`.
    The `role` is useful in later applications where we are evaluating the outputs, so that we can disambiguate between messages that humans sent (`'role': 'user'`) v.s. messages that were sent back by the LLM as a response (`'role': 'assistant'`).
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Altering the SimpleBot's Persona

    One can switch out the persona of a simple bot by changing the `system_prompt`.
    For example, if we want to turn the bot into one that responds like Richard Feynman:
    """
    )
    return


@app.cell
def _(lmb):
    feynman_bot = lmb.SimpleBot(
        system_prompt="You are a helpful assistant who responds like Richard Feynman.",
        model_name="ollama_chat/llama3.2",
    )
    feynman_bot("Give me an explanation on what black holes do.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Exercise

    Now, I'd like you to try setting the persona of your own bot.
    Copy and paste the above code and change the `system_prompt`
    to something that you like.
    """
    )
    return


@app.cell
def _():
    # Your code here!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Setting Personas for Tasks

    In general, setting personas for various tasks is a form of "steering the model"
    to generate text that conforms to your eventual specs.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Steering the LLM's Mission

    The system prompt is a great spot to steer an LLM to respond in ways that are helpful for the situation that you're interested in.

    As an example, you can have an LLM focus on generating poetry by setting the system prompt to something like this:

    ```python
    system_prompt = "You are a romantic poet stuck in the 19th century."
    ```
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Exercise: Make a poetry bot

    Create a `SimpleBot` that generates poetry in response to a topic that you (the user) can specify. Steer the style and persona of the poet, but let the user specify the topic of the poem.
    """
    )
    return


@app.cell
def _():
    # Your code here!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Flip the pattern: Large prompt, small output

    Previously, our bots were "small prompt, large output"-style outputs.
    We're now going to flip the script and try "large prompt, small output"-style problems, which mostly fall under the umbrella of text summarization.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Exercise

    **Option 1:** News summarization

    - Go to ABC/BBC/CBC and find a news article of interest.
    - Set system prompt with its mission to generate a news summary.
    - User prompt should *only* be the news article text.
    - **Tip:** Use triple quotes (`\"\"\"`) around the news article text to avoid conflicts with single and double quotes within the article.

    **Option 2:** Paper abstract generation

    - Find a paper that you're currently writing or reading.
    - Set the system prompt with a mission to generate a paper abstract.
    - User prompt should *only* be the journal article text.
    """
    )
    return


@app.cell
def _():
    # Your code here!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Summary

    - Anatomy of an LLM call
    - How to control diversity in output -- temperature.
    - Patterns of interactions:
        - Short prompt, long generation
        - Long prompt, short generation
        - All are valid. Just text in text out.
    """
    )
    return


if __name__ == "__main__":
    app.run()
