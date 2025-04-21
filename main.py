import os

from System.ai_system import create_ai_with_tags_relationships
from System.event_manager import EventManager
from Funcs.tags_utils import get_weight_distribution, generate_unique_tags
import requests
from dotenv import load_dotenv

load_dotenv()

def main():
    # List of AI names to create
    ai_names = requests.get("https://randommer.io/api/Name?nameType=fullname&quantity=6",
                                     headers={"X-Api-Key": os.getenv("RAND_API"),
                                              "accept": "*/*"}).json()
    gaussian_dist = get_weight_distribution()

    existing_tag_sets = []
    event_manager = EventManager()

    # Generate AIs with tags
    ais = create_ai_with_tags_relationships(
        ai_names,
        lambda dist, num_tags: generate_unique_tags(gaussian_dist, num_tags, existing_tag_sets),
        5,
    )

    for ai in ais:
        ai.event_manager = event_manager
        event_manager.register_ai(ai)
    event_manager.gossip(event_manager.random_assign(), "killed")

    # Display information for each created AI
    for ai in ais:

        ai.display_info()



    # for ai in ais:
    #     print("\n Generated Prompt:")
    #     print(ai.generate_prompt())

if __name__ == "__main__":
    main()