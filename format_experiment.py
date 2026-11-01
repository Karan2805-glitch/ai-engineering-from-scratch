from datasets import load_dataset
from pathlib import Path

# Load a small subset to keep this experiment lightweight
dataset = load_dataset(
    "stanfordnlp/imdb",
    split="train[:1000]",
)

output_dir = Path("data_format_demo")
output_dir.mkdir(exist_ok=True)

# Convert to three file formats
csv_path = output_dir / "imdb.csv"
json_path = output_dir / "imdb.json"
parquet_path = output_dir / "imdb.parquet"

dataset.to_csv(str(csv_path))
dataset.to_json(str(json_path))
dataset.to_parquet(str(parquet_path))

# Compare file sizes
print(f"Rows converted: {len(dataset):,}\n")

for path in [csv_path, json_path, parquet_path]:
    size_kb = path.stat().st_size / 1024
    print(f"{path.name}: {size_kb:.2f} KB")

# Load Parquet back and verify row count
reloaded = load_dataset(
    "parquet",
    data_files=str(parquet_path),
    split="train",
)

print(f"\nRows after Parquet reload: {len(reloaded):,}")
print("First row preserved:", reloaded[0] == dataset[0])
