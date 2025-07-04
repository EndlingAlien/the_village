"""
main.py desc:

    This file controls the core game loop, test logic, and final result calculations.
    It handles the flow between scenes, processes player choices, evaluates test outcomes,
    and manages progression toward the game's multiple endings.
"""

import scenes as sc
import ending_catalogue as ec
import random as r
import analysis as a
import game_db as db


# TODO: Menu should let you read what full desc in final version [endings]


# region Variables
db_instance = db.MockDatabase()
#Track what tests are done
after_swamp = False
after_farm = False
after_church = False

test_mode_state = {
    "active": False,
    "scene_name": None,
    "checkpoint_key": None,
    "questions_list": [],
    "current_index": 0,
    "test_choices": {},
    "test_answers": {},
}
# region Scene Dictionaries

# Each of these holds all checkpoint data for their respective areas
farm_scene = sc.farm_scene_dict
church_scene = sc.church_scene_dict
swamp_scene = sc.swamp_scene_dict
center_scene = sc.center_scene_dict
start_scene = sc.start_scene_dict

# endregion

# Conditions that determine which variation of a scene is loaded
condition_dict = {
    "farm": ['farmer_in_house', 'farmer_outside', 'farmer_in_barn'],
    "swamp": ['heavy_fog', 'light_fog', 'no_fog'],
    "church": ['church_is_empty', 'priest_inside', 'basement_open']
}

# Used by load_info to match scene names to their corresponding dictionaries
scene_dict = {
    "farm": farm_scene,
    "swamp": swamp_scene,
    "church": church_scene,
    "center": center_scene,
    "start": start_scene
}

