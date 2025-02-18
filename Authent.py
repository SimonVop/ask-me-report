import requests

model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token ="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"

def huggingface_api():
    api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"#
    headers = {"Authorization": f"Bearer {hf_token}"}
    return api_url, headers