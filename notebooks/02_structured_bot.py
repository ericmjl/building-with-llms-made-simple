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


@app.cell
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

    The notebook is structured as follows:

    1. Introduction to structured outputs
    2. Creating your first StructuredBot
    3. Understanding structured generation
    4. Custom formatting methods
    5. Complex structured data
    6. Model and temperature comparisons
    7. Summary and key takeaways
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

    return BaseModel, Field, List, Optional, lmb, print


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
    ## Custom Formatting Methods

    We've already seen how to add a custom `format` method to our Pydantic model.
    Let's explore this further by adding more methods to customize how we present our structured data.

    ### Why Custom Formatting?

    Custom formatting methods help:

    1. Present data in different formats (JSON, Markdown, HTML, etc.)
    2. Adapt output for different platforms (GitHub, Slack, etc.)
    3. Create specialized views for different use cases
    4. Maintain consistency across your application
    5. Make the output more readable and useful

    ### Types of Formatting Methods

    We'll implement several formatting methods:

    1. `format_conventional()`: Standard format
    2. `format_with_emoji()`: Adds emojis for better visual scanning
    3. `format_short()`: Compact version for quick reference
    4. `format_markdown()`: GitHub-friendly markdown format

    Each method serves a different purpose and can be used in different contexts.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Complex Structured Data

    So far, we've worked with relatively simple structured data. Let's explore how to handle
    more complex structures, such as nested models and lists.

    ### Types of Complex Structures

    Common complex data structures include:

    1. **Nested Models**
       1. Models within models
       2. Hierarchical relationships
       3. Parent-child connections

    2. **Lists and Collections**
       1. Arrays of items
       2. Multiple related objects
       3. Repeating patterns

    3. **Optional Fields**
       1. Conditional data
       2. Optional relationships
       3. Flexible structures

    ### Best Practices for Complex Data

    When working with complex structures:

    1. Keep models focused and single-purpose
    2. Use clear, descriptive field names
    3. Document relationships between models
    4. Consider validation requirements
    5. Plan for serialization needs
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Model Comparison Exercise

    Let's experiment with different models and temperature settings to see how they affect
    the quality and variability of structured outputs.

    ### Understanding Temperature

    Temperature controls the randomness of the model's outputs:

    1. **Low temperature (0.0)**: More deterministic, consistent outputs
    2. **High temperature (0.8+)**: More creative, varied outputs
    3. **Medium temperature (0.5)**: Balanced between consistency and creativity

    ### Exercise: Compare Model Outputs

    Your task is to:

    1. Create bots with different models and temperatures:
       - Try models like llama3.2, phi4, and gemma2:2b
       - Test temperatures of 0.0, 0.5, and 0.8

    2. Compare their outputs for the same input, looking at:
       - Quality of the output
       - Appropriateness of the content
       - Level of detail
       - Consistency across multiple runs

    3. Document your observations about:
       - Which model/temperature combinations work best
       - Trade-offs between creativity and consistency
       - Impact on structured output quality
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Discussion: Evaluation Best Practices

    Take a few minutes to discuss with your peers:

    1. What principles and practices should guide our approach to structured generation?
    2. How should the potential consequences of an LLM's output influence our evaluation process?
       - Consider: The gravity of consequences should directly inform the depth and rigor of evaluation needed.
    3. What metrics would you use to evaluate the quality of structured outputs?
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Summary & Key Takeaways

    In this notebook, we've explored the fundamentals of structured generation with LLMs.
    Here are the key concepts and lessons learned:

    ### Core Concepts

    1. **Structured Generation**
       - Using Pydantic models to define data schemas
       - Generating consistent, validated outputs
       - Handling complex data structures
       - Customizing output formats

    2. **Pydantic Models**
       - Type safety and validation
       - Field descriptions and constraints
       - Custom methods and properties
       - Serialization capabilities

    3. **StructuredBot Features**
       - Schema-based generation
       - Temperature control
       - Model selection
       - Custom formatting

    ### Best Practices

    1. **Model Design**
       - Keep models focused and single-purpose
       - Use clear, descriptive field names
       - Document relationships and constraints
       - Plan for validation needs

    2. **Implementation**
       - Start with simple structures
       - Add complexity gradually
       - Test with different models
       - Monitor performance

    3. **Output Formatting**
       - Create purpose-specific formats
       - Consider target platforms
       - Maintain consistency
       - Document format methods

    ### Next Steps

    1. **Explore Advanced Features**
       - Custom validators
       - Complex nested structures
       - Dynamic model generation
       - Advanced formatting options

    2. **Apply to Real Projects**
       - API documentation
       - Data processing pipelines
       - Automated workflows
       - Integration with other systems

    3. **Optimize Performance**
       - Model selection
       - Temperature tuning
       - Response formatting
       - Error handling

    Remember: The key to successful structured generation is understanding your data
    requirements and choosing the right tools and approaches for your specific use case.
    Take time to plan your data structures and test different configurations to find
    what works best for your needs.
    """
    )
    return


if __name__ == "__main__":
    app.run()
