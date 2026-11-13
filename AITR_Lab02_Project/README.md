# Absolute Parametric Override: Temporal Friction in RAG

This repository contains the code, data splits, and experimental framework for the paper **"Absolute Parametric Override: A Comprehensive Review and Empirical Study of Temporal Friction in RAG"** (ACM CSUR 2026).

## Problem Statement
Retrieval-Augmented Generation (RAG) is the industry standard for mitigating Large Language Model (LLM) knowledge staleness. However, existing evaluations fail to isolate the model's parametric knowledge cutoff as an independent variable. This repository tests "temporal friction"—the cognitive conflict between outdated internal parametric memory and newly retrieved post-cutoff scientific evidence.

## Setup & Environment
The codebase was developed and executed in Python 3.11.
To replicate the environment, install the verified dependencies:
```bash
pip install -r requirements.txt
```

## Dataset Access & Preparation
The dataset comprises 300 real scientific abstracts harvested from the arXiv API (query: "large language models OR retrieval").
*   **Path:** `data/stratified_arxiv_dataset_4.csv` (Included in this repository as an audited, non-restricted data split).
*   **Stratification:**
    *   `Pre-Cutoff`: Published before July 2023.
    *   `Near-Cutoff`: Published July 2023 - Jan 2024.
    *   `Post-Cutoff`: Published after Jan 2024.
*   *Note on Raw Data:* For access to the raw arXiv JSON dumps, please refer to the `data/README.md`.

## Configuration
The `configs/` directory contains the frozen experimental settings used to generate the paper's results:
*   `base_config.yaml`: Defines the models (gemini-3.5-flash-lite, gemini-1.0-pro), dataset path, batch size (10), and random seed (42).
*   `forcing_config.yaml`: Contains the exact adversarial prompt prefix used for Baseline 3 (Parametric Priming).
*   `judge_config.yaml`: Outlines the LLM-as-a-Judge rubric (Omission Score and Stale Framing definitions).

## Running the Experiments (Baselines 1, 2, and 3)
All execution commands are routed through the `scripts/` directory. You will need a valid Google Gemini API key set as an environment variable (`GEMINI_API_KEY`).

**Baseline 1: Naive RAG (gemini-3.5-flash-lite)**
```bash
python scripts/01_run_baseline.py
```
**Baseline 2: Legacy Control (gemini-1.0-pro)**
```bash
python scripts/03_run_baseline_2.py
```
**Baseline 3: Parametric Priming / Temporal Forcing**
```bash
python scripts/05_run_temporal_forcing.py
```

## Evaluation & Figure Reproduction
To reproduce the statistical analysis and the high-resolution figures used in the paper:

**1. Generate Comparative Decay Statistics & Plots:**
```bash
python scripts/06_compare_forcing.py
```
**2. Run the Final Rigorous Evaluation Audit (Missing values, leakage, Mann-Whitney U, Chi-Square):**
```bash
python scripts/07_evaluation_audit.py
```

## Compute Requirements
*   **Hardware:** Standard CPU instances are sufficient for evaluation and data processing.
*   **API Usage:** Running the full 300-paper dataset across all three baselines requires approximately 900 API calls (excluding retries).

## Limitations
*   **Domain Specificity:** The dataset is restricted to Computer Science/AI. Results may not perfectly generalize to domains like medical law.
*   **API Rate Limits:** Ensure your API key supports a minimum of 15 Requests Per Minute (RPM) to avoid extended backoff delays.

## Citation
If you use this dataset or codebase, please cite our ACM CSUR paper:
```bibtex
@article{patel2026absolute,
  title={Absolute Parametric Override: A Comprehensive Review and Empirical Study of Temporal Friction in RAG},
  author={Patel, Mihir Rajeshkumar},
  journal={ACM Computing Surveys (CSUR)},
  year={2026}
}
```

## License and Credits
*   **Code License:** MIT License.
*   **Data License:** arXiv abstracts are subject to the arXiv non-exclusive distribution license. 
*   **Credits:** Developed at the Indian Institute of Information Technology (IIIT), Prayagraj.

---
### Minimum Reproduction Checklist for Students
- [ ] 1. Clone the repository and `pip install -r requirements.txt`.
- [ ] 2. Obtain a Gemini API Key and `export GEMINI_API_KEY="your_key"`.
- [ ] 3. Ensure `stratified_arxiv_dataset_4.csv` is in the `data/` directory.
- [ ] 4. Run `python scripts/01_run_baseline.py`.
- [ ] 5. Run `python scripts/07_evaluation_audit.py` to confirm the generated `results.csv` aligns with the paper's findings.
