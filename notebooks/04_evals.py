# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "anthropic==0.52.2",
#     "building-with-llms-made-simple==0.0.1",
#     "llamabot[all]==0.12.11",
#     "marimo",
#     "pydantic==2.11.5",
# ]
#
# [tool.uv.sources]
# building-with-llms-made-simple = { path = "../", editable = true }
# ///

import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import llamabot as lmb
    return lmb, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Part 4: Steering LLMs with In-Context Learning

    This notebook demonstrates how to steer LLM behavior using human evaluation and in-context learning.
    We'll use docstring generation as our example task.

    ## The Problem

    Gemma2:2b doesn't naturally generate Sphinx-style docstrings.
    How do we teach it to follow our preferred documentation style?

    ## Our Approach

    1. Generate examples with a basic LLM
    2. Human evaluation: label what's good vs bad
    3. Use good examples as in-context learning data
    4. Compare before/after results
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Step 1: Before (Basic LLM)

    Let's see what happens when we ask Gemma2:2b to generate a function with docstring.
    We'll use structured generation to get: function name, signature, and docstring.
    """
    )
    return


@app.cell
def _(lmb):
    from building_with_llms_made_simple.answers.evals_answers import (
        DocstringBreakdown,
    )


    @lmb.prompt("system")
    def basic_docstring_system_prompt():
        """You are a Python documentation assistant. Given a function description,
        create a function name, signature, and docstring.

        You must generate docstrings using sphinx-style.
        """


    # Demonstrate basic bot output without human examples
    function_request = "a function that calculates the geodesic distance between any pair of longitude and latitude"  # noqa: E501

    # Create bot instances for demonstration
    basic_docstring_bot = lmb.StructuredBot(
        system_prompt=basic_docstring_system_prompt(),
        pydantic_model=DocstringBreakdown,
        model_name="ollama_chat/gemma2:2b",
        temperature=0.0,
    )
    basic_result = basic_docstring_bot(function_request)
    print()
    print("=== BASIC BOT OUTPUT (no human examples) ===")
    print(f"Function Name: {basic_result.function_name}")
    print(f"Signature: {basic_result.function_signature}")
    print(f"Docstring:\n{basic_result.docstring}")
    return DocstringBreakdown, function_request


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **Observation**: Gemma2:2b generates docstrings, but not in any particular style.
    Even when we explicitly ask for Sphinx-style, results are inconsistent.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Step 2: Human Evaluation

    Since explicit prompting doesn't work reliably, we need a different approach.
    We'll collect examples and have humans label them as good or bad.
    This creates training data for in-context learning.

    **In-context learning**: Instead of explicit instructions, we provide the LLM with examples
    of good and bad outputs directly in the prompt. The LLM learns the pattern from these examples
    and applies it to new tasks.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Our Training Examples

    I've prepared examples showing different docstring quality levels.
    We'll evaluate them on two simple criteria:

    1. **Has docstring?** (not empty)
    2. **Is Sphinx-style?** (uses `:param:`, `:return:` format)

    Examples include: missing docstrings, Google-style, NumPy-style, and proper Sphinx-style.
    """
    )
    return


@app.cell
def _():
    # Import our docstring examples for evaluation
    from building_with_llms_made_simple.answers.evals_answers import (
        DOCSTRING_EXAMPLES,
        DocstringEvaluation,
        EVALUATION_CRITERIA,
        create_improved_docstring_bot,
        detailed_docstring_evaluation_system_prompt,
    )
    return (
        DOCSTRING_EXAMPLES,
        DocstringEvaluation,
        create_improved_docstring_bot,
    )


@app.cell
def _(DOCSTRING_EXAMPLES):
    # Show a few examples
    for sample_idx, sample_example in enumerate(DOCSTRING_EXAMPLES[:5]):
        print(f"Example {sample_idx + 1}:")
        print(f"Function: {sample_example['function_name']}")
        print(
            f"Docstring: {sample_example['docstring'][:100]}{'...' if len(sample_example['docstring']) > 100 else ''}"
        )
        print()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Step 3: Label the Examples

    Now we'll build a simple evaluation interface.
    For each example, we'll answer: "Has docstring?" and "Is Sphinx-style?"
    """
    )
    return


@app.cell
def _(DOCSTRING_EXAMPLES, DocstringEvaluation):
    # Create evaluation objects for each docstring
    docstring_evaluations = [DocstringEvaluation() for _ in DOCSTRING_EXAMPLES]
    return (docstring_evaluations,)


@app.cell
def _(DOCSTRING_EXAMPLES, docstring_evaluations):
    import random


    def get_unrated_examples():
        """Get examples that haven't been fully evaluated."""
        unrated_examples = []
        for example_idx in range(len(DOCSTRING_EXAMPLES)):
            evaluation = docstring_evaluations[example_idx]
            # Check if both criteria are missing
            if (
                evaluation.has_docstring is None
                or evaluation.is_sphinx_style is None
            ):
                unrated_examples.append(example_idx)
        return unrated_examples


    def get_random_unrated_example():
        """Get a random unrated example."""
        unrated_examples = get_unrated_examples()
        if unrated_examples:
            return random.choice(unrated_examples)
        return None
    return (get_random_unrated_example,)


