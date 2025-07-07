# Building with LLMs: References

## Multi-Agent Systems

- [How we built our multi-agent research system](https://www.anthropic.com/engineering/built-multi-agent-research-system) - Anthropic's detailed exploration of their multi-agent research system implementation, covering architecture, challenges, and practical applications.
- [Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents) - A critical analysis of multi-agent architectures, arguing that they lead to fragile systems due to context sharing challenges and conflicting decision-making, with principles for building more reliable single-threaded agents.
- [Stop Building AI Agents](https://decodingml.substack.com/p/stop-building-ai-agents) - Hugo Bowne-Anderson's practical guide arguing that agents are overhyped and overused, with five alternative workflow patterns (prompt chaining, parallelization, routing, orchestrator-worker, evaluator-optimizer) that solve most problems more effectively than complex agent systems.

## RAG (Retrieval Augmented Generation)

- [How to Improve RAG Applications: 6 Proven Strategies](https://jxnl.co/writing/2024/11/04/how-to-improve-rag-applications-6-proven-strategies/) - A practical guide covering six key strategies for improving RAG systems, from synthetic testing to query routing and user feedback collection.
- [Jason Liu's RAG Articles Collection](https://jxnl.co/writing/category/rag/) - A comprehensive collection of articles covering RAG fundamentals, implementation strategies, evaluation methods, and future predictions.

## Evaluation Methods

- [LLM Eval FAQ](https://hamel.dev/blog/posts/evals-faq/) - A comprehensive guide to evaluating LLM applications, covering best practices for RAG evaluation, model selection, annotation tools, and synthetic data generation.
- [There Are Only 6 RAG Evals](https://jxnl.co/writing/2025/05/19/there-are-only-6-rag-evals/) - A systematic framework for evaluating RAG systems based on six core relationships between questions, context, and answers.
- [Evaluating Long-Context Question & Answer Systems](https://eugeneyan.com/writing/qa-evals/) - A comprehensive guide to evaluating Q&A systems with long documents, covering faithfulness vs helpfulness metrics, dataset construction, evaluation methods, and benchmarks for narrative, technical, and multi-document scenarios.
- [Jacky Liang on Twitter](https://x.com/jjackyliang/status/1932817119189643699) - A concise thread discussing practical approaches to LLM evaluation, focusing on real-world testing strategies and common pitfalls in evaluation design.

## Production Best Practices

- [A Field Guide to Rapidly Improving AI Products](https://hamel.dev/blog/posts/field-guide/) - A comprehensive guide covering error analysis, data viewers, domain expert collaboration, synthetic data, evaluation trust, and experiment-based roadmaps.

## Security and Safety

- [An Introduction to Google's Approach for Secure AI Agents](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/) - Google's framework for secure AI agents, emphasizing a hybrid defense-in-depth strategy combining traditional security controls with dynamic reasoning-based defenses.
- [Design Patterns for Securing LLM Agents against Prompt Injections](https://arxiv.org/html/2506.08837v2) - A comprehensive study of design patterns and best practices for building AI agents with provable resistance to prompt injection attacks.
- [The Lethal Trifecta for AI Agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) - A critical analysis of the three dangerous capabilities that can lead to data exfiltration in AI agents: private data access, untrusted content exposure, and external communication.

## AI Capabilities and Limitations

- [The Illusion of Self-Improvement: Why AI Can't Think Its Way to Genius](https://medium.com/@vishalmisra/the-illusion-of-self-improvement-why-ai-cant-think-its-way-to-genius-a355ef3e9fd5) - An insightful analysis of the fundamental limitations of AI systems in achieving true self-improvement and the misconceptions about AI's ability to think its way to superintelligence.

## Framework and Architecture

- [The Hidden Simplicity of GenAI Systems](https://docs.google.com/presentation/d/1qUh3snfpXj0CAf8dOlPnc8lM-z4uautEP7pqYAIIlNM/edit?usp=sharing) - A slide deck from a Maven Lightning Lesson hosted by Hugo Bowne-Anderson and John Berryman, providing a great framework for thinking about LLM applications.

## Embeddings and Vector Spaces

- [Harnessing the Universal Geometry of Embeddings](https://arxiv.org/html/2505.12540v2) - A groundbreaking study demonstrating how to translate text embeddings between different vector spaces without paired data, with important implications for vector database security and information extraction.

## Document Processing and Multimodal Models

- [SmolDocling-256M-preview](https://huggingface.co/ds4sd/SmolDocling-256M-preview) - An ultra-compact vision-language model for end-to-end document conversion, featuring OCR, layout preservation, code recognition, and support for various document elements like tables, charts, and formulas.

## Video Resources

- [Error Analysis: The Highest ROI Technique In AI Engineering](https://www.youtube.com/watch?v=e2i6JbU2R-s) - Hamel Husain's guide to conducting error analysis for AI applications, demonstrating foundational evaluation techniques for improving LLM systems.
- [Andrej Karpathy: Software Is Changing (Again)](https://www.youtube.com/watch?v=LCEmiRjPEtQ) - Andrej Karpathy's keynote exploring the evolution of software into the 'Software 3.0' era where natural language becomes the new programming interface and LLMs act as utilities, fabs, and operating systems.
- [12-Factor Agents: Patterns of reliable LLM applications](https://www.youtube.com/watch?v=8kMaTybvDUw) - Dex Horthy's presentation on 12 core engineering principles for building reliable LLM-powered applications by applying classic software engineering discipline to AI agents.

## LLM Tools and Automation

- [Tools: Code Is All You Need](https://lucumr.pocoo.org/2025/7/3/tools/) - Armin Ronacher's 2025 blog post critically examines the Model Context Protocol (MCP) and MCP servers, highlighting their limitations in composability and context requirements. The post argues that code-centric automation is often more efficient, reliable, and verifiable than relying on MCPs, and provides practical insights into why code generation remains preferable for most automation and agentic coding tasks.

## Tools, Libraries & Automation

- [Minish Lab](https://minishlab.github.io/) - An open-source company focused on ultra-fast NLP tools and models, including Model2Vec and Potion. Potion is a small, extremely fast embedding model, and is used as the default fast embedder in llamabot for efficient text processing and retrieval.

## Talks & Conference Sessions

- [Escaping Proof-of-Concept Purgatory: Building Robust LLM-Powered Applications (SciPy 2025)](https://cfp.scipy.org/scipy2025/talk/GJRGVU/) - This talk introduces the LLM software development lifecycle (SDLC) and provides a structured framework for moving LLM projects beyond early-stage demos. It covers best practices for integrating LLMs into scientific Python workflows, handling non-determinism, structured output extraction, and strategies for building reliable, production-ready AI systems.
