# main game loop, logic, UI, etc
import scenes as sc
import ending_catalogue as ec
import random as r
import analysis as a

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
    },
    "red_vial": {
        "desc": "A small vial filled with red liquid. It shimmers in the light...",
        "type": "tool",
        "effect": "Why would the farmer give you this?"
    },
    "blue_vial": {
        "desc": "A small vial filled with blue liquid. It shimmers in the light...",
        "type": "tool",
        "effect": "Why would the aliens give you this?"
    },
    "green_vial": {
        "desc": "A small vial filled with green liquid. It shimmers in the light...",
        "type": "tool",
        "effect": "Why would the priest give you this?"
    }
}
# Checks in load_info if checkpoint_name is a test
test_checkpoint_names = ['trust_test', 'faith_test', 'intuition_test']


# endregion

# TODO: keep track of: what choices they've made (-done for everything) *This will go in final_stats*

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
def calculate_trust_result(test_answers, test_choices):
    # make sure you hold onto the players answers for data analysis report
    trust_test_choices = test_choices
    final_stats['tests']['trust_test_choices'] = trust_test_choices
    a.calc_trust_test_archetype(test_choices)

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
            test_func(farm_scene, 'farm', 'fail_choice')


def calculate_faith_result(test_answers, test_choices):
    # make sure you hold onto the players answers for data analysis report
    faith_test_choices = test_choices
    final_stats['tests']['faith_test_choices'] = faith_test_choices

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
    final_stats['tests']['intuition_test_choices'] = intuition_test_choices

    score = sum(test_choices.values())
    for threshold in sorted(test_answers.keys(), reverse=True):
        if score >= threshold:
            break
    match score:
        case _ if score >= 8:
            test_func(swamp_scene, 'swamp', 'make_choice')
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
        end_key = active_block.get('ending_key')
        print(dialogue)
        # add check for after killed farmer and priest and add key to player_stats
        # TODO: change to game_condition after testing
        test_dict[cp_name] = end_key
        player_stats['ending_key'][end_key] = ec.endings[end_key]
        scene = sc.return_scene(cp_name + '_scene_dict')
        scene['intro']['choices']['option_one']['next_checkpoint'] = 'after_test_start'
        #for the vials
        if active_block.get('inventory_need'):
            for key in active_block['inventory_need']:
                player_stats['inventory'][key] = key_items[key]
        # TODO: change to load_info after testing
        test_func(scene_name, cp_name, cp)
    print(dialogue)
    final_stats['player_stats'] = player_stats

# endregion


# __________________________TESTING AREA________________________________
# TODO: Get started on sqLite db for save mech


player_stats = {
    "explore_flag": {  # all start as False, game changes them to True
        "snooped_house": False,
        "snooped_barn": False,
        "snooped_church": False,
        "snooped_swamp": False,
    },
    "inventory": {  # Needs to be empty when game starts /// Below is for testing

    },
    "choices": {  # all will stay as None, final check will ask: if choices[key] =! None -> save to db
        "vials_choice": None,
        "cube_choice": None,
        "curious_choice": None,
        "basement_door_choice": None,
        "basement_choice": None,
        "basement_two_choice": None,
        "start_choice": None,
        "knock_choice": None,
        "meet_choice": None,
        "break_choice": None
    },
    "ending_key": {
        # can hold ending_key to "stack" and 'bring back' to db
        # ex: trust ending -> game continues -> faith ending -> game continues -> rejected specimen -> game over
        # ^^player obtained 3 ending in 1 playthrough
    }
}

#for db
final_stats = {'tests': {},
               'player_stats': {}
               }


