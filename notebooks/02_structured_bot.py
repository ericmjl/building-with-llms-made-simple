# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "llamabot[all]>=0.12.6",
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

__generated_with = "0.13.11"
app = marimo.App(
    width="medium",
)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Part 2: Structured Outputs with StructuredBot

        In this notebook, we'll learn how to generate structured outputs from LLMs using LlamaBot's StructuredBot interface.
        We'll build on our git commit message generator from Part 1 and enhance it to produce structured, formatted outputs.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Learning Objectives

        By the end of this notebook, you will be able to:

        1. Understand the difference between free-form and structured LLM outputs
        2. Create and use Pydantic models to define structured data schemas
        3. Implement StructuredBot for generating structured outputs
        4. Add custom formatting methods to enhance output presentation
        5. Handle complex nested data structures
        6. Compare different models and temperature settings for structured generation

        The notebook is structured as follows:

        - Section 2.1: Introduction to structured outputs
        - Section 2.2: Creating your first StructuredBot
        - Section 2.3: Understanding structured generation
        - Section 2.4: Structured git commit messages
        - Section 2.5: Custom formatting methods
        - Section 2.6: Complex structured data
        - Section 2.7: Model and temperature comparisons
        - Section 2.8: Summary and key takeaways
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 2.1 Introduction to Structured Outputs

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


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2.2 Creating Your First StructuredBot

        Let's start by creating a simple structured bot that generates a person's information.
        We'll define a Pydantic model to represent the structure we want, then create a StructuredBot
        that will generate data conforming to this model.

        ### Understanding Pydantic Models

        Pydantic models are Python classes that:

        1. Define the structure of your data
        2. Provide automatic validation
        3. Enable type checking
        4. Support serialization/deserialization
        5. Allow for custom methods and properties

        In our example, we'll create a `Person` model with:

        1. `name`: The person's full name
        2. `age`: Their age in years
        3. `occupation`: Their current job or profession

        Each field will have:

        1. A type annotation (str, int, etc.)
        2. A description for the LLM
        3. Validation rules (if needed)
        """
    )
    return


@app.cell
def _(BaseModel, Field, lmb):
    class Person(BaseModel):
        name: str = Field(..., description="The person's full name")
        age: int = Field(..., description="The person's age in years")
        occupation: str = Field(
            ..., description="The person's current job or profession"
        )

    person_bot = lmb.StructuredBot(
        system_prompt="You are a helpful assistant that generates fictional person profiles.",
        pydantic_model=Person,
        model_name="ollama_chat/llama3.2",
    )
    return Person, person_bot


@app.cell
def _(person_bot):
    person = person_bot("Generate a profile for a software developer.")
    return (person,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Anatomy of a Structured Response

        The response from a StructuredBot is an instance of the Pydantic model we defined.
        This means we can:

        1. **Access Attributes Directly**
           ```python
           print(person.name)  # Access the name field
           print(person.age)   # Access the age field
           ```

        2. **Convert to Different Formats**
           ```python
           person_dict = person.model_dump()  # Convert to dictionary
           person_json = person.model_dump_json()  # Convert to JSON
           ```

        3. **Validate Data**
           1. Type checking is automatic
           2. Custom validators can be added
           3. Invalid data raises clear errors

        4. **Add Custom Methods**
           1. Format the data
           2. Compute derived values
           3. Implement business logic

        Let's see these features in action with our person example.
        """
    )
    return


