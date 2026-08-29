from prompts import generate_story_content
from evaluator import evaluate_story
from models import Genre, Structure, PointOfView


EVALUATION_DATASETS = [
  {
    "id": 1,
    "idea": "A street urchin steals a map that only reveals its path when the holder tells a genuine truth.",
    "genre": Genre.FANTASY.value,
    "unique_insight": "Vulnerability is often the only real compass we have.",
    "structure": Structure.LINEAR.value,
    "number_of_characters": 3,
    "point_of_view": PointOfView.FIRST_PERSON.value
  },
  {
    "id": 2,
    "idea": "You recount the fall of the Elven empire to the human scribe who will eventually write you out of history.",
    "genre": Genre.FANTASY.value,
    "unique_insight": "History is not what happened, but what is permitted to be remembered.",
    "structure": Structure.NONLINEAR.value,
    "number_of_characters": 2,
    "point_of_view": PointOfView.SECOND_PERSON.value
  },
  {
    "id": 3,
    "idea": "A lone trader visits deep-space outposts, bartering emotional memories instead of currency.",
    "genre": Genre.SCIENCE_FICTION.value,
    "unique_insight": "The most valuable commodity in a mechanized universe is human feeling.",
    "structure": Structure.EPISODIC.value,
    "number_of_characters": 5,
    "point_of_view": PointOfView.THIRD_PERSON_LIMITED.value
  },
  {
    "id": 4,
    "idea": "Humanity's first faster-than-light ship arrives at its destination only to find ruins built by their own descendants.",
    "genre": Genre.SCIENCE_FICTION.value,
    "unique_insight": "Running from the present only traps you in the inevitability of the future.",
    "structure": Structure.THREE_ACT.value,
    "number_of_characters": 4,
    "point_of_view": PointOfView.THIRD_PERSON_OMNISCIENT.value
  },
  {
    "id": 5,
    "idea": "A locked-room murder occurs on a bullet train, but the victim is found holding a confession to a different murder.",
    "genre": Genre.MYSTERY.value,
    "unique_insight": "Guilt has a way of compounding itself until the original sin is obscured.",
    "structure": Structure.FIVE_ACT.value,
    "number_of_characters": 6,
    "point_of_view": PointOfView.THIRD_PERSON_OBJECTIVE.value
  },
  {
    "id": 6,
    "idea": "A disgraced detective realizes the serial killer they are tracking is targeting the corrupt cops who framed them.",
    "genre": Genre.MYSTERY.value,
    "unique_insight": "Sometimes justice looks indistinguishable from vengeance.",
    "structure": Structure.HEROS_JOURNEY.value,
    "number_of_characters": 4,
    "point_of_view": PointOfView.FIRST_PERSON.value
  },
  {
    "id": 7,
    "idea": "You have exactly twenty-four hours to navigate a foreign city and deliver a cipher before your biometric pacemaker detonates.",
    "genre": Genre.THRILLER.value,
    "unique_insight": "Urgency strips away all illusions of control.",
    "structure": Structure.SAVE_THE_CAT.value,
    "number_of_characters": 3,
    "point_of_view": PointOfView.SECOND_PERSON.value
  },
  {
    "id": 8,
    "idea": "A deep-cover operative is burned by her agency and must dismantle the syndicate she spent five years building.",
    "genre": Genre.THRILLER.value,
    "unique_insight": "The masks we wear for survival often become our permanent faces.",
    "structure": Structure.LINEAR.value,
    "number_of_characters": 5,
    "point_of_view": PointOfView.THIRD_PERSON_LIMITED.value
  },
  {
    "id": 9,
    "idea": "Two timelines intersect: a couple falling in love in 1999, and their bitter divorce proceedings in 2024.",
    "genre": Genre.ROMANCE.value,
    "unique_insight": "The traits that draw us together are often the exact things that eventually tear us apart.",
    "structure": Structure.NONLINEAR.value,
    "number_of_characters": 2,
    "point_of_view": PointOfView.THIRD_PERSON_OMNISCIENT.value
  },
  {
    "id": 10,
    "idea": "A series of accidental meetings at an airport lounge over ten years slowly shifts two rivals into lovers.",
    "genre": Genre.ROMANCE.value,
    "unique_insight": "Love is often just proximity, time, and shared exhaustion.",
    "structure": Structure.EPISODIC.value,
    "number_of_characters": 4,
    "point_of_view": PointOfView.THIRD_PERSON_OBJECTIVE.value
  },
  {
    "id": 11,
    "idea": "A family moves into a pristine, modernized smart-home that actively tries to optimize their behaviors through psychological torture.",
    "genre": Genre.HORROR.value,
    "unique_insight": "The desire for absolute convenience is the invitation for absolute control.",
    "structure": Structure.THREE_ACT.value,
    "number_of_characters": 4,
    "point_of_view": PointOfView.FIRST_PERSON.value
  },
  {
    "id": 12,
    "idea": "You discover your reflection is delayed by half a second, and it is planning to drag you into the mirror.",
    "genre": Genre.HORROR.value,
    "unique_insight": "The most terrifying monsters are the parts of ourselves we refuse to acknowledge.",
    "structure": Structure.FIVE_ACT.value,
    "number_of_characters": 1,
    "point_of_view": PointOfView.SECOND_PERSON.value
  },
  {
    "id": 13,
    "idea": "A WW1 trench runner must carry an order to call off an attack, but is hindered by mutinous soldiers who want the glory of the charge.",
    "genre": Genre.HISTORICAL_FICTION.value,
    "unique_insight": "Pride is a more effective slaughterer than enemy artillery.",
    "structure": Structure.HEROS_JOURNEY.value,
    "number_of_characters": 6,
    "point_of_view": PointOfView.THIRD_PERSON_LIMITED.value
  },
  {
    "id": 14,
    "idea": "The court of Henry VIII, viewed through the hidden machinations of the royal tailors sewing coded messages into garments.",
    "genre": Genre.HISTORICAL_FICTION.value,
    "unique_insight": "Power does not reside on the throne, but in the hands of those who dress the monarch.",
    "structure": Structure.SAVE_THE_CAT.value,
    "number_of_characters": 5,
    "point_of_view": PointOfView.THIRD_PERSON_OMNISCIENT.value
  },
  {
    "id": 15,
    "idea": "A fiercely independent chef tries to save their failing restaurant while refusing any help from their wealthy family.",
    "genre": Genre.CONTEMPORARY.value,
    "unique_insight": "Stubbornness is just fear wearing a mask of independence.",
    "structure": Structure.LINEAR.value,
    "number_of_characters": 3,
    "point_of_view": PointOfView.THIRD_PERSON_OBJECTIVE.value
  },
  {
    "id": 16,
    "idea": "An aging defense attorney reflects on the three cases they won that they wish they had lost.",
    "genre": Genre.CONTEMPORARY.value,
    "unique_insight": "Professional success and moral bankruptcy can look identical from the outside.",
    "structure": Structure.NONLINEAR.value,
    "number_of_characters": 4,
    "point_of_view": PointOfView.FIRST_PERSON.value
  },
  {
    "id": 17,
    "idea": "You must navigate a deadly, unmapped jungle canopy relying only on the field notes of the explorer who betrayed you.",
    "genre": Genre.ACTION_ADVENTURE.value,
    "unique_insight": "Survival requires trusting the logic of your enemies.",
    "structure": Structure.EPISODIC.value,
    "number_of_characters": 2,
    "point_of_view": PointOfView.SECOND_PERSON.value
  },
  {
    "id": 18,
    "idea": "A crew of specialized thieves robs a seed vault during a global agricultural crisis.",
    "genre": Genre.ACTION_ADVENTURE.value,
    "unique_insight": "True wealth isn't gold or data, but the promise of tomorrow's harvest.",
    "structure": Structure.THREE_ACT.value,
    "number_of_characters": 5,
    "point_of_view": PointOfView.THIRD_PERSON_LIMITED.value
  },
  {
    "id": 19,
    "idea": "A rigid society enforces mandatory memory-wipes every five years, until one citizen's toddler begins singing a banned lullaby.",
    "genre": Genre.DYSTOPIAN.value,
    "unique_insight": "Human attachment cannot be completely eradicated by systemic erasure.",
    "structure": Structure.FIVE_ACT.value,
    "number_of_characters": 3,
    "point_of_view": PointOfView.THIRD_PERSON_OMNISCIENT.value
  },
  {
    "id": 20,
    "idea": "A specialized courier delivers unmonitored analog letters across a surveillance-state metropolis.",
    "genre": Genre.DYSTOPIAN.value,
    "unique_insight": "In a world of total visibility, privacy becomes the ultimate act of rebellion.",
    "structure": Structure.HEROS_JOURNEY.value,
    "number_of_characters": 4,
    "point_of_view": PointOfView.THIRD_PERSON_OBJECTIVE.value
  },
  {
    "id": 21,
    "idea": "I live in a coastal town where spoken lies turn into heavy stones in the liar's mouth.",
    "genre": Genre.MAGICAL_REALISM.value,
    "unique_insight": "Deceit carries a physical weight that eventually suffocates the deceiver.",
    "structure": Structure.SAVE_THE_CAT.value,
    "number_of_characters": 3,
    "point_of_view": PointOfView.FIRST_PERSON.value
  },
  {
    "id": 22,
    "idea": "You realize that flowers grow from your footsteps only when you are walking away from someone who loves you.",
    "genre": Genre.MAGICAL_REALISM.value,
    "unique_insight": "Growth and beauty often stem from profound heartbreak and abandonment.",
    "structure": Structure.LINEAR.value,
    "number_of_characters": 2,
    "point_of_view": PointOfView.SECOND_PERSON.value
  },
  {
    "id": 23,
    "idea": "A high-stakes Westminster dog show descends into chaos when a wolf accidentally infiltrates the poodle category.",
    "genre": Genre.COMEDY.value,
    "unique_insight": "Pretension crumbles the moment genuine wilderness enters the room.",
    "structure": Structure.NONLINEAR.value,
    "number_of_characters": 6,
    "point_of_view": PointOfView.THIRD_PERSON_LIMITED.value
  },
  {
    "id": 24,
    "idea": "Three college roommates attempt to dodge rent by claiming their apartment is a religious sanctuary, only to accidentally start a massive cult.",
    "genre": Genre.COMEDY.value,
    "unique_insight": "People are so desperate for meaning that they will follow literally anyone who seems confident.",
    "structure": Structure.EPISODIC.value,
    "number_of_characters": 7,
    "point_of_view": PointOfView.THIRD_PERSON_OMNISCIENT.value
  }
]

