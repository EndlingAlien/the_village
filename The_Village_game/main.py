# main game loop, logic, UI, etc
import scenes as sc
import random as r

# region Variables

# TODO: change test_dict instances to game_condition when done testing
# game_condition = initialize_game_conditions(condition_dict)
test_dict = {
    "farm": 'farmer_in_barn',
    "swamp": 'light_fog',
    "church": 'basement_open'
}

# region Scene Vars
farm_scene = sc.farm_scene_dict
church_scene = sc.church_scene_dict
swamp_scene = sc.swamp_scene_dict
center_scene = sc.center_scene_dict
start_scene = sc.start_scene_dict
# endregion

# dict containing all possible conditions for respective scenes
condition_dict = {
    "farm": ['farmer_in_house', 'farmer_outside', 'farmer_in_barn'],
    "swamp": ['heavy_fog', 'light_fog', 'no_fog'],
    "church": ['church_is_empty', 'priest_inside', 'basement_open']
}
# for load_info to load the proper scene
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
# purely for making life easy in load_test
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
# Answers to trust test and thresholds for faith and intuition tests
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
        8: "curious",  # 8 to 9 → passed
        5: "pass",  # 5 to 7 → survived
        0: "boring"  # 0 to 5 → failed
    },

}
# these get added to inventory in key item scenes
key_items = {
    "decoder": {
        "desc": "a paper you found at the church, it has a table showing how to decode symbols",
        "type": "lore",
        "effect": "You might be able to use this to read unknown markings"
    },
    "mask": {
        "desc": "a creepy mask you found in the barn of the farm",
        "type": "tool",
        "effect": "Wearing it might let you blend in..."
    },
    "bible": {
        "desc": "A bible from the church, its covered in pale yellow leather.",
        "type": "lore",
        "effect": "contains information pertaining to this village"
    },
    "letter": {
        "desc": "A letter from the farmhouse",
        "type": "lore",
        "effect": "it reads: 'Father micheal requests your presence at 9pm sharp for preperation of the chosen' "
    },
    "hammer": {
        "desc": "A hammer you found at the swamp, its rusty.",
        "type": "tool",
        "effect": "Not just a tool..."
    },
    "key": {
        "desc": "A small rusty key from the swamp, hidden in the mud.",
        "type": "tool",
        "effect": "What could this possibly unlock?"
    },
    "screwdriver": {
        "desc": "Surprisingly shiny, as if its never been used",
        "type": "tool",
        "effect": "Could be useful..."
    },
    "knife": {
        "desc": "A knife from the farmhouse",
        "type": "tool",
        "effect": "Its been used...a lot."
    }
}
# Checks in load_info if checkpoint_name is a test
test_checkpoint_names = ['trust_test', 'faith_test', 'intuition_test']


# endregion

# TODO: keep track of: what choices theyve made (-done for everything) *This will go in final_stats*
# TODO: Implement persistent flags and save system to prevent repeated ending dialogue on reload
#  ^^^^^^(cant fully test until, scenes.py dict tags are updated [pretty sure its fixed now])

# TODO: Remember: Ending_Key in scene_dicts used for ending_catalogue at player death
#  to see what they got/achieved(exception:deaths that still let you continue the game
#  Menu should let you read what full desc in final version

# region Functions
def initialize_game_conditions(cond_dict):
    """
    Assigns the dynamic conditions to the scenes at the beginning of the game
    :param cond_dict: conditional dictionary holding game conditions
    """
    return {con: r.choice(options) for con, options in condition_dict.items()}


def load_info(scene, scene_name, checkpoint_key):
    """
    In charge of loading the correct dialogue and options from checkpoint keyword
    :param scene: scene dictionary to search within
    :param scene_name: the name of scene to search
    :param checkpoint_key: name of key in scene dictionary
    """
    current_cond = test_dict.get(scene_name, None)
    checkpoint_data = scene.get(checkpoint_key, {})

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

    # Loop until valid input is received
    valid_input = False
    while not valid_input:
        try:
            x = int(input("Choose an option: "))
            for key in choices:
                if x == choices[key]['id']:
                    follow_text = choices[key].get('follow_up_text') or ''
                    next_cp = choices[key]['next_checkpoint']
                    next_scene = choices[key]['checkpoint_scene']
                    scene_name = scene_dict[next_scene]
                    print(follow_text)
                    if next_cp in test_checkpoint_names:
                        load_test(scene_name, next_cp)
                    elif '_ending' in next_cp:
                        load_ending(scene_name, next_cp)
                    else:
                        load_info(scene_name, next_scene, next_cp)
                    valid_input = True
                    break  # exit for-loop
            if not valid_input:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")


