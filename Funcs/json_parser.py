import json

from Classes.gossip import Gossip


def json_parser(json_content):
    response_json = json.loads(json_content)
    content = response_json['choices'][0]['message']['content']

    print(content)
    return content

def attribute_gossip(parsed_json):
    parsed_json = json.loads(parsed_json)
    gossip_value = Gossip(parsed_json['affects_relationship'], parsed_json['response_type'], None, None, None)
    # else:
    #     gossip_value = Gossip(None, None, parsed_json['perpetrator'], parsed_json['action'], parsed_json['target'])

    return gossip_value