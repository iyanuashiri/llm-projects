import asyncio

from decouple import config
from langsmith import Client

from app.services.story_generator import generate_story_content 
from app.evals.judges.evaluators import story_evaluator
from app.dataset.create_dataset import DATASET_NAME


client = Client()
datasets = client.list_datasets(dataset_name=DATASET_NAME)   
datasets = list(datasets)
print(list(datasets))
dataset = datasets[0]    


async def evaluation_target(inputs: dict) -> dict:
    result = await generate_story_content(
        idea=inputs["idea"],
        genre=inputs["genre"],
        unique_insight=inputs["unique_insight"],
        structure=inputs["structure"],
        number_of_characters=inputs["number_of_characters"],
        point_of_view=inputs["point_of_view"],
    )

    return result.model_dump()


async def get_result():

    results = await client.aevaluate(
        evaluation_target,
        data=dataset.name,
        evaluators=[story_evaluator],
        experiment_prefix="experiment-story-evaluation-2",
        max_concurrency=2,
    )

    print(results)

    return results


if __name__ == "__main__":
    asyncio.run(get_result())