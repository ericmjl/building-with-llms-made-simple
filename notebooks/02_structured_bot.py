# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "llamabot[all]==0.12.10",
#     "marimo",
#     "pyprojroot==0.3.0",
#     "rich==13.9.4",
#     "pydantic==2.10.6",
#     "building-with-llms-made-simple==0.0.1",
# ]
#
# [tool.uv.sources]
# building-with-llms-made-simple = { path = "../", editable = true }
# ///

import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Part 2: Structured Outputs with StructuredBot

    In this notebook, we'll explore how to generate structured outputs from LLMs using LlamaBot's StructuredBot interface.
    We'll learn how to create structured data models and use them to generate consistent, validated outputs.

    ## Learning Objectives

    By the end of this notebook, you will be able to:

    1. Understand the difference between free-form and structured LLM outputs
    2. Create and use Pydantic models to define structured data schemas
    3. Implement StructuredBot for generating structured outputs
    4. Add custom formatting methods to enhance output presentation
    5. Handle complex nested data structures
    6. Compare different models and temperature settings for structured generation
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Introduction to Structured Outputs

    In Part 1, we used SimpleBot to generate free-form text responses.
    While this works for many applications, sometimes we need more structured outputs
    that conform to a specific schema or format.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Why Structured Outputs?

    Structured outputs are important because they enable us to control the structure by which an LLM generates its outputs, and to do so in a consistent format. With this, we are given the affordance of ease of integration with other systems, type safety, and better error handling than with free-form generation.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### When would you use Structured Outputs?

    Essentially when you're looking to fill out anything that could plausibly look like a "form to fill".
    As we'll see later, we'll be modeling the "form" using Pydantic models,
    and the way that we give an LLM the form to fill is by passing the pydantic model into a `StructuredBot`.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Approaches to Structured Generation

    There are two main approaches to generating structured outputs from LLMs:

    1. **Prompting to get JSON**: Ask the model to generate JSON directly. This is simple to implement, but may not always produce valid JSON, and will always require post-processing.
    2. **Logits masking**: Used by the [Outlines](https://github.com/dottxt-ai/outlines) package, one compiles a finite state machine to constrain the model's output tokens. This ensures valid structured data. While more complex to implement, Outlines has made things simpler, and it is more reliable for structured generation.

    Within LlamaBot, because we rely on model providers (via LiteLLM) to handle structured generation, `StructuredBot` is thus agnostic to the method of structured generation.
    """
    )
    return


@app.cell
def _():
    from typing import List, Optional

    import llamabot as lmb
    from pydantic import BaseModel, Field
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Exercise: Create Your First StructuredBot

    Let's start by creating a simple structured bot that generates a person's information.
    We'll define a Pydantic model to represent the structure we want, then create a StructuredBot
    that will generate data conforming to this model.

    Your task is to:

    1. Create a `Person` model with:
        - `name`: The person's full name
        - `age`: Their age in years
        - `occupation`: Their current job or profession
    2. Create a StructuredBot that uses this model to generate person profiles. Each field should have:
        - A type annotation (str, int, etc.)
        - A description for the LLM
        - Validation rules (if needed)

    The LlamaBot API for accomplishing this is as follows:

    ```python
    import llamabot as lmb
    from pydantic import BaseModel, Field


    # In your code, change `ModelName`
    class ModelName(BaseModel):
        # Change `field1/2`, `field_type`, and the description "..."
        field1: field_type = Field(description="...")
        field2: field_type = Field(description="...")

    structured_bot = lmb.StructuredBot(
        system_prompt=...,
        pydantic_model=ModelName, # put the pydantic class name here.
        model_name="provider/model_name", # use ollama_chat/llama3.2 to start
    )
    ```
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
    Now, generate a new Person object using your `StructuredBot`.
    Remember that to call a LlamaBot, you simply call it like this:

    ```python
    response: ModelName = structured_bot("your request here")
    ```

    `response` will be of the class `ModelName` that is passed into it.
    """
    )
    return


