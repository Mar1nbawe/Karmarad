import os

from Classes.AI import AI
from System.Interpretter import run_interpretter
from System.ai_system import create_ai_with_tags_relationships
from System.event_manager import EventManager
from Funcs.tags_utils import get_weight_distribution, generate_unique_tags
import requests
from dotenv import load_dotenv

load_dotenv()

def main():
    # List of Character names to create
    ai_names = requests.get("https://randommer.io/api/Name?nameType=fullname&quantity=6",
                                     headers={"X-Api-Key": os.getenv("RAND_API"),
                                              "accept": "*/*"}).json()
    gaussian_dist = get_weight_distribution()

    existing_tag_sets = []
    event_manager = EventManager()

    # Generate Characters with tags
    ais = create_ai_with_tags_relationships(
        ai_names,
        lambda dist, num_tags: generate_unique_tags(gaussian_dist, num_tags, existing_tag_sets),
        5,
    )

    for ai in ais:
        ai.event_manager = event_manager
        event_manager.register_ai(ai)


    # Display information for each Character
    for ai in ais:

        ai.display_info()

    chosen_character = event_manager.random_assign()
    run_interpretter(character= chosen_character, event_manager=event_manager)


if __name__ == "__main__":
    main()