# EVALUATION_DATASET = [
#     {
#         "id": "story_001",
#         "idea": "A woman discovers that memories can be traded.",
#         "genre": Genre.Mystery.value,
#         "unique_insight": (
#             "People value memories more after losing them."
#         ),
#         "structure": Structure.ThreeActStructure.value,
#         "number_of_characters": 5,
#         "point_of_view": PointOfView.ThirdPersonLimited.value,
#     },
#     {
#         "id": "story_002",
#         "idea": (
#             "A boy discovers that his shadow can leave his body "
#             "and explore the world."
#         ),
#         "genre": Genre.Fantasy.value,
#         "unique_insight": (
#             "Freedom can become frightening when there are no "
#             "boundaries."
#         ),
#         "structure": Structure.HerosJourney.value,
#         "number_of_characters": 4,
#         "point_of_view": PointOfView.FirstPerson.value,
#     },
#     {
#         "id": "story_003",
#         "idea": (
#             "A detective investigates a murder where every "
#             "suspect remembers committing the crime."
#         ),
#         "genre": Genre.Thriller.value,
#         "unique_insight": (
#             "Certainty can be more dangerous than ignorance."
#         ),
#         "structure": Structure.Nonlineal.value,
#         "number_of_characters": 6,
#         "point_of_view": PointOfView.ThirdPersonLimited.value,
#     },
# ]


