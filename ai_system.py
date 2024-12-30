# ai_system.py
from tags_utils import get_weight_distribution


class AI:
    def __init__(self, name, tags, event_manager=None):
        """
        Initialize an AI with a name, tags, and a reference to the event manager.
        :param name: AI name.
        :param tags: List of tags describing the AI's traits.
        :param event_manager: Centralized event manager for communication.
        """
        self.name = name
        self.tags = tags
        self.karma = 0
        self.relationships = {}  # AI relationships (key: AI object, value: strength)
        self.event_manager = event_manager

        # Register this AI with the event manager if provided
        if event_manager:
            event_manager.register_ai(self)

    def set_relationship(self, target_ai, strength):
        """Establishes a one-directional relationship."""
        self.relationships[target_ai] = strength

    def react_to_karma_change(self, change):
        """
        Reacts to a karma change and propagates the event.
        :param change: Karma change value.
        """
        self.karma += change
        print(f"{self.name}'s karma (tags: {', '.join(self.tags)}) is now {self.karma}.")

        # Notify related AIs of the effect
        for related_ai, strength in self.relationships.items():
            related_ai.adjust_karma(change * strength)

        # Broadcast the change to other AIs via the EventManager
        if self.event_manager:
            self.event_manager.broadcast_event(
                self, {"type": "karma_change", "change": change}
            )

    def adjust_karma(self, value):
        """Adjusts karma of this AI due to external events."""
        self.karma += value
        print(f"{self.name}'s karma updated to {self.karma}.")

    def receive_event(self, origin_ai, event):
        """
        Receives an event broadcast by another AI.
        :param origin_ai: The AI that triggered the event.
        :param event: Event data sent to this AI.
        """
        print(f"{self.name} received event from {origin_ai.name}: {event}")

        # Customize behavior based on event type
        if event["type"] == "karma_change":
            print(
                f"{self.name} is aware that {origin_ai.name}'s karma changed by {event['change']}\n"
            )

    def generate_prompt(self):
        """
        Generates a prompt based on this AI's state and relationships.
        """
        relationship_summary = ", ".join(
            [f"{target.name}: {strength}" for target, strength in self.relationships.items()]
        )
        prompt = f"I'm {self.name}. My attributes are {', '.join(self.tags)}.\n"
        prompt += f"My karma is {self.karma}. Relationships: {relationship_summary}.\n"
        return prompt

    def display_info(self):
        """Display the AI's name, tags, karma, and relationships (if any)."""
        print(f"AI Name: {self.name}")
        print(f"Tags: {', '.join(self.tags)}")
        print(f"Karma: {self.karma}")
        if self.relationships:
            print("Relationships:")
            for related_ai, strength in self.relationships.items():
                print(f"    {related_ai.name}: {strength}")
        else:
            print("Relationships: None")
        print("===")


class User:
    def __init__(self, name):
        self.name = name
        self.karma = 0

    def adjust_karma(self, value):
        """Adjust the user's karma."""
        self.karma += value
        print(f"{self.name}'s karma is now {self.karma}.")

    def interact_with_ai(self, ai, change):
        """
        Interact with an AI, causing a karma change.
        :param ai: The AI being interacted with.
        :param change: Karma change value.
        """
        print(f"{self.name} interacts with {ai.name} causing a karma effect: {change}.")
        ai.react_to_karma_change(change)


def create_ai_with_tags(names, tags_generator, number_of_tags=9):
    """
    Create a list of AIs with dynamically generated tags.
    :param names: List of AI names to create.
    :param tags_generator: Function to generate tags.
    :param number_of_tags: Number of tags per AI.
    :return: List of AI objects.
    """
    gaussian_dist = get_weight_distribution()
    ais = []
    for name in names:
        tags = tags_generator(gaussian_dist, number_of_tags)
        ais.append(AI(name, tags))
    return ais
