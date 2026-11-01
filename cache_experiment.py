from huggingface_hub import hf_hub_download

config_path = hf_hub_download(
    repo_id="sentence-transformers/all-MiniLM-L6-v2",
    filename="config.json",
)

print("Configuration downloaded or retrieved from cache:")
print(config_path)
