import asyncio
from statistics import mean

import aiohttp
import requests
import pandas as pd
from decouple import config
import torch
from sentence_transformers import SentenceTransformer

import pinecone


device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = SentenceTransformer('average_word_embeddings_komninos', device=device)


DOMAIN_URL = config('DOMAIN_URL')
TOKEN_AUTHORIZATION = config('TOKEN_AUTHORIZATION')
PINECONE_API_KEY = config('PINECONE_API_KEY')
PINECONE_ENVIRONMENT = config('PINECONE_ENVIRONMENT')

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

index_name = 'summaries-recommendation'

if index_name in pinecone.list_indexes():
    pinecone.delete_index(index_name)

pinecone.create_index(index_name, dimension=300)
index = pinecone.Index(index_name=index_name)
index.describe_index_stats()


NROWS = 200000
BATCH_SIZE = 500


def total_users():
    response = requests.get(f'{DOMAIN_URL}/total-users/')
    data = response.json()
    return data['total_users']


async def query_data_(library_id, session):

    async with session.get(f"{DOMAIN_URL}/instances/total-favourites/{library_id}/",
                           headers={'Authorization': f'Token {TOKEN_AUTHORIZATION}'}) as response:
        data = await response.json()
        data = pd.DataFrame(data)
        encoded_articles = model.encode(data['summary'])
        data['summary_vector'] = pd.Series(encoded_articles.tolist())

    ####################################################

    items_to_upload = [(str(row.id), row.summary_vector) for item, row in data.iterrows()]

    for item in range(0, len(items_to_upload), BATCH_SIZE):
        index.upsert(vectors=items_to_upload[item:item + BATCH_SIZE])

    ####################################################
    a = data['summary_vector']
    user_vector = [*map(mean, zip(*a))]

    # Query Pinecone
    res = index.query(user_vector, top_k=10)

    for match in res.matches:
        payload = {'summary': match.id, 'score': match.score}
        async with session.post(f"{DOMAIN_URL}/recommendations/", data=payload,
                                headers={'Authorization': f'Token {TOKEN_AUTHORIZATION}'}) as response:
            yield response.text()


async def main():
    libraries = total_libraries()
    async with aiohttp.ClientSession() as session:
        tasks = [query_data_(library_id=library_id, session=session) for library_id in range(1, libraries)]
        list_of_tasks = await asyncio.gather(*tasks)

        pinecone.delete_index(index_name)

        return list_of_tasks


if __name__ == '__main__':
    asyncio.run(main())
