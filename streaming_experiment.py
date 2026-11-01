from datasets import load_dataset

dataset = load_dataset(
    "stanfordnlp/imdb",
    split="train",
    streaming=True,
)

print("First 5 reviews using streaming:\n")

for i, example in enumerate(dataset):
    print(f"Review {i + 1}")
    print("Label:", example["label"])
    print("Review:", example["text"][:120], "...")
    print()

    if i >= 4:
        break
