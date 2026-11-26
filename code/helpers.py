# Drafted with Claude Code (Anthropic) from Francesco Cordone's pipeline; reviewed, run and edited by Francesco Cordone
from pathlib import Path

import matplotlib.pyplot as plt

# Paths are built from the repository root, so the code behaves the same
# when it is run from the root folder, from code/ or from a notebook.
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
INTERIM = ROOT / "data" / "interim"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "figures"

# Git does not track empty folders, so a fresh clone needs them created.
for folder in [RAW, INTERIM, PROCESSED, FIGURES]:
    folder.mkdir(parents=True, exist_ok=True)

SEED = 42

# The models are built on loans issued in these years only. Every later
# quarter is the monitoring period and is never used to fit them.
DEV_YEARS = [2009, 2010, 2011]

# The same feature lists are used by every stage, so that the models, the
# stability checks and the drift analysis always look at the same columns.
NUMERIC_FEATURES = [
    "loan_amnt", "log_annual_inc", "dti", "fico", "emp_length_years",
    "log_revol_bal", "revol_util", "open_acc", "total_acc",
    "delinq_2yrs", "inq_last_6mths", "pub_rec", "credit_history_years",
]
CATEGORICAL_FEATURES = ["home_ownership", "purpose", "verification_status"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

# One colour per model, the same in every figure.
MODEL_COLORS = {"pd_logit": "#2a78d6", "pd_xgb": "#eb6834", "pd_grade": "#1baf7a"}
INK, INK_SOFT, INK_MUTED = "#0b0b0b", "#52514e", "#898781"


def set_plot_style():
    # Quiet axes and grid, so that the data is the only loud thing.
    plt.rcParams.update({
        "figure.dpi": 100, "savefig.dpi": 200, "savefig.bbox": "tight",
        "figure.facecolor": "white", "axes.facecolor": "white",
        "font.size": 10, "text.color": INK,
        "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.labelcolor": INK_SOFT, "axes.edgecolor": "#c3c2b7",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "axes.axisbelow": True,
        "grid.color": "#e1e0d9", "grid.linewidth": 0.8,
        "xtick.color": INK_MUTED, "ytick.color": INK_MUTED,
        "xtick.labelcolor": INK_SOFT, "ytick.labelcolor": INK_SOFT,
        "lines.linewidth": 2, "lines.markersize": 5,
        "legend.frameon": False,
    })


def label_quarters(ax, quarters, offset=0.0):
    # Sixteen quarter labels are too many: the year is written once, under
    # its first quarter. `offset` is 0.5 when the cells of a heatmap are
    # drawn between integer positions.
    positions = [i + offset for i in range(len(quarters))]
    labels = [quarter[:4] if quarter.endswith("Q1") else "" for quarter in quarters]
    ax.set_xticks(positions, labels)
