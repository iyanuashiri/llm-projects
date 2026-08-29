import asyncio

from evaluator import evaluate_story
from models import Genre, Structure, PointOfView


async def main():
    story = """
    Chapter 1: The Discovery

    Amara had spent ten years searching for the truth...

    """

    evaluation = await evaluate_story(
        idea="A woman discovers that memories can be traded.",
        genre=Genre.MYSTERY,
        unique_insight="People value memories more after losing them.",
        structure=Structure.THREE_ACT,
        number_of_characters=5,
        point_of_view=PointOfView.THIRD_PERSON_LIMITED,
        story=story,
    )

    print(evaluation.model_dump())


async def main2():
    story = """
    # The Patient Light

## Chapter 1: The Beginning

Naomi Whitfield met Eli Morgan on a rain-slicked Tuesday in the fall of her twenty-third year, in a coffee shop with a broken espresso machine and a line that snaked past the door. She was clutching a laptop bag and a latte she hadn't paid enough attention to, and when a man in a flannel shirt bumped her elbow, the latte went everywhere — across his boots, across her wrist, across the floor in a brown tidal wave.

"I'm so sorry," she said, already reaching for napkins.

He wasn't looking at the mess. He was looking at her burned wrist, already pink and swelling. "You're the one who's sorry?" He took her hand, not in a romantic way, but the way a carpenter inspects a split board — careful, practical. "Come here. There's a sink in the back. Cold water, now."

His name was Eli. He built furniture in a workshop two blocks over, and he had the shoulders and the sawdust-dusted forearms to prove it. He rinsed her wrist under cold water, wrapped it in a clean rag, and then, because the line was still long, they sat together at a wobbly table and talked for three hours. It felt like the most natural thing in the world.

What followed was the best year of Naomi's life. They were never officially anything — no label, no "what are we," no ring — but they were everything. He took her to the farmer's market on Saturdays, where she'd pick out flowers and he'd carry them. She took him to art galleries he didn't understand but pretended to, squinting at abstract canvases like they were joinery problems. They kissed for the first time in his workshop, under a single bare bulb, surrounded by the smell of cedar shavings and linseed oil, and it was so gentle that she cried afterward, laughing at herself for crying.

"You're a strange woman, Naomi Whitfield," Eli said, wiping her tears with a sawdust-stained thumb.

"You're a strange man, Eli Morgan," she said back.

But there was a shadow. Naomi's mother had died of cancer the year before, and grief had hollowed her out. She was searching for something to hold onto, something bigger than coffee shops and carpenter's hands. When a woman from the Lighthouse of Grace Church had pressed a tract into her hands at the bus stop, Naomi had read it twice on the ride home, and then she'd gone to a service. And then she'd gone back. And then she'd gone back again.

The church's pastor was a man named Marcus Hale — silver-tongued, soft-handed, with eyes that seemed to see straight through you and a voice that made scripture sound like a love letter. He told Naomi, in a private prayer session, that her mother was in heaven, that God had a plan for her, that she was chosen. She wept. She felt, for the first time since the funeral, that she wasn't floating.

Eli came to exactly one service. He sat in the back row,

    """

    evaluation = await evaluate_story(
        idea="a love story of two people and eventually happy married life. but the lady was initially manipulated by a false pastor who claimed false prophecy who marry a gay man. she was unhappy, frustrated and she had to act happy. the pastor then claimed that for the husband to not being gay she has to have sex with the pastor that was when she realized that the pastor is false. the initial best friend and lover already told her that the pastor was false and he said it multiple times but she felt he didnt like the pastor. when they were best friends and lovers, they were intimate and deeply in love. they went out on dates and all that but the relationship wasnt defined because she hoped and wanted the best friend to join her church with her beause she felt God told her to join the church whereas it was a lie and manipulation from the pastor",
        genre=Genre.ROMANCE,
        unique_insight="love is a patient, kind, it is not self-seeking",
        structure=Structure.EPISODIC,
        number_of_characters=5,
        point_of_view=PointOfView.THIRD_PERSON_LIMITED,
        story=story,
    )

    print(evaluation.model_dump())


if __name__ == "__main__":
    asyncio.run(main2())