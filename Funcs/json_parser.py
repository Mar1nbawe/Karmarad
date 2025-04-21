import json

from Classes.gossip import Gossip


def json_parser(json_content):
    response_json = json.loads(json_content)
    content = response_json['choices'][0]['message']['content']

    print(content)
    return content

def attribute_gossip(parsed_json):
    if parsed_json == "ERROR|INVALID_INPUT":
        return parsed_json
    if not parsed_json:
        raise ValueError("Input to attribute_gossip is empty or None")
    try:
        parsed_json = json.loads(parsed_json)
    except json.JSONDecodeError as e:
        raise ValueError("Error found:", e)



    gossip_value = Gossip(parsed_json['affects_relationship'], parsed_json['response_type'], None, None, None)
    # else:
    #     gossip_value = Gossip(None, None, parsed_json['perpetrator'], parsed_json['action'], parsed_json['target'])

    return gossip_value