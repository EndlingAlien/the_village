"""
analysis.py desc:

    Responsible for calculating and determining player archetypes based on test results
    (trust, faith, intuition) and in-game choices.
    Outputs archetype labels for use in the final player stats analysis.
"""

from collections import Counter

#region Archetype Dictionaries
# Each dictionary maps which option needs to be picked for each choice to count toward a specific archetype.
stupid_arch = {
    "vials_choice": 1,
    "basement_door_choice": 3,
    "basement_choice": 1,
    "basement_two_choice": 3,
    "knock_choice": 2,
    "meet_choice": 1,
}
observant_arch = {
    "vials_choice": 2,
    "cube_choice": 1,
    "curious_choice": 1,
    "basement_choice": 4,
    "start_choice": 2,
    "break_choice": 1
}
smart_arch = {
    "cube_choice": 2,
    "curious_choice": 2,
    "basement_door_choice": 1,
    "basement_choice": 2,
    "basement_two_choice": 2,
    "knock_choice": 1,
}
timid_arch = {
    "basement_door_choice": 2,
    "basement_choice": 3,
    "basement_two_choice": 1,
    "start_choice": 1,
    "knock_choice": 3,
    "break_choice": 2
}
#endregion

#TODO: choices_list for testing, use player_stats['choices']
choices_list = {  # all will stay as None, final check will ask: if choices[key] =! None -> save to db
    "vials_choice": 1,
    "cube_choice": 1,
    "curious_choice": 2,
    "basement_door_choice": 3,
    "basement_choice": 3,
    "basement_two_choice": 2,
    "start_choice": 1,
    "knock_choice": 2,
    "meet_choice": 2,
    "break_choice": 1
}


def calc_choice_archetype(choices):
    """
    Determines the player's dominant archetype based on their choices in the game.
    :param choices: Dictionary of player choices (key: choice tag, value: choice ID)
    :return: String representing the dominant archetype, or 'wild' if there's a tie
    """
    # Initialize counters for each archetype
    archetype_dict = {
        "stupid": 0,
        "observant": 0,
        "smart": 0,
        "timid": 0
    }

    # Tally points for matching choice IDs in each archetype category
    for key in choices:
        if key in stupid_arch and stupid_arch[key] == choices[key]:
            archetype_dict['stupid'] += 1
        if key in observant_arch and observant_arch[key] == choices[key]:
            archetype_dict['observant'] += 1
        if key in smart_arch and smart_arch[key] == choices[key]:
            archetype_dict['smart'] += 1
        if key in timid_arch and timid_arch[key] == choices[key]:
            archetype_dict['timid'] += 1

    # Get archetype with the highest count
    arch = Counter(archetype_dict).most_common()

    # Handle ties (if top 2 or top 3 are equal)
    if arch[0][1] == arch[1][1] or arch[0][1] == arch[2][1]:
        return 'wild'
    return arch[0][0]


def calc_trust_test_archetype(num_of_correct):
    """
    Categorizes the player's trust archetype based on the number of correct answers.
    :param num_of_correct: Integer count of correct answers (0–9)
    :return: String representing the player's trust archetype
    """
    match num_of_correct:
        case 9:
            return 'chosen'  # Perfect score
        case _ if num_of_correct >= 7:
            return 'average'  # Mostly right
        case _ if num_of_correct < 7:
            return 'disrespectful'  # Failed the test


def calc_faith_test_archetype(test_results):
    """
    Determines the player's faith archetype based on the majority of their answers.
    :param test_results: Dictionary of question tags and chosen answer values (1, 2, or 3)
    :return: String representing the player's faith archetype
    """
    list_of_choices = list(test_results.values())

    # Find the most common answers
    majority_answer = Counter(list_of_choices).most_common(3)

    # If all top three answers have equal count → unreadable
    if len(majority_answer) >= 3 and majority_answer[0][1] == majority_answer[1][1] == majority_answer[2][1]:
        return 'unreadable'

    top_choice = majority_answer[0][0]

    match top_choice:
        case 3:
            return 'lost'  # Open-minded, susceptible
        case 2:
            return "independent"  # Balanced, rational
        case 1:
            return 'unbending'  # Rigid in belief or skepticism


def calc_intuition_test_archetype(test_results):
    """
    Determines the player's intuition archetype based on the majority of their answers.
    :param test_results: Dictionary of question tags and chosen answer values (1, 2, or 3)
    :return: String representing the player's intuition archetype
    """
    list_of_choices = list(test_results.values())

    # Find the most common answers
    majority_answer = Counter(list_of_choices).most_common(3)

    # If all top three answers are equal in frequency → cautious
    if len(majority_answer) >= 3 and majority_answer[0][1] == majority_answer[1][1] == majority_answer[2][1]:
        return 'cautious'

    top_choice = majority_answer[0][0]

    match top_choice:
        case 3:
            return 'curious'  # Willing to explore the unknown
        case 1:
            return 'spineless'  # Overly hesitant or fearful
