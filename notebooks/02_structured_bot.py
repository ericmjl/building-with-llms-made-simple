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
    We'll build on our git commit message generator from Part 1 and enhance it to produce structured, formatted outputs.

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
    4. Structured git commit messages
    5. Custom formatting methods
    6. Complex structured data
    7. Model and temperature comparisons
    8. Summary and key takeaways
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

    ### Why Structured Outputs?

    Structured outputs are important because they:

    1. Enable programmatic processing of LLM responses
    2. Ensure consistent data formats
    3. Make it easier to integrate with other systems
    4. Provide type safety and validation
    5. Allow for better error handling

    ### Approaches to Structured Generation

    There are two main approaches to generating structured outputs from LLMs:

    1. **Prompting to get JSON**:
       1. Ask the model to generate JSON directly
       2. Simple to implement
       3. May not always produce valid JSON
       4. Requires post-processing

    2. **Logits masking**:
       1. Constrain the model's output tokens
       2. Ensures valid structured data
       3. More complex to implement
       4. Better reliability

    Let's explore how StructuredBot implements these approaches to generate
    reliable structured outputs.
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

    2. Create a StructuredBot that uses this model to generate person profiles

    Each field should have:
    - A type annotation (str, int, etc.)
    - A description for the LLM
    - Validation rules (if needed)
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
    ### Discussion: Understanding Pydantic Models

    Pydantic models are Python classes that:

    1. Define the structure of your data
    2. Provide automatic validation
    3. Enable type checking
    4. Support serialization/deserialization
    5. Allow for custom methods and properties

    Let's examine how these features work in practice with our person example.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Structured Git Commit Messages

    Now, let's apply what we've learned to our git commit message generator from Part 1.
    We'll create a structured version that breaks down a commit message into its constituent parts.

    ### Conventional Commits Format

    We'll use the Conventional Commits specification, which provides:

    1. A standardized format for commit messages
    2. Clear categorization of changes
    3. Better changelog generation
    4. Improved version management

    Our structured commit message will include:

    1. `type`: The kind of change (feat, fix, docs, etc.)
    2. `scope`: The part of the codebase affected
    3. `description`: A short, imperative description
    4. `body`: A longer explanation (optional)
    5. `breaking_changes`: Any breaking changes (optional)

    ### Exercise: Implement Conventional Commits

    Your task is to:

    1. Create a `GitCommitMessage` model with the fields described above
    2. Add a `format` method to generate conventional commit messages
    3. Create a StructuredBot that uses this model
    4. Test it with a sample git diff
    """
    )
    return


@app.cell
def _(BaseModel, Field, Optional):
    class GitCommitMessage(BaseModel):
        """A structured git commit message following conventional commits format."""

        type: str = Field(
            ...,
            description="The type of change (e.g., feat, fix, docs, style, refactor, test, chore)",
        )
        scope: Optional[str] = Field(
            None, description="The scope of the change (optional, e.g., component name)"
        )
        description: str = Field(
            ..., description="A short, imperative description of the change"
        )
        body: Optional[str] = Field(
            None, description="A longer explanation of the change (optional)"
        )
        breaking_changes: Optional[str] = Field(
            None, description="Description of any breaking changes (optional)"
        )

        def format(self) -> str:
            """Format the commit message according to conventional commits."""
            # Start with type
            message = f"{self.type}"

            # Add scope if present
            if self.scope:
                message += f"({self.scope})"

            # Add description
            message += f": {self.description}"

            # Add body if present
            if self.body:
                message += f"\n\n{self.body}"

            # Add breaking changes if present
            if self.breaking_changes:
                message += f"\n\nBREAKING CHANGE: {self.breaking_changes}"

            return message

    return (GitCommitMessage,)


@app.cell
def _():
    # Get a git diff to work with
    git_diff = """
    diff --git a/scratch_notebooks/structuredbot.ipynb b/scratch_notebooks/structuredbot.ipynb
    new file mode 100644
    index 00000000..d4c73601
    --- /dev/null
    +++ b/scratch_notebooks/structuredbot.ipynb
    @@ -0,0 +1,60 @@
    +{
    + "cells": [
    +  {
    +   "cell_type": "code",
    +   "execution_count": null,
    +   "metadata": {},
    +   "outputs": [],
    +   "source": [
    +    "%load_ext autoreload\n",
    +    "%autoreload 2"
    +   ]
    +  },
    +  {
    +   "cell_type": "code",
    +   "execution_count": null,
    +   "metadata": {},
    +   "outputs": [],
    +   "source": [
    +    "import llamabot as lmb\n",
    +    "from pydantic import BaseModel, Field\n",
    +    "\n",
    +    "\n",
    +    "class Person(BaseModel):\n",
    +    "    name: str = Field(..., description=\"The name of the person\")\n",
    +    "    age: int = Field(..., description=\"The age of the person\")\n",
    +    "\n",
    +    "\n",
    +    "bot = lmb.StructuredBot(\n",
    +    "    system_prompt=\"You are a helpful assistant.\",\n",
    +    "    pydantic_model=Person,\n",
    +    "    model_name=\"ollama_chat/llama3.2:3b\",\n",
    +    "    stream_target=\"none\",\n",
    +    ")\n",
    +    "\n",
    +    "person = bot(\"Give me a person.\")\n"
    +   ]
    +  }
    + ],
    + "metadata": {
    +  "kernelspec": {
    +   "display_name": "notebooks",
    +   "language": "python",
    +   "name": "python3"
    +  },
    +  "language_info": {
    +   "codemirror_mode": {
    +    "name": "ipython",
    +    "version": 3
    +   },
    +   "file_extension": ".py",
    +   "mimetype": "text/x-python",
    +   "name": "python",
    +   "nbconvert_exporter": "python",
    +   "pygments_lexer": "ipython3",
    +   "version": "3.12.7"
    +  }
    + },
    + "nbformat": 4,
    + "nbformat_minor": 2
    +}
    """
    return (git_diff,)


@app.cell
def _(GitCommitMessage, lmb):
    # Create a structured bot for git commit messages
    commit_message_bot = lmb.StructuredBot(
        system_prompt="You are a helpful assistant who generates structured git commit messages following conventional commits format.",
        pydantic_model=GitCommitMessage,
        model_name="ollama_chat/llama3.2",
        temperature=0.0,  # Keep it deterministic
    )
    return (commit_message_bot,)


@app.cell
def _(lmb):
    @lmb.prompt("user")
    def structured_commit_prompt(git_diff: str):
        """
        Here is the git diff:

        {{ git_diff }}

        Based on this diff, generate a structured git commit message following the conventional commits format.
        Include appropriate type, scope (if relevant), description, and body (if needed).
        If there are breaking changes, please note them.
        """

    return (structured_commit_prompt,)


@app.cell
def _(commit_message_bot, git_diff, structured_commit_prompt):
    # Generate the structured commit message
    commit_message = commit_message_bot(structured_commit_prompt(git_diff))
    return (commit_message,)


@app.cell
def _(commit_message, print):
    # Examine the structured commit message
    print("Type:", commit_message.type)
    print("Scope:", commit_message.scope)
    print("Description:", commit_message.description)
    print("Body:", commit_message.body)
    print("Breaking Changes:", commit_message.breaking_changes)

    print("\nFormatted Commit Message:")
    print(commit_message.format())
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Exercise: Add Emojis to Commit Messages

    Let's enhance our commit message model to include emojis based on the commit type.
    Modify the `GitCommitMessage` class to include an emoji field and update the `format` method
    to include the emoji in the formatted message.
    """
    )
    return


