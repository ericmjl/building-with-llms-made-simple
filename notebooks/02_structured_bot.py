# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "llamabot[all]==0.11.2",
#     "marimo",
#     "pyprojroot==0.3. 0",
#     "rich==13.9.4",
#     "pydantic==2.10.6",
# ]
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
        """  # noqa: E501
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

        There are two main approaches to generating structured outputs from LLMs:

        1. **Prompting to get JSON**: We can ask the model to generate JSON directly in its response.
        2. **Logits masking**: We can constrain the model's output tokens to ensure it generates valid structured data.

        Let's show how each of these work.
        """  # noqa: E501
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
        """  # noqa: E501
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
        system_prompt="You are a helpful assistant that generates fictional person profiles.",  # noqa: E501
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
        This means we can access its attributes directly and use it like any other Python object.
        """  # noqa: E501
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
        """  # noqa: E501
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
        """  # noqa: E501
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2.4 Structured Git Commit Messages

        Now, let's apply what we've learned to our git commit message generator from Part 1.
        We'll create a structured version that breaks down a commit message into its constituent parts.
        """  # noqa: E501
    )
    return


@app.cell
def _(BaseModel, Field, Optional):
    class GitCommitMessage(BaseModel):
        """A structured git commit message following conventional commits format."""

        type: str = Field(
            ...,
            description="The type of change (e.g., feat, fix, docs, style, refactor, test, chore)",  # noqa: E501
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
    """  # noqa: E501
    return (git_diff,)


@app.cell
def _(GitCommitMessage, lmb):
    # Create a structured bot for git commit messages
    commit_message_bot = lmb.StructuredBot(
        system_prompt="You are a helpful assistant who generates structured git commit messages following conventional commits format.",  # noqa: E501
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
        """  # noqa: E501

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
        """  # noqa: E501
    )
    return


@app.cell
def _(BaseModel, Field, Optional):
    class GitCommitMessageWithEmoji(BaseModel):
        """A structured git commit message with emojis following conventional commits format."""  # noqa: E501

        type: str = Field(
            ...,
            description="The type of change (e.g., feat, fix, docs, style, refactor, test, chore)",  # noqa: E501
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
            description="An appropriate emoji for the commit type (e.g., ✨ for feat, 🐛 for fix, 📚 for docs, 💄 for style, ♻️ for refactor, ✅ for test, 🔧 for chore)",  # noqa: E501
        )

        def format(self) -> str:
            """Format the commit message with emoji according to conventional commits."""  # noqa: E501
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
        system_prompt="You are a helpful assistant who generates structured git commit messages with appropriate emojis following conventional commits format. Choose emojis that match the commit type (e.g., ✨ for feat, 🐛 for fix, 📚 for docs, 💄 for style, ♻️ for refactor, ✅ for test, 🔧 for chore).",  # noqa: E501
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
        """  # noqa: E501
    )
    return


@app.cell
def _(BaseModel, Field, Optional):
    class EnhancedGitCommitMessage(BaseModel):
        """An enhanced structured git commit message with multiple formatting options."""  # noqa: E501

        type: str = Field(
            ...,
            description="The type of change (e.g., feat, fix, docs, style, refactor, test, chore)",  # noqa: E501
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
            description="An appropriate emoji for the commit type (e.g., ✨ for feat, 🐛 for fix, 📚 for docs, 💄 for style, ♻️ for refactor, ✅ for test, 🔧 for chore)",  # noqa: E501
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
        system_prompt="You are a helpful assistant who generates structured git commit messages with appropriate emojis following conventional commits format.",  # noqa: E501
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
        """  # noqa: E501
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
        ## 2.6 Handling Complex Structured Data

        So far, we've worked with relatively simple structured data. Let's explore how to handle
        more complex structures, such as nested models and lists.
        """  # noqa: E501
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
        """A detailed git commit message with information about individual file changes."""  # noqa: E501

        type: str = Field(
            ...,
            description="The type of change (e.g., feat, fix, docs, style, refactor, test, chore)",  # noqa: E501
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
                message += f"\n- {change.change_type}: {change.filename} - {change.description}"  # noqa: E501

            # Add breaking changes if present
            if self.breaking_changes:
                message += f"\n\nBREAKING CHANGE: {self.breaking_changes}"

            return message

    return DetailedGitCommitMessage, FileChange


@app.cell
def _(DetailedGitCommitMessage, lmb):
    # Create a structured bot for detailed git commit messages
    detailed_commit_bot = lmb.StructuredBot(
        system_prompt="You are a helpful assistant who generates detailed structured git commit messages. Analyze the git diff to identify all file changes and provide specific descriptions for each file change.",  # noqa: E501
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
        """  # noqa: E501
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
                system_prompt="You are a helpful assistant who generates structured git commit messages following conventional commits format.",  # noqa: E501
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
        """  # noqa: E501
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
        ## 2.8 Summary & Conclusion

        In this notebook, we've learned:

        - How to use `StructuredBot` to generate outputs that conform to a predefined schema
        - How to define Pydantic models to represent structured data
        - How to add custom methods to format and present structured data
        - How to handle complex nested structures and lists
        - How different models and temperature settings affect structured generation

        Key concepts:

        - Templated text is a form, model it using Pydantic, and use structured generation methods to fill it in.
        - Content that we require an LLM to generate requires sufficient context to be provided.
        """  # noqa: E501
    )
    return


if __name__ == "__main__":
    app.run()
