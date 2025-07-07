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
        description="The complete function signature including parameters and types"
    )
    docstring: str = Field(description="A high-quality docstring for this function")


class DocstringEvaluation(BaseModel):
    """Model for storing detailed docstring evaluation criteria."""

    clarity: Optional[bool] = Field(
        description="Is the description clear and specific?", default=None
    )
    completeness: Optional[bool] = Field(
        description="Are parameters, return values, and types documented?", default=None
    )
    usefulness: Optional[bool] = Field(
        description="Would this help someone understand and use the function?",
        default=None,
    )

    def overall_quality(self) -> Optional[str]:
        """Determine overall quality based on individual criteria."""
        if any(
            score is None
            for score in [self.clarity, self.completeness, self.usefulness]
        ):
            return None

        # Good if at least 2 out of 3 criteria are true
        positive_scores = sum([self.clarity, self.completeness, self.usefulness])
        return "good" if positive_scores >= 2 else "bad"


# Evaluation criteria definitions
EVALUATION_CRITERIA = {
    "clarity": {
        "name": "Clarity",
        "question": "Is the description clear and specific?",
        "description": "Does the docstring clearly explain what the function does "
        + "in plain language?",
    },
    "completeness": {
        "name": "Completeness",
        "question": "Are parameters, return values, and types documented?",
        "description": "Does the docstring include parameter types, return types, "
        + "and descriptions?",
    },
    "usefulness": {
        "name": "Usefulness",
        "question": "Would this help someone understand and use the function?",
        "description": "Would a developer be able to use this function correctly "
        + "based on the docstring?",
    },
}


