import os
import json
from pathlib import Path

from decouple import config
from langsmith import Client
from langsmith.utils import LangSmithConflictError


os.environ["LANGSMITH_API_KEY"] = config("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = config("LANGSMITH_TRACING")
os.environ["LANGSMITH_PROJECT"] = config("LANGSMITH_PROJECT")
os.environ["LANGSMITH_ENDPOINT"] = config("LANGSMITH_ENDPOINT")
os.environ["OPENROUTER_API_KEY"] = config("OPENROUTER_API_KEY")


DATASET_NAME = "Story Generation Dataset Evaluation"

INPUT_DATASET_PATH = Path(__file__).with_name("input_dataset.json")
OUTPUT_DATASET_PATH = Path(__file__).with_name("output_dataset.json")


with INPUT_DATASET_PATH.open(encoding="utf-8") as input_dataset_file:
    input_dataset_records = json.load(input_dataset_file)

with OUTPUT_DATASET_PATH.open(encoding="utf-8") as output_dataset_file:
    output_dataset_records = json.load(output_dataset_file)    

examples = [{"inputs": input, "outputs": output} for input, output in zip(input_dataset_records, output_dataset_records) ]

client = Client()

try:
    dataset = client.create_dataset(dataset_name=DATASET_NAME, 
                                description="Story generation datasets for evaluation.")
    client.create_examples(dataset_id=dataset.id, examples=examples)

except:
    print()  


