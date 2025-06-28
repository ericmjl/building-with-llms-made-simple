# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "anthropic==0.54.0",
#     "building-with-llms-made-simple==0.0.1",
#     "llamabot==0.12.10",
#     "marimo",
#     "pydantic==2.11.7",
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
    import llamabot as lmb
    from pydantic import BaseModel, Field

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Creating Deckbot

    In this notebook, we will attempt to re-create "Deckbot", an LLM bot that I once made that generates Markdown slides in a _structured_ fashion. This should give you a sense of the space of design choices involved in making an LLM bot.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Design choices

    Before embarking on the implementation, let us first think through some basic design decisions.

    Firstly, we have a choice between plain old `SimpleBot`-based markdown slides generation, or we can instead take advantage of `StructuredBot` to generate slides. Here, I would lean towards generating slides in a structured fashion, which would logically lead to the next step.

    Secondly, we need to think carefully through the data model of a slide. It can be as simple or as complicated as we make it. I would err on the side of being simpler first.

    Thirdly, we'll need a class method to render the slide to Markdown for us.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Guided Tasks

    If you need guidance to begin, consider the following pointers.

    Firstly, build a `Slide` pydantic model, and test it using a `StructuredBot`. Consider using `marimo.md()` to render the slide.

    Then, build a `Deck` pydantic model, and also test it using a new `StructuredBot`. Build out the rendering method as well.

    Finally, if you're game for it, build a lightning talk that you can present at the SciPy conference!
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Tips

    1. Your prompt and field descriptions may need to be tweaked to get the content generator to work properly.
    2. You may need to tweak the temperature of the bot to coax it to generate diverse content. Try starting at 0.7 and moving higher.
    3. Of the local LLMs that we are using in this tutorial, I would prioritize using llama3.2, but be sure to experiment with others that we've asked you to download, or else set your own `OPENAI_API_KEY` to use `gpt-4.1` (it's pretty good).
    """
    )
    return


@app.cell
def _():
    # Implement a `Slide` class to represent a single slide,
    # which has the `title` and a `content` fields.
    # Also implement a `.render()` method that can render a slide as Markdown.
    # Then implement a `StructuredBot` that can generate a `Slide`.

    from building_with_llms_made_simple.answers.project_deckbot_answers import slidebot

    return (slidebot,)


@app.cell
def _(mo, slidebot):
    slide = slidebot("A slide about why one should eat well.")
    mo.md(slide.render())
    return


@app.cell
def _():
    # Now implement the Deck generator!
    # For a reference on what it could look like, check out the next cell:
    return


@app.cell
def _():
    from building_with_llms_made_simple.answers.project_deckbot_answers import deckbot

    lightning_talk = deckbot("A lightning talk on SciPy conference.")
    return (lightning_talk,)


@app.cell
def _(lightning_talk, mo):
    mo.md(lightning_talk.render())
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