# Example docstrings with varying levels of clarity
# Each entry matches the DocstringBreakdown model structure
DOCSTRING_EXAMPLES = [
    {
        "function_name": "extract_features",
        "function_signature": "extract_features(data: DataFrame) -> DataFrame",
        "docstring": """Perform feature extraction using advanced dimensionality reduction techniques and manifold learning algorithms to identify latent representations.""",  # noqa: E501
    },
    {
        "function_name": "validate_inputs",
        "function_signature": "validate_inputs(data: list, threshold: float) -> bool",
        "docstring": """Check if the provided data meets validation criteria.""",
    },
    {
        "function_name": "optimize_parameters",
        "function_signature": "optimize_parameters(model, data)",
        "docstring": """Optimize model parameters using grid search.

        This function takes a machine learning model and training data, then uses grid search
        to find the optimal hyperparameters that maximize model performance on validation data.""",  # noqa: E501
    },
    {
        "function_name": "update_model",
        "function_signature": "update_model(data)",
        "docstring": """Update the model with new data.""",
    },
    {
        "function_name": "get_gene_sequence",
        "function_signature": "get_gene_sequence(gene_id: str) -> str",
        "docstring": """Retrieve gene sequence from Ensembl using its ID.

Parameters:
gene_id (str): Ensembl gene identifier.

Returns:
str: DNA sequence of the gene.""",
    },
    {
        "function_name": "parse_config",
        "function_signature": "parse_config(config_path: str) -> dict",
        "docstring": """Parse configuration file.

        Reads and parses a configuration file to extract application settings.""",
    },
    {
        "function_name": "calculate_average_temperature",
        "function_signature": "calculate_average_temperature(temperatures: list[float]) -> float",  # noqa: E501
        "docstring": """Calculate the average temperature from a list of readings.

Parameters:
temperatures (list of float): List of temperature values in Celsius.

Returns:
float: The average temperature.""",
    },
    {
        "function_name": "process_batch",
        "function_signature": "process_batch(items: list[dict], batch_size: int) -> list[dict]",  # noqa: E501
        "docstring": """Process items in batches for memory efficiency.""",
    },
    {
        "function_name": "compute_band_gap",
        "function_signature": "compute_band_gap()",
        "docstring": """Compute the energy difference between the valence band and conduction band.""",  # noqa: E501
    },
    {
        "function_name": "correlate_variables",
        "function_signature": "correlate_variables(x: ndarray, y: ndarray) -> float",
        "docstring": """Compute Pearson correlation coefficient between two variables.

        Uses statistical methods to determine the linear relationship strength.""",
    },
    {
        "function_name": "analyze_signal",
        "function_signature": "analyze_signal(signal)",
        "docstring": """Analyze the signal for properties.""",
    },
    {
        "function_name": "transform_coordinates",
        "function_signature": "transform_coordinates(coords, from_system, to_system)",
        "docstring": """Transform coordinates between different reference systems.

        Converts spatial coordinates from one coordinate system to another using
        appropriate transformation matrices and geometric algorithms.""",
    },
    {
        "function_name": "render_map",
        "function_signature": "render_map(coordinates)",
        "docstring": """Render a map based on coordinates.""",
    },
    {
        "function_name": "fit_linear_regression",
        "function_signature": "fit_linear_regression(X: ndarray, y: ndarray) -> ndarray",  # noqa: E501
        "docstring": """Fit a linear regression model using least squares.

Parameters:
X (ndarray): 2D array of input features.
y (ndarray): 1D array of target values.

Returns:
coefficients (ndarray): Fitted model coefficients.""",
    },
    {
        "function_name": "plot_spectrogram",
        "function_signature": "plot_spectrogram(signal, fs: int)",
        "docstring": """Plot the spectrogram of an audio signal.

Parameters:
signal (array-like): Audio time series data.
fs (int): Sampling frequency in Hz.""",
    },
    {
        "function_name": "detect_anomalies",
        "function_signature": "detect_anomalies(data: DataFrame, method: str = 'isolation_forest') -> list[int]",  # noqa: E501
        "docstring": """Detect anomalies in dataset using specified algorithm.""",
    },
    {
        "function_name": "handle_errors",
        "function_signature": "handle_errors(func: callable, *args, **kwargs)",
        "docstring": """Handle exceptions and errors for function execution.

        Wraps function calls with comprehensive error handling and logging mechanisms.""",  # noqa: E501
    },
    {
        "function_name": "calculate_metrics",
        "function_signature": "calculate_metrics(predictions: list, targets: list) -> dict",  # noqa: E501
        "docstring": """Calculate various performance metrics for model evaluation.

        Computes standard metrics like accuracy, precision, recall, and F1-score.""",
    },
    {
        "function_name": "interpolate_missing",
        "function_signature": "interpolate_missing(data: ndarray, method: str) -> ndarray",  # noqa: E501
        "docstring": """Interpolate missing values in time series data.""",
    },
    {
        "function_name": "simulate_population_growth",
        "function_signature": "simulate_population_growth(r: float, N0: int, t: array) -> ndarray",  # noqa: E501
        "docstring": """Simulates population growth using exponential model.

Parameters:
r (float): Growth rate.
N0 (int): Initial population.
t (array): Time points.

Returns:
ndarray: Population values at each time point.""",
    },
    {
        "function_name": "calculate_redshift",
        "function_signature": "calculate_redshift(wavelength_observed: float, wavelength_emitted: float) -> float",  # noqa: E501
        "docstring": """Calculate the redshift of a celestial object.

Parameters:
wavelength_observed (float): Observed wavelength in nanometers.
wavelength_emitted (float): Emitted wavelength in nanometers.

Returns:
float: Redshift value.""",
    },
    {
        "function_name": "calculate_luminosity",
        "function_signature": "calculate_luminosity(distance: float, apparent_magnitude: float) -> float",  # noqa: E501
        "docstring": """Calculate stellar luminosity using distance modulus.

        Applies the inverse square law and magnitude-luminosity relationship.""",
    },
    {
        "function_name": "classify_star",
        "function_signature": "classify_star(spectra: dict, temperature: float) -> str",  # noqa: E501
        "docstring": """Classify stellar type based on spectral analysis.

        Uses Morgan-Keenan system to categorize stars by spectral features.""",
    },
    {
        "function_name": "dna_to_rna",
        "function_signature": "dna_to_rna(dna_seq: str) -> str",
        "docstring": """Convert a DNA sequence to its RNA transcript.

Parameters:
dna_seq (str): A string of nucleotide bases (A, T, C, G).

Returns:
str: RNA sequence with T replaced by U.""",
    },
    {
        "function_name": "normalize_expression",
        "function_signature": "normalize_expression()",
        "docstring": """Normalize gene expression values.""",
    },
    {
        "function_name": "preprocess_data",
        "function_signature": "preprocess_data(raw_data: DataFrame, config: dict) -> DataFrame",  # noqa: E501
        "docstring": """Preprocess raw data for machine learning pipeline.

        Applies standard preprocessing steps including scaling and feature engineering.""",  # noqa: E501
    },
    {
        "function_name": "compute_reaction_time",
        "function_signature": "compute_reaction_time(trials: list[float]) -> float",
        "docstring": """Compute the average reaction time from multiple trials.

Parameters:
trials (list of float): Reaction times in milliseconds.

Returns:
float: Mean reaction time.""",
    },
    {
        "function_name": "assess_cognition",
        "function_signature": "assess_cognition(test_scores: dict, demographics: dict) -> dict",  # noqa: E501
        "docstring": """Assess cognitive function through psychometric analysis.

        Evaluates performance across multiple cognitive domains.""",
    },
    {
        "function_name": "administer_test",
        "function_signature": "administer_test(subject_id: str, test_battery: list) -> dict",  # noqa: E501
        "docstring": """Administer psychological tests to research participants.""",
    },
    {
        "function_name": "estimate_seismic_moment",
        "function_signature": "estimate_seismic_moment(magnitude: float) -> float",
        "docstring": """Estimate the seismic moment from a given magnitude.

Parameters:
magnitude (float): Earthquake magnitude (Richter scale).

Returns:
float: Seismic moment in Newton-meters.""",
    },
    {
        "function_name": "analyze_soil",
        "function_signature": "analyze_soil(sample: dict, tests: list) -> dict",
        "docstring": """Analyze soil composition using geochemical methods.

        Performs comprehensive analysis of soil properties and contamination.""",
    },
    {
        "function_name": "map_elevation",
        "function_signature": "map_elevation(coordinates: list, resolution: float) -> ndarray",  # noqa: E501
        "docstring": """Map elevation data from coordinate points.""",
    },
    {
        "function_name": "compute_ph",
        "function_signature": "compute_ph(concentration: float) -> float",
        "docstring": """Compute pH from hydrogen ion concentration.

Parameters:
concentration (float): [H+] concentration in mol/L.

Returns:
float: pH value.""",
    },
    {
        "function_name": "compute_reaction_rate",
        "function_signature": "compute_reaction_rate(concentrations: dict, temperature: float, catalyst: bool = False) -> float",  # noqa: E501
        "docstring": """Compute chemical reaction rate using kinetics equations.""",
    },
    {
        "function_name": "simulate_catalysis",
        "function_signature": "simulate_catalysis(substrate: str, enzyme: str, conditions: dict) -> dict",  # noqa: E501
        "docstring": """Simulate enzymatic catalysis reaction.

        Models the biochemical reaction using Michaelis-Menten kinetics.""",
    },
    {
        "function_name": "count_unique_species",
        "function_signature": "count_unique_species(observations: list[str]) -> int",
        "docstring": """Calculate the number of unique species in an observation dataset.

Parameters:
observations (list of str): List of observed species.

Returns:
int: Count of unique species.""",  # noqa: E501
    },
    {
        "function_name": "assess_habitat",
        "function_signature": "assess_habitat(location: dict, species_list: list) -> dict",  # noqa: E501
        "docstring": """Assess habitat suitability for target species.

        Evaluates environmental conditions and habitat quality metrics.""",
    },
    {
        "function_name": "model_ecosystem",
        "function_signature": "model_ecosystem(species_matrix: ndarray, interactions: dict) -> dict",  # noqa: E501
        "docstring": """Model ecosystem dynamics using Lotka-Volterra equations.

        Simulates predator-prey relationships and population dynamics.""",
    },
    {
        "function_name": "estimate_carbon_emissions",
        "function_signature": "estimate_carbon_emissions(activities: list[dict]) -> float",  # noqa: E501
        "docstring": """Estimate total carbon emissions from a list of activities.

Parameters:
activities (list of dict): Each dict includes activity and emissions_kg.

Returns:
float: Total carbon footprint in kg CO2 equivalent.""",
    },
    {
        "function_name": "calculate_aqi",
        "function_signature": "calculate_aqi(pollutants: dict, location: str) -> int",
        "docstring": """Calculate Air Quality Index from pollutant measurements.""",
    },
    {
        "function_name": "estimate_emissions",
        "function_signature": "estimate_emissions(source_type: str, activity_data: dict, emission_factors: dict) -> float",  # noqa: E501
        "docstring": """Estimate pollutant emissions using EPA methodology.

        Calculates emissions based on activity data and emission factors.""",
    },
]


