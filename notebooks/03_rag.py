# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "llamabot[all]==0.12.6",
#     "marimo",
#     "pyprojroot==0.3.0",
#     "rich==13.9.4",
#     "lancedb",
#     "sentence-transformers",
#     "chonkie==1.0.8",
# ]
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

        In this notebook, we'll learn how to use LlamaBot's QueryBot to implement Retrieval Augmented Generation (RAG)
        with memory capabilities. We'll build a system that can answer questions based on a knowledge base
        while maintaining conversation history.
        """  # noqa: E501
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 3.1 Introduction to RAG and Memory

        Retrieval Augmented Generation (RAG) combines the power of language models with external knowledge bases.
        The process involves:

        1. Retrieving relevant documents from a knowledge base
        2. Augmenting the prompt with these documents
        3. Generating a response using the augmented context

        Adding memory allows the system to:

        1. Remember previous interactions
        2. Use conversation history for context
        3. Provide more coherent multi-turn conversations
        """  # noqa: E501
    )
    return


@app.cell
def _():
    from pathlib import Path
    from typing import List, Optional

    import llamabot as lmb
    from llamabot.components.docstore import LanceDBDocStore
    from rich import print

    return LanceDBDocStore, Path, lmb, print


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3.2 Setting Up Document Stores

        We'll need two document stores:

        1. A knowledge base store for our documents
        2. A memory store for conversation history

        Let's create these using LanceDB, which is a lightweight vector database
        that provides efficient similarity search capabilities.
        """  # noqa: E501
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

    # For the purposes of this tutorial, we will always reset the knowledge store and memory store to avoid contamination between notebook runs.
    knowledge_store.reset()
    memory_store.reset()

    return knowledge_store, memory_store


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3.3 Creating Sample Documents

        Let's create some sample documents about Python programming to use as our knowledge base.
        We'll add these to our knowledge store.
        """  # noqa: E501
    )
    return


