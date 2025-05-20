# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "llamabot==0.12.1",
#     "marimo",
#     "pyprojroot==0.3.0",
#     "rich==13.9.4",
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


@app.cell
def _(mo):
    mo.md(
        r"""
        # Part 1: Introduction to LLM APIs with SimpleBot

        In this notebook, we'll learn how to interact with LLMs using LlamaBot's SimpleBot interface.
        We'll start with basic interactions and build up to creating a git commit message generator.
        """  # noqa: E501
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1.1 Creating Your First SimpleBot

        Let's start by creating a simple bot and understanding the basic components of an LLM interaction.

        LLM interactions are, for the vast majority of applications, controlled by an API call.
        The absolute basics of this API call are that it needs structured with the following components:

        - A system prompt, which sets the language model's persona across API calls (it is kept constant),
        - A model name specifying which language model, and
        - A user prompt, which sets the specific interaction that a user wants to have with the LM.

        Let's see it in action.
        """  # noqa: E501
    )
    return


@app.cell
def _():
    import llamabot as lmb
    from rich import print

    bot = lmb.SimpleBot(
        system_prompt="You are a helpful assistant who provides concise, accurate responses.",  # noqa: E501
        model_name="ollama_chat/llama3.2",
    )
    return bot, lmb, print


@app.cell
def _(bot):
    response = bot("Aloha")
    return (response,)


@app.cell
def _(mo):
    mo.md(r"""And this is the anatomy of a `response` object:""")
    return


@app.cell
def _(response):
    response.role, response.content
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## 1.2 Altering the `SimpleBot`'s persona

    One can switch out the persona of a simple bot by changing the `system_prompt`.
    For example, if we want to turn the bot
    into one that responds like Richard Feynman:
    """
    )
    return


@app.cell
def _(lmb):
    feynman_bot = lmb.SimpleBot(
        system_prompt="You are a helpful assistant who responds like Richard Feynman.",
        model_name="ollama_chat/llama3.2",
    )
    feynman_bot("Aloha!")
    return (feynman_bot,)


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Exercise

    Now, I'd like you to try setting the persona of your own bot.
    Copy and paste the above code and change the `system_prompt`
    to something that you like.
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
    ### Setting personas for tasks

    In general, setting personas for various tasks is a form of
    "steering the model" to generate text that conforms to your eventual specs.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## 1.3 Poetry, Feynman-style

    Now, we're going to change up the bot a bit.
    We are going to ask the bot to do something slightly different.
    I am going to see if I can come up with poems, Richard Feynman style.
    """
    )
    return


@app.cell
def _(feynman_bot):
    feynman_bot("Write me a poem about scientific computing!")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Making Feynman more creative

    As it turns out, there is a tunable parameter for the `SimpleBot`
    that allows you to set the `temperature` of the model.
    The `temperature` parameter controls the randomness of the model's responses.
    A higher temperature will make the model more creative,
    but also more likely to generate nonsensical responses.
    A lower temperature will make the model more conservative,
    but also more likely to generate boring responses.
    """
    )
    return


