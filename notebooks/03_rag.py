# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "llamabot[all]>=0.12.6",
#     "marimo",
#     "pyprojroot==0.3.0",
#     "rich==13.9.4",
#     "lancedb",
#     "sentence-transformers",
#     "chonkie==1.0.8",
#     "building-with-llms-made-simple",
# ]
#
# [tool.uv.sources]
# building-with-llms-made-simple = { path = "../", editable = true }
# ///

import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Part 3: Retrieval Augmented Generation (RAG) with Memory

    In this notebook, we'll learn how to use LlamaBot's QueryBot
    to implement Retrieval Augmented Generation (RAG)
    with memory capabilities.
    We'll build a system that can answer questions based on a knowledge base
    while maintaining conversation history.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Learning Objectives

    By the end of this notebook, you will be able to:

    1. Understand the core concepts of RAG and memory in LLM applications
    2. Set up and configure document stores for knowledge bases and memory
    3. Create and customize a QueryBot with memory capabilities
    4. Implement different text chunking strategies for various document types
    5. Design effective RAG systems based on query patterns and use cases

    The notebook is structured as follows:

    - Section 3.1: Introduction to RAG and Memory concepts
    - Section 3.2: Setting up document stores
    - Section 3.3: Creating and managing sample documents
    - Section 3.4: Building a QueryBot with memory
    - Section 3.5: Understanding the RAG process
    - Section 3.6: Advanced text chunking strategies
    - Section 3.7: Best practices and implementation guidelines
    - Section 3.8: Summary and key takeaways
    """
    )
    return


@app.cell
def _():
    from pathlib import Path

    import llamabot as lmb
    from llamabot.components.docstore import LanceDBDocStore
    from rich import print

    return LanceDBDocStore, Path, lmb, print


@app.cell
def _(mo):
    mo.md(
        r"""
    ## 3.1 Introduction to RAG and Memory

    Retrieval Augmented Generation (RAG) combines the power of language models with
    external knowledge bases. The process involves:

    1. Retrieving relevant documents from a knowledge base
    2. Augmenting the prompt with these documents
    3. Generating a response using the augmented context

    Adding memory allows the system to:

    1. Remember previous interactions
    2. Use conversation history for context
    3. Provide more coherent multi-turn conversations
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 3.2 Setting Up Document Stores

    We'll need two document stores:

    1. A knowledge base store for our documents
    2. A memory store for conversation history

    Let's create these using LanceDB, which is a lightweight vector database
    that provides efficient similarity search capabilities.

    ### Why LanceDB?

    LanceDB is an excellent choice for our RAG system because:
    - It's lightweight and easy to set up
    - Provides efficient vector similarity search
    - Supports both persistent and in-memory storage
    - Has good integration with Python and machine learning libraries
    """
    )
    return


@app.cell
def _(LanceDBDocStore, Path):
    # Create paths for our document stores
    base_path = Path.home() / ".llamabot"
    knowledge_base_path = base_path / "knowledge_base"
    memory_path = base_path / "memory"

    # Create document stores
    knowledge_store = LanceDBDocStore(
        table_name="knowledge_base",
        storage_path=knowledge_base_path,
    )

    memory_store = LanceDBDocStore(
        table_name="memory",
        storage_path=memory_path,
    )

    # For the purposes of this tutorial,
    # we will always reset the knowledge store and memory store
    # to avoid contamination between notebook runs.
    knowledge_store.reset()
    memory_store.reset()

    return knowledge_store, memory_store


@app.cell
def _(mo):
    mo.md(
        r"""
    ## 3.3 Creating Sample Documents

    Let's create some sample documents about
    a fictional programming language called Zenthing.
    We'll use these documents to demonstrate how RAG works with a knowledge base.

    ### Why Zenthing?

    We're using a fictional language to:
    1. Ensure the bot relies solely on our provided knowledge
    2. Avoid confusion with real programming languages
    3. Demonstrate how RAG works with structured information
    4. Show how the system can handle technical documentation

    The documents will cover:
    - Basic language description
    - Key features and capabilities
    - Use cases and applications
    - Syntax and programming paradigms
    """
    )
    return


@app.cell
def _(knowledge_store):
    # Sample documents about a new programming language named Zenthing
    zenthing_docs = [
        """
        Zenthing is a high-level, interpreted programming language known for its simplicity and readability.
        It was created by Japanese programmer Hiroshi Tanaka and first released in 1995.
        It is intended to be a simple language that is easy to learn and use.
        """,
        """
        Zenthing's key features include:
        - Dynamic typing
        - Automatic memory management
        - Extensive standard library
        - Support for multiple programming paradigms
        """,
        """
        Zenthing is new, but gaining traction in:
        - Web development (Django-Zenthing, Flask-zenthing)
        - Data science (NumZen, ZenPandas)
        - Machine learning (TensorZen, ZenTorch)
        - Automation and scripting
        """,
        """
        Zenthing's syntax emphasizes code readability with its use of significant whitespace.
        It supports multiple programming paradigms, including procedural, object-oriented, and functional programming.
        """,
    ]

    # Add documents to knowledge store
    knowledge_store.extend(zenthing_docs)  # Using extend for bulk addition

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""One of the first things I would like to disambiguate here is that documents are nothing more than text! Given the current state of technology, vector stores most commonly will accept plain text, images, and audio. Complex documents such as PDFs and word documents need to be converted into plain text first."""
    )
    return