@app.cell
def _(BaseModel, Field, Optional):
    class GitCommitMessageWithEmoji(BaseModel):
        """A structured git commit message with emojis following conventional commits format."""

        type: str = Field(
            ...,
            description="The type of change (e.g., feat, fix, docs, style, refactor, test, chore)",
        )
        scope: Optional[str] = Field(
            None, description="The scope of the change (optional, e.g., component name)"
        )
        description: str = Field(
            ..., description="A short, imperative description of the change"
        )
        body: Optional[str] = Field(
            None, description="A longer explanation of the change (optional)"
        )
        breaking_changes: Optional[str] = Field(
            None, description="Description of any breaking changes (optional)"
        )
        emoji: str = Field(
            ...,
            description="An appropriate emoji for the commit type (e.g., ✨ for feat, 🐛 for fix, 📚 for docs, 💄 for style, ♻️ for refactor, ✅ for test, 🔧 for chore)",
        )

        def format(self) -> str:
            """Format the commit message with emoji according to conventional commits."""
            # Start with emoji and type
            message = f"{self.emoji} {self.type}"

            # Add scope if present
            if self.scope:
                message += f"({self.scope})"

            # Add description
            message += f": {self.description}"

            # Add body if present
            if self.body:
                message += f"\n\n{self.body}"

            # Add breaking changes if present
            if self.breaking_changes:
                message += f"\n\nBREAKING CHANGE: {self.breaking_changes}"

            return message

    return (GitCommitMessageWithEmoji,)


