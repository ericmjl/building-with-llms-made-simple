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
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Part 4: Evaluating LLM Outputs

    In this notebook, we'll explore how to evaluate LLM outputs through human
    feedback and labeling. Our focus will be on evaluating docstring quality to
    improve smaller local LLMs.

    ## The Problem: Teaching LLMs to Write Better Docstrings

    Imagine you want to use a small, local LLM to generate high-quality
    docstrings for your code. The challenge: **how do you define "high quality"?**
    And how do you teach the LLM your standards?

    The answer: **human evaluation and labeling**. Humans must provide the
    examples and labels that define quality, which can then be used to improve
    LLM performance.

    ## Learning Objectives

    By the end of this notebook, you will be able to:

    1. Understand why human evaluation is critical for LLM systems
    2. Build custom evaluation interfaces using Marimo
    3. Label examples to create training data for better LLM prompts
    4. Generate system prompts from human-labeled examples
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Demonstration: Before and After

    Let's see how human evaluation can improve LLM outputs. We'll ask a basic
    StructuredBot to generate a function breakdown for "a function that calculates
    statistical metrics from data".
    """
    )
    return


@app.cell
def _(basic_docstring_bot):
    # Demonstrate basic bot output without human examples
    function_request = "a function that calculates the geodesic distance between any pair of longitude and latitude"

    basic_result = basic_docstring_bot(function_request)
    print()
    print("=== BASIC BOT OUTPUT (no human examples) ===")
    print(f"Function Name: {basic_result.function_name}")
    print(f"Signature: {basic_result.function_signature}")
    print(f"Docstring:\n{basic_result.docstring}")
    return (function_request,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Some immediate notes/observations:

    1. `gemma2:2b` is ok at generating docstrings.
    2. However, it doesn't appear to conform to any particular known style of Python docstrings.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## The Human Evaluation Challenge

    When working with LLMs, especially smaller local models, **human evaluation
    is essential**. LLMs can generate plausible-sounding content that may be
    incorrect or unhelpful.

    For docstring generation, humans must define what makes a docstring "good"
    or "bad". This human judgment becomes the foundation for improving LLM
    performance.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Docstring Quality Examples

    To illustrate how we can use human evaluations to improve AI systems,
    let's attempt to make `gemma2:2b` improve how it generates docstrings.
    Moreover, to simplify the problem for illustration purposes,
    we are going to attempt to steer `gemma2:2b`'s generation
    to adhere to Sphinx-style
    (without explicitly stating Sphinx-style instructions in any prompt).

    I have provided some example docstrings with varying levels of quality;
    they were **not** generated with `gemma2:2b`, but rather through Claude Sonnet 4.0.
    I specifically asked for examples that demonstrate two key failure modes:
    missing docstrings and non-Sphinx-style docstrings.

    **Evaluation Criteria:**

    1. **Docstring Presence**: Does the function have a docstring present?
    2. **Sphinx-Style Format**: Is the docstring written in Sphinx-style format?

    We'll present one docstring and one criterion at a time to avoid cognitive overload.
    This simplified approach focuses on the fundamental requirements for
    consistent documentation: presence and style conformance.
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
        basic_docstring_bot,
        create_improved_docstring_bot,
        detailed_docstring_evaluation_system_prompt,
        evaluation_discussion_answers,
    )

    return (
        DOCSTRING_EXAMPLES,
        DocstringEvaluation,
        EVALUATION_CRITERIA,
        basic_docstring_bot,
        create_improved_docstring_bot,
        detailed_docstring_evaluation_system_prompt,
        evaluation_discussion_answers,
    )


@app.cell
def _(DOCSTRING_EXAMPLES):
    # Let's start with a subset of examples for our evaluation exercise
    # We'll use the first 10 examples to keep the exercise manageable
    docstring_subset = DOCSTRING_EXAMPLES[:10]
    return (docstring_subset,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Below are docstring examples with varying quality levels. We'll use
        these to build our evaluation interface.
    """
    )
    return