@app.cell
def _(knowledge_store):
    knowledge_store.retrieve("Zenthing")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 3.4 Creating a QueryBot with Memory

    Now, let's create a QueryBot that uses both our knowledge base and memory store.
    We'll configure it to:
    1. Retrieve relevant documents from our knowledge base
    2. Remember conversation history
    3. Generate responses based on both sources

    ### Key Components

    The QueryBot combines several important features:
    - **Document Store**: For retrieving relevant information
    - **Memory Store**: For maintaining conversation context
    - **System Prompt**: To guide the bot's behavior
    - **Model Configuration**: To control response generation

    ### System Prompt Design

    The system prompt is crucial as it:
    - Sets the bot's personality and behavior
    - Defines how to use retrieved documents
    - Establishes response format and style
    - Ensures consistent and helpful responses
    """
    )
    return


@app.cell
def _(knowledge_store, lmb, memory_store):
    # Create the QueryBot
    @lmb.prompt("system")
    def rag_bot_sysprompt():
        """You are a helpful programming language assistant.
        You will be provided documents to answer questions.
        Answer questions solely based on the provided documents and not your background knowledge.
        If you're not sure about something, say so.
        Keep your responses concise and focused on the question asked.
        """

    rag_bot = lmb.QueryBot(
        system_prompt=rag_bot_sysprompt(),
        docstore=knowledge_store,
        memory=memory_store,
        model_name="ollama_chat/llama3.1",
        temperature=0.0,  # Keep responses deterministic
    )
    return rag_bot, rag_bot_sysprompt


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Exercise: Test the RAG Bot

    Let's test our RAG bot with a series of questions about Zenthing.
    We'll observe how it:

    1. Uses the knowledge base to provide accurate information
    2. Maintains context from previous questions
    3. Combines both sources for comprehensive answers

    #### Testing Strategy

    We'll ask questions that:
    - Start with basic concepts
    - Build on previous context
    - Require information from multiple documents
    - Test the bot's ability to maintain conversation flow

    Try to notice how the responses evolve and how the bot uses both
    the knowledge base and conversation history to provide answers.
    """
    )
    return


@app.cell
def _(print, rag_bot):
    # Example questions to test the bot
    response1 = rag_bot("What is Zenthing?")
    print("Response 1:", response1.content)
    return


@app.cell
def _(print, rag_bot):
    response2 = rag_bot("What are its key features?")
    print("\nResponse 2:", response2.content)

    return