@app.cell
def _(GitCommitMessageWithEmoji, lmb):
    # Create a structured bot for git commit messages with emojis
    emoji_commit_bot = lmb.StructuredBot(
        system_prompt="You are a helpful assistant who generates structured git commit messages with appropriate emojis following conventional commits format. Choose emojis that match the commit type (e.g., ✨ for feat, 🐛 for fix, 📚 for docs, 💄 for style, ♻️ for refactor, ✅ for test, 🔧 for chore).",
        pydantic_model=GitCommitMessageWithEmoji,
        model_name="ollama_chat/llama3.2",
        temperature=0.0,  # Keep it deterministic
    )
    return (emoji_commit_bot,)


@app.cell
def _(emoji_commit_bot, git_diff, structured_commit_prompt):
    # Generate the structured commit message with emoji
    emoji_commit_message = emoji_commit_bot(structured_commit_prompt(git_diff))
    return (emoji_commit_message,)


@app.cell
def _(emoji_commit_message, print):
    # Examine the structured commit message with emoji
    print("Type:", emoji_commit_message.type)
    print("Scope:", emoji_commit_message.scope)
    print("Description:", emoji_commit_message.description)
    print("Emoji:", emoji_commit_message.emoji)

    print("\nFormatted Commit Message with Emoji:")
    print(emoji_commit_message.format())
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## 2.5 Adding Custom Methods to Format Output

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

    1. `format_conventional()`: Standard conventional commits format
    2. `format_with_emoji()`: Adds emojis for better visual scanning
    3. `format_short()`: Compact version for quick reference
    4. `format_markdown()`: GitHub-friendly markdown format

    Each method serves a different purpose and can be used in different contexts.
    """
    )
    return


@app.cell
def _(BaseModel, Field, Optional):
    class EnhancedGitCommitMessage(BaseModel):
        """An enhanced structured git commit message with multiple formatting options."""

        type: str = Field(
            ...,
            description="The type of change (e.g., feat, fix, docs, style, refactor, test, chore)",
        )
        scope: Optional[str] = Field(
            None, description="The scope of the change (optional, e.g., component name)"
        )
        description: str = Field(
            ..., description="A short, imperative description of the change"
        )
        body: Optional[str] = Field(
            None, description="A longer explanation of the change (optional)"
        )
        breaking_changes: Optional[str] = Field(
            None, description="Description of any breaking changes (optional)"
        )
        emoji: str = Field(
            ...,
            description="An appropriate emoji for the commit type (e.g., ✨ for feat, 🐛 for fix, 📚 for docs, 💄 for style, ♻️ for refactor, ✅ for test, 🔧 for chore)",
        )

        def format_conventional(self) -> str:
            """Format the commit message according to conventional commits."""
            # Start with type
            message = f"{self.type}"

            # Add scope if present
            if self.scope:
                message += f"({self.scope})"

            # Add description
            message += f": {self.description}"

            # Add body if present
            if self.body:
                message += f"\n\n{self.body}"

            # Add breaking changes if present
            if self.breaking_changes:
                message += f"\n\nBREAKING CHANGE: {self.breaking_changes}"

            return message

        def format_with_emoji(self) -> str:
            """Format the commit message with emoji."""
            # Start with emoji and type
            message = f"{self.emoji} {self.type}"

            # Add scope if present
            if self.scope:
                message += f"({self.scope})"

            # Add description
            message += f": {self.description}"

            # Add body if present
            if self.body:
                message += f"\n\n{self.body}"

            # Add breaking changes if present
            if self.breaking_changes:
                message += f"\n\nBREAKING CHANGE: {self.breaking_changes}"

            return message

        def format_short(self) -> str:
            """Format a short version of the commit message (first line only)."""
            # Start with emoji and type
            message = f"{self.emoji} {self.type}"

            # Add scope if present
            if self.scope:
                message += f"({self.scope})"

            # Add description
            message += f": {self.description}"

            return message

        def format_markdown(self) -> str:
            """Format the commit message as markdown."""
            # Start with header
            message = f"## {self.emoji} {self.type}"

            # Add scope if present
            if self.scope:
                message += f"({self.scope})"

            # Add description
            message += f": {self.description}"

            # Add body if present
            if self.body:
                message += f"\n\n{self.body}"

            # Add breaking changes if present
            if self.breaking_changes:
                message += f"\n\n**BREAKING CHANGE:** {self.breaking_changes}"

            return message

    return (EnhancedGitCommitMessage,)


@app.cell
def _(EnhancedGitCommitMessage, lmb):
    # Create a structured bot for enhanced git commit messages
    enhanced_commit_bot = lmb.StructuredBot(
        system_prompt="You are a helpful assistant who generates structured git commit messages with appropriate emojis following conventional commits format.",
        pydantic_model=EnhancedGitCommitMessage,
        model_name="ollama_chat/llama3.2",
        temperature=0.0,  # Keep it deterministic
    )
    return (enhanced_commit_bot,)


@app.cell
def _(enhanced_commit_bot, git_diff, structured_commit_prompt):
    # Generate the enhanced structured commit message
    enhanced_commit_message = enhanced_commit_bot(structured_commit_prompt(git_diff))
    return (enhanced_commit_message,)


@app.cell
def _(enhanced_commit_message, print):
    # Display different formatting options
    print("Conventional Format:")
    print(enhanced_commit_message.format_conventional())

    print("\nWith Emoji:")
    print(enhanced_commit_message.format_with_emoji())

    print("\nShort Format:")
    print(enhanced_commit_message.format_short())

    print("\nMarkdown Format:")
    print(enhanced_commit_message.format_markdown())
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Exercise: Create a Custom Formatting Method

    Now it's your turn! Add a new formatting method to the `EnhancedGitCommitMessage` class
    that formats the commit message in a style of your choice. For example, you could create
    a format for HTML, Slack messages, or a custom format for your team.
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
    ## 2.6 Handling Complex Structured Data

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

    Let's see how to implement these concepts with our git commit message example.
    """
    )
    return


