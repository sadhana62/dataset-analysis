import os
import sys
import csv
import requests

# Constants
API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
MODEL = "gpt-4o-mini"

AIPROXY_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjMwMDE5MTRAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.p3jkyCMHiXBJOf4STJgNHFdEscZ-yKqvd9CIGyfZFNc'


# Function to validate the environment
def validate_environment():
    if "AIPROXY_TOKEN" not in os.environ:
        print("Error: AIPROXY_TOKEN environment variable is not set.")
        sys.exit(1)

# Function to read the CSV file
def read_csv(file_path):
    try:
        with open(file_path, "r", encoding="ISO-8859-1") as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Read the header row
            rows = list(reader)  # Read the remaining rows
        return headers, rows
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Could not read the CSV file. Details: {e}")
        sys.exit(1)

# Function to query GPT-4o-Mini via AI Proxy
def query_llm(prompt):
    token = os.environ["AIPROXY_TOKEN"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for data analysis."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 300,
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    else:
        print(f"Error: Failed to communicate with AI Proxy. Status code: {response.status_code}, Response: {response.text}")
        sys.exit(1)

# Main function
def main():
    if len(sys.argv) != 2:
        print("Usage: python autolysis.py <CSV_FILENAME>")
        sys.exit(1)

    csv_file = sys.argv[1]
    validate_environment()

    # Read the CSV file
    headers, rows = read_csv(csv_file)
    print(f"CSV file '{csv_file}' loaded successfully.")
    print(f"Headers: {headers}")
    print(f"Number of rows: {len(rows)}")

    # Generate a summary prompt
    sample_data = rows[:5]  # Take a sample of 5 rows
    sample_text = "\n".join([", ".join(row) for row in sample_data])
    prompt = (
        f"I have loaded a dataset with the following columns: {', '.join(headers)}. "
        f"Here are some sample rows:\n{sample_text}\n"
        "Provide a brief summary of what kind of analysis can be performed on this data."
    )

    # Query GPT-4o-Mini
    print("Querying GPT-4o-Mini for analysis suggestions...")
    result = query_llm(prompt)
    print("\nAI Response:")
    print(result)
    print("now result of response")
    re2 = query_llm(result)
    print(re2)

if __name__ == "__main__":
    main()

