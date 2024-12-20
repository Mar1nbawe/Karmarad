import random

from ai_system import create_ai_with_tags, User
from event_manager import EventManager
from tags_utils import get_weight_distribution, generate_unique_tags, gaussian_dist
import requests


def main():
    # List of AI names to create
    ai_names = requests.get("https://randommer.io/api/Name?nameType=fullname&quantity=5",
                                     headers={"X-Api-Key": "adf5de275e40478693c9f886d1248b5a",
                                              "accept": "*/*"}).json()
    gaussian_dist = get_weight_distribution()

    existing_tag_sets = []
    event_manager = EventManager()

    # Generate AIs with tags
    ais = create_ai_with_tags(
        ai_names,
        lambda dist, num_tags: generate_unique_tags(gaussian_dist, num_tags, existing_tag_sets),
        9,
    )

    for ai in ais:
        ai.event_manager = event_manager
        event_manager.register_ai(ai)

    # Display information for each created AI
    for ai in ais:
        ai.display_info()

    # Establish relationships for demonstration
    if len(ais) > 1:
        ais[0].set_relationship(ais[1], 1)  # AI_1 likes AI_2
        ais[1].set_relationship(ais[2], -1)  # AI_2 dislikes AI_3

    # Create a user and interact with AIs
    user = User("User_1")
    user.interact_with_ai(ais[0], -10)  # User decreases AI_1’s karma

    for ai in ais:
        print("\n Generated Prompt:")
        print(ai.generate_prompt())

if __name__ == "__main__":
    main()