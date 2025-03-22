from Funcs.tags_utils import get_weight_distribution
from Database.Init import driver
from Classes.AI import AI
import random

class User:
    def __init__(self, name):
        self.name = name
        self.karma = 0

    def adjust_karma(self, value):
        self.karma += value
        print(f"{self.name}'s karma is now {self.karma}.")

    def interact_with_ai(self, ai, change):
        print(f"{self.name} interacts with {ai.name} causing a karma effect: {change}.")
        ai.react_to_karma_change(change)


relationships = {
    "friend": 50,
    "enemy": -100,
    "colleague": 20,
    "family": 100,
    "acquaintance": 10,
    "mentor": 70,
    "neighbor": 30,
    "partner": 90,
    "rival": -50
}


def add_relationship_to_db(session, char_name, rel_char_name, rel_type):
    session.run('MATCH (a:Person {name: "' + char_name + '"}), (b:Person {name: "' + rel_char_name + '"}) CREATE (a)-[:' + rel_type + ']->(b)')

def generate_relationship(char_list: list[AI]):
    max_attempts = 10
    with driver.session() as session:
        for char in char_list:
            num_relationships = random.randint(1,3)
            created_relationship = 0
            attempts = 0
            while created_relationship < num_relationships and attempts < max_attempts:
                rel_type = random.choice(list(relationships.keys()))
                rel_number = random.randint(0, len(char_list) - 1)
                rel_char = char_list[rel_number]

                if rel_char == char or rel_char in char.relationships or len(char.relationships) >= num_relationships:
                    attempts +=1
                    continue

                if (len(char.relationships) <= num_relationships or len(rel_char.relationships) <= num_relationships):
                    char.set_relationship(rel_char, rel_type)
                    created_relationship += 1
                    add_relationship_to_db(session, char.name, rel_char.name, rel_type)

                    print("Debug: choosing a random relationship  for", char.name, created_relationship)
        return char_list


def create_ai_with_tags_relationships(names, tags_generator, number_of_tags=9):
    gaussian_dist = get_weight_distribution()
    ais = []

    with driver.session() as session:
        for name in names:
            tags = tags_generator(gaussian_dist, number_of_tags)
            session.run('CREATE (person:Person {name: "' + name + '"})')
            for tag in tags:
                session.run('MATCH (a:Person {name: "' + name + '"}), (t:Trait {name: "' + tag + '"}) CREATE (a)-[:has_trait]->(t)')
            ai_instance = AI(name,tags)
            ais.append(ai_instance)
        ais = generate_relationship(ais)

        return ais