@app.cell
def _(print, rag_bot):
    response3 = rag_bot("How is it used in data science?")
    print("\nResponse 3:", response3.content)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 3.5 Understanding the RAG Process

        Let's break down how our RAG system works:

        1. **Document Retrieval**:
            1. The system searches the knowledge base for relevant documents
            2. It uses hybrid search to find the most relevant content
            3. The retrieved documents are used to augment the prompt
        2. **Memory Integration**:
            1. Previous conversations are stored in the memory store
            2. Relevant past interactions are retrieved based on the current query using hybrid search as well
            3. This provides context for multi-turn conversations
        3. **Response Generation**:
            1. The LLM generates a response using both the retrieved documents and memory
            2. The response is then stored in memory for future reference
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Exercise: Customize the RAG System

        Try modifying the system to:

        1. Change the number of retrieved documents (n_results parameter)
        2. Adjust the temperature for more creative responses
        3. Modify the system prompt to change the bot's personality
        """
    )
    return


@app.cell
def _():
    # Your code here!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 3.6 Advanced Text Chunking Strategies

    Chunking is a critical component of RAG systems that determines how effectively
    the system can retrieve and use information. In this section, we'll explore
    different chunking strategies and their applications.

    ### Why Chunking Matters

    Language models have limited context windows, which means they can't process
    entire documents at once. Chunking helps by:

    1. Breaking documents into manageable pieces
    2. Preserving semantic meaning within chunks
    3. Enabling efficient retrieval of relevant information
    4. Maintaining document structure and relationships

    ### Types of Chunking Strategies

    We'll explore three main approaches:

    1. **Token/Character-based**: Simple, size-based chunking
    2. **Sentence-based**: Natural language boundary chunking
    3. **Recursive**: Structure-aware chunking for complex documents

    Each strategy has its strengths and use cases, which we'll demonstrate
    with practical examples.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Token/Character-based Chunking

    This is the simplest form of chunking, where we split text based on
    a fixed number of tokens or characters. It's useful when:

    - Document structure is not important
    - We need consistent chunk sizes
    - Processing speed is a priority
    - The content is relatively uniform

    However, it has limitations:

    - May split sentences mid-way
    - Doesn't respect natural language boundaries
    - Can break semantic coherence
    - Might miss important context

    Let's see how this works with our climate change essay example.
    """
    )
    return


@app.cell
def _():
    text_to_chunk = """
    ## Introduction

    Climate change is the long-term alteration of temperature and typical weather patterns in a region. It is driven primarily by increased concentrations of greenhouse gases in Earth's atmosphere. These gases trap heat from the sun, leading to higher global temperatures, sea level rise, and changes in precipitation patterns. For an overview of the science behind climate change, see the Intergovernmental Panel on Climate Change (IPCC) website at https://www.ipcc.ch.

    ## Greenhouse gas sources

    The main greenhouse gases are carbon dioxide (CO₂), methane (CH₄), and nitrous oxide (N₂O). Carbon dioxide is released when fossil fuels such as coal, oil, and natural gas are burned for energy or transportation. Methane emissions come from livestock, rice paddies, and the decay of organic waste in landfills. Nitrous oxide is emitted from agricultural soil management, industrial processes, and the combustion of fossil fuels. Deforestation also contributes to higher CO₂ levels because trees absorb CO₂ during photosynthesis. For detailed emission data, NASA's climate portal (https://climate.nasa.gov) provides up-to-date figures on global greenhouse gas concentrations.

    ## Impacts on ecosystems

    Rising temperatures and altered rainfall patterns affect ecosystems worldwide. Coral reefs experience bleaching when ocean temperatures exceed their tolerance levels, threatening marine biodiversity. In polar regions, melting ice reduces habitat for species such as polar bears and seals. Terrestrial ecosystems are also affected: warmer conditions can shift the distribution of plant and animal species, disrupting food chains. For example, warmer winters allow pests like bark beetles to survive, leading to widespread tree mortality in boreal forests.

    ## Societal and economic effects

    Climate change affects agriculture, water resources, and human health. Changes in temperature and precipitation can reduce crop yields, leading to food insecurity. Coastal communities face greater risk of flooding and storm surges as sea levels rise. Heatwaves increase heat-related illnesses, especially among vulnerable populations. Economically, the costs of extreme weather events are rising: hurricanes, wildfires, and droughts lead to billions of dollars in property damage and lost productivity each year.

    ## Mitigation strategies

    Mitigation involves reducing greenhouse gas emissions and enhancing carbon sinks. Transitioning to renewable energy sources—such as solar, wind, and hydroelectric—is critical to reducing CO₂ emissions. Improved energy efficiency in buildings, vehicles, and industrial processes also lowers greenhouse gas output. In agriculture, practices like no-till farming and precision fertilization can reduce N₂O emissions. Reforestation and afforestation projects capture CO₂ from the atmosphere, acting as carbon sinks. Policymakers use tools like carbon pricing and regulations to encourage emission reductions. For example, the European Union Emissions Trading System (EU ETS) is a cap-and-trade program that limits CO₂ emissions from major industries (https://ec.europa.eu/clima/policies/ets).

    ## Conclusion

    Understanding the sources, impacts, and mitigation strategies of climate change is essential to developing effective responses. By identifying entities such as greenhouse gases, emission sources, affected ecosystems, and mitigation technologies, one can build a knowledge graph to map relationships and support data-driven decision-making. For more resources, consult the United Nations Framework Convention on Climate Change (UNFCCC) at https://unfccc.int.
    """
    return (text_to_chunk,)


