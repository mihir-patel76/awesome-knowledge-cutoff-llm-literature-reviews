# Tools & Systems

Literature review generation tools, agentic pipelines, and mitigation techniques discussed in the paper.

## LitLLM
- **Authors:** Agarwal, Laradji, Charlin, & Pal (2024); extended by Agarwal et al. (2025)
- **What it does:** A toolkit combining retrieval-augmented generation with LLM-based reranking to produce related-work sections from a query abstract. The 2025 follow-up decomposes the task into retrieval + plan-then-write generation and introduces a hybrid keyword/embedding search strategy (improving precision by ~10% and recall by ~30% over either method alone).

## ChatCite
- **Authors:** Li, Chen, Liu, Yu, & Wen (2024)
- **What it does:** A human-workflow-inspired LLM agent for comparative literature summarization. Uses a "Key Element Extractor" and a "Reflective Incremental Generator" to separate information extraction from comparative synthesis, reducing compounding of retrieval and generation errors.

## OpenScholar
- **Authors:** Asai, He, Shao, Shi, Singh, Chang, Lo, Soldaini, Feldman, D'Arcy, et al. (2024)
- **What it does:** Synthesizes scientific literature by grounding a retrieval-augmented language model in a large open scientific corpus rather than relying on parametric knowledge alone, providing a natural point for provenance/currency auditing.

## Wu et al. (2025) Domain-Specific Pipeline
- **What it does:** An end-to-end review-generation pipeline for a chemistry subfield (propane dehydrogenation catalysis) with multilayered quality control, including automated verification and expert review — achieving under 0.5% citation hallucination at 95% confidence.

## Retrieval-Augmented Generation (RAG) — general
- **Origin:** Lewis et al. (2020); surveyed by Gao et al. (2024) and Brown et al. (2025)
- **What it does:** Grounds a generative model in documents retrieved from an external, updatable corpus at inference time instead of relying solely on parametric memory. Framed in the paper as the dominant mitigation strategy for both hallucination and outdated internal knowledge, though it only partially decouples review currency from indexing lag.

## Prompted Knowledge-Cutoff Simulation
- **Studied by:** Gao et al. (2025)
- **What it does:** A prompting technique asking a model to reason as though situated at an earlier date. Effective when the model is queried directly about post-cutoff facts, but fails to suppress leakage of causally related downstream knowledge — making it an unreliable control for scoping or evaluation.

## Related mitigation concepts mentioned (not standalone tools)
- **Plan-then-write generation** — first outlining review structure, then executing retrieval and writing against that plan (Agarwal et al., 2025).
- **Provenance-tagging (proposed future direction)** — tagging each claim/citation as retrieved-and-verified, retrieved-but-unverified, or parametric recall.
- **Knowledge editing** — surveyed by Yao et al. (2023) and Wang et al. (2024) as a related but distinct technique for updating model knowledge post-training.
