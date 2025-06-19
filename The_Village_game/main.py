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
        15: "believer",  # 15 to 18 → believer ending
        10: "pass",  # 10 to 14 → pass ending
        0: "death"  # 0 to 9 → failed/doom ending
    },
    'intuition': {
        8: "curious",  # 8 to 9 → passed/insightful ending
        5: "pass",  # 5 to 7 → survived
        0: "boring"  # 0 to 4 → failed/boring ending
    },
}
# TODO: When tkinter in use, polish up the values of this dict
# Key items that are added to the player's inventory during the story
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

# Identifiers used to determine if a checkpoint is a test
test_checkpoint_names = ['trust_test', 'faith_test', 'intuition_test']

# Dictionary that holds all stats and game state for the player
player_data = {
    "explore_flag": {
        "snooped_house": False,
        "snooped_barn": False,
        "snooped_church": False,
        "snooped_swamp": False,
    },
    "inventory": {},
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
    "ending_key": {},
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
        "player_data": {
            "explore_flag": {
                "snooped_house": False,
                "snooped_barn": False,
                "snooped_church": False,
                "snooped_swamp": False,
            },
            "inventory": {},
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
            "ending_key": {}
        },
        "test_data": {
            "trust_answers": {},
            "faith_answers": {},
            "intuition_answers": {}
        },
        "archetype_data": {},
        "cond_data": {}
    }


# region Test Functions

# region Load Test

