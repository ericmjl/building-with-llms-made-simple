# /// script
# requires-python = ">=3.12"
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
    from rich import print

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

    class ModelName(BaseModel):
        field1: field_type
        field2: field_type

    structured_bot = lmb.StructuredBot(
        system_message=...,
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

    # Create the Person model and StructuredBot
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
    return


@app.cell
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
    ## Nested Data Structures

    You can also get `StructuredBot` to generate nested data structures.
    We are going to make this happen by creating a class list,
    which will be a collection of people.
    Nested Pydantic objects can be written as follows:

    ```python
    class Individual(BaseModel):
        something: type = Field("description goes here")

    class GroupLevel(BaseModel):
        group_iterable: list[Individual]
    ```

    The `GroupLevel` object can be passed to a `StructuredBot` to be generated:

    ```python
    structured_bot = lmb.StructuredBot(
        system_message=...,
        pydantic_model=GroupLevel, # put the pydantic class name here.
        model_name="provider/model_name", # use ollama_chat/llama3.2 to start
    )
    ```
    """
    )
    return


@app.cell
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

    return


@app.cell
def _(mo):
    mo.md(r"""## Conclusion""")
    return


@app.cell
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


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Best Practices

    When designing models for structured generation, it's crucial to be specific.
    Each model should serve a specific purpose.
    One big tip is to heavily lean on the `Field` class to describe the data you want.
    As you implement these models, you should start simple and gradually add complexity.
    Always test with different models and monitor performance.

    Output formatting deserves special attention.
    The way you present your generated data can significantly impact its usefulness.
    By creating purpose-specific formats,
    you can ensure that your outputs are contextually useful.
    """
    )
    return


if __name__ == "__main__":
    app.run()
