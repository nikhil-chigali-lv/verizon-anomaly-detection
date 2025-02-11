import os
import sys
from pathlib import Path

# Path to the root directory of the project
ROOT_DIR = Path(__file__).parent.resolve()

# Path to the directory containing the data
DATA_DIR = ROOT_DIR / "data"

# Path to the directory containing the models
MODEL_DIR = ROOT_DIR / "models"

# Path to the features engineering directory
FEATURES_DIR = ROOT_DIR / "features_engineering"

# Path to the modeling directory
MODELING_DIR = ROOT_DIR / "modeling"

# Path to the directory containing the logs
LOG_DIR = ROOT_DIR / "logs"