@app.cell
def _(mo):
    # Simple button that increments its value when clicked
    next_example_button = mo.ui.button(
        label="Next Example",
        value=0,
        on_click=lambda value: value + 1,
    )
    next_example_button
    return (next_example_button,)


@app.cell
def _(get_random_unrated_example, mo, next_example_button):
    # Get a random unrated example, refreshes when button is clicked
    _ = next_example_button.value  # This makes it reactive to button clicks
    random_example_idx = get_random_unrated_example()

    # Create radio buttons for both criteria
    has_docstring_radio = mo.ui.radio(
        options=["Yes", "No"],
        label="Has docstring?",
        value=None,
    )

    is_sphinx_style_radio = mo.ui.radio(
        options=["Yes", "No"],
        label="Is Sphinx-style?",
        value=None,
    )
    return has_docstring_radio, is_sphinx_style_radio, random_example_idx


@app.cell
def _(DOCSTRING_EXAMPLES, random_example_idx):
    # Extract current example
    if random_example_idx is not None:
        current_example = DOCSTRING_EXAMPLES[random_example_idx]
    else:
        current_example = None
    current_example
    return (current_example,)


@app.cell
def _(
    docstring_evaluations,
    has_docstring_radio,
    is_sphinx_style_radio,
    next_example_button,
    random_example_idx,
):
    # Save evaluation when Next button is clicked
    if (
        next_example_button.value  # Button has been clicked
        and random_example_idx is not None
        and has_docstring_radio.value is not None
        and is_sphinx_style_radio.value is not None
    ):
        # Save both evaluations
        docstring_evaluations[random_example_idx].has_docstring = (
            has_docstring_radio.value == "Yes"
        )
        docstring_evaluations[random_example_idx].is_sphinx_style = (
            is_sphinx_style_radio.value == "Yes"
        )
    return


@app.cell
def _(
    DOCSTRING_EXAMPLES,
    current_example,
    docstring_evaluations,
    has_docstring_radio,
    is_sphinx_style_radio,
    mo,
    next_example_button,
    random_example_idx,
):
    # Recalculate unrated examples each time (reactive to button clicks)
    def get_current_unrated_examples():
        """Get examples that haven't been fully evaluated."""
        unrated_examples = []
        for example_idx in range(len(DOCSTRING_EXAMPLES)):
            evaluation = docstring_evaluations[example_idx]
            # Check if both criteria are missing
            if (
                evaluation.has_docstring is None
                or evaluation.is_sphinx_style is None
            ):
                unrated_examples.append(example_idx)
        return unrated_examples


    # Make this reactive to button clicks by referencing the button value
    _ = next_example_button.value
    unrated_examples = get_current_unrated_examples()

    if random_example_idx is not None and current_example is not None:
        # Create the evaluation interface for current example
        evaluation_interface = mo.vstack(
            [
                mo.md("## Docstring Evaluation"),
                mo.md(
                    f"**Example {random_example_idx + 1} of {len(DOCSTRING_EXAMPLES)}**"
                ),
                mo.md(f"**Function:** `{current_example['function_name']}`"),
                mo.md(f"**Signature:** `{current_example['function_signature']}`"),
                mo.md(
                    f"**Docstring:**\n```text\n{current_example['docstring']}\n```"
                ),
                mo.md("### Evaluate both criteria:"),
                has_docstring_radio,
                is_sphinx_style_radio,
                next_example_button,
            ]
        )
    else:
        # All evaluations complete
        evaluation_interface = mo.vstack(
            [
                mo.md("## 🎉 All Evaluations Complete!"),
                mo.md("You have rated all examples."),
                mo.md(
                    "Check the results below to see your progress and generated prompts."
                ),
            ]
        )

    evaluation_interface
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **Exercise**: Use the interface above to label examples.
    Answer both questions, then click "Next Example" to save and continue.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Let's analyze the detailed evaluation results.""")
    return