# Correct answers for the Trust test and score thresholds for Faith and Intuition tests
# TODO: When tkinter in use, polish up the values of this dict
# Key items that are added to the player's inventory during the story, for db
key_items = {
    "decoder": {
        "desc": "A paper you found at the church. It has a table showing how to decode symbols.",
        "type": "lore",
        "effect": "You might be able to use this to read unknown markings."
    },
    "mask": {
        "desc": "A creepy mask you found in the barn on the farm.",
        "type": "tool",
        "effect": "Wearing it might let you blend in..."
    },
    "bible": {
        "desc": "A bible from the church, covered in pale yellow leather.",
        "type": "lore",
        "effect": "Contains information pertaining to this village."
    },
    "letter": {
        "desc": "A letter from the farmhouse.",
        "type": "lore",
        "effect": "It reads: 'Father Michael requests your presence at 9 PM sharp for preparation of the chosen.'"
    },
    "hammer": {
        "desc": "A rusty hammer you found in the swamp.",
        "type": "tool",
        "effect": "Not just a tool..."
    },
    "key": {
        "desc": "A small, rusty key found in the swamp, hidden in the mud.",
        "type": "tool",
        "effect": "What could this possibly unlock?"
    },
    "screwdriver": {
        "desc": "Surprisingly shiny, as if it’s never been used.",
        "type": "tool",
        "effect": "Could be useful..."
    },
    "knife": {
        "desc": "A knife from the farmhouse.",
        "type": "tool",
        "effect": "It's been used... a lot."
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

# Dictionary that holds all stats and game state for the player
player_data = {
    "explore_flag": {
        "snooped_house": False,
        "snooped_barn": False,
        "snooped_church": False,
        "snooped_swamp": False,
    },
    "inventory": {
        "decoder": False,
        "mask": False,
        "bible": False,
        "letter": False,
        "hammer": False,
        "key": False,
        "screwdriver": False,
        "knife": False,
        "red_vial": False,
        "green_vial": False,
        "blue_vial": False,
    },
    "choices": {
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
    "ending_key": [],
}
test_data = {
    "trust_answers": {},
    "faith_answers": {},
    "intuition_answers": {}
}
archetype_data = {
    "trust_archetype": None,
    "faith_archetype": None,
    "intuition_archetype": None,
    "choice_archetype": None,
}
cond_data = {
    "farm": None,
    "swamp": None,
    "church": None
}
final_data = {
    "user_name": None,
    "cond_data": {},
    "player_data": {},
    "test_data": {},
    "archetype_data": {}
}


# endregion

# region Functions
def initialize_game_conditions(cond_dict):
    """
    Assigns the dynamic conditions to the scenes at the beginning of the game at random.
    :param cond_dict: Conditional dictionary holding game conditions.
    """
    return {con: r.choice(options) for con, options in cond_dict.items()}


def reset_game_data():
    return {
        "user_name": None,
        "player_data": {
            "explore_flag": {
                "snooped_house": False,
                "snooped_barn": False,
                "snooped_church": False,
                "snooped_swamp": False,
            },
            "inventory": {
                "decoder": False,
                "mask": False,
                "bible": False,
                "letter": False,
                "hammer": False,
                "key": False,
                "screwdriver": False,
                "knife": False,
                "red_vial": False,
                "green_vial": False,
                "blue_vial": False,
            },
            "choices": {
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
            "ending_key": []
        },
        "test_data": {
            "trust_answers": {},
            "faith_answers": {},
            "intuition_answers": {}
        },
        "archetype_data": {},
        "cond_data": {},
        'test_mode_state' : {
            "active": False,
            "scene_name": None,
            "checkpoint_key": None,
            "questions_list": [],
            "current_index": 0,
            "test_choices": {},
            "test_answers": {},
    }
    }


def load_test_gui(scene_name, scene, checkpoint_key, choice_id=None):
    global test_mode_state
    print(f"load_test choice: {choice_id}")
    print(f"current test mode status: {test_mode_state}")

    # Initialize test state
    if not test_mode_state["active"]:
        print("initializing test state")
        test_name = checkpoint_key.split('_')[0]
        test_block = scene[checkpoint_key]

        test_mode_state.update({
            "active": True,
            "scene_name": scene_name,
            "checkpoint_key": checkpoint_key,
            "questions_list": list(test_block.keys()),
            "current_index": 0,
            "test_choices": {}
        })
        print(f"finished initializing test state: {test_mode_state}")

    test_name = checkpoint_key.split('_')[0]
    print(f"checkpoint key in load test: {checkpoint_key}")
    print("")
    current_q = test_mode_state["questions_list"][test_mode_state["current_index"]]
    question_data = scene[checkpoint_key][current_q]
    tag = question_data["tag"]
    choices = [question_data['choices'][key]['Text'] for key in question_data['choices']]
    dialogue = question_data["dialogue"]

    print(f"Dia: {dialogue}")
    print(f"Choi: {choices}")


    # If a choice was made, save it
    if choice_id is not None:
        print("made a choice in load_test")
        test_mode_state["test_choices"][tag] = choice_id
        test_mode_state["current_index"] += 1

        # If test is finished
        if test_mode_state["current_index"] >= len(test_mode_state["questions_list"]):
            print('finished test')
            print(f"Test state before test eval: {test_mode_state}")
            result = evaluate_test_result(test_name, test_mode_state["test_choices"])
            print(f"returning result from test eval: {result}")
            test_mode_state["active"] = False
            test_mode_state['checkpoint_key'] = result['next_cp']
            print(f"Test state after test finish: {test_mode_state}")
            return result

        next_q = test_mode_state["questions_list"][test_mode_state["current_index"]]
        next_data = scene[checkpoint_key][next_q]
        choices = [next_data['choices'][key]['Text'] for key in next_data['choices']]
        dialogue = next_data["dialogue"]
        print(f'test after making a choice: {test_mode_state}')
        return {
            "dialogue": dialogue,
            "choices": choices,
            "follow_text": None,
            "next_cp": checkpoint_key,
            "next_scene": scene_name,
            "tag": next_data["tag"]
        }

    # Otherwise, return same question
    return {
        "dialogue": dialogue,
        "choices": choices,
        "tag": question_data["tag"]
    }


def evaluate_test_result(test_name, test_choices):
    if test_name == 'trust':
        print('evaluating trust test')
        return calculate_trust_result(test_choices)
    elif test_name == 'faith':
        print('evaluating faith test')
        return calculate_faith_result(test_choices)
    elif test_name == 'intuition':
        print('evaluating intuition test')
        return calculate_intuition_result(test_choices)


def calculate_trust_result(test_choices):
    test_answers = {
        "trust_1": 2,
        "trust_2": 1,
        "trust_3": 2,
        "trust_4": 1,
        "trust_5": 2,
        "trust_6": 1,
        "trust_7": 1,
        "trust_8": 2,
        "trust_9": 1
    }
    correct = sum(1 for k, v in test_answers.items() if test_choices.get(k) == v)
    if correct == 9:
        return {"next_cp": "trust_ending", "next_scene": "farm"}
    elif correct >= 7:
        return {"next_cp": "kindness_ending", "next_scene": "farm"}
    else:
        return {"next_cp": "fail_choice", "next_scene": "farm"}


def calculate_faith_result(test_choices):
    score = sum(test_choices.values())

    if score >= 15:
        return {"next_cp": "believer_ending", "next_scene": "church"}
    elif score >= 10:
        return {"next_cp": "faith_ending", "next_scene": "church"}
    else:
        return {"next_cp": "heretics_ending", "next_scene": "church"}


def calculate_intuition_result(test_choices):
    score = sum(test_choices.values())
    print(f"player test choices: {test_choices}")
    #TODO: Include dialogue and choices OR redirect to load with correct info
    if score >= 8:
        dialogue = scene_dict['swamp']['make_choice']['dialogue']
        choices = [scene_dict['swamp']['make_choice']['choices'][key]['Text'] for key in
                   scene_dict['swamp']['make_choice']['choices']]
        return {
                "next_cp": "make_choice",
                "next_scene": "swamp",
                "dialogue": dialogue,
                "choices": choices
                }
    elif score >= 5:
        dialogue = scene_dict['swamp']['probed_ending']['dialogue']
        return {
                "next_cp": "probed_ending",
                "next_scene": "swamp",
                "ending": True,
                "dialogue": dialogue,
                }
    else:
        dialogue = scene_dict['swamp']['rejected_ending']['dialogue']
        return {
                "next_cp": "rejected_ending",
                "next_scene": "swamp",
                "ending": True,
                "dialogue": dialogue,
                }




# region Main Game Logic
# Ordered by execution flow for improved readability
def load_game_info_gui(scene, scene_name, checkpoint_key, choice_id=None):
    # Setup block: loads the conditionally appropriate dialogue and options
    return_dict = initial_setup_gui(scene_name, scene, checkpoint_key)
    active_block = return_dict['active_block']
    choices = return_dict['choices']
    checkpoint_data = return_dict['checkpoint_data']

    print(f"Recieved: Scene: {scene}\nScene_name: {scene_name}\nCheckpoint_key: {checkpoint_key}\nChoice_id: {choice_id}")

    if after_swamp and scene_name == 'swamp' and checkpoint_key == 'intro' and choice_id == 1:
        scene = scene_dict['swamp']
        scene['intro']['choices']['option_one']['next_checkpoint'] = 'after_test_start'
    if after_farm and scene_name == 'farm' and checkpoint_key == 'intro' and choice_id == 1:
        scene = scene_dict['farm']
        scene['intro']['choices']['option_one']['next_checkpoint'] = 'after_test_start'
    if after_church and scene_name == 'church' and checkpoint_key == 'intro' and choice_id == 1:
        scene = scene_dict['church']
        scene['intro']['choices']['option_one']['next_checkpoint'] = 'after_test_start'

    # Get the current dialogue and available choices
    dialogue, choices_list = get_dialogue_and_choices(active_block, choices)
    # print(f"main.py has dialogue: {dialogue}")
    # print(f"main.py has choices: {choices_list}")
    print(f"current checkpoint key: {checkpoint_key}")
    if checkpoint_key.endswith('_test') and 'after_test' not in checkpoint_key:
        print(f"checkpoint contains test keyword")
        print(f"load_game has choice_id: {choice_id}")
        load_test_info = load_test_gui(scene_name, scene, checkpoint_key, choice_id)
        print(f"Returning from test: {load_test_info}")
        return load_test_info
    if choice_id is None:
        print("No choice was made")
        return {
            'dialogue': dialogue,
            'choices': choices_list
        }
    else:
        print("processing choice")
        result = process_choice_with_checks(choice_id, choices, checkpoint_data)
        return result


def initial_setup_gui(scene_name, scene, checkpoint_key):
    vars_return_dict = {'active_block': {}, 'choices': {}, 'checkpoint_data': {}}
    current_cond = cond_data.get(scene_name, None)
    checkpoint_data = scene.get(checkpoint_key, {})

    # If choice has a conditional branch to take (e.g. 'farmer_in_house'), follow it
    if current_cond and current_cond in checkpoint_data:
        active_block = checkpoint_data[current_cond]
        choices = active_block.get('choices') or checkpoint_data.get('choices', {})
    else:
        active_block = checkpoint_data
        choices = active_block.get('choices', {})

    vars_return_dict['active_block'] = active_block
    vars_return_dict['choices'] = choices
    vars_return_dict['checkpoint_data'] = checkpoint_data
    return vars_return_dict


def get_dialogue_and_choices(active_block, choices):
    dialogue = active_block.get('dialogue') or ''
    choice_list = []

    for key in choices:
        should_display = choices[key].get('is_displayed', True)

        # If not already visible, check if it can be revealed
        if not should_display:
            locked_info = choices[key].get('locked', {})
            # Assume blocked display
            explore_valid = False
            inventory_valid = False

            # Check if player has required explore flags
            if 'explore_flag' in locked_info:
                flags = locked_info['explore_flag']
                explore_valid = all(
                    player_data['explore_flag'].get(flag_key) == val
                    for flag_key, val in flags.items()
                )

            # Check if player has required inventory items
            if 'inventory_need' in locked_info:
                flags = locked_info['inventory_need']

                if any("_vial" in key for key in flags):
                    # VIAL CASE — all vial keys must match
                    inventory_valid = all(
                        player_data['inventory'].get(flag_key) == val
                        for flag_key, val in flags.items()
                        if "_vial" in flag_key
                    )
                else:
                    # GENERAL CASE — at least one key must match
                    inventory_valid = any(
                        player_data['inventory'].get(flag_key) == val
                        for flag_key, val in flags.items()
                    )

            # Reveal if either condition is met
            if explore_valid or inventory_valid:
                choices[key]['is_displayed'] = True
                should_display = True

        # Display unlocked or revealed choice
        if should_display:
            choice_list.append(choices[key]['Text'])
    return dialogue, choice_list


def process_choice_with_checks(choice_id, choices, checkpoint_data):
    for key, choice in choices.items():
        if choice_id == choice['id']:
            # Check if choice is locked
            if 'locked' in choice:
                locked_info = choice['locked']
                allow_progress = key_checks_gui(False, locked_info)

                # Follow the correct branch
                if allow_progress:
                    print('Progress allowed')
                    result = progress_allowed_gui(choice, locked_info, choice_id, checkpoint_data)
                else:
                    print('Progress not allowed')
                    result = progress_locked_gui(locked_info)
                break
            else:
                # Option is not locked — proceed
                print("Not locked option")
                result = not_locked_display_gui(choice, checkpoint_data, choice_id)
                break
    return result


def key_checks_gui(allow_progress, locked_info):
    # Check if there is an explore_flag key, if so, does the player meet the requirements to select?
    if 'explore_flag' in locked_info:
        flags = locked_info['explore_flag']
        for key in flags:
            if key in player_data['explore_flag']:
                if flags[key] == player_data['explore_flag'][key]:
                    allow_progress = True

    # Check if there is an inventory_need key, and the player has everything required
    if 'inventory_need' in locked_info:
        flags = locked_info['inventory_need']
        for key in flags:
            if key in player_data['inventory']:
                if flags[key] == player_data['inventory'][key]:
                    allow_progress = True
    return allow_progress


def progress_allowed_gui(choice, locked_info, choice_id, checkpoint_data):
    follow_text = choice.get('follow_up_text') or 'ERROR progress_allowed_gui: Could not find follow up text'
    next_cp = choice.get('next_checkpoint')
    next_scene = choice.get('checkpoint_scene')

    # Apply flags and inventory changes
    second_key_check_gui(choice, locked_info, checkpoint_data, choice_id)

    # TODO If its a test or ending, redirect
    if '_test' in next_cp:
        print(f"test inside load game_info detected in progress allowed")

    if '_ending' in next_cp:
        return ending_handler(next_cp, next_scene)

    return {
        'choices': [],
        'follow_text': follow_text,
        'next_cp': next_cp,
        'next_scene': next_scene
    }


def second_key_check_gui(choice, locked_info, checkpoint_data, choice_id):
    if 'has_been' in choice:
        if choice['has_been'] in player_data['explore_flag']:
            player_flags = player_data['explore_flag']
            has_key = choice['has_been']
            # Reverse explore_flag so player can't revisit
            player_data['explore_flag'][has_key] = not player_flags[has_key]

    # Add item to player inventory
    if 'inventory_need' in locked_info:
        need = locked_info['inventory_need']
        for key in need:
            player_data['inventory'][key] = not player_data['inventory'][key]

    # Add player game choice with current tag to player_data
    if 'tag' in checkpoint_data:
        tag = checkpoint_data['tag']
        player_data['choices'][tag] = choice_id
    elif 'tag' in choice:
        tag = choice['tag']
        player_data['choices'][tag] = choice_id


def progress_locked_gui(locked_info):
    locked_dialogue = locked_info.get('locked_text') or 'ERROR progress_locked_gui: Could not find locked text'
    next_cp = locked_info.get('locked_checkpoint')
    next_scene = locked_info.get('locked_scene')

    return {
        'choices': [],
        'locked_text': locked_dialogue,
        'next_cp': next_cp,
        'next_scene': next_scene,
    }


def not_locked_display_gui(choice, checkpoint_data, choice_id):
    follow_text = choice.get('follow_up_text') or 'ERROR progress_allowed_gui: Could not find follow up text'
    next_cp = choice.get('next_checkpoint')
    next_scene = choice.get('checkpoint_scene')

    # Add player game choice with current tag to player_data
    if 'tag' in checkpoint_data:
        tag = checkpoint_data['tag']
        player_data['choices'][tag] = choice_id
    elif 'tag' in choice:
        tag = choice['tag']
        player_data['choices'][tag] = choice_id

    # TODO If its a test or ending, redirect
    if '_test' in next_cp:
        print(f"test inside load game_info detected in not locked display")

    if '_ending' in next_cp:
        return ending_handler(choice)

    return {
        'choices': [],
        'follow_text': follow_text,
        'next_cp': next_cp,
        'next_scene': next_scene,
    }


# endregion


def ending_handler(choice):
    global after_swamp
    global after_farm
    global after_church
    print("man handle that ending")
    next_cp = choice.get('next_checkpoint')
    next_scene = choice.get('checkpoint_scene')
    # Get the block of data associated with the ending checkpoint
    ending_block = scene_dict[next_scene][next_cp]
    dialogue = ending_block.get('dialogue')
    end_key = ending_block.get('ending_key')

    # Not a 'true ending', player can continue game
    if ending_block.get('next_checkpoint'):
        dialogue = ending_block.get('dialogue')
        next_cp = ending_block.get('next_checkpoint')
        next_scene = ending_block.get('checkpoint_scene')
        print("This game aint done with you yet")
        # Store the player's ending decision into the test condition dict
        cond_data[next_scene] = end_key

        # Save the ending result into the player stats
        player_data['ending_key'].append(end_key)

        # Check if this ending grants an item and update the inventory
        if ending_block.get('inventory_need'):
            need = ending_block['inventory_need']
            for key in need:
                player_data['inventory'][key] = not player_data['inventory'][key]

        print(f"ending handler next cp: {next_cp}")
        print(f"ending handler next scene: {next_scene}")
        print(f"ending handler dia: {dialogue}")

        if 'after_test_' in next_cp:
            print("Updating AFTER BOOLS")
            if next_scene == 'swamp':
                print("UPDATING SWAMP AFTER")
                after_swamp = True
                print(after_swamp)
            if next_scene == 'farm':
                after_farm = True
            if next_scene == 'church':
                after_church = True

        return {
            'dialogue': dialogue,
            'choices': [],
            'next_cp': next_cp,
            'next_scene': next_scene,
            'ending': False,

        }
    else:
        print("okay bye bye you dead")# Is a 'true ending', player cant continue game
        return {
            'dialogue': dialogue,
            'ending': True,
        }


def update_inventory():
    tools_list = ['key', 'screwdriver', 'hammer', 'knife']
    docs_list = ['decoder', 'bible', 'letter']
    other_list = ['mask']
    vials_list = ['red_vial', 'blue_vial', 'green_vial']

    #Update gui list with player list
    player_tools = [tool for tool in tools_list if player_data['inventory'].get(tool)]
    player_docs = [doc for doc in docs_list if player_data['inventory'].get(doc)]
    player_other = [item for item in other_list if player_data['inventory'].get(item)]
    player_vials = [vial for vial in vials_list if player_data['inventory'].get(vial)]

    return player_tools, player_docs, player_other, player_vials

# region Database Functions


def configure_final_data():
    """
    Configures the final_data dictionary to be uploaded to the database.

    This function:
    - Fills in missing test answers with blank (None) values
    - Sets archetype values to None if the test wasn't taken
    - Always calculates the choice-based archetype
    - Ensures final_data is valid and complete for upload
    """

    # Default empty test answers (None) for all questions
    blank_test_data = {
        "trust_answers": {f"question_{i}": None for i in range(1, 10)},
        "faith_answers": {f"question_{i}": None for i in range(1, 7)},
        "intuition_answers": {f"question_{i}": None for i in range(1, 4)},
    }

    # Checks if a test was actually taken
    def has_real_answers(answers_dict):
        return any(v is not None for v in answers_dict.values())

    # These will be filled in below
    final_test_data = {}
    final_arch_data = {}

    # Fill in test answers and calculate archetypes as appropriate
    check_tests(test_data, final_test_data, final_arch_data, has_real_answers, blank_test_data)

    # Choice archetype is always calculated regardless of test participation
    final_arch_data["choice_archetype"] = a.calc_choice_archetype(player_data["choices"])

    # Assemble final payload for DB
    final_data = {
        "user_name": user_name,
        "cond_data": cond_data,
        "player_data": player_data,
        "test_data": final_test_data,
        "archetype_data": final_arch_data,
    }

    # TODO: Later on replace 'test' placeholder as user_name
    print(final_data)  # for future testing
    db_instance.insert_full_run(final_data['user_name'], final_data)


def check_tests(test_data, final_test_data, final_arch_data, has_real_answers, blank_test_data):
    """
    Fills final_test_data and final_arch_data based on what tests the player completed.
    If a test is missing or all answers are None, it sets blank test data and None archetypes.
    """

    def calc_trust(test_answers, test_choices):
        # Count how many answers the player got correct
        correct = 0
        for key, answer in test_answers.items():
            if test_choices.get(key) == answer:
                correct += 1
        return correct

    # --- Trust Test ---
    if has_real_answers(test_data.get("trust_answers", {})):
        final_test_data["trust_answers"] = test_data["trust_answers"]
        final_arch_data["trust_archetype"] = a.calc_trust_test_archetype(
            calc_trust(test_answers_dict['trust'], test_data["trust_answers"]))
    else:
        final_test_data["trust_answers"] = blank_test_data["trust_answers"]
        final_arch_data["trust_archetype"] = None

    # --- Faith Test ---
    if has_real_answers(test_data.get("faith_answers", {})):
        final_test_data["faith_answers"] = test_data["faith_answers"]
        final_arch_data["faith_archetype"] = a.calc_faith_test_archetype(test_data["faith_answers"])
    else:
        final_test_data["faith_answers"] = blank_test_data["faith_answers"]
        final_arch_data["faith_archetype"] = None

    # --- Intuition Test ---
    if has_real_answers(test_data.get("intuition_answers", {})):
        final_test_data["intuition_answers"] = test_data["intuition_answers"]
        final_arch_data["intuition_archetype"] = a.calc_intuition_test_archetype(test_data["intuition_answers"])
    else:
        final_test_data["intuition_answers"] = blank_test_data["intuition_answers"]
        final_arch_data["intuition_archetype"] = None


# endregion

# endregion

# region Reset All Game Data
final_data = reset_game_data()
player_data = final_data["player_data"]
test_data = final_data["test_data"]
cond_data = final_data["cond_data"]
archetype_data = final_data["archetype_data"]
test_mode_state = final_data['test_mode_state']
user_name = final_data['user_name']
# endregion

cond_data = initialize_game_conditions(condition_dict)
