# List of actions


actions = ["Help", "Fight", "Steal"]

# Dictionary of synonyms for each action
synonyms_dict = {
    "Help": ["Assist", "Aid", "Support", "Rescue", "Serve"],
    "Fight": ["Battle", "Combat", "Brawl", "Clash", "Struggle"],
    "Steal": ["Rob", "Thieve", "Pilfer", "Swipe", "Snatch"]
}


# Function to get the action from the user
def get_action():
    # Get the action from the user
    action = "The peasant assists the knight in his quest."

    # Check if the action is valid
    for key, synonyms in synonyms_dict.items():
        if any(word.lower() in action.lower() for word in [key] + synonyms):
            print(f"Action {action} is valid. Matches with {key} / {synonyms}")
            return key
    print("The action is invalid.")
    return None


# get_action()



# Load the spaCy model
nlp = spacy.load("en_core_web_trf")

# Sentence to analyze
sentence = "The peasant assists the knight in his quest."

# Process the sentence
doc = nlp(sentence)

synonym_exists = any(token.lemma_.lower() in [syn.lower() for syn in synonyms_dict] for token in doc)

print(synonym_exists)