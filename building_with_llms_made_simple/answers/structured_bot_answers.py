"""Example implementations of structured bots for the tutorial.

This module provides example implementations of structured bots
using LlamaBot's StructuredBot interface.
"""

import json

import llamabot as lmb
from pydantic import BaseModel, Field


class Person(BaseModel):
    """A model representing a person with basic attributes.

    :param name: The person's full name
    :param age: The person's age in years
    :param occupation: The person's current job or profession
    """

    name: str = Field(description="Their name. Any ethnicity is okay.")
    age: int = Field(description="Their age in years.")
    occupation: str = Field(description="Their current job description.")

    def _mime_(self) -> tuple[str, str]:
        """Return a MIME type and JSON representation of the person.

        :return: A tuple containing the MIME type and JSON string
        """
        return ("application/json", json.dumps(self.model_dump()))


person_generator = lmb.StructuredBot(
    system_prompt="You are a creative generator of fake personas.",
    pydantic_model=Person,
    model_name="ollama_chat/llama3.1",
    temperature=0.7,
)


class Tutorial(BaseModel):
    """A model representing a tutorial session with attendees.

    :param attendees: List of Person objects attending the tutorial
    """

    attendees: list[Person]

    def _mime_(self) -> tuple[str, str]:
        """Return a MIME type and JSON representation of the tutorial.

        :return: A tuple containing the MIME type and JSON string
        """
        return ("application/json", json.dumps(self.model_dump()))


tutorial_attendee_generator = lmb.StructuredBot(
    system_prompt="You are a creative generator of fake personas.",
    pydantic_model=Tutorial,
    model_name="ollama_chat/llama3.1",
    temperature=0.7,
)