def load_test(scene, checkpoint_key):
    """
    In charge of loading the correct dialogue and options from tests
    :param scene: scene dictionary to search within
    :param checkpoint_key: name of key in scene dictionary
    """
    index = 0
    test_choices = {}
    test_name = checkpoint_key.split('_')[0]
    test_answers = test_answers_dict[test_name]
    key_amount = list(scene.get(checkpoint_key, {}))

    print()
    while index < len(key_amount):
        test_data = scene.get(checkpoint_key, {})
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

        valid_input = False
        while not valid_input:
            try:
                x = int(input("Choose an option: "))
                # store tag and choice in dict
                if tag:
                    test_choices[tag] = x
                else:
                    print("Warning: question missing tag, answer not recorded")

                # Find matching choice and load follow-up
                for key in choices:
                    if x == choices[key]['id']:
                        follow_text = choices[key].get('follow_up_text') or ''
                        print(follow_text)
                        valid_input = True
                        break  # exit for-loop
                if not valid_input:
                    print("Invalid choice. Try Again.")
            except ValueError:
                print("Please enter a number")
        index += 1
    # When you finish the test, calculate choices
    if test_name == 'trust':
        calculate_trust_result(test_answers, test_choices)
    elif test_name == 'faith':
        calculate_faith_result(test_answers, test_choices)
    elif test_name == 'intuition':
        calculate_intuition_result(test_answers, test_choices)


# region Calculate Test Results
# TODO: dialogue repeats for load_info call in all func endings
def calculate_trust_result(test_answers, test_choices):
    # make sure you hold onto the players answers for data analysis report
    trust_test_choices = test_choices

    correct = 0
    for key, answer in test_answers.items():
        if test_choices.get(key) == answer:
            correct += 1
    print(correct)
    match correct:
        case 9:
            load_ending(farm_scene, 'trust_ending')
        case _ if correct >= 7:
            load_ending(farm_scene, 'kindness_ending')
        case _ if correct < 7:
            load_info(farm_scene, 'farm', 'fail_choice')


def calculate_faith_result(test_answers, test_choices):
    # make sure you hold onto the players answers for data analysis report
    faith_test_choices = test_choices

    score = sum(test_choices.values())
    for threshold in sorted(test_answers.keys(), reverse=True):
        if score >= threshold:
            break
    match score:
        case _ if score >= 15:
            load_ending(church_scene, 'believer_ending')
        case _ if score >= 10:
            load_ending(church_scene, 'faith_ending')
        case _ if score < 10:
            load_ending(church_scene, 'heretics_ending')


def calculate_intuition_result(test_answers, test_choices):
    # make sure you hold onto the players answers for data analysis report
    intuition_test_choices = test_choices

    score = sum(test_choices.values())
    for threshold in sorted(test_answers.keys(), reverse=True):
        if score >= threshold:
            break
    match score:
        case _ if score >= 8:
            load_info(swamp_scene, 'swamp', 'make_choice')
        case _ if score >= 5:
            load_ending(swamp_scene, 'probed_ending')
        case _ if score < 5:
            load_ending(swamp_scene, 'rejected_ending')


# endregion


def load_ending(scene, checkpoint_key):
    active_block = scene.get(checkpoint_key)
    dialogue = active_block.get('dialogue')
    if active_block.get('next_checkpoint') and active_block.get('checkpoint_scene'):
        scene_name = scene_dict[active_block.get('checkpoint_scene')]
        cp_name = active_block.get('checkpoint_scene')
        cp = active_block.get('next_checkpoint')
        print(dialogue)
        load_info(scene_name, cp_name, cp)
    print(dialogue)

    # add ending flag to db
    # need a flag for below cause some endings dont finish the game< we need to know when the game is done
    # will eventually call a func that will do a quick analysis on player choices


# endregion


# for testing
# load_test(swamp_scene, 'intuition_test')

# load_info(farm_scene, 'farm', 'intro')

# __________________________TESTING AREA________________________________
# TODO: Get started on sqLite db for save mech



