# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = [
#     "anthropic==0.54.0",
#     "llamabot[all]==0.12.11",
#     "marimo",
#     "pydantic==2.11.7",
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

    return


@app.cell(hide_code=True)
def _():
    # Answer implementation
    class Slide(BaseModel):
        """A single slide in a presentation deck.

        :param title: Title of the slide.
        :param content: Markdown-based syntax of the slide content.
        """

        title: str = Field(
            description="Title of the slide. Unless otherwise specified, it should be an imperative statement of the main message of the slide."
        )
        content: str = Field(
            description="Markdown-based syntax of the slide content. Do NOT include headers of any kind! The contents can be bullet points, HTML, Markdown tables, HTML tables (to go fancier), one or two columns, etc. Design the content to be concise."
        )

        def render(self):
            """Render the slide as a markdown string.

            :return: A markdown string containing the slide's title and content.
            """
            return f"""
## {self.title}

{self.content}
"""

    @lmb.prompt("system")
    def slidebot_sysprompt():
        """You are an expert at building Markdown-based slides that are concise, clear, and coherent. Slides that you build flow seamlessly from slide to slide. For each ask, provide a title and the content of the slide."""

    slidebot = lmb.StructuredBot(
        system_prompt=slidebot_sysprompt(),
        pydantic_model=Slide,
        model_name="ollama_chat/llama3.2:latest",
        temperature=0.0,
    )

    return Slide, slidebot


@app.cell
def _(mo, slidebot):
    slide = slidebot("A slide about why one should eat well.")
    mo.md(slide.render())
    return (slide,)


@app.cell
def _():
    # Now implement the Deck generator!
    # For a reference on what it could look like, check out the next cell:
    return


@app.cell(hide_code=True)
def _(BaseModel, Field, Slide, lmb):
    # Answer implementation
    class Deck(BaseModel):
        """A collection of slides forming a complete presentation deck.

        :param slides: List of Slide objects that make up the deck.
        """

        slides: list[Slide]

        def render(self):
            """Render the entire deck as a markdown string.

            :return: A markdown string containing all slides separated by horizontal rules.
            """
            deck_md = ""

            for slide in self.slides:
                deck_md += slide.render() + "\n\n"
                deck_md += "---"
            return deck_md

    @lmb.prompt("system")
    def deckbot_sysprompt():
        """You are a professional presentation designer and content creator. Your job is to create engaging, well-structured slide decks based on user requests.

        When creating slides, follow these guidelines:
        - Create a logical flow from introduction to conclusion
        - Keep slide content concise and focused on key points
        - Use clear, engaging titles for each slide
        - Structure content with bullet points, short paragraphs, or clear sections
        - Ensure each slide serves a specific purpose in the overall narrative
        - Adapt the tone and complexity to match the intended audience
        - Include a mix of content types (introductory slides, main content, conclusions, etc.)

        Always create complete, presentation-ready slide decks that tell a coherent story."""

    deckbot = lmb.StructuredBot(
        system_prompt=deckbot_sysprompt(),
        pydantic_model=Deck,
        model_name="ollama_chat/llama3.2",
    )

    return Deck, deckbot


@app.cell
def _(deckbot):
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