@app.cell
def _(person, print):
    # Access individual fields
    print(f"Name: {person.name}")
    print(f"Age: {person.age}")
    print(f"Occupation: {person.occupation}")

    # Convert to dictionary
    person_dict = person.model_dump()
    print("\nAs dictionary:")
    print(person_dict)

    # Convert to JSON
    person_json = person.model_dump_json(indent=2)
    print("\nAs JSON:")
    print(person_json)
    return person_dict, person_json


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Exercise: Create Your Own Structured Model

        Now it's your turn! Create a Pydantic model for a book with fields like title, author,
        publication year, and genre. Then create a StructuredBot that generates book information.
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
        ## 2.3 Understanding How Structured Generation Works

        When we use StructuredBot, the following happens behind the scenes:

        1. The bot takes our Pydantic model and converts it to a JSON schema
        2. It includes this schema in the prompt to the LLM
        3. It asks the LLM to generate a valid JSON object that conforms to the schema
        4. It validates the response against the schema
        5. It converts the validated JSON into a Pydantic model instance

        This process ensures that the output conforms to our expected structure.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Autoregressive Generation and Logits Masking

        Modern LLMs generate text token by token in an autoregressive manner - each token is generated
        based on all previous tokens.

        Logits masking is a technique that constrains which tokens the model can generate next.
        For example, if we're generating JSON, we can mask out tokens that would result in invalid JSON.

        This is particularly useful for ensuring the model generates valid structured outputs.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2.4 Structured Git Commit Messages

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

        ### Benefits of Structured Commit Messages

        Using structured commit messages helps:

        1. Maintain consistency across the team
        2. Automate changelog generation
        3. Enable better version management
        4. Improve code review efficiency
        5. Facilitate automated workflows
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

    return DetailedGitCommitMessage, FileChange


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
    return change, i


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2.7 Class Discussion: Comparing Models and Temperatures

        Let's experiment with different models and temperature settings to see how they affect
        the quality and variability of structured outputs.

        ### Understanding Temperature

        Temperature controls the randomness of the model's outputs:

        1. **Low temperature (0.0)**: More deterministic, consistent outputs
        2. **High temperature (0.8+)**: More creative, varied outputs
        3. **Medium temperature (0.5)**: Balanced between consistency and creativity

        ### Model Characteristics

        Different models have different strengths:

        1. **Size and Capability**
           1. Larger models (7B+ parameters) handle complex structures better
           2. Smaller models are faster but may struggle with complex data

        2. **Training Data**
           1. Some models are better at specific domains
           2. Consider the model's training data when choosing

        3. **Response Quality**
           1. Accuracy of structured data
           2. Consistency of formatting
           3. Adherence to schemas

        ### What to Look For

        When comparing models and temperatures, consider:

        1. **Structured Output Quality**
           1. Schema compliance
           2. Data accuracy
           3. Format consistency

        2. **Response Characteristics**
           1. Creativity vs. consistency
           2. Detail level
           3. Error rates

        3. **Performance Metrics**
           1. Response time
           2. Token usage
           3. Cost efficiency
        """
    )
    return


@app.cell
def _(GitCommitMessage, lmb):
    # Create bots with different models and temperatures
    models_to_try = [
        "ollama_chat/llama3.2",
        "ollama_chat/phi4",
        "ollama_chat/gemma2:2b",
    ]

    temperatures = [0.0, 0.5, 0.8]

    # Create a dictionary to store our bots
    bots = {}

    for model in models_to_try:
        for temp in temperatures:
            bot_key = f"{model.split('/')[-1]}_temp{temp}"
            bots[bot_key] = lmb.StructuredBot(
                system_prompt="You are a helpful assistant who generates structured git commit messages following conventional commits format.",
                pydantic_model=GitCommitMessage,
                model_name=model,
                temperature=temp,
            )
    return bot_key, bots, model, models_to_try, temp, temperatures


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Exercise: Compare Model Outputs

        Choose a few bots from the dictionary above and compare their outputs for the same git diff.
        What differences do you notice in terms of:

        1. Quality of the commit message
        2. Appropriateness of the commit type
        3. Level of detail in the description and body
        4. Consistency across multiple runs (for higher temperatures)
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
        ## 2.8 Summary & Key Takeaways

        In this notebook, we've explored the fundamentals of structured generation with LLMs.
        Here are the key concepts and lessons learned:

        ### Core Concepts

        1. **Structured Generation**
           1. Using Pydantic models to define data schemas
           2. Generating consistent, validated outputs
           3. Handling complex data structures
           4. Customizing output formats

        2. **Pydantic Models**
           1. Type safety and validation
           2. Field descriptions and constraints
           3. Custom methods and properties
           4. Serialization capabilities

        3. **StructuredBot Features**
           1. Schema-based generation
           2. Temperature control
           3. Model selection
           4. Custom formatting

        ### Best Practices

        1. **Model Design**
           1. Keep models focused and single-purpose
           2. Use clear, descriptive field names
           3. Document relationships and constraints
           4. Plan for validation needs

        2. **Implementation**
           1. Start with simple structures
           2. Add complexity gradually
           3. Test with different models
           4. Monitor performance

        3. **Output Formatting**
           1. Create purpose-specific formats
           2. Consider target platforms
           3. Maintain consistency
           4. Document format methods

        ### Next Steps

        1. **Explore Advanced Features**
           1. Custom validators
           2. Complex nested structures
           3. Dynamic model generation
           4. Advanced formatting options

        2. **Apply to Real Projects**
           1. API documentation
           2. Data processing pipelines
           3. Automated workflows
           4. Integration with other systems

        3. **Optimize Performance**
           1. Model selection
           2. Temperature tuning
           3. Response formatting
           4. Error handling

        Remember: The key to successful structured generation is understanding your data
        requirements and choosing the right tools and approaches for your specific use case.
        Take time to plan your data structures and test different configurations to find
        what works best for your needs.
        """
    )
    return


if __name__ == "__main__":
    app.run()
