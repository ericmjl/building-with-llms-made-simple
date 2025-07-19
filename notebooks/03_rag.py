# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = [
#     "llamabot[all]==0.12.11",
#     "marimo",
#     "pyprojroot==0.3.0",
#     "rich==14.0.0",
#     "lancedb",
#     "sentence-transformers",
#     "chonkie==1.0.10",
#     "torch>=2.5.1; (platform_system != 'Darwin' or platform_machine != 'x86_64')",
#     "torch==2.2.2; platform_system == 'Darwin' and platform_machine == 'x86_64'",
#     "numpy<2; (platform_system == 'Darwin' and platform_machine == 'x86_64')",
# ]
# ///

import marimo

__generated_with = "0.14.12"
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
    ## RAG in 5 minutes

    <iframe src="https://link.excalidraw.com/readonly/Hd9NUurFW5YdM0zYxUwZ" width="100%" height="800" style="border: none;"></iframe>
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Setting Up Document Stores

    To build our RAG system, we'll need a knowledge base for our documents.
    We'll use LanceDB, a lightweight vector database that, most crucially,
    comes with hybrid search capabilities.
    Within LlamaBot, we provide a `LanceDBDocStore` that has a uniform interface
    and sane defaults on LanceDB that should "just work" for a variety of applications.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Set up a LanceDB document store

    In the cell below, I have created for you two LanceDBDocStores,
    one for document storage about ZenThing (a fictional programming language we'll explore),
    and the other for storing conversation memories.
    The API for the docstore is:

    ```python
    import llamabot as lmb

    # Replace table_name with a human-readable name for what you're storing in here.
    ds = lmb.LanceDBDocStore(table_name="some informative name here")
    ```

    If you're curious to see how `create_knowledge_store` and `create_memory_store` are implemented,
    feel free to peek inside the repo.
    """
    )
    return


@app.cell(hide_code=True)
def _(lmb):
    @lmb.prompt("system")
    def rag_bot_sysprompt():
        """You are a helpful programming language assistant.
        You will be provided documents to answer questions.
        Answer questions solely based on the provided documents
        and not your background knowledge.
        If you're not sure about something, say so.
        Keep your responses concise and focused on the question asked.
        Be concise and to the point!
        When you respond, ensure that you cite the source of your answer,
        including section number and original document.
        """

    def create_knowledge_store():
        """Create and initialize a knowledge store for document storage.

        :return: A LanceDB document store configured for storing the knowledge base
            with table name "knowledge_base". The store is reset before being returned
            to ensure a clean state.
        """
        # Create document stores
        knowledge_store = lmb.LanceDBDocStore(
            table_name="knowledge_base",
        )
        knowledge_store.reset()
        return knowledge_store

    def create_memory_store():
        """Create and initialize a memory store for conversation history.

        :return: A LanceDB document store configured for storing conversation memory
            with table name "memory". The store is reset before being returned to
            ensure a clean state.
        """
        memory_store = lmb.LanceDBDocStore(
            table_name="memory",
        )
        memory_store.reset()
        return memory_store

    def create_rag_bot(
        knowledge_store: lmb.LanceDBDocStore, memory_store: lmb.LanceDBDocStore
    ):
        """Create a RAG bot configured with knowledge and memory stores.

        :param knowledge_store: The document store containing the knowledge base
            for answering questions.
        :param memory_store: The document store for maintaining conversation history.
        :return: A configured RAG bot that can answer questions based on the provided
            knowledge store and maintain conversation context using the memory store.
        """
        rag_bot = lmb.QueryBot(
            system_prompt=rag_bot_sysprompt(),
            docstore=knowledge_store,
            memory=memory_store,
            model_name="ollama_chat/phi4",
            temperature=0.0,  # Keep responses deterministic
        )
        return rag_bot

    return (
        create_knowledge_store,
        create_memory_store,
        create_rag_bot,
        rag_bot_sysprompt,
    )


@app.cell
def _(create_knowledge_store, create_memory_store):
    # Create the document stores

    # Comment the following lines and try to write the code yourself!
    knowledge_store = create_knowledge_store()
    memory_store = create_memory_store()

    # Your answers here!

    return knowledge_store, memory_store


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## What's going on here?

    1. We are intializing two empty LanceDB databases, one for chat memory purposes, and one for document storage purposes.
    2. Underneath the hood, we are setting our vector dims for document embeddings to be 128 in length.
    3. LanceDBDocStores are configured to automatically use **hybrid search**, which means we do both keyword and vector search, so the ColBERTReranker is used to combine the results from both searches into a single list.
    4. The embedding model used in Llamabot is the `minishlab/potion` model, which is 100-500X faster than sentence-transformers and "good enough" for most purposes.
    5. You can ignore the term "Linear dim" 🤗.
    """
    )
    return


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
def _(
    knowledge_store,
    zenthing_ecosystem_use_cases_text,
    zenthing_language_features_text,
    zenthing_overview_text,
    zenthing_syntax_and_programming_style_text,
):
    # Sample documents about a new programming language named Zenthing
    zenthing_docs = [
        zenthing_ecosystem_use_cases_text,
        zenthing_language_features_text,
        zenthing_overview_text,
        zenthing_syntax_and_programming_style_text,
    ]

    # Add documents to knowledge store
    knowledge_store.extend(zenthing_docs)  # Using extend for bulk addition
    return (zenthing_docs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""One of the first things I would like to disambiguate here is that documents are nothing more than text! Given the current state of technology, vector stores most commonly will accept plain text, images, and audio. Complex documents such as PDFs and word documents need to be converted into plain text first.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Now, let's try retrieving documents from the docstore.
    The way that this generically works is as follows:

    ```python
    # replace "docstore", and "query goes here..." and `n_results`.
    docstore.retrieve("query goes here...", n_results=2)
    ```

    Try out different queries for yourself.
    """
    )
    return


@app.cell
def _(knowledge_store):
    # Retrieve something from the document store!
    knowledge_store.retrieve("how does zenthing work?", n_results=3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The retrieved documents can now be passed to an LLM in combination with the user query and system prompt to generate the answer.""")
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
    qb = lmb.QueryBot(
        system_prompt="You are an expert in the Zenthing programming language.",
        docstore=..., # replace with your knowledge store object object
        memory=..., # replace with your memory store object
        model_name="provider/model_name", # e.g. ollama_chat/phi4
        # other SimpleBot kwargs go here.
    )
    ```
    """
    )
    return


@app.cell
def _(create_rag_bot, knowledge_store, memory_store):
    # Comment out the following line if you're going to implement QueryBot on your own.
    rag_bot = create_rag_bot(knowledge_store, memory_store)

    # Your code here!
    return (rag_bot,)


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
def _(rag_bot):
    # Try asking the bot about what is Zenthing.
    rag_bot("what is Zenthing?")
    return


@app.cell
def _(rag_bot):
    # Try asking about Zenthing's key features.
    rag_bot("What are Zenthing's key features?")
    return


@app.cell
def _(rag_bot):
    # Try asking how Zenthing is used in Data Science.
    rag_bot("How is Zenthing used in Data science?")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""To make sure that we are genuinely retrieving from the documents and not just hallucinating based on prior training data and prior chat memory, we should actually set the memory of `rag_bot` as well as the doc store of `rag_bot` to be empty.""")
    return


@app.cell
def _(knowledge_store, lmb, memory_store, rag_bot):
    blank_docstore = lmb.LanceDBDocStore(table_name="blank-docstore")
    blank_docstore.reset()  # make the blank docstore empty

    blank_memory = lmb.LanceDBDocStore(table_name="blank-memory")
    blank_memory.reset()

    rag_bot.docstore = knowledge_store
    rag_bot.memory = memory_store

    rag_bot("How is Zenthing used in Data science?")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Demo: using Marimo UI elements to quickly stand up a prototype""")
    return


@app.cell
def _(mo, rag_bot):
    def chat_callback(messages, config):
        # Each message has a `content` attribute, as well as a `role`
        # attribute ("user", "system", "assistant");
        question = messages[-1].content
        return rag_bot(question).content

    chat = mo.ui.chat(chat_callback)
    chat
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
    which means you can't guarantee that you can process entire documents at once.
    Even the 1M context windows can't stuff all of your company's documents together.
    And moreover, LLMs are known to suffer from the needle-in-a-haystack problem
    when given too much information to answer a very specific request.

    Chunking helps by breaking documents into manageable pieces.
    If done right, you can preserve semantic meaning within chunks,
    but if not done right, you might break documents in undesirable places.
    As such, it's important to figure out a sane chunking strategy,
    based on the kinds of documents that you encounter.

    In the Zenthing example above, we dispensed with chunking and simply stored each document on its own.
    In the following section, we'll see what it's like to chunk documents using different strategies,
    and explore whether they will have an effect on the generated output text.
    """
    )
    return


@app.cell(hide_code=True)
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
def _(zenthing_docs):
    from chonkie import TokenChunker

    text_to_chunk = "\n".join(zenthing_docs)

    # Basic initialization with default parameters
    chunker_basic = TokenChunker(
        tokenizer="gpt2",  # Supports string identifiers
        chunk_size=128,  # Maximum tokens per chunk
        chunk_overlap=8,  # Overlap between chunks
    )

    chunks_basic = chunker_basic(text_to_chunk)
    chunks_basic
    return chunks_basic, text_to_chunk


@app.cell
def _(chunks_basic, lmb):
    zenthing_basic_chunks_docstore = lmb.LanceDBDocStore(
        table_name="zenthing_basic_chunks_docstore"
    )
    zenthing_basic_chunks_docstore.reset()
    zenthing_basic_chunks_docstore.extend([chunk.text for chunk in chunks_basic])
    return (zenthing_basic_chunks_docstore,)


@app.cell
def _(mo):
    mo.md(r"""**Note:** The settings above are by no means sane defaults, they were tuned to this tutorial to make some points more evident!""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Discussion

    What are salient properties that you notice about the chunks? Specifically, where do the chunks start and end?
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
    return (chunks_sentence,)


@app.cell
def _(chunks_sentence, lmb):
    zenthing_sentence_chunks_docstore = lmb.LanceDBDocStore(
        table_name="zenthing_sentence_chunks_docstore"
    )
    zenthing_sentence_chunks_docstore.reset()
    zenthing_sentence_chunks_docstore.extend([chunk.text for chunk in chunks_sentence])
    return (zenthing_sentence_chunks_docstore,)


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
    ## How does chunking change answers?

    We are going to observe the difference by comparing answers with a QueryBot that has access to each of the two docstores. This is going to be pretty trippy with Bot surgery and monkey-patching, I hope you enjoy the ride 🙃.
    """
    )
    return


@app.cell
def _(mo, rag_bot):
    # First off, lobotomy -- disable rag_bot's chat_memory.
    rag_bot.memory = None

    question = mo.ui.text_area(label="Question about Zenthing")
    question
    return (question,)


@app.cell
def _(
    mo,
    question,
    rag_bot,
    zenthing_basic_chunks_docstore,
    zenthing_sentence_chunks_docstore,
):
    # Next up, swap docstores on-the-fly.
    rag_bot.docstore = zenthing_basic_chunks_docstore
    response_basic = rag_bot(question.value)
    basic_md = mo.md(response_basic.content)

    # Next up, swap docstores again
    rag_bot.docstore = zenthing_sentence_chunks_docstore
    response_sentence = rag_bot(question.value)
    sentence_md = mo.md(response_sentence.content)

    # Show the two responses side-by-side.
    response_md = mo.hstack([basic_md, sentence_md])
    response_md
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Discussion: What's the difference?

    Is there a difference between the two ways of chunking, for the given query?

    - Sometimes this will be query-dependent.
    - Can you think of a situation where the two response will look different?
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Custom Chunking

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
def _(
    cleaning_protocol_text,
    lab_protocol_text,
    print,
    quality_control_protocol_text,
):
    # Preview the texts before proceeding
    print(lab_protocol_text)
    print("-----")
    print(cleaning_protocol_text)
    print("-----")
    print(quality_control_protocol_text)
    return


@app.cell(hide_code=True)
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
    insert_delimiter,
    lab_protocol_text,
    quality_control_protocol_text,
):
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
def _():
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

    return (insert_delimiter,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Because we have 3 documents mixed together, one design choice I have made is to append the document source to the end of the chunk so that it maintains its connection to the original document title. We can discuss pros/cons about this later.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Demo: Build another QueryBot

    Now, let's build an SOP bot and try to query it. Key points for this demo:

    1. Create an `sop_docstore`, and an `sop_memorystore`, both being `LanceDBDocStore`s.
    2. Add the chunks that we just
    3. Create an `sop_bot`, passing in `sop_docstore` and `sop_memorystore` into the `QueryBot` constructor.
    4. Then, query the SOP bot!
    """
    )
    return


@app.cell
def _(LanceDBDocStore, lmb, rag_bot_sysprompt, sop_chunks):
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
        model_name="ollama_chat/llama3.2",
        temperature=0.0,  # Keep responses minimally stochastic
    )
    return (sop_bot,)


@app.cell(hide_code=True)
def _():
    return


@app.cell
def _(sop_bot):
    sop_bot("How do we measure the quality of our samples?")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We'll now try another query.""")
    return


@app.cell
def _(sop_bot):
    response = sop_bot(
        "What are the roles of the personnel involved in quality monitoring?"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Take-Home Exercise: Build a ChatUI for SOPBot

    Using what you've seen above, make a ChatUI for the SOPBot below.
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
    ## Take-Home Exercise: 🔴-team the bot

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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Converting Documents

    All of the texts that we dealt with above were given to us in plain text format.
    What if we had to deal with documents of varying types instead?
    How would we convert them to plain text for indexing?

    Here are a few tools you could consider using:

    1. [docling](https://docling-project.github.io/docling/) - in personal testing, this is the most turnkey open source solution.
    2. [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
    3. [Tesseract](https://github.com/tesseract-ocr/tesseract)
    4. [Mistral's OCR API](https://docs.mistral.ai/capabilities/OCR/document_ai_overview/)

    There are many others available, but these are some of the easier ones to get started with.
    In particular, I am a fan of `docling` for its ease of getting started:

    ```bash
    uvx docling 2025-1091.pdf --pipeline vlm --vlm-model smoldocling --image-export-mode referenced --to doctags
    ```

    Doctags appear to be quite a useful data structure in particular:

    > Doctags is a custom format (a but inspired by xml) that is intended to be optimal for LLM's. We try to represent the content and visual structure with special tags, that can be added to the tokenizer of the LLM.
    >
    > Our aim is to train/finetune LLM's on doctags to make it intuitively understand document structure.
    >
    > https://github.com/docling-project/docling/discussions/354
    """
    )
    return


@app.cell(hide_code=True)
def _():
    lab_protocol_text = """
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
    """  # noqa: E501
    return (lab_protocol_text,)


@app.cell(hide_code=True)
def _():
    cleaning_protocol_text = """
    1.	Purpose
    1.1 The purpose of this standard operating procedure (SOP) is to establish a comprehensive cleaning and sanitization protocol for manufacturing equipment and facilities.
    1.1.1 This document outlines the procedures for maintaining a clean and sanitized manufacturing environment.
    1.1.2 It ensures compliance with current Good Manufacturing Practices (cGMP) and regulatory requirements.
    1.2 This SOP helps prevent cross-contamination and ensures product quality and safety.
    2.	Scope
    2.1 This SOP applies to all manufacturing areas, equipment, and surfaces that come into contact with products.
    2.1.1 It covers routine cleaning, sanitization, and disinfection procedures.
    2.1.2 It includes both manual and automated cleaning processes.
    2.2 The SOP is applicable to all manufacturing personnel, cleaning staff, and quality control personnel.
    3.	Responsibilities
    3.1 Manufacturing Manager
    3.1.1 Ensure proper implementation of cleaning procedures.
    3.1.2 Review and approve cleaning validation protocols.
    3.1.3 Monitor cleaning effectiveness through regular audits.
    3.2 Cleaning Staff
    3.2.1 Execute cleaning procedures as specified.
    3.2.2 Document cleaning activities in cleaning logs.
    3.2.3 Report any cleaning-related issues immediately.
    4.	Materials and Equipment
    4.1 Cleaning Agents
    4.1.1 Approved cleaning detergents (e.g., CIP-100, Alkaline Cleaner).
    4.1.2 Sanitizing solutions (e.g., 70% Isopropyl Alcohol, Quaternary Ammonium Compounds).
    4.1.3 Deionized water (Type I, <18 MΩ·cm).
    4.2 Cleaning Tools
    4.2.1 Dedicated cleaning brushes and mops.
    4.2.2 Color-coded cleaning cloths.
    4.2.3 Non-shedding wipes.
    4.3 Equipment
    4.3.1 Automated cleaning systems (CIP/SIP).
    4.3.2 Pressure washers and steam cleaners.
    4.3.3 Cleaning validation test kits.
    5.	Procedure
    5.1 Pre-cleaning Assessment
    5.1.1 Identify cleaning requirements
    5.1.1.1 Review product contact surfaces.
    5.1.1.2 Determine appropriate cleaning agents.
    5.1.2 Prepare cleaning area
    5.1.2.1 Remove or protect sensitive equipment.
    5.1.2.2 Post appropriate warning signs.
    5.2 Cleaning Process
    5.2.1 Initial cleaning
    5.2.1.1 Remove gross contamination.
    5.2.1.2 Apply appropriate cleaning agent.
    5.2.2 Detailed cleaning
    5.2.2.1 Clean all surfaces thoroughly.
    5.2.2.2 Pay special attention to hard-to-reach areas.
    5.3 Sanitization
    5.3.1 Apply sanitizing solution
    5.3.1.1 Use approved sanitizing agents.
    5.3.1.2 Follow contact time requirements.
    5.3.2 Final rinse
    5.3.2.1 Rinse with purified water.
    5.3.2.2 Verify no cleaning agent residues.
    6.	Documentation
    6.1 Cleaning Records
    6.1.1 Document cleaning activities in cleaning logs.
    6.1.2 Record cleaning agent concentrations and contact times.
    6.1.3 Note any deviations or issues.
    6.2 Validation Records
    6.2.1 Maintain cleaning validation protocols.
    6.2.2 Document test results and acceptance criteria.
    6.2.3 Keep records for required retention period.
    7.	Quality Control
    7.1 Visual Inspection
    7.1.1 Verify cleanliness of all surfaces.
    7.1.2 Check for any residues or stains.
    7.2 Microbiological Testing
    7.2.1 Perform surface swab tests.
    7.2.2 Monitor air quality in clean areas.
    7.2.3 Document test results.
    8.	References
    8.1 Internal Documents
    8.1.1 Cleaning Validation Master Plan.
    8.1.2 Equipment Cleaning Logs.
    8.2 External Standards
    8.2.1 FDA cGMP Guidelines.
    8.2.2 ISO 14644 Cleanroom Standards.
    9.	Revision History
    9.1 Revision 0 (June 1, 2025)
    9.1.1 Initial creation of cleaning protocol.
    9.1.2 Established basic cleaning procedures.
    9.2 Future Revisions
    9.2.1 Updates to be made as needed based on regulatory changes or process improvements.
    """  # noqa: E501
    return (cleaning_protocol_text,)


@app.cell(hide_code=True)
def _():
    quality_control_protocol_text = """
    1.	Purpose
    1.1 The purpose of this standard operating procedure (SOP) is to establish specific quality control testing procedures for pharmaceutical tablet products.
    1.1.1 This document outlines the exact methods, equipment, and acceptance criteria for tablet testing.
    1.1.2 It ensures compliance with USP <711> Dissolution, USP <905> Uniformity of Dosage Units, and USP <1217> Tablet Breaking Force.
    1.2 This SOP maintains product quality standards for immediate-release tablet formulations.
    2.	Scope
    2.1 This SOP applies to all immediate-release tablet products manufactured in Facility A.
    2.1.1 It covers physical testing (hardness, friability, disintegration), chemical testing (assay, content uniformity, dissolution), and microbiological testing (bioburden, endotoxin).
    2.1.2 It includes stability testing at 25°C/60%RH, 30°C/65%RH, and 40°C/75%RH conditions.
    2.2 The SOP is applicable to quality control laboratory personnel and manufacturing staff in the tablet production department.
    3.	Responsibilities
    3.1 Quality Control Manager
    3.1.1 Review and approve all test results exceeding ±5% of target values.
    3.1.2 Authorize method modifications and equipment calibration schedules.
    3.1.3 Lead out-of-specification (OOS) investigations when results exceed USP limits.
    3.2 Quality Control Technicians
    3.2.1 Perform testing using calibrated equipment within 24 hours of sample receipt.
    3.2.2 Document all test results in the Laboratory Information Management System (LIMS).
    3.2.3 Maintain equipment calibration records and perform daily system suitability tests.
    4.	Materials and Equipment
    4.1 Physical Testing Equipment
    4.1.1 Tablet Hardness Tester (Pharma Test PTB 311E, calibrated monthly)
    4.1.2 Friability Tester (Erweka TAR 10, calibrated quarterly)
    4.1.3 Disintegration Tester (Erweka ZT 3, calibrated quarterly)
    4.2 Chemical Testing Equipment
    4.2.1 HPLC System (Agilent 1260 Infinity II, calibrated monthly)
    4.2.2 UV-Vis Spectrophotometer (PerkinElmer Lambda 35, calibrated monthly)
    4.2.3 Dissolution Apparatus (Agilent 708-DS, calibrated quarterly)
    4.3 Reference Materials
    4.3.1 USP Reference Standards (stored at 2-8°C)
    4.3.2 Working Standards (prepared monthly)
    4.3.3 System Suitability Solutions (prepared daily)
    5.	Procedure
    5.1 Physical Testing
    5.1.1 Tablet Hardness
    5.1.1.1 Test 10 tablets from each batch
    5.1.1.2 Acceptance criteria: 4-8 kp (kiloponds)
    5.1.2 Friability Testing
    5.1.2.1 Test 20 tablets for 4 minutes at 25 rpm
    5.1.2.2 Acceptance criteria: ≤1.0% weight loss
    5.1.3 Disintegration Testing
    5.1.3.1 Test 6 tablets in 900mL purified water at 37°C
    5.1.3.2 Acceptance criteria: ≤15 minutes
    5.2 Chemical Testing
    5.2.1 Assay Testing
    5.2.1.1 Prepare sample solution in mobile phase (0.1% TFA in water:acetonitrile 70:30)
    5.2.1.2 Run HPLC method: Column: C18, 250mm x 4.6mm, 5μm
    5.2.1.3 Flow rate: 1.0 mL/min, Detection: 254nm
    5.2.1.4 Acceptance criteria: 95.0-105.0% of label claim
    5.2.2 Content Uniformity
    5.2.2.1 Test 10 individual tablets
    5.2.2.2 Acceptance criteria: Each unit 85.0-115.0% of label claim
    5.2.3 Dissolution Testing
    5.2.3.1 Apparatus: USP Apparatus 2 (Paddle), 50 rpm
    5.2.3.2 Medium: 900mL 0.1N HCl, 37°C
    5.2.3.3 Test 12 tablets, sample at 15, 30, 45, and 60 minutes
    5.2.3.4 Acceptance criteria: Q=80% at 30 minutes
    6.	Documentation
    6.1 Test Records
    6.1.1 Record all raw data in bound notebooks (pre-numbered pages)
    6.1.2 Document instrument parameters, calibration status, and environmental conditions
    6.1.3 Include chromatograms, spectra, and dissolution profiles
    6.2 Certificate of Analysis
    6.2.1 Include batch number, manufacturing date, and expiry date
    6.2.2 List all test results with acceptance criteria
    6.2.3 Require signatures from analyst, reviewer, and QC manager
    7.	Quality Assurance
    7.1 Method Validation
    7.1.1 Specificity: Resolution ≥2.0 between peaks
    7.1.2 Linearity: R²≥0.999 over 50-150% of target concentration
    7.1.3 Accuracy: 98.0-102.0% recovery
    7.1.4 Precision: RSD≤2.0% for six replicates
    7.2 Out-of-Specification Investigation
    7.2.1 Phase 1: Laboratory investigation (24 hours)
    7.2.2 Phase 2: Full-scale investigation (5 business days)
    7.2.3 Phase 3: CAPA implementation (10 business days)
    8.	References
    8.1 Internal Documents
    8.1.1 Quality Manual (QM-001, Rev. 5)
    8.1.2 Test Method Procedures (TMP-001 through TMP-010)
    8.2 External Standards
    8.2.1 USP <711> Dissolution
    8.2.2 USP <905> Uniformity of Dosage Units
    8.2.3 USP <1217> Tablet Breaking Force
    9.	Revision History
    9.1 Revision 0 (June 1, 2025)
    9.1.1 Initial creation of tablet testing protocol
    9.1.2 Established specific acceptance criteria
    9.2 Future Revisions
    9.2.1 Updates to be made as needed based on regulatory changes or process improvements
    """  # noqa: E501

    return (quality_control_protocol_text,)


@app.cell(hide_code=True)
def _():
    zenthing_overview_text = """
    # Overview and History

    Zenthing is a high-level, interpreted programming language designed with simplicity and clarity in mind. It was created in 1995 by Hiroshi Tanaka, a Japanese software engineer who sought to develop a programming language that felt natural to write and read, even for beginners. Tanaka believed that the best code is code that communicates intent as clearly as possible—both to machines and to humans. With that in mind, Zenthing adopts a philosophy of minimalism and elegance, favoring explicitness over implicit behavior and readability over syntactic cleverness.

    Zenthing's syntax and structure borrow ideas from several influential languages of the 1980s and 1990s, but it takes a distinct approach in how it balances pragmatism with aesthetics. From its inception, Zenthing was intended to be a general-purpose language that could grow with the programmer—from learning basic algorithms to building large-scale systems.

    Although its adoption was initially limited to a niche community in Japan and East Asia, Zenthing gained international visibility in the early 2000s due to its elegant documentation, active developer community, and growing number of open-source libraries. Today, it enjoys an expanding user base worldwide and is used in both hobbyist projects and professional environments.

    ## Historical Development

    The language's development can be traced through several key milestones:

    **1995-1998: Foundation Years**
    - Initial design focused on educational use and rapid prototyping
    - First implementation written in C, targeting Unix-like systems
    - Basic syntax established with emphasis on readability
    - Introduction of the "zen" philosophy: code should be as clear as poetry

    **1999-2003: Community Growth**
    - Release of Zenthing 1.0 with comprehensive standard library
    - Establishment of the Zenthing Package Index (ZPI)
    - First major frameworks emerge (Django-Zenthing, Flask-zenthing)
    - Documentation translated into multiple languages

    **2004-2010: Enterprise Adoption**
    - Zenthing 2.0 introduces advanced features like decorators and context managers
    - Major companies begin adopting Zenthing for internal tools
    - Performance improvements through JIT compilation research
    - Integration with popular databases and web services

    **2011-Present: Modern Era**
    - Zenthing 3.0 brings type hints, async/await, and pattern matching
    - Growing ecosystem for data science and machine learning
    - Cloud-native development tools and containerization support
    - Active development of WebAssembly and mobile targets

    ## Design Philosophy

    Zenthing's design is guided by several core principles:

    **Readability First**: Every language feature is evaluated against its impact on code readability. Complex features are avoided if they make code harder to understand.

    **Explicit Over Implicit**: Zenthing prefers explicit behavior over hidden magic. When there are multiple ways to do something, the most explicit approach is usually the most "Zenthingic."

    **Batteries Included**: The standard library is comprehensive and well-designed, reducing the need for third-party dependencies for common tasks.

    **Progressive Disclosure**: The language is designed to be learnable incrementally. Beginners can write useful programs with basic syntax, while advanced users can leverage sophisticated features.

    **Community-Driven**: Language evolution is heavily influenced by community feedback and real-world usage patterns, rather than theoretical purity.

    ## Language Characteristics

    **Interpreted and Dynamic**: Zenthing is an interpreted language, which means code is executed directly without a separate compilation step. This enables rapid development cycles and interactive programming sessions.

    **Cross-Platform**: Zenthing runs on virtually all major operating systems including Windows, macOS, Linux, and various Unix variants. The same code can run unchanged across different platforms.

    **Extensible**: The language is designed to be easily extensible through modules and packages. The import system allows for clean separation of concerns and modular code organization.

    **High-Level**: Zenthing abstracts away many low-level details like memory management, making it easier to focus on solving problems rather than managing system resources.

    **Multi-Paradigm**: While Zenthing supports multiple programming paradigms, it doesn't force any particular approach. Developers can use procedural, object-oriented, or functional programming styles as appropriate.

    ## Performance Characteristics

    **Startup Time**: Zenthing has relatively fast startup times compared to compiled languages, making it ideal for scripting and automation tasks.

    **Memory Usage**: The language uses automatic memory management with a sophisticated garbage collector, though memory usage can be higher than compiled languages for certain workloads.

    **Execution Speed**: While not as fast as compiled languages like C or Rust, Zenthing's performance is adequate for most applications. Critical sections can be optimized using C extensions or specialized libraries.

    **Concurrency**: Modern Zenthing provides excellent support for concurrent programming through asyncio, threading, and multiprocessing modules, allowing developers to write efficient concurrent applications.

    ## Community and Ecosystem

    **Open Source**: Zenthing is developed as an open-source project with contributions from thousands of developers worldwide. The development process is transparent and community-driven.

    **Package Ecosystem**: The Zenthing Package Index (ZPI) contains over 400,000 packages covering virtually every domain of software development, from web frameworks to scientific computing libraries.

    **Documentation**: Zenthing is known for its excellent documentation, which is comprehensive, well-organized, and includes numerous examples and tutorials.

    **Learning Resources**: The language has a wealth of learning resources including official tutorials, community-contributed guides, books, online courses, and interactive platforms.

    **Conferences and Events**: The Zenthing community hosts numerous conferences and events worldwide, including PyCon (which has inspired ZenthingCon), local meetups, and specialized workshops.

    ## Future Directions

    **Performance Improvements**: Ongoing work on performance optimization includes JIT compilation research, better memory management, and specialized optimizations for common patterns.

    **Language Evolution**: The language continues to evolve with new features being added based on community needs and modern programming practices.

    **Tooling**: Development tools are constantly improving, with better IDEs, debugging tools, profiling utilities, and code analysis tools being developed.

    **Platform Expansion**: Efforts are underway to expand Zenthing's reach to new platforms including WebAssembly, mobile devices, and embedded systems.

    **AI and Machine Learning**: Zenthing is becoming increasingly important in the AI and machine learning space, with specialized libraries and frameworks being developed for these domains.
    """  # noqa: E501
    return (zenthing_overview_text,)


@app.cell(hide_code=True)
def _():
    zenthing_language_features_text = """
    Zenthing comes with a number of features that make it both powerful and approachable. Chief among these are its dynamic type system, automatic memory management, and an extensive standard library that covers everything from string manipulation to networking.

    **Key features include:**

    - **Dynamic typing**: Variables in Zenthing do not need explicit type declarations. Types are inferred at runtime, which speeds up development and reduces verbosity.

    - **Automatic memory management**: Zenthing handles memory allocation and garbage collection internally, freeing developers from manual memory handling and reducing the likelihood of memory leaks or segmentation faults.

    - **Extensive standard library**: The built-in library is designed to cover most common programming tasks. It includes modules for regular expressions, file I/O, JSON parsing, HTTP requests, multithreading, and more.

    - **Multi-paradigm support**: Zenthing allows developers to mix procedural, object-oriented, and functional programming styles. It does not force one paradigm over another but provides well-integrated support for each, making it easy to adopt whatever approach fits the problem best.

    - **Interoperability**: Although not a core feature in the early versions, modern Zenthing now supports Foreign Function Interfaces (FFIs) to interact with C libraries, and has evolving tools for WebAssembly and JVM interop, broadening its reach in cross-platform development.

    ## Advanced Language Features

    ### Type System and Annotations

    Zenthing's type system has evolved significantly since its inception. While the language remains dynamically typed, it now supports optional type annotations that provide several benefits. These annotations serve as documentation, enable better IDE support with autocomplete and error detection, and allow for static type checking tools to catch potential issues before runtime. The type system supports complex types including generics, union types, optional types, and callable types, making it possible to express sophisticated type relationships while maintaining the flexibility of dynamic typing.

    ### Memory Management and Performance

    Zenthing's garbage collector uses a sophisticated generational approach with three distinct generations. The collector automatically handles reference counting and circular reference detection, making memory management completely transparent to developers. This design allows Zenthing to efficiently manage memory for both short-lived objects (common in scripting) and long-lived objects (typical in long-running applications). The garbage collector is highly optimized and can be tuned for different application profiles, from memory-constrained embedded systems to high-throughput web servers.

    ### Concurrency and Asynchrony

    Modern Zenthing provides robust support for concurrent programming through multiple complementary approaches. The asyncio module offers cooperative multitasking for I/O-bound applications, allowing thousands of concurrent operations with minimal memory overhead. The threading module provides preemptive multitasking for CPU-bound tasks, while the multiprocessing module enables true parallelism across multiple CPU cores. These concurrency primitives are designed to work together seamlessly, allowing developers to choose the most appropriate approach for their specific use case.

    ### Metaprogramming Capabilities

    Zenthing's metaprogramming features enable powerful abstractions and code generation. Decorators provide a clean way to add cross-cutting concerns like logging, caching, and authentication to functions and classes. Context managers ensure proper resource management through the "with" statement, automatically handling setup and cleanup operations. Metaclasses allow for sophisticated class creation and modification, while descriptors provide fine-grained control over attribute access. These features make Zenthing particularly well-suited for building frameworks and libraries that need to provide elegant APIs while handling complex underlying logic.

    ### Pattern Matching and Structural Programming

    Recent versions of Zenthing have introduced structural pattern matching, which provides a powerful and readable way to handle complex conditional logic. This feature allows developers to match against data structures based on their shape and content, making code more expressive and less error-prone than traditional if-else chains. Pattern matching works seamlessly with Zenthing's data structures and can be extended to work with custom classes through special methods.

    ## Standard Library Highlights

    The Zenthing standard library is organized into several key areas, each designed to provide comprehensive functionality for common programming tasks:

    ### Data Structures and Algorithms

    The collections module provides specialized data structures that extend Zenthing's built-in types. These include defaultdict for automatic default values, Counter for frequency counting, deque for efficient double-ended queues, and OrderedDict for maintaining insertion order. The itertools module offers tools for working with iterators and generators, enabling memory-efficient processing of large datasets. The functools module provides higher-order functions and operations on callable objects, supporting functional programming patterns.

    ### System and OS Integration

    Zenthing provides comprehensive access to operating system functionality through modules like os, pathlib, and subprocess. The os module offers cross-platform access to operating system features, while pathlib provides an object-oriented interface to filesystem paths. The subprocess module enables spawning and managing child processes, making it easy to integrate with external programs and system commands. The multiprocessing module provides tools for parallel execution across multiple CPU cores.

    ### Network and Web Development

    Zenthing's networking capabilities are built around the socket module, which provides low-level network programming primitives. Higher-level modules like urllib and http build on this foundation to provide easy access to web resources and HTTP protocol implementation. The json module offers efficient JSON encoding and decoding, while the xml module provides tools for XML processing. These modules work together to provide comprehensive support for modern web development and API integration.

    ### Data Processing and Persistence

    Zenthing includes robust support for data processing and persistence. The csv module handles comma-separated value files, while the sqlite3 module provides a built-in database interface. The pickle module offers object serialization for saving and loading Zenthing objects, while the json module handles structured data exchange. The xml module provides tools for parsing and generating XML documents, making Zenthing suitable for enterprise data processing applications.

    ### Development Tools and Quality Assurance

    Zenthing's development tooling is built into the standard library. The unittest module provides a comprehensive testing framework, while the logging module offers flexible event logging capabilities. The pdb module provides an interactive debugger, and the profile module offers performance profiling tools. These tools enable developers to write, test, and maintain high-quality Zenthing code with confidence.

    ## Performance and Optimization

    Zenthing's performance characteristics make it suitable for a wide range of applications. The language's startup time is relatively fast compared to compiled languages, making it ideal for scripting and automation tasks. Memory usage is managed automatically through the garbage collector, though it can be higher than compiled languages for certain workloads. Execution speed is adequate for most applications, with critical sections being optimizable through C extensions or specialized libraries. The language's concurrency support allows for efficient handling of I/O-bound and CPU-bound workloads.

    ## Interoperability and Extensibility

    Zenthing's design emphasizes interoperability with other languages and systems. The Foreign Function Interface (FFI) allows Zenthing code to call functions written in C, enabling access to existing libraries and system APIs. The ctypes module provides a way to create Zenthing bindings to C libraries, while the cffi module offers a more modern approach to foreign function interfaces. Zenthing can also be embedded in C applications, allowing it to be used as a scripting language within larger systems.

    ## Language Evolution and Backward Compatibility

    Zenthing's development process emphasizes backward compatibility while allowing for language evolution. New features are introduced gradually, often starting as optional imports or experimental features before becoming part of the core language. This approach ensures that existing code continues to work while providing access to new capabilities. The language's versioning strategy allows developers to target specific Zenthing versions, ensuring predictable behavior across different environments.

    ## Community and Ecosystem Integration

    Zenthing's features are designed to work well with the broader ecosystem. The import system supports both relative and absolute imports, making it easy to organize code into packages and modules. The packaging tools provide standardized ways to distribute Zenthing code, while the virtual environment system allows for isolated dependency management. These features make Zenthing particularly well-suited for collaborative development and deployment in production environments.
    """  # noqa: E501
    return (zenthing_language_features_text,)


@app.cell(hide_code=True)
def _():
    zenthing_ecosystem_use_cases_text = """
    # Ecosystem and Use Cases

    Zenthing is rapidly carving out a space for itself in a number of software development domains. Thanks to its clean syntax, powerful libraries, and increasing third-party support, developers are beginning to adopt Zenthing for tasks ranging from web development to machine learning.

    **Notable areas of adoption:**

    - **Web development**: Zenthing frameworks like Django-Zenthing and Flask-zenthing provide intuitive, high-level APIs for building dynamic web applications. Zenthing's built-in web server and routing utilities make prototyping and deployment fast and flexible.

    - **Data science**: Libraries such as NumZen (numerical computing) and ZenPandas (tabular data manipulation) are modeled after their counterparts in other ecosystems, with a focus on clarity and integration. Zenthing's interactive console and rich visualization tools are attracting data analysts and scientists.

    - **Machine learning**: Zenthing is used in AI development through frameworks like TensorZen and ZenTorch, which provide high-level abstractions over computational graphs, training loops, and model serialization. Zenthing's syntax makes experimentation readable and repeatable.

    - **Scripting and automation**: Zenthing scripts are increasingly used in DevOps workflows, personal productivity tooling, and test automation. The language's quick startup time and batteries-included approach make it ideal for writing short programs and glue code.

    The Zenthing Package Index (ZPI) continues to grow rapidly, and the official documentation encourages contributions from the community, fostering an open and welcoming environment for new developers.

    ## Web Development Ecosystem

    ### Full-Stack Frameworks

    Django-Zenthing stands as the most comprehensive full-stack web framework in the Zenthing ecosystem. It provides a complete solution for building web applications with built-in support for database management, user authentication, admin interfaces, and form handling. The framework follows the Model-View-Template (MVT) architecture pattern, which promotes clean separation of concerns and maintainable code organization. Django-Zenthing's "batteries-included" philosophy means that developers can build production-ready applications without needing to integrate numerous third-party libraries.

    Flask-zenthing offers a lightweight alternative that gives developers more flexibility and control over their application architecture. It provides a minimal core with a rich ecosystem of extensions that can be added as needed. This approach makes Flask-zenthing particularly well-suited for microservices, APIs, and applications with specific requirements that don't fit the Django-Zenthing mold. The framework's simplicity makes it an excellent choice for learning web development and for projects where minimal overhead is desired.

    ### API Development and Microservices

    FastAPI-Zenthing has emerged as the leading framework for building high-performance APIs in the Zenthing ecosystem. It combines automatic request/response validation, automatic API documentation generation, and high performance through async support. The framework's type system integration means that API contracts are automatically validated and documented, reducing the likelihood of runtime errors and improving developer experience. FastAPI-Zenthing's performance characteristics make it suitable for high-throughput applications and microservices architectures.

    ### Frontend Integration and Modern Web Development

    Zenthing's web development ecosystem has evolved to support modern frontend development practices. Frameworks like Streamlit-Zenthing enable rapid development of data-focused web applications with minimal frontend code. For more complex applications, Zenthing can be integrated with modern JavaScript frameworks through API development, or used with WebAssembly targets for client-side Zenthing execution. The ecosystem also includes tools for static site generation, server-side rendering, and progressive web application development.

    ## Data Science and Analytics

    ### Numerical Computing and Scientific Computing

    NumZen provides the foundation for numerical computing in Zenthing, offering efficient array operations and mathematical functions. The library is designed to be both powerful and accessible, with syntax that closely resembles mathematical notation. NumZen's performance is optimized through vectorized operations and integration with optimized C libraries, making it suitable for both interactive data analysis and production scientific computing applications.

    ZenPandas builds on NumZen to provide powerful data manipulation capabilities for structured data. The library's DataFrame abstraction makes it easy to work with tabular data, while its Series type provides efficient handling of one-dimensional data. ZenPandas includes comprehensive tools for data cleaning, transformation, aggregation, and visualization, making it the go-to library for data analysis tasks.

    ### Statistical Analysis and Modeling

    The Zenthing ecosystem includes specialized libraries for statistical analysis and modeling. ZenStats provides comprehensive statistical functions, while ZenScikit offers machine learning algorithms with a consistent API. These libraries integrate seamlessly with NumZen and ZenPandas, creating a cohesive environment for data analysis and modeling. The ecosystem also includes libraries for specialized statistical techniques, time series analysis, and experimental design.

    ### Visualization and Interactive Computing

    Zenthing's visualization capabilities are built around libraries like ZenPlot and ZenBokeh, which provide both static and interactive plotting capabilities. These libraries integrate well with Jupyter notebooks and other interactive computing environments, enabling exploratory data analysis and reproducible research. The ecosystem also includes specialized visualization libraries for geographic data, network analysis, and scientific visualization.

    ## Machine Learning and Artificial Intelligence

    ### Deep Learning and Neural Networks

    TensorZen provides the foundation for deep learning in Zenthing, offering both high-level APIs for common tasks and low-level control for custom implementations. The library's computational graph abstraction allows for efficient execution on both CPU and GPU hardware, while its automatic differentiation capabilities simplify gradient computation for training neural networks. TensorZen's design emphasizes readability and experimentation, making it suitable for both research and production applications.

    ZenTorch offers an alternative approach to deep learning with a more dynamic computational graph model. This design makes it easier to debug and modify models during development, while still providing good performance for production use. ZenTorch's extensive library of pre-trained models and utilities makes it easy to get started with common deep learning tasks.

    ### Natural Language Processing

    The Zenthing ecosystem includes specialized libraries for natural language processing tasks. ZenNLP provides tools for text preprocessing, tokenization, and feature extraction, while ZenTransformers offers implementations of modern transformer architectures. These libraries integrate with the broader machine learning ecosystem, enabling end-to-end NLP applications from research to production deployment.

    ### Computer Vision and Image Processing

    Zenthing's computer vision capabilities are built around libraries like ZenCV and ZenPIL, which provide comprehensive tools for image processing and analysis. These libraries integrate with deep learning frameworks to enable computer vision applications, from simple image manipulation to complex object detection and recognition systems.

    ## DevOps and Infrastructure

    ### Infrastructure as Code and Configuration Management

    Zenthing's ecosystem includes tools for infrastructure automation and configuration management. ZenTerraform provides Zenthing bindings for Terraform, enabling infrastructure definition and management through Zenthing code. ZenAnsible offers similar capabilities for Ansible, while ZenKubernetes provides tools for working with Kubernetes clusters. These tools make it possible to manage complex infrastructure using familiar Zenthing syntax and patterns.

    ### Continuous Integration and Deployment

    The Zenthing ecosystem includes tools for automating software delivery pipelines. ZenActions provides Zenthing bindings for GitHub Actions, enabling complex workflow automation. ZenJenkins offers similar capabilities for Jenkins, while ZenDocker provides tools for container management and orchestration. These tools integrate with Zenthing's testing and packaging ecosystem to provide end-to-end automation of software delivery.

    ### Monitoring and Observability

    Zenthing's monitoring capabilities are built around libraries like ZenPrometheus and ZenGrafana, which provide tools for metrics collection, visualization, and alerting. These libraries integrate with the broader observability ecosystem, enabling comprehensive monitoring of Zenthing applications in production environments.

    ## Desktop and Mobile Development

    ### Graphical User Interfaces

    Zenthing's GUI development capabilities are built around libraries like ZenTkinter and ZenQt, which provide cross-platform graphical user interface development. These libraries offer both simple widgets for basic applications and sophisticated components for complex desktop applications. The ecosystem also includes specialized libraries for scientific visualization, data dashboards, and multimedia applications.

    ### Mobile and Cross-Platform Development

    Zenthing's mobile development capabilities are evolving through projects like ZenMobile and ZenKivy, which provide tools for building cross-platform mobile applications. These frameworks enable developers to write Zenthing code that can run on iOS, Android, and other mobile platforms. The ecosystem also includes tools for WebAssembly compilation, enabling Zenthing code to run in web browsers and other WebAssembly environments.

    ## Package Management and Distribution

    ### Package Index and Distribution

    The Zenthing Package Index (ZPI) serves as the central repository for Zenthing packages, providing tools for package discovery, installation, and distribution. The ZPI ecosystem includes tools for package building, testing, and deployment, making it easy for developers to share their code with the community. The ecosystem also includes tools for private package repositories and enterprise distribution.

    ### Development Environment Management

    Zenthing's development environment management is built around virtual environments and dependency management tools. ZenPoetry provides modern dependency management with lock files and dependency resolution, while ZenPipenv offers similar capabilities with a focus on security and reproducibility. These tools integrate with the broader Zenthing ecosystem to provide seamless development workflows.

    ### Testing and Quality Assurance

    Zenthing's testing ecosystem includes comprehensive tools for unit testing, integration testing, and performance testing. ZenPytest provides a powerful testing framework with extensive plugin support, while ZenCoverage offers code coverage analysis. The ecosystem also includes tools for static analysis, linting, and security scanning, enabling developers to maintain high code quality standards.

    ## Community and Learning Resources

    ### Documentation and Tutorials

    The Zenthing community maintains comprehensive documentation covering all aspects of the language and ecosystem. Official tutorials provide step-by-step guidance for common tasks, while community-contributed guides offer specialized knowledge and best practices. The documentation is available in multiple languages and formats, making Zenthing accessible to developers worldwide.

    ### Conferences and Events

    The Zenthing community hosts numerous conferences and events worldwide, providing opportunities for learning, networking, and collaboration. ZenthingCon serves as the primary international conference, while regional events and local meetups provide more intimate settings for knowledge sharing. These events feature talks from both core developers and community members, covering topics from language internals to application development.

    ### Educational Resources

    Zenthing's educational ecosystem includes online courses, interactive tutorials, and structured learning paths. Platforms like ZenAcademy provide comprehensive courses for beginners and advanced users alike, while interactive platforms like ZenPlayground offer hands-on learning experiences. The ecosystem also includes tools for creating educational content, making it easy for educators to develop Zenthing curriculum.

    This comprehensive ecosystem makes Zenthing suitable for virtually any programming task, from simple scripts to complex enterprise applications, while providing the tools and resources needed for successful development and deployment.
    """  # noqa: E501
    return (zenthing_ecosystem_use_cases_text,)


@app.cell(hide_code=True)
def _():
    zenthing_syntax_and_programming_style_text = """
    # Syntax and Programming Style

    Zenthing is often praised for its highly readable and consistent syntax. One of its most distinctive features is the use of significant whitespace to define code blocks. Instead of braces or keywords like `end`, Zenthing relies on indentation levels, which encourages a clean and uniform visual structure in code.

    **Key aspects of Zenthing syntax and style:**

    - **Significant whitespace**: Code blocks are defined by consistent indentation. This eliminates many of the visual clutter points found in other languages and promotes a visually clean structure.

    - **Minimalist keywords**: Zenthing's core language syntax is designed to be as simple as possible. Keywords are few, carefully chosen, and used consistently. This helps reduce the cognitive overhead when reading unfamiliar code.

    - **First-class functions and lambdas**: Functions are first-class citizens, and anonymous functions (lambdas) can be passed as arguments or returned from other functions. Zenthing embraces the functional programming mindset without enforcing it.

    - **Class and object support**: Zenthing supports object-oriented programming with classes, inheritance, and method overriding. It also provides features like mixins and decorators to encourage modular, reusable code.

    - **Pattern matching and comprehensions**: More recent versions of Zenthing have introduced native support for pattern matching and list/dictionary comprehensions, giving developers expressive ways to write transformations and filters.

    - **Zenic style guide**: The community maintains a style guide known informally as the "Zenic Way," which outlines conventions for naming, spacing, file organization, and idiomatic usage. These conventions are widely followed and reinforced by the official formatter, `zentidy`.

    Overall, Zenthing syntax encourages clarity, consistency, and the principle that "code is read more often than it is written."

    ## Core Syntax Elements

    ### Variables and Assignment

    Zenthing's variable assignment system is designed for clarity and flexibility. Variables are created through simple assignment statements, with no need for explicit type declarations. The language supports multiple assignment patterns, including tuple unpacking and extended unpacking with the asterisk operator. Augmented assignment operators provide concise ways to modify variables in place, while maintaining readability. The dynamic typing system allows variables to hold different types of values over their lifetime, though this flexibility should be used judiciously to maintain code clarity.

    ### Control Flow and Decision Making

    Zenthing's control flow statements are designed to be intuitive and readable. Conditional statements use clear if-elif-else structures that mirror natural language reasoning. The language supports both traditional if-else chains and ternary conditional expressions for simple cases. Loop constructs include for loops for iteration over sequences and while loops for conditional iteration. Loop control statements like break and continue provide fine-grained control over loop execution. The range function and enumerate function make it easy to work with numeric sequences and indexed iteration.

    ### Function Definition and Organization

    Functions in Zenthing are defined using the def keyword, with support for various parameter patterns. Positional parameters are the most common, but the language also supports keyword-only parameters, default values, and variable-length argument lists. Type hints can be added to function signatures to improve documentation and enable static analysis tools. Function return values are handled implicitly, with the return statement being optional for simple functions. The language's first-class function support means that functions can be assigned to variables, passed as arguments, and returned from other functions.

    ### Data Structures and Collections

    Zenthing provides several built-in data structures designed for different use cases. Lists are mutable sequences that support indexing, slicing, and various modification operations. Tuples are immutable sequences that provide data integrity and can be used as dictionary keys or set elements. Dictionaries provide key-value mappings with fast lookup times and support for various key types. Sets offer unordered collections of unique elements with mathematical set operations. Each data structure includes comprehensive methods for manipulation and querying, with consistent APIs that promote learning and productivity.

    ## Object-Oriented Programming Features

    ### Class Definition and Structure

    Zenthing's class system provides a clean and powerful way to organize code and data. Classes are defined using the class keyword, with support for inheritance, method overriding, and special methods. The __init__ method serves as the constructor, allowing for object initialization with custom parameters. Class variables and instance variables provide different scopes for data storage, while property decorators enable controlled access to object attributes. The language's multiple inheritance support allows for complex class hierarchies, though it should be used carefully to avoid the "diamond problem."

    ### Inheritance and Polymorphism

    Zenthing's inheritance system supports both single and multiple inheritance, providing flexibility in class design. Method overriding allows subclasses to customize behavior inherited from parent classes, while the super function provides a clean way to call parent class methods. Abstract base classes and interfaces can be implemented using the abc module, enabling polymorphic behavior and design by contract. The language's duck typing philosophy means that objects are judged by their behavior rather than their type, promoting flexible and reusable code.

    ### Special Methods and Operator Overloading

    Zenthing's special methods (also known as magic methods) allow classes to define how they respond to built-in operations. Methods like __str__ and __repr__ control string representation, while __len__, __getitem__, and __setitem__ enable sequence-like behavior. Arithmetic operations can be customized through methods like __add__, __sub__, and __mul__, while comparison operations use methods like __eq__ and __lt__. Context managers are implemented through __enter__ and __exit__ methods, enabling the with statement for resource management.

    ## Functional Programming Features

    ### Higher-Order Functions and Lambda Expressions

    Zenthing's functional programming features provide powerful tools for data transformation and abstraction. Built-in functions like map, filter, and reduce enable functional programming patterns, while lambda expressions provide concise ways to create anonymous functions. The functools module offers additional higher-order functions and utilities for functional programming. List comprehensions and generator expressions provide declarative ways to create and transform sequences, often with better performance than equivalent functional approaches.

    ### Iterators and Generators

    Zenthing's iterator protocol provides a unified way to iterate over different types of collections. Iterators are objects that implement the __iter__ and __next__ methods, enabling lazy evaluation and memory-efficient processing of large datasets. Generators are a special type of iterator created using the yield keyword, allowing for simple creation of iterators without explicit class definition. Generator functions and generator expressions provide different ways to create generators, each suited to different use cases.

    ### Decorators and Metaprogramming

    Decorators provide a clean way to modify or enhance functions and classes without changing their source code. They are implemented using the @ syntax and can be used for cross-cutting concerns like logging, caching, and authentication. Decorators can accept arguments and can be stacked to apply multiple transformations. The language's metaprogramming capabilities also include metaclasses for customizing class creation and descriptors for fine-grained control over attribute access.

    ## Error Handling and Exception Management

    ### Exception Handling Patterns

    Zenthing's exception handling system provides comprehensive error management capabilities. The try-except-finally structure allows for graceful handling of exceptions while ensuring proper cleanup. Multiple except clauses can handle different types of exceptions, while the else clause provides code that runs only when no exceptions occur. The finally clause ensures that cleanup code runs regardless of whether exceptions occur. Exception chaining and context managers provide additional ways to handle complex error scenarios.

    ### Custom Exceptions and Error Design

    Zenthing allows developers to create custom exception classes that inherit from the built-in Exception class. Custom exceptions should provide meaningful error messages and can include additional data to help with debugging and error recovery. Exception hierarchies can be designed to group related errors and provide different levels of error handling. The language's exception system encourages explicit error handling while providing mechanisms for propagating errors when appropriate.

    ## Modern Language Features

    ### Type Hints and Static Analysis

    Zenthing's type hint system provides optional static typing that improves code documentation and enables better tooling support. Type hints can be added to function parameters, return values, and variable assignments, providing information about expected types without affecting runtime behavior. The typing module provides additional type constructs like generics, union types, and optional types. Static analysis tools can use type hints to catch potential type-related errors before runtime.

    ### Pattern Matching and Structural Programming

    Recent versions of Zenthing have introduced structural pattern matching, providing a powerful and readable way to handle complex conditional logic. Pattern matching allows developers to match against data structures based on their shape and content, making code more expressive and less error-prone than traditional if-else chains. The match statement supports various patterns including literal patterns, capture patterns, and structural patterns. Pattern matching can be extended to work with custom classes through special methods.

    ### Asynchronous Programming

    Zenthing's async/await syntax provides built-in support for asynchronous programming, enabling efficient handling of I/O-bound operations. Async functions are defined using the async def syntax and can use await to pause execution while waiting for asynchronous operations to complete. The asyncio module provides the event loop and utilities for managing asynchronous tasks. Asynchronous programming in Zenthing is designed to be approachable while providing the performance benefits of non-blocking I/O.

    ## Style Guidelines and Best Practices

    ### Naming Conventions and Code Organization

    Zenthing's style guide, known as PEP 8, provides comprehensive guidelines for code formatting and organization. Variable and function names use snake_case, while class names use PascalCase. Constants are typically written in UPPER_SNAKE_CASE. The style guide also covers indentation, line length, import organization, and documentation standards. Following these conventions promotes code readability and consistency across projects.

    ### Documentation and Comments

    Zenthing's documentation system is built around docstrings, which are string literals that appear at the beginning of modules, functions, classes, and methods. Docstrings can be accessed at runtime and are used by documentation generators and help systems. The language supports both single-line and multi-line docstrings, with the latter providing space for detailed documentation including parameter descriptions, return values, and usage examples. Comments should be used sparingly and should explain why rather than what.

    ### Code Quality and Testing

    Zenthing's ecosystem includes numerous tools for maintaining code quality. Linters like flake8 and pylint check for style violations and potential errors, while formatters like black and isort automatically format code according to style guidelines. Type checkers like mypy can analyze type hints to catch type-related errors. Testing frameworks like pytest provide comprehensive testing capabilities, while coverage tools measure how much of the code is tested. These tools work together to ensure high-quality, maintainable code.

    ## Performance and Optimization

    ### Profiling and Performance Analysis

    Zenthing provides built-in tools for performance analysis and optimization. The profile and cProfile modules offer function-level profiling, while the timeit module provides precise timing measurements for small code snippets. Memory profiling can be done using tools like memory_profiler, while line-by-line profiling is available through line_profiler. These tools help developers identify performance bottlenecks and optimize critical code sections.

    ### Optimization Techniques

    Zenthing's performance can be optimized through various techniques. List comprehensions and generator expressions often provide better performance than equivalent loops. Built-in functions like map and filter can be more efficient than custom implementations. The functools.lru_cache decorator provides easy memoization for expensive function calls. For performance-critical sections, C extensions can be written using the C API or tools like Cython.

    This comprehensive overview of Zenthing's syntax and programming style demonstrates the language's commitment to readability, expressiveness, and maintainability while providing powerful features for modern software development.
    """  # noqa: E501

    return (zenthing_syntax_and_programming_style_text,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
