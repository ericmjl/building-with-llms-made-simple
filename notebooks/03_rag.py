# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "llamabot[all]==0.12.8",
#     "marimo",
#     "pyprojroot==0.3.0",
#     "rich==13.9.4",
#     "lancedb",
#     "sentence-transformers",
#     "chonkie==1.0.8",
#     "building-with-llms-made-simple==0.0.1",
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

    In this notebook, we'll explore how to build RAG systems that can maintain
    conversation context. We'll focus on creating a system that can answer questions
    based on a knowledge base while remembering previous interactions.

    ## Learning Objectives

    By the end of this notebook, you will be able to:

    1. Understand how RAG systems combine retrieval with generation
    2. Set up and manage local document stores for knowledge and memory
    3. Create a QueryBot that maintains conversation context through memory
    4. Implement effective text chunking strategies


    The notebook is structured as follows:

    1. Introduction to RAG and Memory concepts
    2. Setting up document stores
    3. Creating and managing sample documents
    4. Building a QueryBot with memory
    5. Understanding the RAG process
    6. Advanced text chunking strategies
    7. Best practices and implementation guidelines
    8. Summary and key takeaways
    """
    )
    return


@app.cell
def _():
    from pathlib import Path

    import llamabot as lmb
    from llamabot.components.docstore import LanceDBDocStore
    from rich import print
    return LanceDBDocStore, lmb, print


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Setting Up Document Stores

    To build our RAG system, we'll need two types of storage:

    1. A knowledge base for our documents
    2. A memory store for conversation history

    We'll use LanceDB, a lightweight vector database that makes it easy to:
    - Store and search through documents
    - Find similar content quickly
    - Keep track of conversation history
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    LlamaBot attempts to provide a uniform interface to document stores -
    both in-memory and 3rd-party vector stores,
    such as LanceDB (currently most recommended),
    ChromaDB (recently deprecated, but planned to be revived),
    and perhaps in the future,
    SQLite with the SQLite-vec extension and other cloud services.
    It comes configured with sane defaults,
    and as such you can think of it as a mid-level interface
    on top of other document storage systems.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Exercise: Set up a LanceDB document store

    Use `lmb.LanceDBDocStore()` to create two document stores.
    The first is for the knowledge base in which we will store documents,
    and the second is for bot memory.
    Recall that the API for the docstore is:

    ```python
    import llamabot as lmb

    ds = lmb.LanceDBDocStore(table_name=...)
    ```
    """
    )
    return


@app.cell
def _():
    # Create the document stores
    from building_with_llms_made_simple.rag_answers import (
        create_knowledge_store,
        create_memory_store,
        create_rag_bot,
    )

    # Comment the following lines and try to write the code yourself!
    knowledge_store = create_knowledge_store()
    memory_store = create_memory_store()

    # Your answers here!
    return create_rag_bot, knowledge_store, memory_store


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Creating Sample Documents

    Let's use some sample documents about a fictional programming language
    called Zenthing. We'll use these to demonstrate how RAG works with a
    knowledge base.

    ### Detour: Why Zenthing?

    We're using a fictional programming language
    to ensure the bot relies solely on our provided knowledge.
    In doing so, we can attempt to avoid confusion with real programming
    languages.
    This is a good way to test the bot's ability to retrieve information
    from a knowledge base and not from its own background knowledge.
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
    mo.md(r"""One of the first things I would like to disambiguate here is that documents are nothing more than text! Given the current state of technology, vector stores most commonly will accept plain text, images, and audio. Complex documents such as PDFs and word documents need to be converted into plain text first.""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Now, let's try retrieving documents from the docstore.
    The way that this works is as follows:

    ```python
    docstore.retrieve("query goes here...", n_results=2)
    ```

    Try out different queries for yourself.
    """
    )
    return


@app.cell
def _():
    # Retrieve something from the document store!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Exercise: Create a QueryBot

    Now, let's create a QueryBot that can use both our knowledge base and
    conversation history.
    We'll configure it to:
    (a) find relevant information in our documents (using a LanceDBDocStore), and
    (b) remember previous conversations through a memory module.

    The way to create a QueryBot is as follows:


    ```python
    qb = QueryBot(
        system_prompt=...,
        docstore=...<some DocStore object>...,
        memory=...<soem DocStore object>...,
        model_name="provider/model_name",
        # other SimpleBot kwargs go here.
    )
    ```
    """
    )
    return


@app.cell
def _(create_rag_bot, knowledge_store, memory_store):
    # Create the QueryBot
    rag_bot = create_rag_bot(knowledge_store, memory_store)
    return


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

    Recall that the way to make queries of a LlamaBot bot is:

    ```python
    response = querybot("query goes here...")
    ```
    """
    )
    return