@app.cell
def _(docstring_subset):
    # Display the first few examples to see what we're working with
    for sample_idx, sample_example in enumerate(docstring_subset[:5]):
        print(f"Example {sample_idx + 1}:")
        print(f"Function: {sample_example['function_name']}")
        print(f"Signature: {sample_example['function_signature']}")
        print(f"Docstring: {sample_example['docstring']}")
        print("\n" + "=" * 50 + "\n")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Now let's build a custom evaluation interface using Marimo's UI
        components.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Random Evaluation Interface

    Instead of manually navigating through all combinations, we'll randomly
    present unrated example-criterion pairs. This approach:

    - **Reduces bias** by eliminating order effects
    - **Focuses attention** on one decision at a time
    - **Prevents fatigue** from systematic evaluation patterns
    - **Ensures completeness** by tracking remaining unrated pairs
    """
    )
    return


@app.cell
def _(DocstringEvaluation, docstring_subset):
    # Create evaluation objects for each docstring
    docstring_evaluations = [DocstringEvaluation() for _ in docstring_subset]
    return (docstring_evaluations,)


@app.cell
def _(EVALUATION_CRITERIA, docstring_evaluations, docstring_subset):
    import random

    # Get list of all possible example-criterion pairs
    criteria_list = list(EVALUATION_CRITERIA.keys())

    def get_unrated_pairs():
        """Get all unrated example-criterion pairs."""
        unrated_pairs = []
        for example_idx in range(len(docstring_subset)):
            for criterion_key in criteria_list:
                current_value = getattr(
                    docstring_evaluations[example_idx], criterion_key
                )
                if current_value is None:
                    unrated_pairs.append((example_idx, criterion_key))
        return unrated_pairs

    def get_random_unrated_pair():
        """Get a random unrated example-criterion pair."""
        unrated_pairs = get_unrated_pairs()
        if unrated_pairs:
            return random.choice(unrated_pairs)
        return None

    return criteria_list, get_random_unrated_pair, get_unrated_pairs


@app.cell
def _(mo):
    # Button to get next random unrated pair
    next_pair_button = mo.ui.button(
        label="Get Next Random Unrated Pair",
    )
    return (next_pair_button,)


@app.cell
def _(get_random_unrated_pair, mo, next_pair_button):
    # Get a random unrated pair, refreshes when button is clicked
    # Button click count triggers re-evaluation
    _ = next_pair_button.value  # This makes it reactive to button clicks
    random_pair = get_random_unrated_pair()
    evaluation_radio = mo.ui.radio(
        options=["Yes", "No"],
        label="Evaluation",
        value=None,
    )
    return evaluation_radio, random_pair


@app.cell
def _(EVALUATION_CRITERIA, criteria_list, docstring_subset, random_pair):
    # Extract current example and criterion from random pair
    if random_pair:
        random_example_idx, random_criterion_key = random_pair
        random_criterion_info = EVALUATION_CRITERIA[random_criterion_key]
        random_example_dict = docstring_subset[random_example_idx]

        # Find criterion index for display
        random_criterion_idx = criteria_list.index(random_criterion_key)
    else:
        random_example_idx = None
        random_criterion_key = None
        random_criterion_info = None
        random_example_dict = None
        random_criterion_idx = None
    return (
        random_criterion_idx,
        random_criterion_info,
        random_criterion_key,
        random_example_dict,
        random_example_idx,
    )


@app.cell
def _(
    docstring_evaluations,
    evaluation_radio,
    random_criterion_key,
    random_example_idx,
):
    # Auto-save evaluation when radio button changes
    if (
        evaluation_radio.value is not None
        and random_example_idx is not None
        and random_criterion_key is not None
    ):
        evaluation_value = evaluation_radio.value == "Yes"
        setattr(
            docstring_evaluations[random_example_idx],
            random_criterion_key,
            evaluation_value,
        )
    return


@app.cell
def _(
    docstring_subset,
    evaluation_radio,
    get_unrated_pairs,
    mo,
    next_pair_button,
    random_criterion_idx,
    random_criterion_info,
    random_example_dict,
    random_example_idx,
):
    # Check if we have any unrated pairs left
    unrated_pairs = get_unrated_pairs()

    if random_example_idx is not None and random_criterion_info is not None:
        # Create the evaluation interface for current random pair
        evaluation_interface = mo.vstack(
            [
                mo.md("## Random Evaluation"),
                mo.md(
                    f"**Example {random_example_idx + 1} of {len(docstring_subset)}**"
                ),
                mo.md(f"**Function:** `{random_example_dict['function_name']}`"),
                mo.md(f"**Signature:** `{random_example_dict['function_signature']}`"),
                mo.md(
                    f"**Docstring:**\n```text\n{random_example_dict['docstring']}\n```"
                ),
                mo.md(
                    f"### Criterion: {random_criterion_info['name']} "
                    + f"({random_criterion_idx + 1} of 2)"
                ),
                mo.md(f"**Question:** {random_criterion_info['question']}"),
                mo.md(f"*{random_criterion_info['description']}*"),
                evaluation_radio,
                next_pair_button,
                mo.md(f"**Remaining unrated pairs:** {len(unrated_pairs)}"),
            ]
        )
    else:
        # All evaluations complete
        evaluation_interface = mo.vstack(
            [
                mo.md("## 🎉 All Evaluations Complete!"),
                mo.md("You have rated all example-criterion pairs."),
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
    ## Exercise: Random Evaluation

    We'll present random unrated example-criterion pairs to avoid bias and
    cognitive overload:

    1. **Review** the docstring example and evaluation criterion
    2. **Answer** Yes/No based on the specific criterion
    3. **Click** "Get Next Random Unrated Pair" for the next evaluation
    4. **Repeat** until all pairs are evaluated

    This random approach ensures unbiased evaluation and keeps you focused on
    one decision at a time.
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
        print(f"  Docstring Present: {docstring_symbol} ({evaluation.has_docstring})")
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
    ## Generating System Prompts from Human Labels

    Once we have human labels, we can use them to create better system prompts for LLMs.
    Let's separate our labeled examples into "good" and "bad" categories.
    """
    )
    return


