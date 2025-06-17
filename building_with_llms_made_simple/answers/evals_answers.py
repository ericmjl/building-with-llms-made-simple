"""Module for evaluating LLM outputs from scientific abstract extraction.

This module provides tools and models for extracting and evaluating information
from scientific abstracts using LLMs. It includes:

- A Pydantic model for structured extraction of research findings
- A StructuredBot implementation for extracting information
- Evaluation criteria and discussion points for assessing extraction quality

The module is designed to be used in conjunction with Marimo notebooks for
interactive evaluation of LLM outputs.
"""

from typing import List, Optional

import llamabot as lmb
from pydantic import BaseModel, Field


class ResearchFindings(BaseModel):
    """Model for extracting key findings from scientific abstracts."""

    main_hypothesis: str = Field(
        description="The primary hypothesis or research question being tested"
    )
    methodology: str = Field(
        description="The main experimental or analytical approach used"
    )
    key_results: List[str] = Field(
        description="List of the most important findings or results"
    )
    limitations: Optional[List[str]] = Field(
        description="Any limitations or caveats mentioned in the abstract",
        default_factory=list,
    )
    confidence_score: float = Field(
        description="Model's confidence in the extraction (0-1)",
        ge=0.0,
        le=1.0,
    )

    def __str__(self):
        """Returns a formatted string representation of the research findings.

        This method provides a structured and readable output for the research
        findings, including the main hypothesis, methodology, key results,
        limitations, and confidence score."""

        return f"""## Research Findings

### Main Hypothesis

{self.main_hypothesis}

### Methodology

{self.methodology}

### Key Results

{", ".join(self.key_results)}

### Limitations (if any)

{", ".join(self.limitations) if self.limitations else "None reported"}

### Confidence Score

{self.confidence_score:.2f}
"""


@lmb.prompt("system")
def extraction_system_prompt():
    """You are a scientific information extraction assistant.
    Your task is to extract key information from scientific abstracts
    into a structured format. Be precise and only include information
    that is explicitly stated in the text. If you're uncertain about
    any information, mark it with a lower confidence score.
    """


extraction_bot = lmb.StructuredBot(
    system_prompt=extraction_system_prompt(),
    pydantic_model=ResearchFindings,
    model_name="ollama_chat/llama3.1",
    temperature=0.0,
)


def evaluation_discussion_answers():
    """Returns a markdown-formatted discussion of evaluation best practices.

    This function provides guidance on:
    - Using human evaluators for initial assessment
    - Defining meaningful evaluation criteria
    - Considerations for using LLMs as evaluators
    - Recommended resources for evaluation methodology

    Returns:
        marimo.md: A markdown-formatted discussion of evaluation practices
    """
    import marimo as mo

    return mo.md(
        """
This is not easy!

I would ask expert humans to do the evaluation at first,
use the human's intuition at first to guide, and record the scores provided by a human.
The criteria would likely be:

1. Did the LLM extract the main hypothesis correctly? (boolean)
5. How many factual inaccuracies did the LLM make in the hypothesis? (integer) And what were they? (qualitative)
2. How many factual inaccuracies did the LLM make in the methodology? (integer) And what were they? (qualitative)
3. How many factual inaccuracies did the LLM make in the key results? (integer) And what were they? (qualitative)
4. How many factual inaccuracies did the LLM make in the limitations? (integer) And what were they? (qualitative)

Your metrics should be defined against what's important.
Vanity metrics, such as "number of tokens", are generally not useful
except for measuring the cost of the LLM call.

Once the human evaluation is done,
it _may_ be possible to use in-context learning to steer an LLM-as-a-judge
to mimick what a human does,
but this has the risk of introducing a new LLM layer in the mix.
Proceed very carefully with this, and make sure you are constantly monitoring
the LLM-as-a-judge's performance.
I would only do this if you have way too many examples to evaluate by hand
and only a few human evaluators available,
and where you need the level of consistency that a human cannot provide.

I would strongly recommend reading [this blog post](https://hamel.dev/blog/posts/evals-faq/)
by Hamel Husain for an extensive FAQ on evals. 11/10 would recommend!
"""  # noqa: E501
    )
