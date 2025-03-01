from prefect import flow, task
import os
import json

FOLDER_PATH = "json_data"  # Adjust to your folder path

# Task: Reads JSON files from a folder
@task
def read_json_files():
    files = [f for f in os.listdir(FOLDER_PATH) if f.endswith(".json")]
    data_list = []
    for file in files:
        with open(os.path.join(FOLDER_PATH, file), "r") as f:
            data = json.load(f)
            data_list.append(data)
        os.remove(os.path.join(FOLDER_PATH, file))  # Delete after processing
    return data_list

# Task: Process JSON data (you can modify this)
@task
def process_json(data_list):
    for data in data_list:
        print(f"Processing: {data}")  # Replace with actual processing logic

# Flow: Orchestrates tasks
@flow
def json_ingestion_flow():
    data_list = read_json_files()
    process_json(data_list)

# Run the flow locally
if __name__ == "__main__":
    json_ingestion_flow()
