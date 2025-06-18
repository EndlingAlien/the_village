# where to calc stuff for end game analysis
from collections import Counter

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
    archetype_dict = {
        "stupid": 0,
        "observant": 0,
        "smart": 0,
        "timid": 0
    }

    for key in choices:

        if key in stupid_arch:
            if stupid_arch[key] == choices[key]:
                archetype_dict['stupid'] += 1

        if key in observant_arch:
            if observant_arch[key] == choices[key]:
                archetype_dict['observant'] += 1

        if key in smart_arch:
            if smart_arch[key] == choices[key]:
                archetype_dict['smart'] += 1

        if key in timid_arch:
            if timid_arch[key] == choices[key]:
                archetype_dict['timid'] += 1

    arch = Counter(archetype_dict).most_common()
    if arch[0][1] == arch[1][1] or arch[0][1] == arch[2][1]:
        return 'wild'
    return arch[0][0]


def calc_trust_test_archetype(num_of_correct):
    match num_of_correct:
        case 9:
            return 'chosen'
        case _ if num_of_correct >= 7:
            return 'average'
        case _ if num_of_correct < 7:
            return 'disrespectful'


def calc_faith_test_archetype(test_results):
    list_of_choices = list(test_results.values())
    majority_answer = Counter(list_of_choices).most_common(3)
    # Handle tiebreaker: all top three have same count
    if len(majority_answer) >= 3 and majority_answer[0][1] == majority_answer[1][1] == majority_answer[2][1]:
        return 'unreadable'

    top_choice = majority_answer[0][0]

    match top_choice:
        case 3:
            return 'lost'
        case 2:
            return "independent"
        case 1:
            return 'unbending'


def calc_intuition_test_archetype(test_results):
    list_of_choices = list(test_results.values())
    majority_answer = Counter(list_of_choices).most_common(3)
    # Handle tiebreaker: all top three have same count
    if len(majority_answer) >= 3 and majority_answer[0][1] == majority_answer[1][1] == majority_answer[2][1]:
        return 'cautious'
    else:
        top_choice = majority_answer[0][0]
        match top_choice:
            case 3:
                return 'curious'
            case 1:
                return 'spineless'