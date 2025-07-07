"""Module for evaluating LLM outputs focusing on docstring clarity.

This module provides tools and models for evaluating docstring quality using human
feedback to train better LLM systems. It includes:

- Example docstrings with varying levels of clarity
- Tools for human evaluation and labeling
- System prompt generation from labeled examples
- Evaluation criteria for docstring quality

The module is designed to be used in conjunction with Marimo notebooks for
interactive evaluation of LLM outputs.
"""

from typing import List, Optional

import llamabot as lmb
from pydantic import BaseModel, Field


class DocstringBreakdown(BaseModel):
    """Model for breaking down a function into its components."""

    function_name: str = Field(description="The name of the function")
    function_signature: str = Field(
        description="The complete function signature including parameters and types. Excludes the content of the docstring."  # noqa: E501
    )
    docstring: str = Field(
        description="A docstring for this function. This is the stuff between the triple quotes."  # noqa: E501
    )


class DocstringEvaluation(BaseModel):
    """Model for storing docstring evaluation criteria focused on presence and style."""

    has_docstring: Optional[bool] = Field(
        description="Does the function have a docstring present?", default=None
    )
    is_sphinx_style: Optional[bool] = Field(
        description="Is the docstring written in Sphinx-style format?", default=None
    )

    def overall_quality(self) -> Optional[str]:
        """Determine overall quality based on individual criteria."""
        if any(score is None for score in [self.has_docstring, self.is_sphinx_style]):
            return None

        # Good if both criteria are true
        return "good" if self.has_docstring and self.is_sphinx_style else "bad"


# Evaluation criteria definitions
EVALUATION_CRITERIA = {
    "has_docstring": {
        "name": "Docstring Presence",
        "question": "Does the function have a docstring present?",
        "description": "Is there any docstring content between the triple quotes, "
        + "or is the docstring empty/missing?",
    },
    "is_sphinx_style": {
        "name": "Sphinx-Style Format",
        "question": "Is the docstring written in Sphinx-style format?",
        "description": "Does the docstring use Sphinx directives like :param:, :type:, "
        + ":return:, :rtype: rather than other formats like Google, NumPy, or plain text?",  # noqa: E501
    },
}


