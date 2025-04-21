import random

from Database.Init import driver
from Funcs.endpoint_funcs import gossip_endpoint
from Funcs.json_parser import attribute_gossip
from Prompts.gossip_prompter import gossip_prompt
from Classes.AI import AI
from System.karma_calculator import Calculate_Karma


class EventManager:
    def __init__(self):
        self.ai_list : list[AI] = []

    def register_ai(self, ai):
        self.ai_list.append(ai)
        print("Added to queue:", ai.name, "\n")

    def random_assign(self):
        return random.choice(self.ai_list)

    def gossip(self, victim, action):
        with driver.session() as session:
            for ai in self.ai_list:
                if ai != victim:

                    print(ai)
                    gprompt = gossip_prompt(perp="User", action=action, target=victim.name, traits= ai.tags, perp_karma="50", target_karma= victim.karma)
                    print(gprompt)
                    gfile = gossip_endpoint(gprompt)
                    print(gfile.affects_relationship)
                else: continue



    # def attributeKarma(self):
    #     for i in self.ai_list:



# a = ["Artem Donner", "Alfonso Person", "Jamira Antonucci", "Jaliah Brenneman", "Akshara Mesa", "Stanton Tadlock"]
# ev = EventManager()
# for i in a:
#     ev.ai_list = a
# print(ev.gossip("Artem Donner", "spreads_rumors") )