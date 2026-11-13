# Research Decisions & AI Assistance Log

This document tracks the step-by-step progress, prompt history, and critical research decisions made during the formulation and execution of the "Absolute Parametric Override" study.

## Phase 1: Conceptualization & Gap Analysis
*   **Initial Prompt:** Asked for a gap matrix on current RAG evaluations.
*   **Decision:** We discovered that existing RAG evaluations fail to isolate the LLM's parametric knowledge cutoff as an independent variable. We decided to focus entirely on "Temporal Friction."

## Phase 2: Experimental Design & Data Sourcing
*   **Dataset:** Decided to use the arXiv API to source real scientific abstracts rather than synthetic datasets to ensure external validity.
*   **Stratification:** Chose October 2023 as the focal cutoff boundary, splitting 300 papers into Pre-Cutoff (before July 2023), Near-Cutoff, and Post-Cutoff (after Jan 2024).

## Phase 3: Baseline Construction & Testing
*   **Baseline 1 (Naive RAG):** Evaluated `gemini-3.5-flash-lite` on the dataset.
*   **Baseline 2 (Legacy Control):** We actively chose to benchmark against `gemini-1.0-pro` to act as a control for parametric ignorance.
*   **Error Handling:** Implemented exponential backoff for HTTP 503 errors during batch processing to prevent dropped data and maintain statistical power.

## Phase 4: Targeted Intervention (Baseline 3)
*   **Decision Pivot:** After observing a "null result" (no decay) in Baseline 1, we designed Baseline 3 (Parametric Priming/Temporal Forcing).
*   **Implementation:** We altered the prompt to explicitly force the model to state historical consensus *before* reading the new abstracts, attempting to artificially induce temporal friction.

## Phase 5: Rigorous Evaluation & Auditing
*   **Statistical Tests:** Decided on non-parametric tests (Kruskal-Wallis for Omission Score, Chi-Square for Stale Framing) because the data distributions were not guaranteed to be normal.
*   **Data Leakage Audit:** Implemented `07_evaluation_audit.py` to strictly check for partition alignment, metric boundaries, and missing values before finalizing the $p$-values.

## Phase 6: Manuscript Drafting & Peer Review
*   **Formatting:** Adopted the strict ACM Computing Surveys (CSUR) format.
*   **Peer Review Simulation:** Conducted a harsh self-review, leading to the inclusion of a "Research Gaps" section outlining the limitations regarding architectural dependencies and context window stress.
