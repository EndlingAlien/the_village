# main game loop, logic, UI, etc
import scenes as sc
import random as r

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

#change test_dict instances to game_condition when done testing
#game_condition = initialize_game_conditions(condition_dict)
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

# TODO: make a list or dict of ending names to check if checkpoint keyword == so game can quit
# TODO: ending catalogue.py maybe??

# TODO: go through tests, change answers around, make func for each test to calculate score and assign correct ending
# TODO: keep track of: what player has in inventory, where theyve explored, what choices theyve made
# TODO: create a tag for each decision (no need for intro or crossroads, or non-important) think walking dead stats at end on display
# TODO: still need to create logic for locked text vs follow up
def initialize_game_conditions(cond_dict):
    """
    Assigns the dynamic conditions to the scenes at the beginning of the game
    :param cond_dict: conditional dictionary holding game conditions
    """
    return {con: r.choice(options) for con, options in condition_dict.items()}


# do this later --------
# need to account for :
# *DONE* = dialogue/null dialogue, conditional/null choices, follow-up/
# locked text, conditions
# ----------


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



load_info(start_scene, None, 'intro')
#load_checkpoint(farm_scene, 'farm', 'start_position')