@app.cell
def _(docstring_evaluations):
    # Display evaluation progress and results
    total_evaluations = len(docstring_evaluations) * 2  # 2 criteria per example
    completed_evaluations = 0

    print("=== EVALUATION PROGRESS ===")
    for progress_idx, evaluation in enumerate(docstring_evaluations):
        has_docstring_done = evaluation.has_docstring is not None
        is_sphinx_style_done = evaluation.is_sphinx_style is not None

        criteria_completed = sum([has_docstring_done, is_sphinx_style_done])
        completed_evaluations += criteria_completed

        overall_quality = evaluation.overall_quality()

        print(f"Example {progress_idx + 1}:")
        docstring_symbol = "✓" if has_docstring_done else "○"
        print(
            f"  Docstring Present: {docstring_symbol} ({evaluation.has_docstring})"
        )
        sphinx_symbol = "✓" if is_sphinx_style_done else "○"
        print(f"  Sphinx-Style: {sphinx_symbol} ({evaluation.is_sphinx_style})")
        print(f"  Overall Quality: {overall_quality or 'Incomplete'}")
        print()

    progress_text = (
        f"Progress: {completed_evaluations}/{total_evaluations} "
        + "evaluations completed"
    )
    print(progress_text)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Step 4: Generate Training Prompt

    After labeling, we separate examples into "good" (passes both criteria) and "bad" (fails either).
    These become our in-context learning examples.
    """
    )
    return


@app.cell
def _(DOCSTRING_EXAMPLES, docstring_evaluations):
    # Collect only examples that pass BOTH criteria
    gold_standard_examples = []

    for eval_idx, _evaluation in enumerate(docstring_evaluations):
        # Only include if both criteria are True
        if (
            _evaluation.has_docstring is True
            and _evaluation.is_sphinx_style is True
        ):
            example_dict = DOCSTRING_EXAMPLES[eval_idx]
            example_display = f"Function: {example_dict['function_name']}\nSignature: {example_dict['function_signature']}\nDocstring: {example_dict['docstring']}"
            gold_standard_examples.append(example_display)

    print(f"Found {len(gold_standard_examples)} examples that pass BOTH criteria:")
    print("- Has docstring: Yes")
    print("- Is Sphinx-style: Yes")
    print()

    if gold_standard_examples:
        print("These are the gold standard examples for in-context learning!")
        for idx, _example in enumerate(gold_standard_examples):
            print(f"\nExample {idx + 1}:")
            print(_example[:100] + "..." if len(_example) > 100 else _example)
    else:
        print("No examples pass both criteria yet.")
        print("Continue evaluating to find high-quality examples.")
    return (gold_standard_examples,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Step 5: After (Improved LLM)

    Now let's test if in-context learning works.
    We'll create an improved bot using the good examples from our labeling.
    """
    )
    return


@app.cell
def _(gold_standard_examples):
    gold_standard_examples
    return


@app.cell
def _(create_improved_docstring_bot, function_request, gold_standard_examples):
    # Use the gold standard examples (those that pass BOTH criteria)
    if gold_standard_examples:
        improved_bot = create_improved_docstring_bot(gold_standard_examples)
        # improved_bot.model_name = "ollama_chat/llama3.2"
        improved_result = improved_bot(function_request)
        print()
        print(improved_result.docstring)

    else:
        print("Complete evaluations to see the improvement demonstration!")
        print("Need examples that pass both criteria to continue.")
        print("Label more examples to find gold standard examples.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    If this example reproduces on your machine, you may notice that all of that work didn't do anything to change the output!

    First off, this is normal -- all of the `Bots` that are present in LlamaBot should be considered to be complex systems, where things that you think might be levers turn out not to be levers when empirically tested.

    Second, you should expect the vast majority of your attempts to fix a complex system (like this one) to fail, and that's perfectly normal! The most productive way to think about these things is as information to guide iterative experimentation on what to try next.

    On that point, I've decided to try a separate solution, which would be to try a different model.
    """
    )
    return


@app.cell
def _(gold_standard_examples, lmb):
    @lmb.prompt("system")
    def improved_system_prompt(good_examples: list[str]):
        """You are a Python documentation assistant. Create high-quality function
        breakdowns with clear, informative docstrings.

        HIGH QUALITY DOCSTRINGS should:
        - Clearly explain what the function does
        - Document all parameters with types
        - Document return values with types
        - Use proper formatting and grammar

        =====
        Examples of HIGH QUALITY docstrings:
        {% for example in good_examples %}
        ---
        {{ example }}

        {% endfor %}
        ---
        =====

        Your instructions: generate a docstring following the patterns of the high quality docstrings."""


    system_prompt = improved_system_prompt(good_examples=gold_standard_examples)
    print(system_prompt.content)
    return (improved_system_prompt,)


@app.cell
def _(mo):
    mo.md(
        r"""After cycling through `llama3.1`, `llama3.2`, and finally `phi4`, I found `phi4` to be the one model that was able to follow the examples provided and use sphinx-style docstrings:"""
    )
    return


@app.cell
def _(
    DocstringBreakdown,
    function_request,
    gold_standard_examples,
    improved_system_prompt,
    lmb,
):
    bot = lmb.StructuredBot(
        system_prompt=improved_system_prompt(good_examples=gold_standard_examples),
        pydantic_model=DocstringBreakdown,
        # model_name="ollama_chat/llama3.1:latest",
        model_name="ollama_chat/phi4:latest",
    )

    response_phi4 = bot(function_request)
    print(response_phi4.docstring)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""However, we should also ablate the prompt (by switching it back to the basic prompt to make sure that the in-context learning examples were the ones that steered the LLM the right way."""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Summary

    This notebook demonstrated steering LLM behavior through in-context learning:

    1. **Before**: Gemma2:2b generates inconsistent docstring styles
    2. **Human evaluation**: We labeled examples as good/bad
    3. **In-context learning**: Good examples become training data in the prompt
    4. **After**: LLM learns to generate Sphinx-style docstrings

    This pattern works for any task where you want to steer LLM behavior.

    Some broader lessons to learn from this notebook:

    1. The moteley collection of docstrings serves as a placeholder for user-generated data.
    2. Always be testing and experimenting!
    """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