@app.cell
def _(mo):
    mo.md(
        r"""Given this text, observe how the chunks vary as we change chunking strategy."""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Introducing Chonkie: A Modern Text Chunking Library

        Chonkie is a powerful Python library designed specifically for text chunking in RAG applications.
        It provides several advantages:

        1. **Multiple Chunking Strategies**: From simple token-based to sophisticated recursive chunking
        2. **Customizable Parameters**: Fine-tune chunk sizes, overlaps, and boundaries
        3. **Language Support**: Built-in support for multiple languages and document types
        4. **Easy Integration**: Simple API that works well with popular vector stores

        In this section, we'll explore different chunking strategies using Chonkie
        and see how they affect our RAG system's performance.
        """
    )
    return


@app.cell
def _(text_to_chunk):
    from chonkie import TokenChunker

    # Basic initialization with default parameters
    chunker_basic = TokenChunker(
        tokenizer="gpt2",  # Supports string identifiers
        chunk_size=128,  # Maximum tokens per chunk
        chunk_overlap=8,  # Overlap between chunks
    )

    chunks_basic = chunker_basic(text_to_chunk)
    chunks_basic
    return


@app.cell
def _(text_to_chunk):
    from chonkie import SentenceChunker

    # Basic initialization with default parameters
    chunker_sentence = SentenceChunker(
        tokenizer_or_token_counter="gpt2",  # Supports string identifiers
        chunk_size=128,  # Maximum tokens per chunk
        chunk_overlap=8,  # Overlap between chunks
        min_sentences_per_chunk=1,  # Minimum sentences in each chunk
    )
    chunks_sentence = chunker_sentence(text_to_chunk)
    chunks_sentence
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Exercise: Experimenting with Chunking Parameters

        Let's explore how different chunking parameters affect our results.
        Try modifying the following parameters in the code above:

        1. **Chunk Size**:
           - Try values like 64, 256, or 512 tokens
           - Observe how larger chunks maintain more context
           - Notice how smaller chunks might split sentences

        2. **Chunk Overlap**:
           - Experiment with overlaps of 0, 16, or 32 tokens
           - See how overlap helps maintain context between chunks
           - Notice the trade-off between overlap and storage efficiency

        3. **Minimum Sentences**:
           - Try different values for `min_sentences_per_chunk`
           - Observe how it affects the natural language boundaries
           - Consider the impact on semantic coherence

        After experimenting, discuss:

        - Which parameters worked best for this climate change text?
        - How might different parameters be needed for other document types?
        - What trade-offs did you notice between chunk size and context?
        """
    )
    return


