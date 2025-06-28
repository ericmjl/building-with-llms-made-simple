"""Sample answers for the project deckbot notebook."""

import llamabot as lmb
from pydantic import BaseModel, Field


class Slide(BaseModel):
    """A single slide in a presentation deck.

    :param title: Title of the slide.
    :param content: Markdown-based syntax of the slide content.
    """

    title: str = Field(
        description="Title of the slide. Unless otherwise specified, it should be an imperative statement of the main message of the slide."  # noqa: E501
    )
    content: str = Field(
        description="Markdown-based syntax of the slide content. Do NOT include headers of any kind! The contents can be bullet points, HTML, Markdown tables, HTML tables (to go fancier), one or two columns, etc. Design the content to be concise."  # noqa: E501
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
    """You are an expert at building Markdown-based slides that are concise, clear, and coherent. Slides that you build flow seamlessly from slide to slide. For each ask, provide a title and the content of the slide."""  # noqa: E501


slidebot = lmb.StructuredBot(
    system_prompt=slidebot_sysprompt(),
    pydantic_model=Slide,
    model_name="ollama_chat/llama3.2:latest",
    temperature=0.0,
)


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

    Always create complete, presentation-ready slide decks that tell a coherent story."""  # noqa: E501


deckbot = lmb.StructuredBot(
    system_prompt=deckbot_sysprompt(),
    pydantic_model=Deck,
    model_name="ollama_chat/llama3.2",
)
