import random


from Database.Init import driver
from Funcs.endpoint_funcs import gossip_endpoint
from Funcs.json_parser import attribute_gossip
from Prompts.gossip_prompter import gossip_prompt
from Classes.AI import AI
from System.ai_system import relationships
from System.karma_calculator import Calculate_Karma


def find_shortest_path(victim, ai):
    # query = """
    # MATCH p = shortestPath((a:Person {name: "$victim"})-[r WHERE type(r) <> 'has_trait']-(b:Person {name: "$ai"}))
    # RETURN length(p) AS length
    # """

    query = """
    MATCH p = shortestPath((a:Person {name: $startName})-[r*]-(b:Person {name: $endName}))
    WHERE ALL(rel IN relationships(p) WHERE type(rel) <> 'has_trait')
    RETURN length(p) AS length, type(relationships(p)[-1]) AS type_rel
    """
    try:
        session = driver.session()
        try:
            result = session.run(query, startName=victim, endName=ai)
            for record in result:
                return record['length']
            session.close()
        except Exception as e:
            print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e} again")



class EventManager:
    def __init__(self):
        self.ai_list : list[AI] = []

    def register_ai(self, ai):
        self.ai_list.append(ai)
        print("Added to queue:", ai.name, "\n")

    def random_assign(self):
        return random.choice(self.ai_list)

    def gossip(self, victim, karma, action):
        print(victim.name)
        victim_karma = 0
        with driver.session() as session:
            karma_affects = 0
            for ai in self.ai_list:
                if ai != victim:
                    for related_ai, strength in ai.relationships.items():
                        if related_ai.name == victim.name:
                            victim_karma = relationships.get(strength)
                            print("Karma of victim: " + str(victim_karma))
                            break  # Exit the loop once the correct relationship is found

                    # Verify karma by matching with value in relationships dictionary.
                    gprompt = gossip_prompt(perp_karma=ai.karma, target_karma= victim_karma, sentiment=action)
                    print(gprompt)
                    gfile = gossip_endpoint(gprompt)
                    gfile = gfile.lower()
                    print("Endpoint from gossip:"+ gfile)
                    rel_len = find_shortest_path(victim.name, ai.name)
                    if gfile == "neutral":
                        continue
                    if gfile == "positive":
                        karma_affects = round(karma / (2 ** int(rel_len)), 0)

                    elif gfile == "hostile":
                        karma_affects = round(karma / (2 ** int(rel_len) * -1), 0)
                    print("Karma affects value: "+ str(karma_affects))

                    ai.adjust_karma(karma_affects)




    # def attributeKarma(self):
    #     for i in self.ai_list:





# a = ["Artem Donner", "Alfonso Person", "Jamira Antonucci", "Jaliah Brenneman", "Akshara Mesa", "Stanton Tadlock"]
# ev = EventManager()
# for i in a:
#     ev.ai_list = a
# print(ev.gossip("Artem Donner", "spreads_rumors") )

# print(find_shortest_path("Tyron Flinn", "Daelynn Riccio"))