player_stats = {
    "explore_flag": {  # all start as False, game changes them to True
        "has_snooped_house": False,
        "has_snooped_barn": False,
        "has_snooped_church": False,
        "has_snooped_swamp": False,
        "has_all_vials": False
    },
    "inventory": {  # Needs to be empty when game starts /// Below is for testing
        "letter": "hello",
        "knife": "hello"
    },
    "choices": {  # all will stay as None, final check will ask: if choices[key] =! None -> save to db
        "vials_choice": None,
        "cube_choice": None,
        "curious_choice": None,
        "basement_choice": None,
        "basement_choice_two": None,
        "start_choice": None,
        "knock_choice": None,
        "meet_choice": None,
    }
}

final_stats = {}

#backup of test_func while messing around adding more checks
def test_func_backup(scene, scene_name, checkpoint_key):
    """
    In charge of loading the correct dialogue and options from checkpoint keyword
    :param scene: scene dictionary to search within
    :param scene_name: the name of scene to search
    :param checkpoint_key: name of key in scene dictionary
    """
    # region Get initial info
    current_cond = test_dict.get(scene_name, None)
    checkpoint_data = scene.get(checkpoint_key, {})

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
        # check if the option can be displayed
        if choices[key].get('is_displayed', True):
            print(f"{choices[key]['id']}: {choices[key]['Text']}")
    # endregion

    # Loop until valid input is received
    valid_input = False
    while not valid_input:
        try:
            x = int(input("Choose an option: "))
            for main_key in choices:
                if x == choices[main_key]['id']:
                    if 'locked' in choices[main_key]:
                        locked_info = choices[main_key]['locked']
                        allow_progress = False  # Assume blocked

                        # region Key Checks
                        # 1. Check if been used (hard lock override)
                        if locked_info.get('been_used', False):
                            print('has been used')
                            allow_progress = False  # force block

                        # 2. Check explore_flag
                        if 'explore_flag' in locked_info:
                            print('has explore tag')
                            flags = locked_info['explore_flag']
                            for key in flags:
                                if key in player_stats['explore_flag']:
                                    if flags[key] == player_stats['explore_flag'][key]:
                                        print('explore flag matches')
                                        allow_progress = True
                                    else:
                                        print('explore flag mismatch')

                        # 3. Check inventory_need
                        if 'inventory_need' in locked_info:
                            print('has inventory tag')
                            need = locked_info['inventory_need']
                            for key in need:
                                if key in player_stats['inventory']:
                                    print('found key in player inventory')
                                    allow_progress = True
                                else:
                                    print(f'missing item: {key}')

                        # endregion

                        # FINAL DECISION
                        if allow_progress:
                            follow_text = choices[main_key].get('follow_up_text') or ''
                            next_cp = choices[main_key]['next_checkpoint']
                            next_scene = choices[main_key]['checkpoint_scene']
                            scene_name = scene_dict[next_scene]
                            print(follow_text)

                            if next_cp in test_checkpoint_names:
                                load_test(scene_name, next_cp)
                            elif '_ending' in next_cp:
                                load_ending(scene_name, next_cp)
                            else:
                                test_func(scene_name, next_scene, next_cp)
                        else:
                            print("locked info displayed")
                            text = locked_info['locked_text']
                            next_cp = locked_info['locked_checkpoint']
                            next_scene = locked_info['locked_scene']
                            scene_name = scene_dict[next_scene]
                            print(text)
                            test_func(scene_name, next_scene, next_cp)

                        valid_input = True
                        break  # break the for-loop

                    else:
                        # No locked key, display the normal option
                        print('display normal shit')
                        follow_text = choices[main_key].get('follow_up_text') or ''
                        next_cp = choices[main_key]['next_checkpoint']
                        next_scene = choices[main_key]['checkpoint_scene']
                        scene_name = scene_dict[next_scene]
                        print(follow_text)
                        if next_cp in test_checkpoint_names:
                            load_test(scene_name, next_cp)
                        elif '_ending' in next_cp:
                            load_ending(scene_name, next_cp)
                        else:
                            test_func(scene_name, next_scene, next_cp)
                        valid_input = True
                        break

            if not valid_input:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")

