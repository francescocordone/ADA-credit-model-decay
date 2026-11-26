# How long does a credit scoring model stay reliable?

Individual project for the course Advanced Data Analytics, by Francesco Cordone.

A bank builds a default model on past borrowers and then uses it for years. This project
replicates that situation on Lending Club data: a logistic regression and an XGBoost model
are trained on 36-month loans issued in 2009-2011, frozen, and tested on every quarter from
2012Q1 to 2015Q4, to measure when their performance starts to drop and why.

This repository is published in stages. This first stage contains the setup, the data
download and the cleaning of the loans; the models and the analysis follow (see Roadmap).

## Installation

Python 3.11 or later.

```
python -m venv .venv
.venv\Scripts\activate          (Windows)
source .venv/bin/activate       (Linux, macOS, Nuvolos)
pip install -r requirements.txt
```

## How to reproduce

Run the stages in this order from the repository root. Each stage loads what the previous
one saved and saves what the next one needs.

```
python code/01_get_data.py
jupyter nbconvert --to notebook --execute --inplace code/02_clean.ipynb
```

The notebook can also be opened in Jupyter and run with Restart & Run All.

| Stage | File | What it does | Main output | Time |
| --- | --- | --- | --- | --- |
| 1 | `code/01_get_data.py` | Downloads the raw file and keeps the 36-month loans issued 2009-2015 | `data/interim/lc_36m_2009_2015.parquet` | 3-10 min (download) |
| 2 | `code/02_clean.ipynb` | Target, cohort, features, occupation groups, sample | `data/processed/loans_clean.parquet` | under 1 min |

`code/helpers.py` holds the paths, the feature lists and the plotting style shared by the
stages; the functions of the later stages are added together with them. Every figure and
result table is written to `figures/` by the code; nothing in that folder is edited by hand.
The seed is 42 everywhere.

## Data

Source: Kaggle dataset [wordsforthewise/lending-club](https://www.kaggle.com/datasets/wordsforthewise/lending-club),
file `accepted_2007_to_2018Q4.csv.gz` (393 MB). Licence: CC0 Public Domain.
Downloaded on 16 November 2026.

The raw file is not stored in this repository: `code/01_get_data.py` downloads it into
`data/raw/`. No Kaggle account or API key is needed. If the download link stops working,
download the file by hand from the Kaggle page and place it in `data/raw/`.

The project works on a sample: all the 28,538 loans issued in 2009-2011 and at most 12,000
loans per quarter from 2012, 211,505 loans in total.

## Compute

Developed and run on a laptop: Intel Core i5-1135G7 (4 cores), 8 GB of RAM, Windows 11,
Python 3.14.3, no GPU. After the download, the cleaning stage runs in under a minute. A fresh
clone of the project, run in this order, reproduced every result table exactly.

## Roadmap

- **Models and monitoring:** `code/03_models.ipynb` trains the logistic regression and
  XGBoost on 2009-2011, with the Lending Club grade as a benchmark;
  `code/04_monitoring.ipynb` tests the three models on every quarter from 2012Q1 to 2015Q4
  for discrimination (Gini), calibration and stability (PSI), with traffic lights.
- **Why the models degrade:** `code/05_drift.ipynb` separates a different population, a
  changed relationship and a shifted level, and looks at occupations and at a PCA of the
  features; `code/06_extensions.ipynb` adds a Gaussian process trend of the quarterly results
  and borrower clusters. The step-by-step pipeline of the project, `PIPELINE.md`, and the
  final README come with this stage.

## Use of AI

The idea and the research question, the setup of the analysis and the pipeline are the
author's own work. The author wrote the pipeline as a step-by-step plan, a kind of
pseudo-code that sets the data rules, the models, the tests and the thresholds of every
stage. Claude Code (Anthropic) helped the author write the code from that plan and was used
for debugging. Every code file states this in its first line. The full declaration of AI use
is in the paper.
