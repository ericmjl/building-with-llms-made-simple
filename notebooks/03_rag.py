# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "llamabot[all]==0.12.1",
#     "marimo",
#     "pyprojroot==0.3.0",
#     "rich==13.9.4",
#     "lancedb",
#     "sentence-transformers",
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
        It was created by Guido van Rossum and first released in 1991.
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

    response2 = rag_bot("What are its key features?")
    print("\nResponse 2:", response2.content)

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
           - The system searches the knowledge base for relevant documents
           - It uses semantic similarity to find the most relevant content
           - The retrieved documents are used to augment the prompt

        2. **Memory Integration**:
           - Previous conversations are stored in the memory store
           - Relevant past interactions are retrieved based on the current query
           - This provides context for multi-turn conversations

        3. **Response Generation**:
           - The LLM generates a response using both the retrieved documents and memory
           - The response is then stored in memory for future reference
        """  # noqa: E501
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
        r"""
        ## 3.6 Best Practices for RAG Systems

        When building RAG systems, consider these best practices:

        1. **Document Chunking**:
           - Split documents into appropriate-sized chunks
           - Consider semantic boundaries when chunking
           - Balance chunk size with retrieval quality

        2. **Memory Management**:
           - Implement memory pruning to prevent context overflow
           - Consider relevance thresholds for memory retrieval
           - Balance recent vs. relevant memory

        3. **Prompt Engineering**:
           - Clearly instruct the model on how to use retrieved documents
           - Specify how to handle conflicting information
           - Guide the model in combining multiple sources
        """  # noqa: E501
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
        """  # noqa: E501
    )
    return


if __name__ == "__main__":
    app.run()