def load_test(scene, checkpoint_key):
    """
    In charge of loading the correct dialogue and options from a test scene.
    :param scene: Dictionary to search within.
    :param checkpoint_key: Name of the key in scene dictionary.
    """
    # region Vars

    index = 0  # Tracks which question we’re currently on
    test_choices = {}  # Stores the player's answers by tag
    test_name = checkpoint_key.split('_')[0]  # Derives the test type (e.g., 'faith') from key like 'faith_test'
    test_answers = test_answers_dict[test_name]  # Gets the correct answers for this test
    key_amount = list(scene.get(checkpoint_key, {}))  # Gets all the keys in the test section (question_1...n)

    # Ordered list of question keys expected in the test
    questions_str = [
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
    # endregion

    # Load and process the test questions, returning the player's answers
    test_choices = load_test_info(index, key_amount, scene, checkpoint_key, questions_str, test_choices)

    # Evaluate results based on the test type
    if test_name == 'trust':
        calculate_trust_result(test_answers, test_choices)
    elif test_name == 'faith':
        calculate_faith_result(test_answers, test_choices)
    elif test_name == 'intuition':
        calculate_intuition_result(test_answers, test_choices)


def load_test_info(index, key_amount, scene, checkpoint_key, questions_str, test_choices):
    """
    In charge of loading the dialogue and choices for the test scene.
    :param index: Index of question we're on.
    :param key_amount: Number of keys inside the test scene dictionary.
    :param scene: What scene this test belongs to.
    :param checkpoint_key: Name of checkpoint.
    :param questions_str: List of strings: question_1-9.
    :param test_choices: Dictionary of players' choices.
    :return: Returns final test_choices dictionary
    """
    # Loop through the questions in the test
    while index < len(key_amount):
        test_data = scene.get(checkpoint_key, {})  # Pulls the full test data block
        question_data = test_data.get(questions_str[index], {})  # Get the current question

        tag = question_data.get('tag', '')  # Used to record the answer by this identifier

        dialogue = question_data.get('dialogue', '')  # Main question text
        print(f"\n{dialogue}\n")

        choices = question_data.get('choices', {})  # All available answer options

        # Print out each choice line with its ID
        for choice_key, choice_data in choices.items():
            print(f"{choice_data['id']}: {choice_data['Text']}")

        # Delegate input/recording to assign_test_tags
        return_dict = assign_test_tags(tag, test_choices, choices, index)
        index = return_dict['index']
        test_choices = return_dict['test_choices']
    return test_choices


def assign_test_tags(tag, test_choices, choices, index):
    """
    Assigns the tag of each question into the test_choices dictionary, assuring the input is saved properly.
    :param tag: Tag of the question.
    :param test_choices: Dictionary of players' choices.
    :param choices: Options within the test, they can choose.
    :param index: Index of question we're on.
    :return: Returns a dictionary containing both the updated index and the test_choices.
    """
    valid_input = False
    vars_dict_return = {"index": None, "test_choices": {}}

    # Keep looping until player enters a valid answer
    while not valid_input:
        try:
            x = int(input("Choose an option: "))

            # Store the answer in test_choices using the tag
            if tag:
                test_choices[tag] = x
            else:
                print("Warning: question missing tag, answer not recorded")

            # Check if input matches a valid choice and print follow-up text
            for key in choices:
                if x == choices[key]['id']:
                    follow_text = choices[key].get('follow_up_text') or ''
                    print(follow_text)
                    valid_input = True
                    break  # Exit loop once valid

            if not valid_input:
                print("Invalid choice. Try Again.")
        except ValueError:
            print("Please enter a number")

    index += 1  # Move to next question

    # Package updated state for return
    vars_dict_return['index'] = index
    vars_dict_return['test_choices'] = test_choices
    return vars_dict_return


# endregion


# region Calculate Test Results

def calculate_trust_result(test_answers, test_choices):
    """
    Calculates the results of the player choices for Trust test, located in the farm scene.
    :param test_answers: The correct answers to the Trust test.
    :param test_choices: A dictionary received from load_test, has the player's answers for the test.
    """
    # Store the test choices in final stats for later analysis
    test_data['trust_answers'] = test_choices

    # Count how many answers the player got correct
    correct = 0
    for key, answer in test_answers.items():
        if test_choices.get(key) == answer:
            correct += 1

    # Run an archetype analysis (external analysis logic), and save to final_data
    final_data['archetype_data']['trust_archetype'] = a.calc_trust_test_archetype(correct)

    # Determine ending based on the number of correct answers
    match correct:
        case 9:
            load_ending(farm_scene, 'trust_ending')
        case _ if correct >= 7:
            load_ending(farm_scene, 'kindness_ending')
        case _ if correct < 7:
            load_game_info(farm_scene, 'farm', 'fail_choice')


def calculate_faith_result(test_answers, test_choices):
    """
    Calculates the results of the player choices for Faith test, located in the church scene.
    :param test_answers: The score threshold dictionary for the Faith test.
    :param test_choices: A dictionary received from load_test, has the player's answers for the test.
    """
    # Store player answers to final stats for analysis
    test_data['faith_answers'] = test_choices

    # Run an archetype analysis (external analysis logic), and save to final_data
    final_data['archetype_data']['faith_archetype'] = a.calc_faith_test_archetype(test_choices)

    # Score is the sum of all choice values
    score = sum(test_choices.values())

    # Determine which threshold was passed (this loop is a soft fallback/expansion hook)
    for threshold in sorted(test_answers.keys(), reverse=True):
        if score >= threshold:
            break

    # Assign ending based on score tiers
    match score:
        case _ if score >= 15:
            load_ending(church_scene, 'believer_ending')
        case _ if score >= 10:
            load_ending(church_scene, 'faith_ending')
        case _ if score < 10:
            load_ending(church_scene, 'heretics_ending')


def calculate_intuition_result(test_answers, test_choices):
    """
    Calculates the results of the player choices for Intuition test, located in the swamp scene.
    :param test_answers: The score threshold dictionary for the Intuition test.
    :param test_choices: A dictionary received from load_test, has the player's answers for the test.
    """
    # Store player answers in final stats
    test_data['intuition_answers'] = test_choices

    # Run an archetype analysis (external analysis logic), and save to final_data
    final_data['archetype_data']['intuition_archetype'] = a.calc_intuition_test_archetype(test_choices)

    # Score is the sum of the test values
    score = sum(test_choices.values())

    # Check thresholds for logic hook/flexibility
    for threshold in sorted(test_answers.keys(), reverse=True):
        if score >= threshold:
            break

    # Assign scene or ending based on score range
    match score:
        case _ if score >= 8:
            load_game_info(swamp_scene, 'swamp', 'make_choice')  # Leads to another choice scene
        case _ if score >= 5:
            load_ending(swamp_scene, 'probed_ending')
        case _ if score < 5:
            load_ending(swamp_scene, 'rejected_ending')


# endregion

# endregion


# region Main Game Logic
# Ordered by execution flow for improved readability

def load_game_info(scene, scene_name, checkpoint_key):
    """
    Handles scene progression logic during gameplay.
    Loads dialogue and choices from the given checkpoint, handles player input, and applies all necessary conditions
    before continuing to the next part of the game.
    :param scene: Dictionary containing the scene's structure and checkpoints.
    :param scene_name: Key that identifies the scene in global scene_dict.
    :param checkpoint_key: The checkpoint tag used to retrieve dialogue/choice data from the scene.
    """
    # Setup block: loads the conditionally appropriate dialogue and options
    return_dict = initial_setup(scene_name, scene, checkpoint_key)
    active_block = return_dict['active_block']
    choices = return_dict['choices']
    checkpoint_data = return_dict['checkpoint_data']

    # Display the current dialogue and available choices
    display_dialogue_and_choices(active_block, choices)

    # region Player Input Loop
    valid_input = False
    while not valid_input:
        try:
            x = int(input("Choose an option: "))

            # Run conditional logic to evaluate player's choice
            valid_input = choice_selection_with_checks(valid_input, choices, x, checkpoint_data)

            if not valid_input:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")
    # endregion


def initial_setup(scene_name, scene, checkpoint_key):
    """
    Determines which block of a scene to load, accounting for any conditional logic.
    :param scene_name: Key name of the current scene.
    :param scene: Scene dictionary.
    :param checkpoint_key: Which part of the scene to access.
    :return: Dictionary of the current active block, choices, and full checkpoint data.
    """
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


def display_dialogue_and_choices(active_block, choices):
    """
    Prints the dialogue and available choices, dynamically revealing locked options
    based on inventory or exploration flags.
    :param active_block: The dictionary with dialogue and choice info.
    :param choices: The full choices' dict.
    """
    dialogue = active_block.get('dialogue') or ''
    print(dialogue)

    for key in choices:
        should_display = choices[key].get('is_displayed', True)

        # If not already visible, check if it can be revealed
        if not should_display:
            locked_info = choices[key].get('locked', {})
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
                need = locked_info['inventory_need']
                true_keys = [k for k, v in need.items() if v is True]
                false_keys = [k for k, v in need.items() if v is False]

                has_required = any(key in player_data['inventory'] for key in true_keys)
                has_wrong = any(key in player_data['inventory'] for key in false_keys)

                # You can see this option if:
                # - You have at least one of the required items
                # - AND none of the "should not have" items
                if has_required and not has_wrong:
                    inventory_valid = True

            # Reveal if either condition is met
            if explore_valid or inventory_valid:
                choices[key]['is_displayed'] = True
                should_display = True

        # Display unlocked or revealed choice
        if should_display:
            print(f"{choices[key]['id']}: {choices[key]['Text']}")


def choice_selection_with_checks(valid_input, choices, x, checkpoint_data):
    """
    Evaluates the player's choice input, performs the necessary checks,
    and routes to the appropriate outcome.
    :param valid_input: Boolean tracking if input is valid.
    :param choices: Dictionary of current choices.
    :param x: Player's input (int).
    :param checkpoint_data: Full block data for the current checkpoint.
    :return: True if a valid input and transition occurred, False otherwise.
    """
    for main_key in choices:
        if x == choices[main_key]['id']:
            if 'locked' in choices[main_key]:
                locked_info = choices[main_key]['locked']
                allow_progress = False  # Assume blocked

                # Run checks on required flags and inventory
                allow_progress = key_checks(allow_progress, locked_info)

                # Follow the correct branch
                if allow_progress:
                    progress_allowed(choices, main_key, locked_info, checkpoint_data, x)
                else:
                    progress_locked(locked_info)
                valid_input = True
                break
            else:
                # Option is not locked — proceed
                not_locked_display(choices, main_key, checkpoint_data, x)
                valid_input = True
                break
    return valid_input


def key_checks(allow_progress, locked_info):
    """
    Performs flag and inventory validation for locked choices.
    :param allow_progress: Boolean tracking current progress status.
    :param locked_info: Dict of lock conditions.
    :return: Updated boolean for progress permission.
    """

    # Check if there is an explore_flag key, if so, does the player meet the requirements to select?
    if 'explore_flag' in locked_info:
        flags = locked_info['explore_flag']
        for key in flags:
            if key in player_data['explore_flag']:
                if flags[key] == player_data['explore_flag'][key]:
                    allow_progress = True

    # Check if there is an inventory_need key, and the player has everything required
    if 'inventory_need' in locked_info:
        need = locked_info['inventory_need']

        true_keys = [k for k, v in need.items() if v is True]
        false_keys = [k for k, v in need.items() if v is False]

        has_required = any(key in player_data['inventory'] for key in true_keys)
        has_wrong = any(key in player_data['inventory'] for key in false_keys)

        if has_wrong:
            allow_progress = True
        elif not has_required and true_keys:
            allow_progress = True
        else:
            allow_progress = True


    return allow_progress


def progress_allowed(choices, main_key, locked_info, checkpoint_data, x):
    """
    Handles valid transitions once conditions are met, including applying flags,
    inventory updates, and choice tagging.
    """
    follow_text = choices[main_key].get('follow_up_text') or ''
    next_cp = choices[main_key]['next_checkpoint']
    next_scene = choices[main_key]['checkpoint_scene']
    scene_name = scene_dict[next_scene]
    print(follow_text)

    # Apply flags and inventory changes
    second_key_check(choices, main_key, locked_info, checkpoint_data, x)

    # Move to the appropriate next function
    if next_cp in test_checkpoint_names:
        load_test(scene_name, next_cp)
    elif '_ending' in next_cp:
        load_ending(scene_name, next_cp)
    else:
        load_game_info(scene_name, next_scene, next_cp)


def second_key_check(choices, main_key, locked_info, checkpoint_data, x):
    """
    Performs follow-up updates: toggles exploration flags, gives inventory items,
    and record choice tags for analysis.
    """
    if 'has_been' in choices[main_key]:
        if choices[main_key]['has_been'] in player_data['explore_flag']:
            player_flags = player_data['explore_flag']
            has_key = choices[main_key]['has_been']
            # Reverse explore_flag so player can't revisit
            player_data['explore_flag'][has_key] = not player_flags[has_key]

    # Add item to player inventory
    if 'inventory_need' in locked_info:
        need = locked_info['inventory_need']
        for key in need:
            player_data['inventory'][key] = key_items[key]

    # Add player game choice with current tag to player_data
    if 'tag' in checkpoint_data:
        tag = checkpoint_data['tag']
        player_data['choices'][tag] = x
    elif 'tag' in choices[main_key]:
        tag = choices[main_key]['tag']
        player_data['choices'][tag] = x


def progress_locked(locked_info):
    """
    Handles transitions when conditions aren't met.
    Displays locked message and routes to locked scene checkpoint.
    """
    locked_dialogue = locked_info['locked_text']
    next_cp = locked_info['locked_checkpoint']
    next_scene = locked_info['locked_scene']
    scene_name = scene_dict[next_scene]
    print(locked_dialogue)
    load_game_info(scene_name, next_scene, next_cp)


def not_locked_display(choices, main_key, checkpoint_data, x):
    """
    Displays standard options (not locked), saves choice tags,
    and moves to the next checkpoint or ending.
    """
    follow_text = choices[main_key].get('follow_up_text') or ''
    next_cp = choices[main_key]['next_checkpoint']
    next_scene = choices[main_key]['checkpoint_scene']
    scene_name = scene_dict[next_scene]
    print(follow_text)

    # Add player game choice with current tag to player_data
    if 'tag' in checkpoint_data:
        tag = checkpoint_data['tag']
        player_data['choices'][tag] = x
    elif 'tag' in choices[main_key]:
        tag = choices[main_key]['tag']
        player_data['choices'][tag] = x

    # Move to the appropriate next function
    if next_cp in test_checkpoint_names:
        load_test(scene_name, next_cp)
    elif '_ending' in next_cp:
        load_ending(scene_name, next_cp)
    else:
        load_game_info(scene_name, next_scene, next_cp)


# endregion


def load_ending(scene, checkpoint_key):
    """
    Loads the ending scene.
    :param scene: What scene this ending is from.
    :param checkpoint_key: The name of the checkpoint.
    """
    # Get the block of data associated with the ending checkpoint
    active_block = scene.get(checkpoint_key)
    dialogue = active_block.get('dialogue')
    end_key = active_block.get('ending_key')

    # Check if there's a defined next checkpoint and scene to continue into
    if active_block.get('next_checkpoint') and active_block.get('checkpoint_scene'):
        # Grab the name of the next scene and checkpoint
        scene_name = scene_dict[active_block.get('checkpoint_scene')]
        cp_name = active_block.get('checkpoint_scene')
        cp = active_block.get('next_checkpoint')

        # Print the current dialogue to the screen
        print(dialogue)

        # Store the player's ending decision into the test condition dict
        cond_data[cp_name] = end_key

        # Save the ending result into the player stats
        player_data['ending_key'][end_key] = ec.endings[end_key]

        # Load the correct scene dictionary
        scene = sc.return_scene(cp_name + '_scene_dict')

        # Modify the intro block to jump to post-test content
        scene['intro']['choices']['option_one']['next_checkpoint'] = 'after_test_start'

        # Check if this ending grants an item and update the inventory
        if active_block.get('inventory_need'):
            for key in active_block['inventory_need']:
                player_data['inventory'][key] = key_items[key]

        # Load into the next scene and checkpoint
        load_game_info(scene_name, cp_name, cp)

    # Final dialogue print if no scene continuation is provided
    print(dialogue)
    # Save the ending result into the player stats
    player_data['ending_key'][end_key] = ec.endings[end_key]
    # Game is over, configure data to insert into db
    configure_final_data()

#region Database Functions


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
        "cond_data": cond_data,
        "player_data": player_data,
        "test_data": final_test_data,
        "archetype_data": final_arch_data,
    }

    #TODO: Later on replace 'test' placeholder as user_name
    #print(final_data) for future testing
    db_instance.insert_full_run('Tester', final_data)


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


#endregion

#endregion

#region Reset All Game Data
final_data = reset_game_data()
player_data = final_data["player_data"]
test_data = final_data["test_data"]
cond_data = final_data["cond_data"]
archetype_data = final_data["archetype_data"]
#endregion

cond_data = initialize_game_conditions(condition_dict)
load_game_info(start_scene, 'start', 'intro')
