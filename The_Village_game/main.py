# main game loop, logic, UI, etc
import scenes as sc
import random as r

# region Variables


farm_scene = sc.farm_scene_dict
church_scene = sc.church_scene_dict
swamp_scene = sc.swamp_scene_dict
center_scene = sc.center_scene_dict
start_scene = sc.start_scene_dict

# dict containing all possible conditions for respective scenes
condition_dict = {
    "farm": ['farmer_in_house', 'farmer_outside', 'farmer_in_barn'],
    "swamp": ['heavy_fog', 'light_fog', 'no_fog'],
    "church": ['church_is_empty', 'priest_inside', 'basement_open']
}

# TODO: change test_dict instances to game_condition when done testing
# game_condition = initialize_game_conditions(condition_dict)
test_dict = {
    "farm": 'farmer_in_house',
    "swamp": 'light_fog',
    "church": 'priest_inside'
}

scene_dict = {
    "farm": farm_scene,
    "swamp": swamp_scene,
    "church": church_scene,
    "center": center_scene,
    "start": start_scene
}

# for later use in db
ending_flags = {
    "cleansed": False,
    "vessel": False,
    "rejected": False,
    "probed": False,
    "you_belong": False,
    "intuition_pass": False,
    "believer": False,
    "faith_pass": False,
    "heretic": False,
    "priest_death": False,
    "altar": False,
    "butcher": False,
    "kindness": False,
    "self_defense": False,
    "tainted_meat": False,
    "trust_pass": False
}

#purely for making life easy in load_test
questions = [
    "question_1",
    "question_2",
    "question_3",
    "question_4",
    "question_5",
    "question_6",
    "question_7",
    "question_8",
    "question_9"
]

#answer to trust and thresholds for faith and intuition
test_answers_dict = {
    "trust": {
        "trust_1": 2,
        "trust_2": 1,
        "trust_3": 2,
        "trust_4": 1,
        "trust_5": 2,
        "trust_6": 1,
        "trust_7": 1,
        "trust_8": 2,
        "trust_9": 1
    },
    'faith': {
        15: "believer",  # 15 to 18 → join
        10: "pass",  # 10 to 14 → passed
        0: "death"  # 0 to 9 → failed
    },
    'intuition': {
        8: "curious",
        5: "pass",
        0: "boring"
    },

}


# endregion

# TODO: go through tests, change answers around, make func for each test to calculate score and assign correct ending
# TODO: keep track of: what player has in inventory, where they've explored, what choices theyve made
# TODO: still need to create logic for locked text vs follow up
# TODO: if user does input something valid catch it

# region Functions
def initialize_game_conditions(cond_dict):
    """
    Assigns the dynamic conditions to the scenes at the beginning of the game
    :param cond_dict: conditional dictionary holding game conditions
    """
    return {con: r.choice(options) for con, options in condition_dict.items()}


def load_info(dic, scene_name, checkpoint_key):
    """
    In charge of loading the correct dialogue and options from checkpoint keyword
    :param dic: scene dictionary to search within
    :param scene_name: the name of scene to search
    :param checkpoint_key: name of key in scene dictionary
    """
    current_cond = test_dict.get(scene_name, None)
    checkpoint_data = dic.get(checkpoint_key, {})

    # Determine if this checkpoint uses conditional branching
    if current_cond and current_cond in checkpoint_data:
        print('conditional\n')  # testing
        active_block = checkpoint_data[current_cond]

        # fallback to base choices if conditional has no choices
        choices = active_block.get('choices')
        if choices is None:
            choices = checkpoint_data.get('choices', {})
    else:
        print('typical\n')  # testing
        active_block = checkpoint_data
        choices = active_block.get('choices', {})

    # Get dialogue (fallback if None)
    dialogue = active_block.get('dialogue') or ''
    print(dialogue)

    # Display choices
    for key in choices:
        print(f"{choices[key]['id']}: {choices[key]['Text']}")

    # Get user input
    x = int(input("Choose an option: "))

    # Find matching choice and load follow-up
    for key in choices:
        if x == choices[key]['id']:
            follow_text = choices[key]['follow_up_text']
            next_cp = choices[key]['next_checkpoint']
            next_scene = choices[key]['checkpoint_scene']
            print(follow_text)
            load_info(scene_dict[next_scene], next_scene, next_cp)
            break
    else:
        print("Invalid choice.")  # Optional: if no match found


def load_test(dic, checkpoint_key):
    index = 0
    test_choices = {}
    test_name = checkpoint_key.split('_')[0]
    test_answers = test_answers_dict[test_name]
    key_amount = dic.get(checkpoint_key, {}).keys()

    print()
    while index < len(key_amount):
        test_data = dic.get(checkpoint_key, {})
        question_data = test_data.get(questions[index], {})

        # Get tag for choice dict
        tag = question_data.get('tag', '')

        # Get and print the dialogue
        dialogue = question_data.get('dialogue', '')
        print(f"\n{dialogue}\n")

        # Get and print choices
        choices = question_data.get('choices', {})
        for choice_key, choice_data in choices.items():
            print(f"{choice_data['id']}: {choice_data['Text']}")

        x = int(input("Choose an option: "))
        # store tag and choice in dict
        test_choices[tag] = x

        # Find matching choice and load follow-up
        for key in choices:
            if x == choices[key]['id']:
                follow_text = choices[key].get('follow_up_text') or ''
                print(follow_text)
                break
        else:
            print("Invalid choice.")  # Optional: if no match found

        index += 1
    # when you finish the test calculate choices to see how many you got right/wrong
    if test_name == 'trust':
        calculate_trust_result(test_answers, test_choices)
    elif test_name == 'faith':
        calculate_faith_result(test_answers, test_choices)
    elif test_name == 'intuition':
        calculate_intuition_result(test_answers, test_choices)


#region Calculate Test Results
def calculate_trust_result(test_answers, test_choices):
    # make sure you hold onto the players answers for data analysis report
    trust_test_choices = test_choices

    correct = 0
    for key, answer in test_answers.items():
        if test_choices.get(key) == answer:
            correct += 1
    print(correct)
    # redirect to correct ending


def calculate_faith_result(test_answers, test_choices):
    # make sure you hold onto the players answers for data analysis report
    faith_test_choices = test_choices

    score = sum(test_choices.values())
    for threshold in sorted(test_answers.keys(), reverse=True):
        if score >= threshold:
            print(test_answers[threshold])
            break


def calculate_intuition_result(test_answers, test_choices):
    # make sure you hold onto the players answers for data analysis report
    intuition_test_choices = test_choices

    score = sum(test_choices.values())
    for threshold in sorted(test_answers.keys(), reverse=True):
        if score >= threshold:
            print(test_answers[threshold])
            break

#endregion

# endregion




load_test(swamp_scene, 'intuition_test')

# load_info(start_scene, None, 'intro')
# load_checkpoint(farm_scene, 'farm', 'start_position')
