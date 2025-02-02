#resources

## Abstract

In this tutorial, you will learn how to integrate Large Language Models (LLMs) directly into Python programs as thoughtfully-designed core components of the program rather than bolt-on additions. This hands-on session teaches design principles and practical techniques for incorporating LLM outputs into program control flow. We will use LlamaBot, an open-source Python interface to LLMs, focusing on local execution with local and efficient models.

## Description

This hands-on tutorial teaches practical integration of Large Language Models (LLMs) into Python programs using LlamaBot and Ollama. Working with locally-run models that fit within 16GB RAM, participants will build a git commit message generator while learning core concepts of LLM application development.

Through Jupyter notebooks, we'll progress from basic LLM interactions with SimpleBot to structured outputs using Pydantic, culminating in systematic evaluation and practical deployment. The tutorial emphasizes learning-by-doing: participants will experiment with different models, prompting strategies, and temperature settings to understand their effects on output quality.

Key learning outcomes include mastering prompt design, implementing structured generation with schema validation, developing systematic evaluation approaches, and integrating LLM-powered features into existing workflows. The session concludes with a class-chosen discussion on broader implications of LLM applications in practice.

## Prerequisites

- Python programming experience
- Hardware Requirements:
  - Mac: 16GB RAM minimum
  - Linux/Windows: 16-32GB RAM
- Ability to install and run Ollama and the `smollm2`, `gemma2:2b`, `mistral`, and `phi4` models

## Use of AI

AI was used as a typing assistance tool, as I have carpal tunnel. Specifically, this proposal was transcribed from my head using Whisper (speech-to-text) as a first draft. It was then formatted into the SciPy submission format using Claude 3.5 Sonnet. It was edited heavily, ~70% edited, mostly through Whisper transcription.

## Outline

Part 1: Introduction to LLM APIs with `SimpleBot` (45 min)
- We will use LlamaBot as an API frontend and Ollama as a local LLM provider.
- Hands-on: Creating a `llamabot.SimpleBot` to interact with a language model.
	- Brief notes: anatomy of an LLM API call: system prompt, user prompt, temperature, model name.
	- Exercise: "Hello LLM!". Change system prompt to set LM persona, change temperature for greater variation in responses, vary user prompts based on user intent
	- Exercise: Guided build of prototype of a git commit message generator. Vary system prompt, temperature, user prompt; vibe check outputs.
	- Exercise: Change LLM model and re-vibe check outputs.
	- Demo: Outputs using `gpt-4o` v.s. `llama3.2` + tutorial class evaluation discussion.
- Key concepts:
	- API calls are state-less/memoryless.
	- Prompts can be designed (not engineered!) to steer the LM to do what we need.
	- Vibe checking is the first thing needed to be done when evaluating an LLM.

Break (15 min)

Part 2: Structured Outputs `StructuredBot` (45 min)
- We will introduce the use of `StructuredBot` to generate outputs that conform to a pre-specified schema.
- Brief lecture: how structured outputs are generated:
	- Prompting to get JSON.
	- Logits masking. <-- will give us the *perfect* opportunity to show how most modern LMs work: autoregressive generation.
- Hands-on: Restructure the git commit message generator from free text to a structured form.
	- Exercise: Decompose a git commit message into its constituent components, implement it as a Pydantic model, use `StructuredBot` to generate commit message, and format it.
	- Exercise: Add jazz and snazz to the git commit message by adding emojis!
	- Exercise: Add custom class methods to format the commit message.
- Key concepts:
	- Templated text is a form, model it using Pydantic, and use structured generation methods to fill it in.
	- Content that we require an LLM to generate requires sufficient context to be provided.

Break (15 min)

Part 3: Evaluation and embedding LLM-based text generation in a product (45 min)
- We will introduce the methodology behind evaluating LLM-generated text.
- Group hands-on: Evaluations
	- Class group exercise: Systematically evaluate the accuracy of the commit message against curated commit messages. Critique where the commit message writer misses information. Identify where additional context needs to be provided, e.g. intents behind changes (usually not available in code).
	- Exercise: Propose and implement changes to the git commit message composer.
- Hands-on: Embedding
	- Exercise: Embed text generation in a shell executable that automatically composes commit messages.
	- Demo: Show how LlamaBot goes further and hooks directly into git's `prepare-commit-msg` hook.
- Key concepts:
	- Systematic evaluation requires effort, the effort put in should be proportional to the impact of the generated text.
	- Operationalizing LLM text generation requires thoughtfulness in workflow integration.

Break (15 min)

Part 4: Discussion of class' choice (20 min)
- Four choices:
	- Option 1: Design principles for LLM-enhanced applications.
	- Option 2: Ideation brainstorm for the application of LLMs to accelerate one's work.
	- Option 3: What's the future of data science roles in GenAI?
	- Option 4: Ethics discussion.
- Class will choose by voting. Most popular wins.

## Additional Information

Content is being developed on a branch of this repo: https://github.com/ericmjl/building-with-llms-made-simple.

## Notes

I have extensive experience teaching tutorials at SciPy, including topics on Network Analysis, Bayesian Statistics, and Deep Learning Fundamentals. The format of this tutorial follows best practices that I have learned from previous tutorials.
