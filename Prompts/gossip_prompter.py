


def gossip_prompt(perp_karma, target_karma, sentiment):
    return f"""PERP_KARMA: {perp_karma}  
               VICTIM_KARMA: {target_karma}
               SENTIMENT: {sentiment}"""
    # return f"{perp} {action} > {target} | {traits} | {perp_karma} {target_karma}"

