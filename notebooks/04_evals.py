# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "anthropic==0.52.2",
#     "building-with-llms-made-simple==0.0.1",
#     "llamabot[all]==0.12.10",
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
    basic_result = basic_docstring_bot(
        "a function that calculates statistical metrics from data"
    )
    print()
    print("=== BASIC BOT OUTPUT (no human examples) ===")
    print(f"Function Name: {basic_result.function_name}")
    print(f"Signature: {basic_result.function_signature}")
    print(f"Docstring:\n{basic_result.docstring}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Note the issues above:

    1. The docstring is defined in the "function signature" field, and the implementation went into the "docstring" field.
    2. It is evident that the LLM does not fully understand what we want.
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

    Let's examine some example docstrings with varying levels of quality.
    You'll evaluate each docstring on THREE specific criteria, one at a time.

    **Evaluation Criteria:**

    1. **Clarity**: Does the docstring clearly explain what the function does?
    2. **Completeness**: Are parameters, return values, and types documented?
    3. **Usefulness**: Would this help someone understand and use the function?

    We'll present one docstring and one criterion at a time to avoid cognitive overload.
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
                current_value = getattr(docstring_evaluations[example_idx], criterion_key)
                if current_value is None:
                    unrated_pairs.append(
                        (example_idx, criterion_key)
                    )
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
    if (evaluation_radio.value is not None and
        random_example_idx is not None and
        random_criterion_key is not None):
        evaluation_value = evaluation_radio.value == "Yes"
        setattr(
            docstring_evaluations[random_example_idx],
            random_criterion_key,
            evaluation_value
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
        evaluation_interface = mo.vstack([
            mo.md("## Random Evaluation"),
            mo.md(f"**Example {random_example_idx + 1} of {len(docstring_subset)}**"),
            mo.md(f"**Function:** `{random_example_dict['function_name']}`"),
            mo.md(f"**Signature:** `{random_example_dict['function_signature']}`"),
            mo.md(f"**Docstring:**\n```python\n{random_example_dict['docstring']}\n```"),
            mo.md(
                f"### Criterion: {random_criterion_info['name']} " +
                f"({random_criterion_idx + 1} of 3)"
            ),
            mo.md(f"**Question:** {random_criterion_info['question']}"),
            mo.md(f"*{random_criterion_info['description']}*"),
            evaluation_radio,
            next_pair_button,
            mo.md(f"**Remaining unrated pairs:** {len(unrated_pairs)}"),
        ])
    else:
        # All evaluations complete
        evaluation_interface = mo.vstack([
            mo.md("## 🎉 All Evaluations Complete!"),
            mo.md("You have rated all example-criterion pairs."),
            mo.md(
                "Check the results below to see your progress and generated prompts."
            ),
        ])

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
    total_evaluations = len(docstring_evaluations) * 3  # 3 criteria per example
    completed_evaluations = 0

    print("=== EVALUATION PROGRESS ===")
    for progress_idx, evaluation in enumerate(docstring_evaluations):
        clarity_done = evaluation.clarity is not None
        completeness_done = evaluation.completeness is not None
        usefulness_done = evaluation.usefulness is not None

        criteria_completed = sum([clarity_done, completeness_done, usefulness_done])
        completed_evaluations += criteria_completed

        overall_quality = evaluation.overall_quality()

        print(f"Example {progress_idx + 1}:")
        print(f"  Clarity: {'✓' if clarity_done else '○'} ({evaluation.clarity})")
        completeness_symbol = '✓' if completeness_done else '○'
        print(f"  Completeness: {completeness_symbol} ({evaluation.completeness})")
        usefulness_symbol = '✓' if usefulness_done else '○'
        print(f"  Usefulness: {usefulness_symbol} ({evaluation.usefulness})")
        print(f"  Overall Quality: {overall_quality or 'Incomplete'}")
        print()

    progress_text = (f"Progress: {completed_evaluations}/{total_evaluations} " +
                     "evaluations completed")
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
    clarity_examples = {"good": [], "bad": []}
    completeness_examples = {"good": [], "bad": []}
    usefulness_examples = {"good": [], "bad": []}

    # Collect examples for each criterion
    for criteria_eval_idx, criteria_evaluation in enumerate(docstring_evaluations):
        example_dict = docstring_subset[criteria_eval_idx]
        # Format example for display
        example_display = f"Function: {example_dict['function_name']}\nSignature: {example_dict['function_signature']}\nDocstring: {example_dict['docstring']}"

        # Clarity examples
        if criteria_evaluation.clarity is True:
            clarity_examples["good"].append(example_display)
        elif criteria_evaluation.clarity is False:
            clarity_examples["bad"].append(example_display)

        # Completeness examples
        if criteria_evaluation.completeness is True:
            completeness_examples["good"].append(example_display)
        elif criteria_evaluation.completeness is False:
            completeness_examples["bad"].append(example_display)

        # Usefulness examples
        if criteria_evaluation.usefulness is True:
            usefulness_examples["good"].append(example_display)
        elif criteria_evaluation.usefulness is False:
            usefulness_examples["bad"].append(example_display)

    # Generate detailed system prompt if we have any examples
    total_examples = (
        len(clarity_examples["good"]) + len(clarity_examples["bad"]) +
        len(completeness_examples["good"]) + len(completeness_examples["bad"]) +
        len(usefulness_examples["good"]) + len(usefulness_examples["bad"])
    )

    if total_examples > 0:
        detailed_system_prompt = detailed_docstring_evaluation_system_prompt(
            clarity_examples, completeness_examples, usefulness_examples
        )
        print("Generated detailed criteria-based system prompt:")
        print("=" * 60)
        print(detailed_system_prompt)

        # Also show statistics
        print("\n" + "=" * 60)
        print("EVALUATION STATISTICS:")
        print(
            f"Clarity: {len(clarity_examples['good'])} good, "
            f"{len(clarity_examples['bad'])} bad"
        )
        print(
            f"Completeness: {len(completeness_examples['good'])} good, "
            f"{len(completeness_examples['bad'])} bad"
        )
        print(
            f"Usefulness: {len(usefulness_examples['good'])} good, "
            f"{len(usefulness_examples['bad'])} bad"
        )
    else:
        print("No criteria evaluations completed yet.")
        print("Complete some evaluations to generate a detailed system prompt.")

    return clarity_examples, completeness_examples, usefulness_examples


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

    1. **Label more examples**: Go through all the docstrings and provide
       quality ratings
    2. **Add criteria**: What other aspects of docstring quality should we evaluate?
    3. **Test the system prompt**: Use the generated prompt with a local LLM to
       evaluate new docstrings
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
    clarity_examples,
    completeness_examples,
    create_improved_docstring_bot,
    usefulness_examples,
):
    # Collect all good examples from the detailed criteria
    all_good_examples = []

    # Add examples that scored well on any criterion
    all_criteria = [clarity_examples, completeness_examples, usefulness_examples]
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
        improved_result = improved_bot(
            "a function that calculates statistical metrics from data"
        )

        print("=== IMPROVED BOT OUTPUT (with criteria-based examples) ===")
        print(f"Function Name: {improved_result.function_name}")
        print(f"Signature: {improved_result.function_signature}")
        print(f"Docstring:\n{improved_result.docstring}")
        print("\n" + "=" * 50)
        print("Compare this to the basic bot output at the beginning!")
        print(f"This improvement used {len(unique_good_examples)} examples that scored")
        print("positively on clarity, completeness, or usefulness criteria.")

        # Show breakdown by criteria
        print("\nExample breakdown:")
        print(f"- {len(clarity_examples['good'])} examples with good clarity")
        completeness_count = len(completeness_examples['good'])
        print(f"- {completeness_count} examples with good completeness")
        print(f"- {len(usefulness_examples['good'])} examples with good usefulness")
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
