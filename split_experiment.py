from datasets import load_dataset

# Load the IMDB training split
dataset = load_dataset(
    "stanfordnlp/imdb",
    split="train",
)

# First, reserve 30% for validation and testing
first_split = dataset.train_test_split(
    test_size=0.30,
    seed=42,
)

train_ds = first_split["train"]
remaining_ds = first_split["test"]

# Divide the remaining 30% equally
second_split = remaining_ds.train_test_split(
    test_size=0.50,
    seed=42,
)

val_ds = second_split["train"]
test_ds = second_split["test"]

print("Dataset sizes:")
print(f"Train: {len(train_ds):,} ({len(train_ds) / len(dataset):.0%})")
print(f"Validation: {len(val_ds):,} ({len(val_ds) / len(dataset):.0%})")
print(f"Test: {len(test_ds):,} ({len(test_ds) / len(dataset):.0%})")

print("\nTotal rows:", len(train_ds) + len(val_ds) + len(test_ds))
print("Original rows:", len(dataset))

print("\nFirst training label:", train_ds[0]["label"])
print("First validation label:", val_ds[0]["label"])
print("First test label:", test_ds[0]["label"])

# Repeat the same splitting procedure
repeat_split = dataset.train_test_split(
    test_size=0.30,
    seed=42,
)

repeat_remaining = repeat_split["test"].train_test_split(
    test_size=0.50,
    seed=42,
)

# Verify that the first examples match
print("\nReproducibility checks:")
print(
    "Train matches:",
    train_ds[0]["text"] == repeat_split["train"][0]["text"],
)
print(
    "Validation matches:",
    val_ds[0]["text"] == repeat_remaining["train"][0]["text"],
)
print(
    "Test matches:",
    test_ds[0]["text"] == repeat_remaining["test"][0]["text"],
)