# Example docstrings focusing on two evaluation criteria:
# 1. Are docstrings present?
# 2. Are docstrings in Sphinx-style format?
# Each entry matches the DocstringBreakdown model structure
DOCSTRING_EXAMPLES = [
    # GOOD: Has docstring AND is Sphinx-style
    {
        "function_name": "calculate_average_temperature",
        "function_signature": "calculate_average_temperature(temperatures: list[float]) -> float",  # noqa: E501
        "docstring": """Calculate the average temperature from a list of readings.

        :param temperatures: List of temperature values in Celsius
        :type temperatures: list[float]
        :return: The average temperature
        :rtype: float
        """,
    },
    {
        "function_name": "get_gene_sequence",
        "function_signature": "get_gene_sequence(gene_id: str) -> str",
        "docstring": """Retrieve gene sequence from Ensembl using its ID.

        :param gene_id: Ensembl gene identifier
        :type gene_id: str
        :return: DNA sequence of the gene
        :rtype: str
        """,
    },
    {
        "function_name": "simulate_population_growth",
        "function_signature": "simulate_population_growth(r: float, N0: int, t: array) -> ndarray",  # noqa: E501
        "docstring": """Simulate population growth using exponential model.

        :param r: Growth rate
        :type r: float
        :param N0: Initial population
        :type N0: int
        :param t: Time points
        :type t: array
        :return: Population values at each time point
        :rtype: ndarray
        """,
    },
    # BAD: Missing docstring entirely
    {
        "function_name": "process_data",
        "function_signature": "process_data(data: list[dict]) -> dict",
        "docstring": "",
    },
    {
        "function_name": "validate_inputs",
        "function_signature": "validate_inputs(data: list, threshold: float) -> bool",
        "docstring": "",
    },
    {
        "function_name": "compute_metrics",
        "function_signature": "compute_metrics(predictions: list, targets: list) -> dict",  # noqa: E501
        "docstring": "",
    },
    {
        "function_name": "transform_data",
        "function_signature": "transform_data(raw_data: DataFrame) -> DataFrame",
        "docstring": "",
    },
    # BAD: Has docstring but NOT Sphinx-style (Google style)
    {
        "function_name": "extract_features",
        "function_signature": "extract_features(data: DataFrame) -> DataFrame",
        "docstring": """Extract features from the input dataset.

        Args:
            data (DataFrame): Input dataset for feature extraction.

        Returns:
            DataFrame: Dataset with extracted features.
        """,
    },
    {
        "function_name": "optimize_hyperparameters",
        "function_signature": "optimize_hyperparameters(model, space: dict) -> dict",
        "docstring": """Optimize model hyperparameters.

        Args:
            model: Machine learning model instance.
            space (dict): Hyperparameter search space.

        Returns:
            dict: Optimal hyperparameter configuration.
        """,
    },
    # BAD: Has docstring but NOT Sphinx-style (NumPy style)
    {
        "function_name": "analyze_signal",
        "function_signature": "analyze_signal(signal: ndarray, fs: int) -> dict",
        "docstring": """Analyze audio signal properties.

        Parameters
        ----------
        signal : ndarray
            Audio time series data.
        fs : int
            Sampling frequency in Hz.

        Returns
        -------
        dict
            Signal analysis results.
        """,
    },
    {
        "function_name": "fit_model",
        "function_signature": "fit_model(X: ndarray, y: ndarray) -> object",
        "docstring": """Fit machine learning model to training data.

        Parameters
        ----------
        X : ndarray
            Training features.
        y : ndarray
            Training targets.

        Returns
        -------
        object
            Fitted model instance.
        """,
    },
    # BAD: Has docstring but NOT Sphinx-style (Plain text)
    {
        "function_name": "parse_config",
        "function_signature": "parse_config(config_path: str) -> dict",
        "docstring": """Parse configuration file and return settings as dictionary.

        Takes a path to a configuration file and parses it to extract
        application settings. Supports JSON and YAML formats.
        """,
    },
    {
        "function_name": "detect_anomalies",
        "function_signature": "detect_anomalies(data: DataFrame, method: str) -> list[int]",  # noqa: E501
        "docstring": """Detect anomalies in the dataset using specified algorithm.

        The function applies the chosen anomaly detection method to identify
        outliers in the data and returns their indices.
        """,
    },
    {
        "function_name": "render_plot",
        "function_signature": "render_plot(data: DataFrame, chart_type: str) -> None",
        "docstring": """Create and display a plot of the data.

        Generates a visualization based on the specified chart type.
        Supports bar charts, line plots, and scatter plots.
        """,
    },
    # BAD: Has docstring but NOT Sphinx-style (Mixed/inconsistent style)
    {
        "function_name": "calculate_statistics",
        "function_signature": "calculate_statistics(values: list[float]) -> dict",
        "docstring": """Calculate descriptive statistics for a list of values.

        Args:
            values: List of numerical values to analyze.

        :return: Dictionary containing mean, median, std, etc.
        :rtype: dict
        """,
    },
    {
        "function_name": "preprocess_text",
        "function_signature": "preprocess_text(text: str, lowercase: bool = True) -> str",  # noqa: E501
        "docstring": """Preprocess text data for analysis.

        Parameters
        ----------
        text : str
            Input text to preprocess.

        :param lowercase: Whether to convert to lowercase
        :type lowercase: bool
        :return: Cleaned and processed text
        """,
    },
]


