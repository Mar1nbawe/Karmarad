

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



tag_list = ["hateful", "dumb", "smart", "kind", "empathetic", "greedy", "generous", "narcissistic", "selfless",
        "egoistic", "egoless", "impulsive", "calm", "rational", "irrational", "fanatic", "sympathetic", "apathetic",
        "indifferent", "leader", "self-aware", "logical", "silver-tongued", "intelligent", "compliance"]

# Dictionary with tags and their weights
weights_dict = {
    "hateful": -100,
    "kind": 100,
    "dumb": -50,
    "smart": 50,
    "greedy": -40,
    "generous": 40,
    "narcissistic": -60,
    "selfless": 60,
    "egoistic": -55,
    "egoless": 55,
    "impulsive": -30,
    "calm": 30,
    "rational": 70,
    "irrational": -70,
    "fanatic": -80,
    "sympathetic": 80,
    "apathetic": -35,
    "empathetic": 35,
    "indifferent": -10,
    "leader": 100,
    "self-aware": 45,
    "logical": 65,
    "silver-tongued": 75,
    "intelligent": 85,
    "compliance": 15,
    "creative": 90,
    "innovative": 95,
    "pessimistic": -45,
    "optimistic": 45,
    "realistic": 70,
    "idealistic": 50,
    "pragmatic": 40,
    "visionary": 60,
    "cynical": -50,
    "trusting": 35,
    "curious": 20,
    "adventurous": 30,
    "cautious": -20,
    "skeptical": -25,
    "decisive": 25,
    "indecisive": -15
}

# Dictionary to map each tag to its opposite
opposites_dict = {
    "hateful": "kind",
    "dumb": "smart",
    "intelligent": "dumb",
    "greedy": "generous",
    "narcissistic": "selfless",
    "egoistic": "egoless",
    "impulsive": "calm",
    "rational": "irrational",
    "fanatic": "sympathetic",
    "apathetic": "empathetic",
    "indifferent": "leader",
    "pessimistic": "optimistic",
    "cynical": "trusting",
    "skeptical": "curious",
    "cautious": "adventurous",
    "indecisive": "decisive"
}


# List of groups of tags with similar meanings
similar_tags_groups = [
    {"smart", "intelligent"},
    {"creative", "innovative"},
    {"rational", "logical"},
    {"realistic", "pragmatic"},
    {"visionary", "idealistic"}
]



weights = np.array([weights_dict[tag] for tag in tag_list])

mean = np.mean(weights)
std_dev = np.std(weights)

gaussian_dist = np.random.normal(mean, std_dev, 100000)

def map_to_tag(value):
    closest_weight = min(weights, key=lambda x:abs(x-value))
    return tag_list[weights.tolist().index(closest_weight)]

assigned_tags = [map_to_tag(value) for value in gaussian_dist]

previously_selected_tags = set()

def is_valid_tag(tag, selected_tags):
    if tag in selected_tags:
        print(f"Tag {tag} is already selected.")
        return False
    if tag in opposites_dict and opposites_dict[tag] in selected_tags:
        print(f"Tag {tag} is opposite of {opposites_dict[tag]} which is already selected.")
        return False
    for group in similar_tags_groups:
        if tag in group and any(similar_tag in selected_tags for similar_tag in group):
            print(f"Tag {tag} is similar to one of {group} which is already selected.")
            return False
    return True

selected_tags =[]

for tag in assigned_tags:
    if is_valid_tag(tag, previously_selected_tags):
        selected_tags.append(tag)
        previously_selected_tags.add(tag)
    if len(selected_tags) >= 9:
        break

# selected_tags = random.sample([tag for tag in assigned_tags if tag not in previously_selected_tags], 9 - len(previously_selected_tags))
# previously_selected_tags.update(selected_tags)
print(previously_selected_tags)

sns.kdeplot(gaussian_dist, fill=True)
plt.xlabel("Weight")
plt.ylabel("Density")





def get_tag_from_weight(value):
    """Map a weight to its closest tag."""
    closest_weight = min(weights, key=lambda x: abs(x - value))
    return tag_list[weights.tolist().index(closest_weight)]


def generate_unique_tags(gaussian_dist, number_of_tags=9, existing_tag_sets=None):
    """
    Generate a unique set of tags for an AI.
    Ensures no AI has an identical set of tags to another AI.

    :param gaussian_dist: Gaussian distribution for tag weights.
    :param number_of_tags: How many tags to generate.
    :param existing_tag_sets: Set of previously assigned tag sets to avoid duplication.
    :return: A unique list of tags.
    """
    if existing_tag_sets is None:
        existing_tag_sets = []

    # Generate a candidate set of tags
    candidate_tags = set()
    while len(candidate_tags) < number_of_tags:
        # Get a tag from the Gaussian distribution
        value = np.random.choice(gaussian_dist)
        tag = get_tag_from_weight(value)
        candidate_tags.add(tag)

    # Check if this list is already used
    if candidate_tags in existing_tag_sets:
        # If duplicate, recurse until a unique set is found
        return generate_unique_tags(gaussian_dist, number_of_tags, existing_tag_sets)

    # Save the unique tag set and return it
    existing_tag_sets.append(candidate_tags)
    return list(candidate_tags)

plt.show()


def get_weight_distribution():
    """Creates Gaussian distribution for weights."""
    mean = np.mean(weights)
    std_dev = np.std(weights)
    return np.random.normal(mean, std_dev, 100000)