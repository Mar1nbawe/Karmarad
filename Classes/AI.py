from Database.Init import driver

class AI:
    def __init__(self, name, tags, event_manager=None):

        self.name = name
        self.tags = tags
        self.karma = 0
        self.relationships = {}  # AI relationships (key: AI object, value: strength)
        self.event_manager = event_manager

        if event_manager:
            event_manager.register_ai(self)

    def set_relationship(self, target_ai, strength):
        self.relationships[target_ai] = strength
        target_ai.relationships[self] = strength

    def react_to_karma_change(self, change):

        self.karma += change
        print(f"{self.name}'s karma (tags: {', '.join(self.tags)}) is now {self.karma}.")

        for related_ai, strength in self.relationships.items():
            related_ai.adjust_karma(change * strength)

        if self.event_manager:
            self.event_manager.broadcast_event(
                self, {"type": "karma_change", "change": change}
            )

    def adjust_karma(self, value):
        self.karma += value
        print(f"{self.name}'s karma updated to {self.karma}.")

    def generate_prompt(self):

        relationship_summary = ", ".join(
            [f"{target.name}: {strength}" for target, strength in self.relationships.items()]
        )
        prompt = f"I'm {self.name}. My attributes are {', '.join(self.tags)}.\n"
        prompt += f"My karma is {self.karma}. Relationships: {relationship_summary}.\n"
        return prompt

    def display_info(self):
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