@lmb.prompt("system")
def detailed_docstring_evaluation_system_prompt(
    has_docstring_examples: dict, sphinx_style_examples: dict
):
    """You are a docstring quality evaluator. Assess docstrings based on two key
    criteria with specific examples from human evaluators.

    ## EVALUATION CRITERIA

    ### 1. DOCSTRING PRESENCE
    Does the function have a docstring present?

    {% if has_docstring_examples.get('good') %}
    Examples with docstrings present:
    {% for example in has_docstring_examples['good'] %}
    {{ example }}

    {% endfor %}
    {% endif %}

    {% if has_docstring_examples.get('bad') %}
    Examples with missing docstrings:
    {% for example in has_docstring_examples['bad'] %}
    {{ example }}

    {% endfor %}
    {% endif %}

    ### 2. SPHINX-STYLE FORMAT
    Is the docstring written in Sphinx-style format?

    {% if sphinx_style_examples.get('good') %}
    Examples of proper Sphinx-style format:
    {% for example in sphinx_style_examples['good'] %}
    {{ example }}

    {% endfor %}
    {% endif %}

    {% if sphinx_style_examples.get('bad') %}
    Examples of non-Sphinx-style format:
    {% for example in sphinx_style_examples['bad'] %}
    {{ example }}

    {% endfor %}
    {% endif %}

    ## EVALUATION TASK
    Evaluate the given docstring on each criterion:
    1. First, check if a docstring is present (not empty)
    2. Then, if present, check if it uses Sphinx-style formatting (:param:, :type:, :return:, :rtype:)

    Use the human-labeled examples above as your reference standards.
    """  # noqa: E501


def create_improved_docstring_bot(good_examples: List[str]) -> lmb.StructuredBot:
    """Create an improved docstring bot using good examples."""

    @lmb.prompt("system")
    def improved_system_prompt(good_examples: List[str]):
        """You are a Python documentation assistant. Create high-quality function
        breakdowns with clear, informative docstrings.

        HIGH QUALITY DOCSTRINGS should:
        - Clearly explain what the function does
        - Document all parameters with types
        - Document return values with types
        - Use proper formatting and grammar

        Examples of HIGH QUALITY docstrings:
        {% for example in good_examples %}
        {{ example }}

        {% endfor %}

        Generate a function breakdown following these quality standards."""

    return lmb.StructuredBot(
        system_prompt=improved_system_prompt(good_examples),
        pydantic_model=DocstringBreakdown,
        model_name="ollama_chat/gemma2:2b",
        temperature=0.0,
    )


def evaluation_discussion_answers():
    """Returns a markdown-formatted discussion of evaluation best practices.

    This function provides guidance on:
    - The importance of human evaluation for LLM outputs
    - How to generate training data for better LLM systems
    - Using human labels to improve model quality

    Returns:
        marimo.md: A markdown-formatted discussion of evaluation practices
    """
    import marimo as mo

    return mo.md(
        """
## The Critical Role of Human Evaluation

When working with LLMs, especially smaller local models, **human evaluation is
essential**. Here's why:

### Why Human Evaluation Matters

1. **LLMs are not perfect**: They can generate plausible-sounding but incorrect
   or unhelpful content
2. **Quality is subjective**: What makes a "good" docstring depends on human
   judgment and context
3. **Training data generation**: Human labels become the foundation for improving
   LLM performance

### The Evaluation-Improvement Cycle

1. **Generate examples**: Have your LLM produce docstrings
2. **Human labeling**: People evaluate and label the quality
3. **Create training data**: Use labels to build better prompts and fine-tuning
   datasets
4. **Improve the model**: Use human feedback to make the LLM better

### Why This Approach Works

- **Humans define quality**: We set the standards for what "good" means
- **Scalable improvement**: Once we have enough human labels, we can train better
  systems
- **Iterative refinement**: The process improves over time as we collect more
  feedback

The key insight: **humans are the source of truth for quality**. LLMs should
amplify human judgment, not replace it.

For more on evaluation best practices, read
[Hamel Husain's evaluation FAQ](https://hamel.dev/blog/posts/evals-faq/).
"""
    )