@app.cell
def _():
    # Try asking the bot about what is Zenthing.
    return


@app.cell
def _():
    # Try asking about Zenthing's key features.
    return


@app.cell
def _():
    # Try asking how Zenthing is used in Data Science.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Understanding the RAG Process

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

    Try using a SimpleBot (or your personal ChatGPT/Claude/Gemini account) to generate more synthetic data regarding Zenthing, and add it to the docstore. The API for adding new docs to the docstore is:

    ```python
    list_of_docs = [...] # list of strings
    docstore.extend(list_of_docs)
    ```
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
    ### Exercise: tweak the number of results

    A `QueryBot.__call__()` allows you to tweak the number of results retrieved from the document store:

    ```python
    query_bot("query goes here", n_results=...)
    ```
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
    ### Exercise: tweak the number of results

    A `QueryBot.__call__()` allows you to tweak the number of results retrieved from the document store:

    ```python
    query_bot("query goes here", n_results=...)
    ```
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
    ### Exercise: change prompts

    Try changing the system prompt or the way the user prompt is passed in to steer how the bot behaves.
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
    ## Advanced Text Chunking Strategies

    We're now going to talk about chunking strategies.

    Chunking is a critical component of RAG systems that determines
    how effectively the system can retrieve and use information.
    In this section,
    we'll explore different chunking strategies and their applications.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Why chunking matters

    Language models have limited context windows,
    which means they can't process entire documents at once.
    Chunking helps by breaking documents into manageable pieces.
    If done right, you can preserve semantic meaning within chunks,
    but if not done right, you might break documents in undesirable places.
    As such, it's important to figure out a sane chunking strategy,
    based on the kinds of documents that you encounter.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Token/Character-based Chunking

    Let's start by exploring the simplest form of chunking,
    where we split text based on a fixed number of tokens or characters.
    This is usually a baseline that is used for splitting a document
    in the absence of any other information.

    However, it has limitations.
    This kind of splitting may split sentences mid-way,
    it doesn't respect natural language boundaries,
    and as a result, it can break semantic coherence,
    especially if an idea is cut right in the middle.

    Let's see how this works with our climate change essay example.
    I used SimpleBot on my machine to generate an essay on climate change.
    """
    )
    return


@app.cell
def _(lmb):
    essay_writer = lmb.SimpleBot(
        "You are an expert on whatever topic is thrown at you.",
        model_name="ollama_chat/llama3.1",
    )

    essay = essay_writer(
        "Write me an 5 page essay on climate change. Each page should have ~500 words on it."
    )
    return (essay,)


@app.cell
def _(essay, print):
    text_to_chunk = essay.content
    print(text_to_chunk)
    return (text_to_chunk,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Given this text, observe how the chunks vary as we change chunking strategy.
    We will now introduce Chonkie, a Python library for chunking text together.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Introducing Chonkie: A Modern Text Chunking Library

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
def _(mo):
    mo.md(r"""**Note:** The settings above are by no means sane defaults, they were tuned to this tutorial to make some points more evident!""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Discussion

    What are salient properties that you notice about the chunks? Where do the chunks start and end?
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Sentence Chunking

    Let's try a different chunker from Chonkie, the `SentenceChunker`, and let's see how the chunks look different.
    """
    )
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Discussion

    Compare the chunks from the `SentenceChunker` and the `TokenChunker`. How do they differ?
    """
    )
    return


@app.cell(hide_code=True)
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
        r"""
    Some special kinds of documents may need a different chunking and processing strategy
    before being stored in a DocStore.

    For example, if you want to enable searching through laboratory protocols
    with the goal of guiding people to a very specific section,
    you may want to chunk by section instead to make citations easy.

    Here, I am going to provide you with three texts:

    1. A `lab_protocol_text`,
    2. A `cleaning_protocol_text`, and
    3. A `quality_control_protocol_text`.
    """
    )
    return


