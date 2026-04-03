import json
import boto3
from decouple import config


def get_client():
    return boto3.client(
        "bedrock-runtime",
        region_name=config("AWS_REGION_NAME"),
        aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
    )


CONTENT_GENERATION_TEMPLATE = """You are an expert educator. Write a comprehensive, informative piece of content on the following topic.

Topic: {topic}

Requirements:
- Write at least 400 words of clear, factual content
- Cover key concepts, definitions, and important details
- Structure it with natural paragraphs
- Make it suitable for generating quiz questions from
- Do not include any headings, bullet points, or markdown — plain paragraphs only

Return only the content text. No preamble.
"""

QUIZ_GENERATION_TEMPLATE = """You are a quiz generator. Based on the text below, generate exactly {number_of_questions} multiple choice questions.

Rules:
- Each question must have exactly {number_of_options} answer options
- EXACTLY ONE option must be correct — mark it by writing it in ALL CAPS
- The remaining {wrong_count} options must be plausible but clearly wrong — write them in lowercase
- Questions must be directly answerable from the provided text
- Do not repeat questions or options
- Make wrong options believable but unambiguously incorrect

Text:
{text}

Return your response as a valid JSON object in this exact format:
{{
  "questions": {{
    "Question text here?": ["CORRECT ANSWER IN CAPS", "wrong option one", "wrong option two", "wrong option three"],
    "Another question here?": ["wrong option", "CORRECT ANSWER IN CAPS", "wrong option", "wrong option"]
  }}
}}

Return ONLY the JSON object. No explanation, no markdown, no code blocks.
"""


async def generate_content_from_topic(topic: str) -> str:
    client = get_client()
    response = client.converse(
        modelId="us.amazon.nova-lite-v1:0",
        messages=[{
            "role": "user",
            "content": [{"text": CONTENT_GENERATION_TEMPLATE.format(topic=topic)}]
        }],
        inferenceConfig={"maxTokens": 2048, "temperature": 0.5}
    )
    return response["output"]["message"]["content"][0]["text"].strip()


async def generate_quizzes(number_of_questions: int, number_of_options: int, text: str) -> list:
    from .schemas import QuizSchema

    client = get_client()
    wrong_count = number_of_options - 1

    response = client.converse(
        modelId="us.amazon.nova-lite-v1:0",
        messages=[{
            "role": "user",
            "content": [{
                "text": QUIZ_GENERATION_TEMPLATE.format(
                    number_of_questions=number_of_questions,
                    number_of_options=number_of_options,
                    wrong_count=wrong_count,
                    text=text
                )
            }]
        }],
        inferenceConfig={"maxTokens": 4096, "temperature": 0.3}
    )

    raw_text = response["output"]["message"]["content"][0]["text"].strip()

    # Strip markdown fences if model adds them
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    parsed = json.loads(raw_text)
    return [QuizSchema(questions=parsed["questions"])]
