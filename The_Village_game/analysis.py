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
        print('arch is incon')

    print(archetype_dict)


def calc_trust_test_archetype(num_of_correct):
    match num_of_correct:
        case 9:
            print('Chosen material')
        case _ if num_of_correct >= 7:
            print('just a person')
        case _ if num_of_correct < 7:
            print('Disrespectful')


def calc_faith_test_archetype(test_results):
    list_of_choices = list(test_results.values())
    majority_answer = Counter(list_of_choices).most_common()[0][0]
    if majority_answer[0][1] == majority_answer[1][1] and majority_answer[0][1] == majority_answer[2][1]:
        print('unable to read')
    match majority_answer[0][0]:
        case 3:
            print('you lost')
        case 2:
            print('your independent')
        case 1:
            print('unbending')


def calc_intuition_test_archetype(test_results):
    list_of_choices = list(test_results.values())
    majority_answer = Counter(list_of_choices).most_common()
    if majority_answer[0][1] == majority_answer[1][1] and majority_answer[0][1] == majority_answer[2][1]:
        print('your cautious')
    else:
        match majority_answer[0][0]:
            case 3:
                print('you curious')
            case 1:
                print('your scared')


calc_choice_archetype(choices_list)
