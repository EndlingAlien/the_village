# main game loop, logic, UI, etc
import scenes as sc
import random as r

farm_scene = sc.farm_scene_dict
church_scene = sc.church_scene_dict
swamp_scene = sc.swamp_scene_dict
center_scene = sc.center_scene_dict

# holds play-through conditions
game_condition = {}
# dict containing all possible conditions for respective scenes
condition_dict = {
    "farm": ['farmer_in_house', 'farmer_outside', 'farmer_in_barn'],
    "swamp": ['heavy_fog', 'light_fog', 'no_fog'],
    "church": ['church_is_empty', 'priest_inside', 'basement_open']
}


def assign_conditions():
    """ Assigns the dynamic conditions to the scenes at the beginning of the game"""
    for con in condition_dict:
        inside_lists = condition_dict[con]
        num = r.randint(0, len(inside_lists) - 1)
        game_condition[con] = inside_lists[num]
    # for testing purposes keep print() active
    print(game_condition)


# replace with game_condition after testing
test_cond_dict = {
    "farm": 'farmer_in_barn',
    "swamp": 'no_fog',
    "church": 'priest_inside'
}


# do this later --------
# need to account for :
# *DONE* = dialogue/null dialogue, conditional/null choices,

# no follow up text or next_checkpoint
# locked text, conditions
# ----------

# clean up later, it works but looks janky af
def load_checkpoint(dic, scene_name, checkpoint_key):
    current_cond = test_cond_dict[scene_name]
    if checkpoint_key in dic.keys():
        if current_cond in dic[checkpoint_key]:  # follows conditional template
            print('conditional\n')  # testing
            cond_key = dic[checkpoint_key][current_cond]
            dialogue = cond_key['dialogue']
            print(dialogue)
            if cond_key['choices'] is None:  # if choices are empty
                options = dic[checkpoint_key]['choices']
                for key in options:
                    choices = options[key]['Text']
                    print(choices)
            else:
                options = cond_key['choices']
                for key in options:
                    choices = options[key]['Text']
                    print(choices)
        else:  # follows typical checkpoint template
            print('typical\n')  # testing
            dialogue = dic[checkpoint_key]['dialogue']
            if dialogue is None:
                dialogue = ''  # maybe?? placeholder
            print(dialogue)
            options = dic[checkpoint_key]['choices']
            for key in options:
                choices = options[key]['Text']
                print(choices)


'''for index, checkpoint_key in enumerate(farm_scene):
    limit = 0
    checkpoint = farm_scene[checkpoint_key]
    dialogue = checkpoint['dialogue']
    print(dialogue)

    options = checkpoint['choices']

    for option_key in options:
        print(options[option_key]['Text'])

    if index == limit:
        break'''

# assign_conditions()
load_checkpoint(farm_scene, 'farm', 'choose_farmhouse')
