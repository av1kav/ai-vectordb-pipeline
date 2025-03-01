import marqo
import json
import os
from pprint import pprint

from index_settings import pmec_index_settings

mq = marqo.Client(url='http://localhost:8882')
index_name = "wny-manufacturing-companies"
local_json_filename = 'sample.json'

TENSOR_SEARCH_IGNORED_FIELDS = [
    '_id', # _id cannot be a tensor field in Marqo
]

def read_json_documents(mode='single', preprocess=True, folder_prefix='data'):
    """"
    Read JSON objects (either a single consolidated file or multiple individual files) 
    in the specified folder and return their content as a list of objects.

    :param: mode: Either 'single' or 'multi'. In 'single' mode, it is assumed that all
            data is in a single consolidated JSON file (list of objects). In 'multi'
            mode, all JSON files in the specified directory are ingested.
    :param: preprocess: Toggle preprocessing (str-concatenating lists, etc)
    :param: folder_prefix: A folder path relative from the working directory which contains
            JSON data. By default, it assumes the folder is called 'data'.
    """
    document_list = []
    print(f'Document fetch mode: {mode}. Preprocessing: {preprocess}')
    if mode == 'single':
        with open(os.path.join(folder_prefix, os.listdir(folder_prefix)[0]), 'r') as f:
            print(f"Using consolidated file: '{os.path.join(folder_prefix, os.listdir(folder_prefix)[0])}'")
            json_data = json.load(f)
            for json_object in json_data:
                if preprocess:
                    json_data = preprocess_json(json_object=json_object)
                else:
                    json_data=json_object
                document_list.append(json_data)
    elif mode == 'multiple':
        print(f"Found {len(os.listdir())} objects under {folder_prefix}/.")
        for filename in os.listdir(folder_prefix):
            with open(os.path.join(folder_prefix, filename), 'r') as f:
                json_data = json.load(f)
                if preprocess:
                    json_data = preprocess_json(json_object=json_object)
                else:
                    json_data=json_object
                document_list.append(json_data)
    else:
        raise ValueError(f"Invalid mode: '{mode}' ")
    print(f"{len(document_list)} object(s) extracted.")
    return document_list

def preprocess_json(json_object):
    """Flatten composite structured in a JSON object and return it."""
    for key, value in json_object.items():
        if type(value) is list:
            json_object[key] = ', '.join(value)
    return json_object

def clear_indexes_if_exist(index_name=index_name):
    # Drop existing index - for development purposes
    for index in mq.get_indexes()['results']:
        if index['indexName'] == index_name:
            mq.index(index_name=index['indexName']).delete()
            print(f"Index '{index_name}' cleared.")

# Create index and add documents
clear_indexes_if_exist()
mq.create_index(index_name, settings_dict=pmec_index_settings)

# Add JSON data, make all fields available to tensor search
json_data = read_json_documents(mode='single', preprocess=False)
for datapoint in json_data:
    pprint(datapoint)
    result = mq.index(index_name).add_documents(datapoint)
    print(result)

# Perform a search query on the index
if 1==2:
    query="What companies have laser cutting facilities?"
    results = mq.index(index_name).search(q=query)
    print(f"\nThe query was: {query}")
    print("Hits from Vector DB: \n==============\n")
    print(f"ID: {results['hits'][0]['_id']}, Score: {results['hits'][0]['_score']:.3f}.")
    print("Company Name:", results['hits'][0]['company_name'])
    print("Relevant data:")
    pprint(results['hits'][0]['_highlights'])



