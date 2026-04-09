import os
import pandas as pd
from preprocessing import preprocess_stock
from experiment_config import EXPERIMENTS

RAW_PATH = "data/raw"
BASE_OUTPUT = "data/processed"

files = os.listdir(RAW_PATH)

for exp in EXPERIMENTS:
    print(f"\n🚀 Running Experiment: {exp['name']}")

    output_path = os.path.join(BASE_OUTPUT, exp["name"])
    os.makedirs(output_path, exist_ok=True)

    for file in files:
        if file.endswith(".csv"):
            print(f"Processing {file}...")

            df = pd.read_csv(os.path.join(RAW_PATH, file))
            # This now correctly calls the function from preprocessing.py
            df = preprocess_stock(df, exp)

            save_path = os.path.join(output_path, file)
            df.to_csv(save_path, index=False)

print("\n🎉 All experiments completed!")