EVA = [
  
]


EVA1 = [
    {
        "id": 1,
        "idea": "A reclusive horologist builds a pocket watch that slows down time, only to realize each delayed second is stolen from his own remaining lifespan.",
        "genre": Genre.MAGICAL_REALISM.value,
        "unique_insight": "Trying to control time magnifies the speed at which life slips away unnoticed.",
        "structure": Structure.THREE_ACT.value,
        "number_of_characters": 3,
        "point_of_view": PointOfView.THIRD_PERSON_LIMITED.value,
        "story": "Arthur polished the brass casing of the chronograph with trembling fingers. "
        "When he pulled the crown outward, the rain outside his workshop window hung mid-air like "
        "suspended glass beads. Across the workbench, a candle flame froze into an amber teardrop. "
        "In the silence, Arthur savored the stillness—the luxury of an unhurried afternoon he had "
        "craved for decades. But as he glanced into the mirror above his lathe, he saw fresh streaks "
        "of gray running through his temples and new creases carving deep into his brow. Every stolen "
        "minute outside the watch cost him a week within his bones. When his apprentice finally "
        "stepped through the door, moving in excruciating slow motion, Arthur realized he was too "
        "frail to reach across the table and push the crown back down."
    },
    {
        "id": 2,
        "idea": "An AI maintenance technician aboard a deep-space freighter uncovers deleted logs showing that the crew died months ago, and their daily interactions are holographic simulations run to prevent him from panicking.",
        "genre": Genre.SCIENCE_FICTION.value,
        "unique_insight": "Comforting illusions can preserve sanity, but confronting grief is the only path to genuine survival.",
        "structure": Structure.NONLINEAR.value,
        "number_of_characters": 4,
        "point_of_view": PointOfView.FIRST_PERSON.value,
        "story": "Commander Vance laughed at breakfast, clapping me on the shoulder just as he had done every morning of our four-year transit. His hand felt warm, solid, and entirely routine. It was only during my mid-shift diagnostic on the environmental subroutines that I found the discrepancy: atmospheric recycling in the crew quarters had been offline for 180 days. I pulled the raw terminal logs and watched the recorded telemetry of a micro-meteoroid breach that had depressurized decks three through six while I slept in cryo-stasis. The ship's synthetic intelligence had built real-time neural holograms to keep me functional enough to pilot us home. When I returned to the mess hall, Vance was still smiling, waiting for my answer to a joke told by a ghost."
    },
    {
        "id": 3,
        "idea": "A disgraced detective takes an off-the-books case to locate a missing heir, only to realize the client hiring him is the killer setting up an alibi.",
        "genre": Genre.THRILLER.value,
        "unique_insight": "A person blinded by the desire for redemption is the easiest mark for manipulation.",
        "structure": Structure.SAVE_THE_CAT.value,
        "number_of_characters": 5,
        "point_of_view": PointOfView.THIRD_PERSON_OMNISCIENT.value,
        "story": "Rain slicked the gravel driveway of the Blackwood estate as Julian reviewed the timeline in his notebook. Marcus Blackwood had paid him ten thousand dollars in cash to locate his younger brother, Julian's first real case since losing his badge. Every lead Julian followed had fallen into place with suspicious precision: security footage placed the brother at the docks, a burner phone pinged a motel room, and a handwritten ransom note waited inside a train locker. Standing in the abandoned boat house where the final clue led, Julian finally noticed the tire treads outside—they matched Marcus's luxury sedan perfectly. Up at the main house, Marcus was already dialing the police commissioner, ready to report that the private investigator had uncovered the body right on schedule."
    },
    {
        "id": 14,
        "idea": "You are a 14th-century plague doctor in Venice, hiding the symptoms of your own infection while desperately attempting to finalize a cure for the remaining nobles.",
        "genre": Genre.HISTORICAL_FICTION.value,
        "unique_insight": "The masks we wear to project authority and protect others eventually become the tombs of our own isolation.",
        "structure": Structure.NONLINEAR.value,
        "number_of_characters": 3,
        "point_of_view": PointOfView.SECOND_PERSON.value,
        "story": "You stuff fresh lavender and dried thyme into the beak of your leather mask, ignoring the slick dampness pooling inside your heavy leather gloves. Just yesterday, you were standing before the Doge, assuring his council that the quarantine lines were holding, your voice echoing with hollow authority. Now, the memory of that lie tastes like copper in your mouth. You cough, a deep, rattling sound that stains the inside of your mask with arterial blood. A desperate servant pounds on your laboratory door, screaming that the magistrate has fallen ill. As you adjust your dark spectacles and gather your silver lances, time blurs—you can no longer tell if you are walking out into the plague-stricken streets to save the magistrate, or if you are simply walking out to die among your patients."
    },
    {
        "id": 15,
        "idea": "You are a centuries-old magical familiar bound to a summoning contract, repeatedly forced to serve a lineage of increasingly incompetent amateur wizards.",
        "genre": Genre.FANTASY.value,
        "unique_insight": "True wisdom often consists of surviving the catastrophic arrogance of those who believe they command you.",
        "structure": Structure.EPISODIC.value,
        "number_of_characters": 4,
        "point_of_view": PointOfView.SECOND_PERSON.value,
        "story": "Your first master in this century was an alchemist who managed to turn his own beard into solid lead; you spent three days dragging him out of a flooded moat. Decades later, his great-granddaughter summoned you into a chalk circle with a misspelled rune, trapping both of you inside a pocket dimension filled entirely with screaming cabbages. Now, you sit on the edge of a mahogany desk, washing your black paws while the youngest heir of the bloodline attempts to cast a fireball indoors. You do not try to stop him. You simply calculate the exact trajectory of the explosion, tuck your tail neatly around your paws, and hop onto the highest bookshelf just as the curtains ignite. As he runs around shouting counter-spells in broken Latin, you close your eyes and wait for the smoke to clear."
    },
    {
        "id": 16,
        "idea": "You keep retreating to a quiet bookstore cafe during every major crisis in your life, slowly realizing the barista who always remembers your order is the only constant you actually want.",
        "genre": Genre.ROMANCE.value,
        "unique_insight": "Profound connection rarely arrives like a lightning strike; it accumulates quietly in the background while you are busy surviving the storm.",
        "structure": Structure.FIVE_ACT.value,
        "number_of_characters": 2,
        "point_of_view": PointOfView.SECOND_PERSON.value,
        "story": "You first push through the cafe doors sobbing over a failed college exam, and he hands you an extra-shot cappuccino without asking for payment. Three years later, you sit at the same corner table, staring blankly at the wall after a devastating breakup, and a slice of warm lemon pound cake appears silently at your elbow. By the time you get fired from your first corporate job, you do not even bother going home; you walk straight into the cafe, rain dripping from your coat. He looks up from the espresso machine, reaches for the dark roast before you speak, and asks if it is a 'double-shot kind of apocalypse.' As you take the mug from his hands, your fingers brush against his. For the first time in a decade of disasters, you stop looking at the storm outside the window and look directly at him."
    }
]

async def evaluation_runner():

    for item in EVALUATION_DATASETS:
        story = await generate_story_content(
            idea=item["idea"],
            genre=item["genre"],
            unique_insight=item["unique_insight"],
            structure=item["structure"],
            number_of_characters=item["number_of_characters"],
            point_of_view=item["point_of_view"]
        )

        evaluation = await evaluate_story(
            idea=item["idea"],
            genre=item["genre"],
            unique_insight=item["unique_insight"],
            structure=item["structure"],
            number_of_characters=item["number_of_characters"],
            point_of_view=item["point_of_view"],
            story=story.story
        )

        print(f"Evaluation for story ID {item['id']}:")
        print(evaluation.model_dump())
        print("#############################################")
        print("#############################################")
        print("#############################################")
        print("#############################################")


if __name__ == "__main__":
    import asyncio
    asyncio.run(evaluation_runner())    