@app.cell
def _(BaseModel, Field, List, Optional):
    class FileChange(BaseModel):
        """Represents a single file change in a git commit."""

        filename: str = Field(..., description="The name of the file that was changed")
        change_type: str = Field(
            ..., description="The type of change (added, modified, deleted, renamed)"
        )
        description: str = Field(
            ..., description="A brief description of what changed in this file"
        )

    class DetailedGitCommitMessage(BaseModel):
        """A detailed git commit message with information about individual file changes."""

        type: str = Field(
            ...,
            description="The type of change (e.g., feat, fix, docs, style, refactor, test, chore)",
        )
        scope: Optional[str] = Field(  # noqa: F821
            None, description="The scope of the change (optional, e.g., component name)"
        )
        description: str = Field(
            ..., description="A short, imperative description of the change"
        )
        body: Optional[str] = Field(  # noqa: F821
            None, description="A longer explanation of the change (optional)"
        )
        breaking_changes: Optional[str] = Field(  # noqa: F821
            None, description="Description of any breaking changes (optional)"
        )
        emoji: str = Field(..., description="An appropriate emoji for the commit type")
        file_changes: List[FileChange] = Field(
            ..., description="List of files changed in this commit with descriptions"
        )

        def format_detailed(self) -> str:
            """Format a detailed commit message including file changes."""
            # Start with emoji and type
            message = f"{self.emoji} {self.type}"

            # Add scope if present
            if self.scope:
                message += f"({self.scope})"

            # Add description
            message += f": {self.description}"

            # Add body if present
            if self.body:
                message += f"\n\n{self.body}"

            # Add file changes
            message += "\n\nChanges:"
            for change in self.file_changes:
                message += f"\n- {change.change_type}: {change.filename} - {change.description}"

            # Add breaking changes if present
            if self.breaking_changes:
                message += f"\n\nBREAKING CHANGE: {self.breaking_changes}"

            return message

    return (DetailedGitCommitMessage,)


@app.cell
def _(DetailedGitCommitMessage, lmb):
    # Create a structured bot for detailed git commit messages
    detailed_commit_bot = lmb.StructuredBot(
        system_prompt="You are a helpful assistant who generates detailed structured git commit messages. Analyze the git diff to identify all file changes and provide specific descriptions for each file change.",
        pydantic_model=DetailedGitCommitMessage,
        model_name="ollama_chat/llama3.2",
        temperature=0.0,  # Keep it deterministic
    )
    return (detailed_commit_bot,)


@app.cell
def _(detailed_commit_bot, git_diff, structured_commit_prompt):
    # Generate the detailed structured commit message
    detailed_commit_message = detailed_commit_bot(structured_commit_prompt(git_diff))
    return (detailed_commit_message,)


@app.cell
def _(detailed_commit_message, print):
    # Display the detailed commit message
    print("Detailed Commit Message:")
    print(detailed_commit_message.format_detailed())

    print("\nFile Changes:")
    for i, change in enumerate(detailed_commit_message.file_changes, 1):
        print(f"{i}. {change.filename} ({change.change_type}): {change.description}")
    return


@app.cell(hide_code=True)
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

    2. Compare their outputs for the same git diff, looking at:
       - Quality of the commit message
       - Appropriateness of the commit type
       - Level of detail in the description and body
       - Consistency across multiple runs

    3. Document your observations about:
       - Which model/temperature combinations work best
       - Trade-offs between creativity and consistency
       - Impact on structured output quality
    """
    )
    return


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
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