@app.cell
def _(text_to_chunk):
    from chonkie import RecursiveChunker

    chunker_recursive = RecursiveChunker.from_recipe("markdown", lang="en")

    chunks_recursive = chunker_recursive(text_to_chunk)
    chunks_recursive
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""Some special kinds of documents may need a different chunking and processing strategy
        before being stored in a DocStore.

        For example, if you want to enable searching through laboratory protocols
        with the goal of guiding people to a very specific section,
        you may want to chunk by section instead to make citations easy."""
    )
    return


@app.cell
def _():
    protocol = """
    1.	Purpose
    1.1 The purpose of this standard operating procedure (SOP) is to outline a generic workflow for routine laboratory analyses.
    1.1.1 This document is intended as a template to demonstrate hierarchical formatting up to three levels, facilitating chunking for large language models.
    1.1.2 It does not describe a specific analytical technique; users should replace placeholder text with details applicable to their own assays.
    1.2 By following this SOP, laboratory personnel will ensure consistency, traceability, and compliance with basic quality requirements.
    2.	Scope
    2.1 This SOP applies to all laboratory staff who perform routine sample preparation, measurement, and data recording activities.
    2.1.1 It covers general responsibilities, materials, procedural steps, data management, and safety considerations.
    2.1.2 Specialized or highly regulated techniques (e.g., radioactive work, GLP studies) are outside the scope of this document.
    2.2 The SOP is suitable for use in academic, industrial, or regulatory research settings where a generic framework is acceptable.
    3.	Responsibilities
    3.1 Laboratory manager
    3.1.1 Review and approve any modifications to this SOP.
    3.1.2 Ensure that all staff are trained on the current version.
    3.1.3 Conduct periodic audits to confirm adherence.
    3.2 Laboratory technician
    3.2.1 Follow the procedural steps as written.
    3.2.2 Document any deviations or unexpected observations in the laboratory notebook.
    3.2.3 Report equipment malfunctions to the laboratory manager immediately.
    4.	Materials and equipment
    4.1 Reagents
    4.1.1 Placeholder buffer solution (e.g., 0.1 M phosphate buffer, pH 7.4).
    4.1.2 Calibration standards appropriate for the chosen analytical method.
    4.1.3 Deionized water (Type I, <18 MΩ·cm).
    4.2 Consumables
    4.2.1 Disposable pipette tips (various sizes).
    4.2.2 Sample vials or tubes (e.g., 2 mL microcentrifuge tubes).
    4.2.3 Laboratory gloves (nitrile or latex, depending on compatibility).
    4.3 Equipment
    4.3.1 Analytical instrument (e.g., spectrophotometer, chromatography system).
    4.3.2 Calibrated balance capable of at least 0.1 mg readability.
    4.3.3 Vortex mixer and centrifuge.
    4.3.4 Computer workstation with data acquisition software.
    5.	Procedure
    5.1 Sample preparation
    5.1.1 Verify sample identification
    5.1.1.1 Confirm that each sample is labeled with a unique identifier (e.g., "SMP-001").
    5.1.1.2 Cross-check the sample list in the laboratory information management system (LIMS).
    5.1.2 Prepare reagents
    5.1.2.1 Retrieve reagents from storage; inspect expiration dates.
    5.1.2.2 Prepare working solutions according to manufacturer instructions.
    5.1.3 Aliquot samples
    5.1.3.1 Pipette the required volume of each sample into a clean tube.
    5.1.3.2 If necessary, dilute samples using the placeholder buffer to fall within the calibration range.
    5.2 Instrument calibration and setup
    5.2.1 Power on the instrument and allow it to warm up for at least 15 minutes.
    5.2.2 Perform daily verification using calibration standards.
    5.2.2.1 Load the calibration standard.
    5.2.2.2 Confirm that the instrument response is within predefined acceptance criteria.
    5.2.3 Configure analysis parameters
    5.2.3.1 Open the data acquisition software.
    5.2.3.2 Select the method file or input method details (e.g., wavelength, flow rate).
    5.3 Sample analysis
    5.3.1 Place prepared samples in the sample tray or autosampler.
    5.3.2 Begin the run sequence according to predefined sample order.
    5.3.2.1 Monitor the first few injections or readings to verify stable performance.
    5.3.2.2 If abnormalities are detected, pause the run and troubleshoot per Section 7.
    5.3.3 Record raw data files in the designated project folder on the laboratory server.
    5.3.4 At the end of the sequence, run a system blank to check for carryover.
    6.	Data management
    6.1 Data recording
    6.1.1 Transfer measurement results from the instrument to the LIMS or electronic notebook.
    6.1.2 Annotate each data entry with date, operator initials, and instrument ID.
    6.1.3 Note any deviations from standard operating conditions (e.g., pump pressure fluctuations).
    6.2 Data backup and storage
    6.2.1 Save raw data and processed results to a secure network drive.
    6.2.2 Maintain a local backup on an external hard drive, if required by institutional policy.
    6.2.3 Retain data for at least five years or as dictated by regulatory guidelines.
    7.	Safety and quality control
    7.1 General safety precautions
    7.1.1 Always wear appropriate personal protective equipment (PPE), including lab coat, gloves, and safety glasses.
    7.1.2 Refer to material safety data sheets (MSDS) for all reagents at https://www.osha.gov/laboratory-safety.
    7.1.3 Maintain a clean work area; immediately clean any spills using appropriate disinfectants.
    7.2 Equipment maintenance
    7.2.1 Perform weekly checks on critical components (e.g., lamp alignment, pump seals).
    7.2.1.1 Document maintenance activities in the instrument logbook.
    7.2.1.2 Replace consumables (e.g., septa, tubing) as recommended by the manufacturer.
    7.2.2 If the instrument fails calibration for more than two consecutive days, remove it from service and notify the equipment administrator.
    8.	References
    8.1 Internal documents
    8.1.1 Laboratory handbook – Version 3.0 (last updated January 2025).
    8.1.2 Instrument user manual (Model ABC-123, Document No. XYZ-789).
    8.2 External standards
    8.2.1 ISO 17025:2017 – General requirements for the competence of testing and calibration laboratories.
    8.2.2 Good Laboratory Practice (GLP) guidelines, U.S. FDA (https://www.fda.gov).
    9.	Revision history
    9.1 Revision 0 (June 1, 2025)
    9.1.1 Initial creation of dummy SOP for LLM chunking demonstration.
    9.1.2 Hierarchical numbering tested up to three levels.
    9.2 Future revisions
    9.2.1 Any updates should include date, author, and a brief description of changes.

    Note: Replace all placeholder text (e.g., reagent names, instrument details) with information specific to your laboratory's workflows before implementation.
    """
    return (protocol,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Custom Chunking for Specialized Documents

        Some documents require specialized chunking strategies. For example,
        laboratory protocols need to maintain their hierarchical structure
        to be useful. Let's explore how to create a custom chunking strategy
        for such documents.

        #### Why Custom Chunking?

        Standard chunking methods might not be suitable for:

        - Hierarchical documents (like SOPs)
        - Technical specifications
        - Legal documents
        - Medical protocols
        - Any document where structure is crucial

        Our custom chunker will:

        1. Preserve section hierarchy
        2. Maintain cross-references
        3. Keep related information together
        4. Enable precise retrieval of specific sections
        """
    )
    return


