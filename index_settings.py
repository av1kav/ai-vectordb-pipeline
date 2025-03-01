import marqo
import json

MODEL = "hf/e5-base-v2"
VECTOR_NUMERIC_TYPE = None

pmec_index_settings = {
    "type": "structured",
    "allFields": [
        {"name": "company_id","type": "text","features": ["lexical_search","filter"]},
        {"name": "company_name", "type": "text","features": ["lexical_search"]},
        {"name": "datapoint_type","type": "text","features": ["lexical_search"]},
        {"name": "datapoint_value","type": "text","features": ["lexical_search"]},
        {"name": "source_urls","type": "array<text>","features": ["lexical_search"]},
        {"name": "source_inferred","type": "array<text>","features": ["lexical_search"]},
        {"name": "source_excerpts","type": "array<text>","features": ["lexical_search"]}
    ],
    "tensorFields": ["company_name","datapoint_value","datapoint_type"]
}