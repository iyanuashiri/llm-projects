from langchain_openrouter import ChatOpenRouter
from openevals import create_llm_as_judge
from decouple import config

from app.evals.judges.story_generator_judge import STORY_EVALUATION_PROMPT


def story_evaluator(inputs: dict, outputs: dict):
    evaluator = create_llm_as_judge(
        prompt=STORY_EVALUATION_PROMPT,
        judge=ChatOpenRouter(model="deepseek/deepseek-v4-flash-0731", 
                             api_key=config("OPENROUTER_API_KEY"), temperature=0, max_tokens=2048),
        feedback_key="correctness")
    eval_result = evaluator(inputs=inputs, outputs=outputs)
    return eval_result