# TODO: Clean this before starting Save Mechs
# future load info
# need to break this down at some point, its huge
def test_func(scene, scene_name, checkpoint_key):
    """
    In charge of loading the correct dialogue and options from checkpoint keyword
    :param scene: scene dictionary to search within
    :param scene_name: the name of scene to search
    :param checkpoint_key: name of key in scene dictionary
    """

    # region Initial Setup & Conditional Branching
    current_cond = test_dict.get(scene_name, None)
    checkpoint_data = scene.get(checkpoint_key, {})
    global final_stats

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
    # endregion

    # region Dialogue & Choice Display
    dialogue = active_block.get('dialogue') or ''
    print(dialogue)

    for key in choices:
        should_display = choices[key].get('is_displayed', True)

        if not should_display:
            locked_info = choices[key].get('locked', {})
            explore_valid = False
            inventory_valid = False

            # Check explore_flag
            if 'explore_flag' in locked_info:
                print('found explore tag for display check')
                flags = locked_info['explore_flag']
                explore_valid = all(
                    player_stats['explore_flag'].get(flag_key) == val
                    for flag_key, val in flags.items()
                )
                if explore_valid:
                    print('explore flag matches for display check')

            # Check inventory_need
            if 'inventory_need' in locked_info:
                need = locked_info['inventory_need']
                inventory_valid = all(
                    need_key in player_stats['inventory']
                    for need_key in need
                )
                if inventory_valid:
                    print('found key in player inventory for display check')

            if explore_valid or inventory_valid:
                choices[key]['is_displayed'] = True
                should_display = True

        if should_display:
            print(f"{choices[key]['id']}: {choices[key]['Text']}")
    # endregion

    # region Player Input Loop
    valid_input = False
    while not valid_input:
        try:
            x = int(input("Choose an option: "))

            # region Choice Selection & Lock Checks
            for main_key in choices:
                if x == choices[main_key]['id']:
                    if 'locked' in choices[main_key]:
                        locked_info = choices[main_key]['locked']
                        allow_progress = False  # Assume blocked

                        # region Key Checks

                        # 1. Check explore_flag
                        print("explore_flag CHECK")
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

                        # 2. Check inventory_need
                        print("inventory_need CHECK")
                        if 'inventory_need' in locked_info:
                            print('has inventory tag')
                            need = locked_info['inventory_need']

                            true_keys = [k for k, v in need.items() if v is True]
                            false_keys = [k for k, v in need.items() if v is False]

                            has_required = any(key in player_stats['inventory'] for key in true_keys)
                            has_wrong = any(key in player_stats['inventory'] for key in false_keys)

                            if has_wrong:
                                print("[FAIL] Player has an item they shouldn't.")
                                allow_progress = True
                            elif not has_required and true_keys:
                                print("[FAIL] Player lacks all required items.")
                            else:
                                print("[PASS] Inventory requirement met.")
                                allow_progress = True

                        # endregion

                        #region Final Decision if allowed
                        if allow_progress:
                            print("progress ALLOWED CHECK")
                            follow_text = choices[main_key].get('follow_up_text') or ''
                            next_cp = choices[main_key]['next_checkpoint']
                            next_scene = choices[main_key]['checkpoint_scene']
                            scene_name = scene_dict[next_scene]
                            print(follow_text)

                            #region Second round of Key Checks
                            print("has_been CHECK")
                            if 'has_been' in choices[main_key]:
                                if choices[main_key]['has_been'] in player_stats['explore_flag']:
                                    player_flags = player_stats['explore_flag']
                                    has_key = choices[main_key]['has_been']
                                    player_stats['explore_flag'][has_key] = not player_flags[has_key]

                            print("2nd inventory_need CHECK")
                            if 'inventory_need' in locked_info:
                                print('has inventory tag 2.0')
                                need = locked_info['inventory_need']
                                for key in need:
                                    player_stats['inventory'][key] = key_items[key]

                            print("tag CHECK")
                            if 'tag' in checkpoint_data:
                                print("tag found in checkpoint data")
                                tag = checkpoint_data['tag']
                                player_stats['choices'][tag] = x
                            elif 'tag' in choices[main_key]:
                                print("tag found in choices")
                                tag = choices[main_key]['tag']
                                player_stats['choices'][tag] = x
                            # endregion

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
                        #endregion
                    else:
                        #region Normal Choice (No lock)
                        print('display normal shit')
                        follow_text = choices[main_key].get('follow_up_text') or ''
                        next_cp = choices[main_key]['next_checkpoint']
                        next_scene = choices[main_key]['checkpoint_scene']
                        scene_name = scene_dict[next_scene]
                        print(follow_text)

                        print('tag check')
                        if 'tag' in checkpoint_data:
                            print("tag found in checkpoint data")
                            tag = checkpoint_data['tag']
                            player_stats['choices'][tag] = x
                        elif 'tag' in choices[main_key]:
                            print("tag found in choices")
                            tag = choices[main_key]['tag']
                            player_stats['choices'][tag] = x

                        if next_cp in test_checkpoint_names:
                            load_test(scene_name, next_cp)
                        elif '_ending' in next_cp:
                            load_ending(scene_name, next_cp)
                        else:
                            test_func(scene_name, next_scene, next_cp)
                        valid_input = True
                        break
                        #endregion
            # endregion

            if not valid_input:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")
    # endregion



test_func(start_scene, 'start', 'intro')
print(player_stats)