print("GitHub Secrets Automation Script Started...")

import os
import requests
import base64
from nacl import encoding, public

# Here we are configuring our environment
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    print("ERROR: GITHUB_TOKEN not found. Export it first.")
    exit()

OWNER = "M-Abubakr04"
REPO = "tech_nebula_github_actions"

ENV_NAME = input("Enter Environment (production/staging): ").strip()

# Header Section
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Looking for Public Key
url = f"https://api.github.com/repos/{OWNER}/{REPO}/environments/{ENV_NAME}/secrets/public-key"

res = requests.get(url, headers=headers)

if res.status_code != 200:
    print("Error fetching public key:", res.text)
    exit()

data = res.json()

public_key = data["key"]
key_id = data["key_id"]

print("Public key fetched successfully")

# Applying Encryption
def encrypt_secret(public_key, secret_value):
    public_key = public.PublicKey(public_key.encode(), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode())
    return base64.b64encode(encrypted).decode()

# Reading Varibales form .env file present in our local machine or ec2
env_vars = {}

with open(".env") as f:
    for line in f:
        if "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            env_vars[k] = v

print("Loaded variables:", list(env_vars.keys()))

# We are Pushing Secrets Now
for key, value in env_vars.items():

    encrypted_value = encrypt_secret(public_key, value)

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/environments/{ENV_NAME}/secrets/{key}"

    data = {
        "encrypted_value": encrypted_value,
        "key_id": key_id
    }

    r = requests.put(url, headers=headers, json=data)

    if r.status_code in [201, 204]:
        print(f"{key} uploaded successfully")
    else:
        print(f"Error for {key}: {r.text}")

print("All secrets uploaded successfully.")