@app.cell
def _(lmb):
    creative_feynman_bot = lmb.SimpleBot(
        system_prompt="You are a helpful assistant who responds like Richard Feynman.",
        model_name="ollama_chat/llama3.2",
        temperature=0.8,
    )

    creative_feynman_bot("Write me a poem about scientific computing!")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Exercise

    It's now your turn! Take your bot, which you created above,
    and turn it into a more creative version by tweaking the temperature parameter.
    Execute the bot a few times and observe what the variation in outputs is like.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## 1.4 A new task: Composing commit messages

    Within `llamabot`, I developed (and evolved) a commit message writing bot
    in September of 2023.
    Using this as a case study, I am going to show you the development process
    of building stuff that include LLMs as part of the mix.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Class discussion

    To write a git commit message drafter, what components do we need?

    - Point 1...
    - Point 2...
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Exercise

        Obtain a git diff from any repository that you have access to. Make sure the diff isn't too long, i.e. it fits within one screen. You may need to execute the following terminal commands:

        ```bash
        git diff HEAD~2 HEAD~1  # put the lower number in the last position.
        # OR
        git diff HEAD~3 HEAD~2
        ```

        Copy and paste them into the following code block, or else just use what I've provided below instead.
        """  # noqa: E501
    )
    return


@app.cell
def _():
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
def _(mo):
    mo.md(
        r"""
    Now, create the SimpleBot that is
    going to be generating the commit message.
    """
    )
    return


@app.cell
def _(git_diff, lmb):
    commit_message_bot = lmb.SimpleBot(
        system_prompt="You are a helpful assistant who generates git commit messages.",
        # `ollama_chat/` as a prefix is necessary
        # b/c we are using Ollama as our LM provider.
        model_name="ollama_chat/llama3.2",
        temperature=0.0,
    )

    commit_message_bot(git_diff)
    return (commit_message_bot,)


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Class discussion

    What do you like, and what do you not like, about this implementation thus far?

    ✅ Like:

    - Point 1...

    ❌ Dislike:

    - Point 1...
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Improve the prompt

    As it turns out, we can improve the prompt further.
    We are allowed to provide multiple messages to a SimpleBot.
    """
    )
    return


@app.cell
def _(commit_message_bot, git_diff):
    commit_message_bot(
        "Here is the git diff: ",
        git_diff,
        "Now return for me the git commit message in conventional commits format.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Note how we've steered the prompt to be more specific to the task at hand.
    This is a form of "prompt design" that is crucial to getting the model
    to generate the desired output.
    I do not use the term "prompt engineering",
    as there is little engineering happening here. It's mostly linguistics,
    and it engages the design side of our heads more than the engineering side.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Notice how the prompt is a bit verbose this way?
    It feels like this could be templated.
    LlamaBot has a `@prompt` decorator
    that can give us the ability to template prompts
    using `jinja2` templates and docstrings,
    within a Python docstring.
    This turns out to be super ergonomic!
    """
    )
    return


@app.cell
def _(lmb):
    @lmb.prompt("user")
    def commit_bot_user_prompt(git_diff: str):
        """
        Here is the git diff:

        {{ git_diff }}

        Now return for me the git commit message in conventional commits format.
        """

    return (commit_bot_user_prompt,)


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Exercise: run commit bot user prompt

    Now, the `commit_bot_user_prompt` will interpolate the docstring accordingly.
    Try it out below:
    """
    )
    return


@app.cell
def _(commit_bot_user_prompt, git_diff, print):
    commit_message_prompt = commit_bot_user_prompt(git_diff)
    print(commit_message_prompt)
    return (commit_message_prompt,)


@app.cell
def _(mo):
    mo.md(
        r"""
    It returns a User message (instantiated as a BaseMessage),
    and has both the `role` and the `content` fields.
    """
    )
    return


@app.cell
def _(commit_message_prompt, print):
    print(commit_message_prompt.content)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Since we have the message formatted properly,
    we can pass it directly to our commit message bot:
    """
    )
    return


@app.cell
def _(commit_message_bot, commit_message_prompt):
    commit_message_response = commit_message_bot(commit_message_prompt)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Exercise: vary the bot's settings.

    Try changing the language model for the commit message bot
    and see how the commit message changes.
    I suggest that you try `phi4` or `gemma2:2b`.
    Also try varying the system prompt, temperature, and user prompt template,
    while keeping the git diff the same.
    """
    )
    return


@app.cell
def _():
    # Put your code here
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## 1.5 Class Demo: GPT-4o v.s. Llama 3.2

    I'm now going to demo using `gpt-4o` the original commit message bot,
    specifically using the original code in `llamabot`'s Git commit message writer.
    """
    )
    return


@app.cell
def _():
    # Live copy/paste code here, with incremental explanations.
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Class Discussion: What have you learned so far?

    - Point 1...
    - Point 2...
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## 1.6 Summary & Conclusion

    - API calls are state-less/memoryless.
    - Prompts can be designed (not engineered!) to steer the LM to do what we need.
    - Vibe checking is the first thing needed to be done when evaluating an LLM.
    """
    )
    return


if __name__ == "__main__":
    app.run()