@app.cell
def _(
    detailed_docstring_evaluation_system_prompt,
    docstring_evaluations,
    docstring_subset,
):
    # Separate examples by individual criteria
    has_docstring_examples = {"good": [], "bad": []}
    sphinx_style_examples = {"good": [], "bad": []}

    # Collect examples for each criterion
    for criteria_eval_idx, criteria_evaluation in enumerate(docstring_evaluations):
        example_dict = docstring_subset[criteria_eval_idx]
        # Format example for display
        example_display = f"Function: {example_dict['function_name']}\nSignature: {example_dict['function_signature']}\nDocstring: {example_dict['docstring']}"

        # Docstring presence examples
        if criteria_evaluation.has_docstring is True:
            has_docstring_examples["good"].append(example_display)
        elif criteria_evaluation.has_docstring is False:
            has_docstring_examples["bad"].append(example_display)

        # Sphinx-style examples
        if criteria_evaluation.is_sphinx_style is True:
            sphinx_style_examples["good"].append(example_display)
        elif criteria_evaluation.is_sphinx_style is False:
            sphinx_style_examples["bad"].append(example_display)

    # Generate detailed system prompt if we have any examples
    total_examples = (
        len(has_docstring_examples["good"])
        + len(has_docstring_examples["bad"])
        + len(sphinx_style_examples["good"])
        + len(sphinx_style_examples["bad"])
    )

    if total_examples > 0:
        detailed_system_prompt = detailed_docstring_evaluation_system_prompt(
            has_docstring_examples, sphinx_style_examples
        )
        print("Generated detailed criteria-based system prompt:")
        print("=" * 60)
        print(detailed_system_prompt.content)

        # Also show statistics
        print("\n" + "=" * 60)
        print("EVALUATION STATISTICS:")
        print(
            f"Docstring Presence: {len(has_docstring_examples['good'])} good, "
            f"{len(has_docstring_examples['bad'])} bad"
        )
        print(
            f"Sphinx-Style: {len(sphinx_style_examples['good'])} good, "
            f"{len(sphinx_style_examples['bad'])} bad"
        )
    else:
        print("No criteria evaluations completed yet.")
        print("Complete some evaluations to generate a detailed system prompt.")
    return has_docstring_examples, sphinx_style_examples


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Discussion: The Human-in-the-Loop Process

    What we've just demonstrated is a fundamental pattern in LLM development:

    1. **Human evaluation**: People define what "good" means
    2. **Label collection**: Gather examples with quality judgments
    3. **System prompt generation**: Use labels to create better LLM instructions
    4. **Iterative improvement**: Repeat the process to refine quality
    """
    )
    return


@app.cell
def _(evaluation_discussion_answers):
    # Show the discussion about evaluation best practices
    evaluation_discussion_answers()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Exercise: Extend the Evaluation Process

    Try the following:

    1. **Label more examples**: Go through all the docstrings and evaluate them on
       docstring presence and Sphinx-style formatting
    2. **Explore patterns**: Notice how different documentation styles (Google, NumPy,
       plain text) fail the Sphinx-style criterion
    3. **Test the system prompt**: Use the generated prompt with a local LLM to
       evaluate new docstrings and see if it learns to prefer Sphinx-style
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Demonstration: The Improvement in Action

    Now let's see how our human labels improve the LLM's output! We'll create an
    improved bot using good examples from our labeling exercise.
    """
    )
    return


