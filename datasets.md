# Datasets & Benchmarks

The paper is a review/synthesis piece and does not use a dataset directly, but it discusses the following datasets and evaluation benchmarks used by the underlying literature review generation and retrieval systems it surveys.

## LitSearch
- **Source:** Ajith, Xia, Chevalier, Goyal, Chen, & Gao (2024)
- **Purpose:** A dedicated benchmark for scientific literature *retrieval* — an upstream capability that review-generation quality depends on.
- **Reference:** arXiv:2407.18940

## SciReviewGen
- **Source:** Kasanishi, Isonuma, Mori, & Sakata (2023)
- **Purpose:** A large-scale dataset for automatic literature review generation.
- **Reference:** arXiv:2305.15186

## Rolling arXiv Evaluation Protocol
- **Source:** Agarwal et al. (2025)
- **Purpose:** A contamination-resistant evaluation protocol that constructs test sets from recent arXiv papers on a recurring basis, specifically designed to remain valid for newly released LLMs (i.e., papers unlikely to have been seen in training). Used to evaluate retrieval precision/recall and hallucination in review generation.
- **Reference:** arXiv:2412.15249

## Wu et al. (2025) Domain-Specific Evaluation Set
- **Source:** Wu et al. (2025)
- **Purpose:** An expert-verified evaluation corpus of 343 source articles across 35 topics in the chemistry subfield of propane dehydrogenation catalysis, used to measure citation-integrity hallucination rates (<0.5% at 95% confidence) in an end-to-end review-generation pipeline.
- **Reference:** https://doi.org/10.1093/nsr/nwaf169

## Scherbakov et al. (2025) Systematic Review Corpus
- **Source:** Scherbakov et al. (2025)
- **Purpose:** A corpus of 172 eligible studies on LLM use in review automation, systematically reviewed (itself LLM-assisted) to assess hallucination rates across review stages (search, screening, extraction, citation generation).
- **Reference:** https://doi.org/10.1093/jamia/ocaf063

## Brown et al. (2025) RAG Study Corpus
- **Source:** Brown, Roman, & Devereux (2025)
- **Purpose:** A systematic review corpus of 128 highly cited RAG studies published between 2020 and mid-2025, used to characterize RAG as the standard architectural response to knowledge staleness.
- **Reference:** arXiv:2508.06401

---
**Note:** No raw dataset files, download links, or dataset cards are provided in the source paper itself — the entries above are the datasets/benchmarks it *references* as used by other works, not data included with this paper.