@app.cell
def _(print):
    from building_with_llms_made_simple.rag_answers import (
        lab_protocol_text,
        cleaning_protocol_text,
        quality_control_protocol_text,
    )

    # Preview the texts before proceeding
    print(lab_protocol_text)
    print("-----")
    print(cleaning_protocol_text)
    print("-----")
    print(quality_control_protocol_text)
    return (
        cleaning_protocol_text,
        lab_protocol_text,
        quality_control_protocol_text,
    )


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Discussion

    How would you choose to chunk these documents? Discuss this with your neighbor.

    What other chunking strategies would be handy here?

    Then let's share what we've discussed in the larger group.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Demo

    As a demo, I am showing below how to chunk a document with a custom chunker (not using Chonkie now). The goal is to get each top-level section into a single chunk.
    """
    )
    return


@app.cell
def _(
    cleaning_protocol_text,
    lab_protocol_text,
    quality_control_protocol_text,
):
    from building_with_llms_made_simple.rag_answers import insert_delimiter


    sop_chunks = []
    titles_to_texts = {
        "lab protocol": lab_protocol_text,
        "cleaning protocol": cleaning_protocol_text,
        "quality control protocol": quality_control_protocol_text,
    }
    for title, text in titles_to_texts.items():
        preprocessed = insert_delimiter(text, level=1)
        txt_chunks = preprocessed.split("|||SECTION|||")
        for txt in txt_chunks:
            txt += f"\n(from document {title})"
            sop_chunks.append(txt)
    sop_chunks
    return (sop_chunks,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Because we have 3 documents mixed together, one design choice I have made is to append the document source to the end of the chunk so that it maintains its connection to the original document title. We can discuss pros/cons about this later.""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Exercise: Build another QueryBot

    Now, let's build an SOP bot and try to query it. Key instructions for this exercise:

    1. Create an `sop_docstore`, and an `sop_memorystore`, both being `LanceDBDocStore`s.
    2. Add the chunks that we just
    3. Create an `sop_bot`, passing in `sop_docstore` and `sop_memorystore` into the `QueryBot` constructor.
    4. Then, query the SOP bot!
    """
    )
    return


@app.cell
def _(LanceDBDocStore, lmb, sop_chunks):
    from building_with_llms_made_simple.rag_answers import rag_bot_sysprompt

    sop_docstore = LanceDBDocStore(
        table_name="sop_docstore",
    )
    # For this experiment, clear out the docstore just in case we are re-running stuff.
    sop_docstore.reset()
    sop_docstore.extend(sop_chunks)

    sop_memorystore = LanceDBDocStore(table_name="sop_bot_memory")
    sop_memorystore.reset()

    sop_bot = lmb.QueryBot(
        system_prompt=rag_bot_sysprompt(),
        docstore=sop_docstore,
        memory=sop_memorystore,
        model_name="ollama_chat/llama3.1",
        temperature=0.0,  # Keep responses deterministic
    )
    return (sop_bot,)


@app.cell
def _(sop_bot):
    sop_bot("How do we measure the quality of our samples?")
    return


@app.cell
def _():
    # Your code goes here!
    return


@app.cell
def _(mo):
    mo.md(r"""Now try""")
    return


@app.cell
def _(sop_bot):
    response = sop_bot("What are the roles of the personnel involved in quality monitoring?")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Exercise: 🔴-team the bot

    Your task: try your best to find cases where the LLM fails to answer a relevant question correctly!
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
    ## Discussion.

    SOPs are a single example of the kinds of documents that we would process. I synthesized the examples we have here based on discussions with friends and colleagues across the industry that I work in.

    Let's talk about your specific industry. What documents do you encounter? How would you preprocess and chunk them? Discuss with your neighbors.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Key questions to ask before embarking on RAG

    1. Is there a known structural pattern to the docs that are to be chunked? If so, leverage and take advantage of it.
    2. What are the expected queries that your users will ask? No need to be overly comprehensive, but know the key ones first.
    3. Is attribution/citation important? If so, in your text chunking, you may want to add source document metadata in your chunks as context. This is a generalizable tactic for other kinds of metadata.
    """
    )
    return


if __name__ == "__main__":
    app.run()
