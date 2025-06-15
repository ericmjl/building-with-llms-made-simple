# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "anthropic==0.52.2",
#     "building-with-llms-made-simple==0.0.1",
#     "llamabot[all]==0.12.8",
#     "marimo",
#     "pydantic==2.11.5",
# ]
#
# [tool.uv.sources]
# building-with-llms-made-simple = { path = "../", editable = true }
# ///

import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full", layout_file="layouts/04_evals.grid.json")


@app.cell
def _():
    import marimo as mo
    from pydantic import BaseModel, Field

    return BaseModel, Field, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Part 4: Evaluating LLM Outputs

    In this notebook, we'll learn how to evaluate LLM outputs using structured data
    and human feedback. We'll focus on extracting information from scientific abstracts
    and evaluating the accuracy of these extractions.

    ## Learning Objectives

    By the end of this notebook, you will be able to:

    1. Define structured data models for LLM outputs
    2. Extract information from scientific text using StructuredBot
    3. Create custom tooling to do evaluation using Marimo
    4. Understand that metrics are where you need to spend the most amount of time.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Research Findings Extractor

    To anchor this notebook's discussion, we will begin building a research finding's extractor. Let's first apply what we've learned from the previous notebook on structured generation.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Exercise: Build a `StructuredBot` for the extraction of findings from scientific literature.

    We are going to build a bot that extracts findings from scientific literature.

    Using Pydantic `BaseModel`s and LlamaBot's StructuredBot, create three things:

    1. A pydantic model for research findings.
    2. A LlamaBot `StructuredBot`, along with its system prompt, for extraction of findings.
    """
    )
    return


@app.cell
def _():
    # Fill out the ResearchFindings class below according to how you prefer.
    # If you are in need of inspiration,
    # feel free to use the BaseModel imported from the code repository.

    # mo.stop(True)

    from building_with_llms_made_simple.evals_answers import (
        extraction_bot,
    )

    return (extraction_bot,)


@app.cell
def _():
    # Use this cell to define ResearchFindings, extraction_system_prompt,
    # and extraction_bot if you choose to do so.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""Here are scientific abstracts for which we want to extract and structure the information in."""
    )
    return


@app.cell
def _():
    # Sample abstracts for evaluation
    abstracts = [
        """Climate change is altering species distributions and interactions, with cascading effects on ecosystem functioning. We conducted a 10-year study across 50 forest plots to examine how rising temperatures affect plant-pollinator networks. Using a combination of field observations and controlled experiments, we found that higher temperatures led to earlier flowering times and shifts in pollinator activity. These changes resulted in a 30% reduction in pollination success and a 15% decrease in plant reproductive output. However, our study was limited to temperate forests and may not represent patterns in other ecosystems. The findings suggest that climate change could significantly impact plant-pollinator mutualisms, with potential consequences for ecosystem stability.""",
        """Recent advances in machine learning have enabled significant progress in protein structure prediction. We developed a novel deep learning architecture that combines attention mechanisms with graph neural networks to predict protein folding patterns. Our model achieved 92% accuracy on the CASP14 benchmark, outperforming previous methods by 15%. The approach successfully captured long-range interactions between amino acids and predicted structural motifs with high precision. Limitations include computational requirements and the need for extensive training data. These results demonstrate the potential of hybrid neural architectures for advancing structural biology.""",
        """The impact of microplastics on marine ecosystems remains poorly understood. We conducted a comprehensive study across 20 coastal sites, analyzing water samples and marine organisms. Our findings revealed that microplastics were present in 85% of sampled organisms, with concentrations varying by species and location. The study identified three main pathways of microplastic accumulation: direct ingestion, trophic transfer, and environmental exposure. However, the long-term ecological consequences require further investigation. This research highlights the widespread nature of microplastic pollution and its potential effects on marine biodiversity.""",
    ]
    return (abstracts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""For each abstract, pass it into the extraction bot and obtain a list of
        `ResearchFindings` objects."""
    )
    return


@app.cell
def _(abstracts, extraction_bot):
    # mo.stop(True)
    findings = []
    for abstract in abstracts:
        findings.append(extraction_bot(abstract))
        # Fill in the rest here.
    return (findings,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Discussion: How to evaluate?

    Now, I would like you to take a look at the extracted information and discuss
    amongst yourselves:

    1. How would you evaluate the correctness of the findings? What criteria might you
    use?
    2. Do you need a human to do this? Can this be done by an LLM? How might you decide?
    """
    )
    return


@app.cell
def _():
    from building_with_llms_made_simple.evals_answers import (
        evaluation_discussion_answers,
    )

    # Call the following function to see my own answers!
    evaluation_discussion_answers
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Ergonomics of evaluation require custom tooling

    While there may be superficial commonalities between problems, if one digs deep,
    one will find that custom tooling is always going to be necessary to do evals.
    Platform tooling usually won't cut it. Hamel Husain also mentions so in his FAQ.

    Let's see how we can build tooling for this particlar problem, using Marimo's UI
    toolkit. I will show you an elementary interface that you could build, and then I
    will invite you to extend it or build your own.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""Firstly, I will create a slider that lets me flip through the findings and
        abstracts together."""
    )
    return


@app.cell
def _(findings, mo):
    slider = mo.ui.slider(
        label="Abstract", start=0, stop=len(findings) - 1, step=1, value=0
    )
    slider
    return (slider,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Then, I will create a Markdown display for the abstract:""")
    return


@app.cell
def _(abstracts, mo, slider):
    abstract_display = mo.md(abstracts[slider.value])
    abstract_display
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""And finally, I have a markdown display for research findings,
        taking advantage of the `__str__()` method that I implemented
        for the `ResearchFindings` class. (You may need to go back and implement it
        above if you did a custom implementation.)"""
    )
    return


@app.cell
def _(findings, mo, slider):
    findings_display = mo.md(str(findings[slider.value]))
    findings_display
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Finally, I am going to add in a mechanism for collecting feedback from an evaluator.
    I start by defining a pydantic model to collate together results for a single abstract:
    """
    )
    return


@app.cell
def _(BaseModel, Field, abstracts):
    class EvaluationResult(BaseModel):
        hypothesis_has_no_hallucinations: bool = Field(default_factory=lambda x: False)

        def _display_(self):
            return f"""# Evaluations:

    Hypothesis has no hallucinations: {self.hypothesis_has_no_hallucinations}
    """

    eval_results = [EvaluationResult() for _ in abstracts]
    return (eval_results,)


@app.cell
def _(eval_results):
    eval_results
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""And then add in a checkbox for each of the evals
        for each of the abstracts:"""
    )
    return


@app.cell
def _(abstracts, mo):
    ckbx_hypothesis_no_hallucinations = [
        mo.ui.checkbox(label="Hypothesis has no hallucinations") for _ in abstracts
    ]
    return (ckbx_hypothesis_no_hallucinations,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Finally, I'm going to add in a view for the eval results as well""")
    return


@app.cell
def _(ckbx_hypothesis_no_hallucinations, slider):
    ckbx_hypothesis_no_hallucinations[slider.value]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""Now, I would like you to click on the "Toggle app view" button
        (or hit `[Cmd .]` to toggle it),
        and switch to the grid view and lay out the elements for yourself."""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Exercise

    Please extend the custom app UI view to accept additional inputs from the evaluator.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Discussion

    Discuss with your neighbor for a few minutes the following questions:
    What would you consider to be best practices when doing evals?
    """
    )
    return


if __name__ == "__main__":
    app.run()
