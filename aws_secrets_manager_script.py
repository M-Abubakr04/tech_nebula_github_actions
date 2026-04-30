import boto3
import json

region_name = "ap-south-1"
secret_name = "my-app-secrets"

secret_data = {
    "DB_URL": "mongodb://localhost:27017",
    "JWT_SECRET": "mysecretkey",
    "PORT": "3000",
    "NODE_ENV": "production"
}

print("Preparing Secret Data:", secret_data)

client = boto3.client("secretsmanager", region_name=region_name)

secret_string = json.dumps(secret_data)

try:
    response = client.create_secret(
        Name=secret_name,
        SecretString=secret_string
    )
    print("Secret Created Successfully")

except client.exceptions.ResourceExistsException:
    response = client.update_secret(
        SecretId=secret_name,
        SecretString=secret_string
    )
    print("Secret Updated Successfully")

print("FINAL RESPONSE:", response)