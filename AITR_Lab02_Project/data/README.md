# Dataset Documentation

The file `stratified_arxiv_dataset_4.csv` is included directly in this repository. 
It contains 300 processed and binned scientific abstracts, making it fully ready for the evaluation scripts. 

The dataset is sanitized; it does not contain private data, restricted model weights, or API secrets.

Data Columns:
* `paper_id`: arXiv identifier.
* `published_date`: Original publication date.
* `title`: Paper title.
* `abstract`: The raw abstract text.
* `temporal_window`: The assigned stratification bin (Pre-Cutoff, Near-Cutoff, Post-Cutoff).
