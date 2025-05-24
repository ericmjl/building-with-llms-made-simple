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

__generated_with = "0.13.11"
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
    # Sample documents about Python programming
    python_docs = [
        """
        Python is a high-level, interpreted programming language known for its simplicity and readability.
        It was created by Guido van Rossum and first released in 1991.
        """,
        """
        Python's key features include:
        - Dynamic typing
        - Automatic memory management
        - Extensive standard library
        - Support for multiple programming paradigms
        """,
        """
        Python is widely used in:
        - Web development (Django, Flask)
        - Data science (NumPy, Pandas)
        - Machine learning (TensorFlow, PyTorch)
        - Automation and scripting
        """,
        """
        Python's syntax emphasizes code readability with its use of significant whitespace.
        It supports multiple programming paradigms, including procedural, object-oriented, and functional programming.
        """,
    ]

    # Add documents to knowledge store
    knowledge_store.extend(python_docs)  # Using extend for bulk addition

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
    rag_bot = lmb.QueryBot(
        system_prompt="""You are a helpful Python programming assistant.
        Use the provided documents to answer questions accurately.
        If you're not sure about something, say so.
        Keep your responses concise and focused on the question asked.""",
        docstore=knowledge_store,
        memory=memory_store,
        model_name="ollama_chat/llama3.2",
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
        """  # noqa: E501
    )
    return


@app.cell
def _(print, rag_bot):
    # Example questions to test the bot
    response1 = rag_bot("What is Python?")
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
        """  # noqa: E501
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


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3.7 Summary & Conclusion

        In this notebook, we've learned:

        - How to implement RAG using QueryBot
        - How to add memory capabilities to maintain conversation context
        - Best practices for building effective RAG systems
        - How to customize and optimize the system for different use cases

        Key takeaways:

        - RAG combines the power of LLMs with external knowledge
        - Memory adds context and coherence to conversations
        - Proper document management is crucial for effective RAG
        - System design choices significantly impact performance
        """  # noqa: E501
    )
    return


if __name__ == "__main__":
    app.run()
