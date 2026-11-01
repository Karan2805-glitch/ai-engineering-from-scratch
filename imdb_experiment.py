from datasets import load_dataset

dataset = load_dataset("stanfordnlp/imdb")

print("Available splits:", list(dataset.keys()))

for split_name, split_data in dataset.items():
    print(f"{split_name}: {len(split_data):,} examples")

print("\nFirst 3 training examples:")
for i in range(3):
    example = dataset["train"][i]
    print(f"\nReview {i + 1}")
    print("Label:", example["label"])
    print("Review:", example["text"][:150], "...")