@app.cell
def _(protocol):
    import re

    def insert_delimiter(
        text: str, level: int = 1, delim: str = "|||SECTION|||"
    ) -> str:
        """Insert delimiters before section headers at a specified level.

        For a given level K, this function:

        1. Adds delimiters to all sections whose own level is from 1 to K.
        2. Crucially, if a section (e.g., "1.2.3") gets a delimiter because its
           level is <= K, then all its parent sections ("1." and "1.2" in this
           example) will also get a delimiter, regardless of whether K would
           have independently selected them.
        3. Places delimiters before section numbers, preserving original formatting.

        For example, if level=2:

        - If we see "1. Title", its level is 1. Since 1 <= 2, "1." gets a delimiter.
        - If we see "1.1 Title", its level is 2. Since 2 <= 2, "1.1" gets a delimiter.
          Its parent "1." also gets a delimiter.
        - If we see "1.1.1 Title", its level is 3. Since 3 > 2, "1.1.1" does NOT get
          a delimiter, and this line does not cause "1." or "1.1" to get delimiters
          if they wouldn't have otherwise.

        :param text: The text to process.
        :param level: The maximum section depth (K) to consider for adding delimiters.
            Sections up to this depth, and their parents, will be marked.
        :param delim: The delimiter string to insert.
        :return: The text with delimiters inserted according to the rules.
        """
        # First, remove any existing delimiters to prevent duplication
        text = text.replace(delim, "")

        lines = text.split("\n")
        result_lines = []

        # Pass 1: Identify all canonical section numbers that need delimiters
        sections_to_delim = set()
        for line_content in lines:
            match = re.match(r"^[ \t]*(\d+(?:\.\d+)*\.?)\s", line_content)
            if match:
                section_num_raw = match.group(1)  # e.g., "1.", "1.1", "1.1.1"

                # Normalize by removing trailing dot for consistent processing
                cleaned_section_num = section_num_raw.rstrip(
                    "."
                )  # e.g., "1", "1.1", "1.1.1"

                parts = cleaned_section_num.split(".")
                current_section_level = len(parts)

                if current_section_level <= level:
                    # Add this section and all its parents to the set
                    for i in range(len(parts)):
                        parent_canonical_num = ".".join(parts[: i + 1])
                        sections_to_delim.add(parent_canonical_num)

        # Pass 2: Add delimiters to the identified sections
        for line_content in lines:
            match = re.match(r"^[ \t]*(\d+(?:\.\d+)*\.?)\s", line_content)
            if match:
                section_num_raw = match.group(1)  # e.g., "1.", "1.1"
                cleaned_section_num = section_num_raw.rstrip(".")  # e.g., "1", "1.1"

                if cleaned_section_num in sections_to_delim:
                    # Use regex to insert delimiter while preserving leading whitespace
                    # and full section number
                    # The pattern matches:
                    # (leading whitespace)(section_number_with_optional_dot
                    # and_trailing_space)
                    # This ensures we re-insert the original section number format
                    # from the line.
                    line_content = re.sub(
                        r"^([ \t]*)((?:\d+(?:\.\d+)*\.?)\s)",
                        r"\1" + delim + r" \2",
                        line_content,
                        count=1,
                    )  # Apply only once per line
            result_lines.append(line_content)

        return "\n".join(result_lines)

    preprocessed_protocol = insert_delimiter(protocol, level=1)
    chunks_header = preprocessed_protocol.split("|||SECTION|||")
    chunks_header
    return (chunks_header,)