@app.cell
def _():
    # Your code here!

    # Or uncomment my answer to see what to expect:
    # from building_with_llms_made_simple.answers.structured_bot_answers import (
    #     Person,
    #     person_generator,
    # )

    # person = person_generator("A technologist at a startup.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Filling in forms

    To hammer home the analogy that structured outputs are basically about filling in forms, I think it's useful to see the filling out of a form in action. Execution of the code above should automatically fill out the following Marimo UI elements, which I believe you can appreciate is just a form that needs to be filled out that can be used in downstream applications.
    """
    )
    return


@app.cell
def _(mo, person):
    name_field = mo.ui.text(label="Name", value=person.name)
    age_field = mo.ui.slider(
        label="Age", value=person.age, start=0, stop=120, step=1
    )
    occupation_field = mo.ui.text(label="Occupation", value=person.occupation)
    mo.vstack(
        [
            name_field,
            age_field,
            occupation_field,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Extend models

    Pydantic models are Python classes that define the structure of your data.
    Using Pydantic, we can take advantage of automatic validation and type checking,
    and it is easy to de/serialize from/to JSON.

    But on top of that, we can also provide custom methods (such as those used for rendering)!

    Go ahead and modify the Person object with a class method defined
    that returns a string representation of the object.
    (It can be `.str()` if you are a method chainer,
    or `__str__()` if you prefer to adhere to Python idioms.)
    Then, regenerate the object and try using its string display method.
    Or, if you're feeling fancy, refer to Marimo's [documentation on rich displays](https://docs.marimo.io/guides/integrating_with_marimo/displaying_objects/#option-2-implement-an-ipython-_repr__-method)
    for inspiration!
    """
    )
    return


@app.cell
def _():
    # Go and modify the Person object above,
    # and then print str(person) or person.str(), whichever you implemented.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Nested Data Structures

    You can also get `StructuredBot` to generate nested data structures.
    We are going to make this happen by creating a class list,
    which will be a collection of people.
    Nested Pydantic objects can be written as follows:

    ```python
    class Individual(BaseModel):
        # Change "something", "type", and "description goes here"
        something: type = Field("description goes here")

    class GroupLevel(BaseModel):
        # Change "group_iterable", "Individual", and "description goes here"
        group_iterable: list[Individual] = Field("description of group goes here.")
    ```

    The `GroupLevel` object can be passed to a `StructuredBot` to be generated:

    ```python
    structured_bot = lmb.StructuredBot(
        system_prompt=...,
        pydantic_model=GroupLevel, # put the pydantic class name here.
        model_name="provider/model_name", # use ollama_chat/llama3.2 to start
    )
    ```
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Exercise: Generate a class list of people

    Using the prompt above, generate for me a classrom's worth of people.
    """
    )
    return


@app.cell
def _():
    # Your code goes here!

    # Or uncomment my answers to see what happens!
    # from building_with_llms_made_simple.answers.structured_bot_answers import (
    #     tutorial_attendee_generator,
    # )

    # tutorial_attendee_generator("classroom of 5 senior/elderly people")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Check out notebook 09

    This notebook shows an example of how to use GPT-4o (you will need an OpenAI API key) for structured generation from images. It's super cool!
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Conclusions""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Core Concepts

    Structured generation represents
    a powerful paradigm shift in how we interact with LLMs.
    By using Pydantic models to define our data schemas,
    we gain the ability to generate consistent, validated outputs
    that can be seamlessly integrated into your applications.
    This approach not only ensures type safety
    but also provides a clear contract between your code
    and the LLM's output.

    I built StructuredBot as an interface to this structured world.
    Through it, you can control the generation process, fine-tune the temperature,
    and select the most appropriate model for your needs.
    The ability to customize output formats adds another layer of flexibility,
    allowing you to present the generated data in ways
    that best serve your specific use cases.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Best Practices

    When designing models for structured generation, it's crucial to be specific.
    Each model should serve a specific purpose.
    For most applications that I have seen, the more precise your object definition, the better.

        **Important Tip**: Avoid nesting your Pydantic models as much as possible!
    While nested structures can be useful, they often make it harder for LLMs to generate
    consistent outputs and can lead to more complex validation errors.
    Flatter structures tend to work better with structured generation.
    ([Source: Gabriel Harris on LinkedIn](https://www.linkedin.com/posts/drgabrielharris_struggling-to-get-consistent-structured-llm-activity-7344306907467186176-Bz78))

    Be sure to leverage pydantic model validators to catch errors in LLM output!
    For example, if you want an LLM to generate a prior probability value
    that corresponds to the likelihood of an event happening,
    you have two choices:

    1. Ask it to generate a float constrained to be between 0 and 1, or
    2. Ask it to generate the log odds (unbounded) and then inverse logit transform that value, thus obviating the need for constraint checks.

    I would lean towards using the latter, as it is easier to guarantee correctness through the logit transform, but the former is not wrong, we just can't guarantee one-shot mathematical correctness, as the LLM may still have a chance of proposing a value out of bounds, thus necessitating a second shot.

    One big tip is to heavily lean on the `Field` class to describe the data you want! The description is fed as context to the LLM. Any natural language provided will steer the LLM in a particular way.

    And don't forget to do Evals! That is a topic for the Evals notebook to cover 🤗.
    """
    )
    return


if __name__ == "__main__":
    app.run()