@app.cell
def _(knowledge_store):
    # Sample documents about a new programming language named Zenthing
    zenthing_docs = [
        """
        Zenthing is a high-level, interpreted programming language known for its simplicity and readability.
        It was created by Japanese programmer Hiroshi Tanaka and first released in 1995.
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
        """  # noqa: E501
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
        Keep your responses concise and focused on the question asked."""

    rag_bot = lmb.QueryBot(
        system_prompt=rag_bot_sysprompt(),
        docstore=knowledge_store,
        memory=memory_store,
        model_name="ollama_chat/llama3.1",
        temperature=0.0,  # Keep responses deterministic
    )
    return (rag_bot,)


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Exercise: Test the RAG Bot

    Try asking the bot some questions about Python programming.
    Notice how it:

    1. Uses the knowledge base to provide accurate information
    2. Maintains context from previous questions
    3. Combines both sources for comprehensive answers
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
        1. It uses semantic similarity to find the most relevant content
        1. The retrieved documents are used to augment the prompt
    2. **Memory Integration**:
        1. Previous conversations are stored in the memory store
        1. Relevant past interactions are retrieved based on the current query
        1. This provides context for multi-turn conversations
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


@app.cell
def _(mo):
    mo.md(
        """
    ## Chunking

    Chunking allows language models with limited context to operate on large documents nonetheless.
    We will show examples of different ways of chunking, and where they may be appropriate.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    ### Token/Character-based chunking

    This form of chunking is agnostic to the contents of a document, and simply relies on fixing the total number of characters (or tokenizer tokens) at a particular size.

    Let's see how this works for the essay below. I asked ChatGPT to generate a coherent-sounding essay on climate for me, the facts may be off, and if so, please call them out! Nonetheless, it should prove the point.
    """
    )
    return


@app.cell
def _():
    text_to_chunk = """
    ## Introduction

    Climate change is the long-term alteration of temperature and typical weather patterns in a region. It is driven primarily by increased concentrations of greenhouse gases in Earth’s atmosphere. These gases trap heat from the sun, leading to higher global temperatures, sea level rise, and changes in precipitation patterns. For an overview of the science behind climate change, see the Intergovernmental Panel on Climate Change (IPCC) website at https://www.ipcc.ch.

    ## Greenhouse gas sources

    The main greenhouse gases are carbon dioxide (CO₂), methane (CH₄), and nitrous oxide (N₂O). Carbon dioxide is released when fossil fuels such as coal, oil, and natural gas are burned for energy or transportation. Methane emissions come from livestock, rice paddies, and the decay of organic waste in landfills. Nitrous oxide is emitted from agricultural soil management, industrial processes, and the combustion of fossil fuels. Deforestation also contributes to higher CO₂ levels because trees absorb CO₂ during photosynthesis. For detailed emission data, NASA’s climate portal (https://climate.nasa.gov) provides up-to-date figures on global greenhouse gas concentrations.

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
    mo.md("""Given this text, observe how the chunks vary as we change chunking strategy.""")
    return


@app.cell
def _(text_to_chunk):
    from chonkie import TokenChunker

    # Basic initialization with default parameters
    chunker_basic = TokenChunker(
        tokenizer="gpt2",  # Supports string identifiers
        chunk_size=128,    # Maximum tokens per chunk
        chunk_overlap=8  # Overlap between chunks
    )

    chunks_basic = chunker_basic(text_to_chunk)
    chunks_basic
    return


@app.cell
def _(text_to_chunk):
    from chonkie import SentenceChunker

    # Basic initialization with default parameters
    chunker_sentence = SentenceChunker(
        tokenizer_or_token_counter="gpt2",                # Supports string identifiers
        chunk_size=128,                  # Maximum tokens per chunk
        chunk_overlap=8,               # Overlap between chunks
        min_sentences_per_chunk=1        # Minimum sentences in each chunk
    )
    chunks_sentence = chunker_sentence(text_to_chunk)
    chunks_sentence
    return


@app.cell
def _(text_to_chunk):
    from chonkie import RecursiveChunker, RecursiveRules

    chunker_recursive = RecursiveChunker.from_recipe("markdown", lang="en")

    chunks_recursive = chunker_recursive(text_to_chunk)
    chunks_recursive
    return


@app.cell
def _(mo):
    mo.md(r"""Some special kinds of documents may need a different chunking and processing strategy before being stored in a DocStore. For example, if you want to enable searching through laboratory protocols with the goal of guiding people to a very specific section, you may want to chunk by section instead.""")
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
    5.1.1.1 Confirm that each sample is labeled with a unique identifier (e.g., “SMP-001”).
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

    Note: Replace all placeholder text (e.g., reagent names, instrument details) with information specific to your laboratory’s workflows before implementation.
    """
    return (protocol,)


@app.cell
def _(mo):
    mo.md(r"""Chunking this protocol up by section is a bit challenging with plain old Chonkie, so let's try a custom chunking strategy.""")
    return


@app.cell
def _(protocol):
    import re

    import re

    def insert_delimiter(text: str, level: int = 1, delim: str = "|||SECTION|||") -> str:
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

        Args:
            text: The text to process.
            level: The maximum section depth (K) to consider for adding delimiters.
                   Sections up to this depth, and their parents, will be marked.
            delim: The delimiter string to insert.

        Returns:
            The text with delimiters inserted according to the rules.
        """
        # First, remove any existing delimiters to prevent duplication
        text = text.replace(delim, "")

        lines = text.split('\n')
        result_lines = []

        # Pass 1: Identify all canonical section numbers that need delimiters
        sections_to_delim = set()
        for line_content in lines:
            match = re.match(r'^[ \t]*(\d+(?:\.\d+)*\.?)\s', line_content)
            if match:
                section_num_raw = match.group(1)  # e.g., "1.", "1.1", "1.1.1"
            
                # Normalize by removing trailing dot for consistent processing
                cleaned_section_num = section_num_raw.rstrip('.') # e.g., "1", "1.1", "1.1.1"
            
                parts = cleaned_section_num.split('.')
                current_section_level = len(parts)

                if current_section_level <= level:
                    # Add this section and all its parents to the set
                    for i in range(len(parts)):
                        parent_canonical_num = '.'.join(parts[:i+1])
                        sections_to_delim.add(parent_canonical_num)

        # Pass 2: Add delimiters to the identified sections
        for line_content in lines:
            match = re.match(r'^[ \t]*(\d+(?:\.\d+)*\.?)\s', line_content)
            if match:
                section_num_raw = match.group(1) # e.g., "1.", "1.1"
                cleaned_section_num = section_num_raw.rstrip('.') # e.g., "1", "1.1"

                if cleaned_section_num in sections_to_delim:
                    # Use regex to insert delimiter while preserving leading whitespace and full section number
                    # The pattern matches: (leading whitespace)(section_number_with_optional_dot and_trailing_space)
                    # This ensures we re-insert the original section number format from the line.
                    line_content = re.sub(r'^([ \t]*)((?:\d+(?:\.\d+)*\.?)\s)', 
                                          r'\1' + delim + r' \2', 
                                          line_content, 
                                          count=1) # Apply only once per line
            result_lines.append(line_content)

        return '\n'.join(result_lines)


    preprocessed_protocol = insert_delimiter(protocol, level=3)
    chunks_header = preprocessed_protocol.split("|||SECTION|||")
    chunks_header
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
        ## 3.8 Summary & Conclusion

        In this notebook, we've learned:

        - How to implement RAG using QueryBot
        - How to add memory capabilities to maintain conversation context
        - Best practices for building effective RAG systems
        - Advanced text chunking strategies for different query types
        - How to customize and optimize the system for different use cases

        Key takeaways:

        - RAG combines the power of LLMs with external knowledge
        - Memory adds context and coherence to conversations
        - Proper document management is crucial for effective RAG
        - System design choices significantly impact performance
        - Different query types require different chunking and indexing strategies


        AI, please make sure this is up-to-date.
        """  # noqa: E501
    )
    return


if __name__ == "__main__":
    app.run()