@app.cell
def _(mo):
    mo.md(
        r"""We did a very granular chunking strategy here. How would it perform on a broad query? Will granular chunks make it challenging for an LLM to retrieve enough information to synthesize a coherent answer?"""
    )
    return


@app.cell
def _(LanceDBDocStore, chunks_header, lmb, rag_bot_sysprompt):
    sop_docstore = LanceDBDocStore(
        table_name="sop_docstore",
    )
    # For this experiment, clear out the docstore just in case we are re-running stuff.
    sop_docstore.reset()
    sop_docstore.extend(chunks_header)

    sop_memorystore = LanceDBDocStore(table_name="sop_bot_memory")

    sop_bot = lmb.QueryBot(
        system_prompt=rag_bot_sysprompt(),
        docstore=sop_docstore,
        memory=sop_memorystore,
        model_name="ollama_chat/llama3.1",
        temperature=0.0,  # Keep responses deterministic
    )

    sop_bot("What do we do with consumables?")
    return (sop_bot,)


@app.cell
def _(mo):
    mo.md(
        r"""Your task: try your best to find cases where the LLM fails to answer a question correctly!"""
    )
    return


@app.cell
def _(print, sop_bot):
    response = sop_bot("What do I do if a machine has broken down?")
    print()
    print(response.content)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    This is a single example of many that my friends and colleagues have seen that involve documents of varying types.

    Let's have a discussion and explore what would be simple yet effective ways to preprocess the following textual data? AI notes will be taken live.

    1. Business/Legal contracts (relatively uniform?)
    2. Laboratory SOPs
    3. Recipes scraped from the internet (high variability in structure)
    4. Scientific literature (with tables, images, etc.)
    5. Any others you can think of?
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    What influences chunking strategy?

    - The queries that are expected,
    - The nature of the document (hierarchical or not)
    - ...anything else? LLM please help me flesh this out.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 3.7 Advanced Text Chunking Strategies

    The effectiveness of a RAG system heavily depends on how documents are chunked and indexed. Different types of queries require different chunking strategies:

    | Query Type | Example | Chunking Strategy | Index Type |
    |:---------:|:--------|:------------------|:-----------|
    | **Emergency/Protocol** | "What's the protocol for handling a data breach?" | • Split by procedure/step boundaries<br>• Include clear action items and decision points<br>• Maintain hierarchical structure (e.g., "Step 1: Assess Impact") | • Vector index for semantic similarity<br>• Full-text index for exact protocol matching |
    | **Concept/Knowledge** | "What was that idea about improving model performance?" | • Split by conceptual boundaries<br>• Include context about related concepts<br>• Preserve relationships between ideas | • Knowledge Graph:<br>  - Nodes: Concepts and ideas<br>  - Edges: Relationships and dependencies<br>  - Metadata: Timestamps, authors, context |
    | **Citation/Reference** | "What's the exact procedure for handling a protocol deviation in experiment XYZ?" | • Maintain exact hierarchical structure (e.g., SOP-123.4.5)<br>• Preserve all metadata (version, date, author)<br>• Include cross-references to related procedures<br>• Keep regulatory compliance information intact | • Hierarchical Index:<br>  - Tree structure matching document hierarchy<br>  - Full-text search within sections<br>  - Vector embeddings for semantic search<br>  - Metadata index for filtering by document type, version, dates, requirements<br>  - Citation tracking for audit trails |
    | **Hybrid** | "Find the protocol for handling errors in the authentication module" | • Multi-level chunking<br>• Preserve both semantic and structural information<br>• Include metadata about document type and purpose | • Multi-index System:<br>  - Vector index for semantic search<br>  - Full-text index for exact matches<br>  - Knowledge graph for relationships<br>  - Hierarchical index for structure |
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Best Practices for Implementation

    | Category | Key Considerations |
    |:--------:|:------------------|
    | **Query Analysis** | • Analyze common query patterns<br>• Identify primary use cases<br>• Design chunking strategy accordingly |
    | **Chunking Rules** | • Define clear chunking boundaries<br>• Consider overlap between chunks<br>• Maintain context across chunks |
    | **Index Selection** | • Choose appropriate index types<br>• Consider hybrid approaches<br>• Balance retrieval speed and accuracy |
    | **Metadata Management** | • Include relevant metadata<br>• Track chunk relationships<br>• Maintain document structure |
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 3.7 Discussion: Document Types and Chunking Strategies

        Different types of documents require different preprocessing and chunking strategies.
        Let's explore some common document types and their specific needs:

        ### 1. Business/Legal Contracts
        - **Structure**: Hierarchical, with clear sections and subsections
        - **Key Elements**: Parties, terms, conditions, dates, signatures
        - **Chunking Strategy**:
          - Preserve clause hierarchy
          - Keep related clauses together
          - Maintain cross-references
          - Include metadata (dates, versions)

        ### 2. Laboratory SOPs
        - **Structure**: Step-by-step procedures with safety information
        - **Key Elements**: Materials, steps, safety warnings, references
        - **Chunking Strategy**:
          - Group by procedure sections
          - Keep safety information with relevant steps
          - Maintain equipment and material lists
          - Preserve version and approval information

        ### 3. Recipes
        - **Structure**: Variable, often includes ingredients and steps
        - **Key Elements**: Ingredients, quantities, instructions, notes
        - **Chunking Strategy**:
          - Keep ingredients with their quantities
          - Group related steps together
          - Include preparation and cooking times
          - Preserve special notes and tips

        ### 4. Scientific Literature
        - **Structure**: Abstract, introduction, methods, results, discussion
        - **Key Elements**: Figures, tables, citations, data
        - **Chunking Strategy**:
          - Maintain section hierarchy
          - Keep figures with their descriptions
          - Preserve citation context
          - Include metadata (authors, dates, journal)

        ### 5. Other Document Types
        - **Technical Documentation**:
          - API references
          - Code examples
          - Version history
        - **Medical Records**:
          - Patient information
          - Treatment history
          - Test results
        - **Academic Papers**:
          - Abstract and keywords
          - Methodology
          - Results and discussion
          - References

        ### Key Considerations for All Types
        1. **Query Patterns**: How will users search for information?
        2. **Document Structure**: What hierarchy needs to be preserved?
        3. **Context Requirements**: What related information should stay together?
        4. **Metadata Importance**: What additional information needs to be tracked?
        5. **Update Frequency**: How often does the content change?
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 3.8 Summary & Key Takeaways

        In this notebook, we've explored the fundamentals of building effective RAG systems.
        Here are the key concepts and lessons learned:

        ### Core Concepts
        1. **RAG Architecture**
           - Combines retrieval with generation
           - Uses external knowledge bases
           - Maintains conversation context
           - Enables more accurate and contextual responses

        2. **Document Management**
           - Importance of proper chunking
           - Different strategies for different document types
           - Balancing chunk size and context
           - Preserving document structure

        3. **Memory Integration**
           - Storing conversation history
           - Using past context for better responses
           - Managing memory efficiently
           - Balancing recent and relevant information

        ### Best Practices
        1. **System Design**
           - Choose appropriate document stores
           - Design effective chunking strategies
           - Implement proper memory management
           - Consider query patterns and use cases

        2. **Implementation**
           - Start with simple chunking strategies
           - Test with different document types
           - Monitor system performance
           - Iterate and improve based on feedback

        3. **Optimization**
           - Fine-tune chunk sizes
           - Adjust retrieval parameters
           - Optimize memory usage
           - Balance speed and accuracy

        ### Next Steps
        1. Experiment with different chunking strategies
        2. Try various document types and structures
        3. Implement custom chunking for specific use cases
        4. Explore advanced memory management techniques
        5. Consider hybrid retrieval approaches

        Remember: The effectiveness of a RAG system depends on how well it's designed
        for your specific use case. Take time to understand your documents, queries,
        and requirements before implementing a solution.
        """
    )
    return


if __name__ == "__main__":
    app.run()