#TODO: Clean this before starting Save Mechs
# future load info
# need to break this down at some point, its huge
def test_func(scene, scene_name, checkpoint_key):
    """
    In charge of loading the correct dialogue and options from checkpoint keyword
    :param scene: scene dictionary to search within
    :param scene_name: the name of scene to search
    :param checkpoint_key: name of key in scene dictionary
    """
    # region Get initial info
    current_cond = test_dict.get(scene_name, None)
    checkpoint_data = scene.get(checkpoint_key, {})
    global final_stats

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
        # check if the option can be displayed
        if choices[key].get('is_displayed', True):
            print(f"{choices[key]['id']}: {choices[key]['Text']}")
    # endregion

    # Loop until valid input is received
    valid_input = False
    while not valid_input:
        try:
            x = int(input("Choose an option: "))
            for main_key in choices:
                if x == choices[main_key]['id']:
                    if 'locked' in choices[main_key]:
                        locked_info = choices[main_key]['locked']
                        allow_progress = False  # Assume blocked

                        # region Key Checks
                        # 1. Check if been used (hard lock override)
                        if locked_info.get('been_used', False):
                            print('has been used')
                            allow_progress = False  # force block

                        # 2. Check explore_flag
                        if 'explore_flag' in locked_info:
                            print('has explore tag')
                            flags = locked_info['explore_flag']
                            for key in flags:
                                if key in player_stats['explore_flag']:
                                    if flags[key] == player_stats['explore_flag'][key]:
                                        print('explore flag matches')
                                        allow_progress = True
                                    else:
                                        print('explore flag mismatch')

                        # 3. Check inventory_need
                        if 'inventory_need' in locked_info:
                            print('has inventory tag')
                            need = locked_info['inventory_need']
                            for key in need:
                                if key in player_stats['inventory']:
                                    print('found key in player inventory')
                                    allow_progress = True
                                else:
                                    print(f'missing item: {key}')

                        # endregion

                        # FINAL DECISION
                        if allow_progress:
                            follow_text = choices[main_key].get('follow_up_text') or ''
                            next_cp = choices[main_key]['next_checkpoint']
                            next_scene = choices[main_key]['checkpoint_scene']
                            scene_name = scene_dict[next_scene]
                            print(follow_text)

                            #region Second round of Key Checks
                            # TODO: BELOW IMPORTANT [FOR FINAL ANALYSIS]
                            #This changes player_stats explore flags
                            if 'has_been' in choices[main_key]:
                                if choices[main_key]['has_been'] in player_stats['explore_flag']:
                                    player_flags = player_stats['explore_flag']
                                    has_key = choices[main_key]['has_been']
                                    player_stats['explore_flag'][has_key] = not player_flags[has_key]

                            #this adds items to the player_stats inventory
                            if 'inventory_need' in locked_info:
                                print('has inventory tag 2.0')
                                need = locked_info['inventory_need']
                                for key in need:
                                    player_stats['inventory'][key] = key_items[key]

                            #adds decision tag to player_stats
                            if 'tag' in active_block:
                                tag = active_block['tag']
                                player_stats['choices'][tag] = x
                            #endregion

                            if next_cp in test_checkpoint_names:
                                load_test(scene_name, next_cp)
                            elif '_ending' in next_cp:
                                load_ending(scene_name, next_cp)
                            else:
                                # TODO: change after testing
                                test_func(scene_name, next_scene, next_cp)
                        else:
                            print("locked info displayed")
                            text = locked_info['locked_text']
                            next_cp = locked_info['locked_checkpoint']
                            next_scene = locked_info['locked_scene']
                            scene_name = scene_dict[next_scene]
                            print(text)
                            # TODO: change after testing
                            test_func(scene_name, next_scene, next_cp)
                        valid_input = True
                        break  # break the for-loop
                    else:
                        # No locked key, display the normal option
                        print('display normal shit')
                        follow_text = choices[main_key].get('follow_up_text') or ''
                        next_cp = choices[main_key]['next_checkpoint']
                        next_scene = choices[main_key]['checkpoint_scene']
                        scene_name = scene_dict[next_scene]
                        print(follow_text)

                        # TODO: save to db either here or in possible death func
                        # adds decision tag to player_stats
                        if 'tag' in active_block:
                            tag = active_block['tag']
                            player_stats['choices'][tag] = x

                        if next_cp in test_checkpoint_names:
                            load_test(scene_name, next_cp)
                        elif '_ending' in next_cp:
                            load_ending(scene_name, next_cp)
                        else:
                            # TODO: change after testing
                            test_func(scene_name, next_scene, next_cp)
                        valid_input = True
                        break
            if not valid_input:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")


#test_func(farm_scene, 'farm', 'meet_farmer')
test_func(start_scene, 'start', 'house_key_items')