@app.cell
def _(unique_good_examples):
    unique_good_examples
    return


@app.cell
def _(
    create_improved_docstring_bot,
    function_request,
    has_docstring_examples,
    sphinx_style_examples,
):
    # Collect all good examples from the detailed criteria
    all_good_examples = []

    # Add examples that scored well on any criterion
    all_criteria = [has_docstring_examples, sphinx_style_examples]
    for criterion_examples in all_criteria:
        all_good_examples.extend(criterion_examples["good"])

    # Remove duplicates while preserving order
    unique_good_examples = []
    for example in all_good_examples:
        if example not in unique_good_examples:
            unique_good_examples.append(example)

    # If we have good examples from our detailed evaluations, demonstrate the
    # improved bot
    if unique_good_examples:
        improved_bot = create_improved_docstring_bot(unique_good_examples)
        improved_result = improved_bot(function_request)

        print("=== IMPROVED BOT OUTPUT (with criteria-based examples) ===")
        print(f"Function Name: {improved_result.function_name}")
        print(f"Signature: {improved_result.function_signature}")
        print(f"Docstring:\n{improved_result.docstring}")
        print("\n" + "=" * 50)
        print("Compare this to the basic bot output at the beginning!")
        print(f"This improvement used {len(unique_good_examples)} examples that scored")
        print("positively on docstring presence or Sphinx-style formatting.")

        # Show breakdown by criteria
        print("\nExample breakdown:")
        docstring_count = len(has_docstring_examples["good"])
        print(f"- {docstring_count} examples with docstrings present")
        sphinx_count = len(sphinx_style_examples["good"])
        print(f"- {sphinx_count} examples with good Sphinx-style formatting")
    else:
        print("Complete evaluations to see the improvement demonstration!")
        print("Need examples with positive ratings on any criteria to continue.")
    return (unique_good_examples,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Key Takeaways

    1. **Human evaluation is essential**: LLMs need human judgment to define quality
    2. **Custom tools matter**: Marimo's UI components let us build exactly what we need
    3. **Labels become training data**: Human feedback directly improves LLM performance
    4. **Iterative process**: Evaluation and improvement happen continuously

    Remember: **humans are the source of truth for quality**. LLMs should
    amplify human judgment, not replace it.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Interface Layout

    Click the "Toggle app view" button (or press `[Cmd .]`) and switch to grid view
    to arrange these elements in a layout that works for your evaluation workflow.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Summary

    In this notebook, we've learned how to:
    - Build human evaluation interfaces for LLM outputs
    - Collect quality labels from human evaluators
    - Generate system prompts from human feedback
    - Create an iterative process for improving LLM performance

    This human-in-the-loop approach is fundamental to building reliable LLM
    systems.
    """
    )
    return


if __name__ == "__main__":
    app.run()