@lmb.prompt("system")
def basic_docstring_system_prompt():
    """Generate a function breakdown with a docstring."""
    return """You are a Python documentation assistant. Given a function description,
    create a function name, signature, and docstring."""


@lmb.prompt("system")
def detailed_docstring_evaluation_system_prompt(
    clarity_examples: dict, completeness_examples: dict, usefulness_examples: dict
):
    """You are a docstring quality evaluator. Assess docstrings based on three key
    criteria with specific examples from human evaluators.

    ## EVALUATION CRITERIA

    ### 1. CLARITY
    Does the docstring clearly explain what the function does?

    {% if clarity_examples.get('good') %}
    Good Clarity:
    {% for example in clarity_examples['good'] %}
    {{ example }}

    {% endfor %}
    {% endif %}

    {% if clarity_examples.get('bad') %}
    Poor Clarity:
    {% for example in clarity_examples['bad'] %}
    {{ example }}

    {% endfor %}
    {% endif %}

    ### 2. COMPLETENESS
    Are parameters, return values, and types documented?

    {% if completeness_examples.get('good') %}
    Good Completeness:
    {% for example in completeness_examples['good'] %}
    {{ example }}

    {% endfor %}
    {% endif %}

    {% if completeness_examples.get('bad') %}
    Poor Completeness:
    {% for example in completeness_examples['bad'] %}
    {{ example }}

    {% endfor %}
    {% endif %}

    ### 3. USEFULNESS
    Would this help someone understand and use the function?

    {% if usefulness_examples.get('good') %}
    Good Usefulness:
    {% for example in usefulness_examples['good'] %}
    {{ example }}

    {% endfor %}
    {% endif %}

    {% if usefulness_examples.get('bad') %}
    Poor Usefulness:
    {% for example in usefulness_examples['bad'] %}
    {{ example }}

    {% endfor %}
    {% endif %}

    ## EVALUATION TASK
    Evaluate the given docstring on each criterion and provide an overall quality
    assessment. Use the human-labeled examples above as your reference standards.
    """


# Create bot instances for demonstration
basic_docstring_bot = lmb.StructuredBot(
    system_prompt=basic_docstring_system_prompt(),
    pydantic_model=DocstringBreakdown,
    model_name="ollama_chat/llama3.2",
    temperature=0.0,
)


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
        model_name="ollama_chat/llama3.2",
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
