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

    In this notebook, we'll explore how to evaluate LLM outputs through structured data
    and human feedback. Our focus will be on extracting and validating information from
    scientific abstracts.

    ## Learning Objectives

    By the end of this notebook, you will be able to:

    1. Design structured data models for LLM outputs
    2. Extract information from scientific text using StructuredBot
    3. Build custom evaluation tools using Marimo
    4. Understand the critical role of metrics in LLM evaluation
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Research Findings Extractor

    Let's build a research findings extractor to demonstrate the concepts we'll cover.
    We'll apply the structured generation techniques we learned in the previous notebook.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Exercise: Build a Research Findings Extractor

    Your task is to create a bot that extracts key findings from scientific literature.

    Using Pydantic `BaseModel`s and LlamaBot's StructuredBot, you'll need to create:

    1. A Pydantic model to structure the research findings
    2. A LlamaBot `StructuredBot` with an appropriate system prompt for extraction
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
        r"""Below are several scientific abstracts. We'll use these to test our extraction capabilities."""
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
        r"""Process each abstract through the extraction bot to generate a list of structured `ResearchFindings` objects."""
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
    ## Discussion: Evaluation Strategies

    Let's examine the extracted information and discuss:

    1. What criteria would you use to evaluate the accuracy of these findings?
    2. Should this evaluation be done by humans or LLMs? What factors would influence this decision?
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
    ## Building Custom Evaluation Tools

    While evaluation problems may seem similar on the surface, effective evaluation often
    requires custom tooling. As Hamel Husain notes in his FAQ, platform tools alone are
    rarely sufficient.

    Let's build a custom evaluation interface using Marimo's UI toolkit. I'll demonstrate
    a basic implementation that you can later extend or modify.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""Let's build our evaluation interface step by step:

    1. First, we'll create a slider to navigate between abstracts and their findings
    2. Then, we'll add a display for the abstract text
    3. Finally, we'll show the extracted findings using the `__str__()` method of our `ResearchFindings` class"""
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
        r"""Now, let's add a feedback mechanism for evaluators. We'll start by defining a Pydantic model to structure our evaluation results."""
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
    ## Exercise: Extend the Evaluation Interface

    Enhance the evaluation interface by adding more input options for evaluators.
    Consider what additional metrics or feedback would be valuable for assessing
    the quality of the extractions.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Discussion: Evaluation Best Practices

    Take a few minutes to discuss with your peers:
    What principles and practices should guide our approach to LLM evaluation?
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""To organize the interface:
    1. Click the "Toggle app view" button (or press `[Cmd .]`)
    2. Switch to grid view
    3. Arrange the elements to create an intuitive evaluation workflow"""
    )
    return


if __name__ == "__main__":
    app.run()
