"""
scenes.py desc:

    Responsible for defining all scene dictionaries used in the game.
    Includes:
        - Full scene structures with their respective checkpoints and dialogue branches.
        - A checkpoint template to streamline the creation of new checkpoint entries.
        - Documentation for keys, tags, and expected structures inside each option dict.

    Acts as the core data structure hub for all scene progressions and branching logic.
"""

# Checkpoint Template
'''
"checkpoint_name": {
        "tag": "For the player_stats['choices']",
        "dialogue": "Dialogue to display",
        "choices": {
            "option_one": {
                "Text": "text",
                "id": 1,
                "follow_up_text": "text",
                "next_checkpoint": "text"
            },
        }
},
'''

# region Definition of Option Keys
"""
option_definition:
    Required Keys (all options must include these):
    ----------------------------------------------
    "Text"              : The text shown to the player for this choice. (string)
    "id"                : The numeric ID the player must input to select this option. (int)
    "follow_up_text"    : The text displayed after the player selects this option. (string)
    "next_checkpoint"   : The name of the checkpoint this option leads to. (string)
    "checkpoint_scene"  : The name of the scene this option leads to. (string)

    Optional Keys (included as needed):
    -----------------------------------
    "is_displayed"      : Whether this option is visible to the player. Defaults to True. (bool)

    "locked"            : A dictionary of conditions that must be met before this option is selectable. (dict)
        - "locked_text"       : The message shown if the player doesn’t meet the conditions. (string)
        - "locked_checkpoint" : The fallback checkpoint if the option is locked. (string)
        - "locked_scene"      : The fallback scene if the option is locked. (string)
        - "inventory_need"    : A dictionary of inventory requirements. Items marked True must be present; items marked False must not. (dict)
        - "explore_flag"      : A dictionary tracking areas the player has discovered. (dict)

    "ending_key"        : The key used to track which ending has been unlocked. (string)
"""
# endregion

# region Tag definitions for player_stats['choices']
"""
vials_choice - Where you poured the vials. Located in center_scene_dict["statue_vials"].

cube_choice - Whether you tried to back away from the cube. Located in swamp_scene_dict["approach_cube"].

curious_choice - Which ending you chose after passing the Intuition test. Located in swamp_scene_dict["make_choice"].

basement_door_choice - Whether or not you entered the open basement (like the marshmallow test: wait, yell, go). Located in church_scene_dict["inside_church"] (requires the basement to be open).

basement_choice - What you chose to do after seeing the men in the basement. Located in church_scene_dict["church_basement"].

basement_two_choice - What you chose to do after the men saw you. Located in church_scene_dict["basement_ritual"].

start_choice - Where you started at the farm (barn or farmhouse). Located in farm_scene_dict["start_position"].

knock_choice - Whether you knocked or banged on the door. Located in farm_scene_dict["choose_farmhouse"] (requires the farmer to be inside the house).

meet_choice - Whether you chose to kill the farmer before the test. Located in farm_scene_dict["meet_farmer"].

break_choice - Whether you took a break on the porch. Located in after_test_house["trust_pass"].
"""


# endregion


def return_scene(string):
    """
    Returns the correct scene.
    :param string: Name of the scene.
    """
    match string:
        case 'farm_scene_dict':
            return farm_scene_dict
        case 'swamp_scene_dict':
            return swamp_scene_dict
        case 'church_scene_dict':
            return church_scene_dict
        case 'center_scene_dict':
            return center_scene_dict
        case 'start_scene_dict':
            return start_scene_dict


# TODO: When tkinter in use, redo all dialogue/text (didn't do yet becasue formatting might be weird)
# region Scene Dictionaries

# Where the game starts
start_scene_dict = {
    "intro": {
        "dialogue": "You wake up alone in a forest surrounded by trees",
        "choices": {
            "option_one": {
                "Text": "go forward [Village Center]",
                "id": 1,
                "follow_up_text": "you start walking forward...",
                "next_checkpoint": "intro",
                "checkpoint_scene": "center"
            },
            "option_two": {
                "Text": "go right [Farm]",
                "id": 2,
                "follow_up_text": "you start walking right...",
                "next_checkpoint": "intro",
                "checkpoint_scene": "farm"
            },
            "option_three": {
                "Text": "go left [Church]",
                "id": 3,
                "follow_up_text": "you start walking left...",
                "next_checkpoint": "intro",
                "checkpoint_scene": "church"
            }
        }
    },
}

# Village Center Dictionary
center_scene_dict = {
    "intro": {
        "dialogue": "After awhile, you come up on a small circle of houses, with an organic statue in the center. "
                    "You cant see people, could it be abandoned?",
        "choices": {
            "option_one": {
                "Text": "Walk to the center",
                "id": 1,
                "follow_up_text": "You decide to continue on...",
                "next_checkpoint": "village_center",
                "checkpoint_scene": "center"
            },
            "option_two": {
                "Text": "Leave",
                "id": 2,
                "follow_up_text": "You decide to head back to the crossroads...",
                "next_checkpoint": "center_crossroads",
                "checkpoint_scene": "center"
            }
        }
    },
    "center_crossroads": {
        "dialogue": "Where do you want to go?",
        "choices": {
            "option_one": {
                "Text": "Go right [Farm]",
                "id": 1,
                "follow_up_text": "you start walking right...",
                "next_checkpoint": "intro",
                "checkpoint_scene": "farm"
            },
            "option_two": {
                "Text": "Go left [Church]",
                "id": 2,
                "follow_up_text": "you start walking left...",
                "next_checkpoint": "intro",
                "checkpoint_scene": "church"
            },
            "option_three": {
                "Text": "Go forward [Swamp]",
                "id": 3,
                "follow_up_text": "you start walking forward...",
                "next_checkpoint": "intro",
                "checkpoint_scene": "swamp"
            }
        }
    },
    "village_center": {
        "dialogue": "The place looks empty. There are houses surrounding a small courtyard. There "
                    "is a large statue in the middle of the courtyard, littered by strange "
                    "letters on it.",
        "choices": {
            "option_one": {
                "Text": "Try the houses",
                "id": 1,
                "follow_up_text": "You knock on some doors and try opening them. The curtains are "
                                  "drawn. You swear you can hear something behind a couple doors "
                                  "but no one answers.",
                "next_checkpoint": "village_center",
                "checkpoint_scene": "center"
            },
            "option_two": {
                "Text": "Go to the statue",
                "id": 2,
                "follow_up_text": "You walk towards the statue in the square...",
                "next_checkpoint": "center_statue",
                "checkpoint_scene": "center"
            },
            "option_three": {
                "Text": "Turn and leave",
                "id": 3,
                "follow_up_text": "You turn around leaving the small village center behind",
                "next_checkpoint": "center_crossroads",
                "checkpoint_scene": "center"
            }
        }
    },
    "center_statue": {
        "dialogue": "You walk towards the statue in the middle of the courtyard, there is a small "
                    "fountain at its feet. The statue looks to be made of organic material, "
                    "plants, roots and vines. It has strange words "
                    "engraved into it...",
        "choices": {
            "option_one": {
                "Text": "touch statue",
                "id": 1,
                "follow_up_text": "You touch the statue. Its made of intertwined sticks and mud. "
                                  "Its covered in plants and flowers and moss.",
                "next_checkpoint": "center_statue",
                "checkpoint_scene": "center",
            },
            "option_two": {
                "Text": "use decoder",
                "id": 2,
                "follow_up_text": "You use the decoder to read the strange words. the first engraving across the base of the statue reads,"
                                  "'Quench the hands, heal the spring—One binds flesh to fury, the other frees the soul 'The second engraving "
                                  "running along the base of the fountain reads, 'Blood of the forest, tears of the sky, veins of the earth'",
                "next_checkpoint": "center_statue",
                "checkpoint_scene": "center",
                "locked": {
                    "locked_text": "If only you could read these...",
                    "locked_checkpoint": "center_statue",
                    "locked_scene": "center",
                    "inventory_need": {
                        "decoder": True,
                    }
                }
            },
            "option_three": {
                "Text": "leave",
                "id": 3,
                "follow_up_text": "You turn and leave, walking back to the crossroads...",
                "next_checkpoint": "center_crossroads",
                "checkpoint_scene": "center"
            },
            "option_four": {
                "Text": "give up",
                "id": 4,
                "follow_up_text": "Maybe its time...",
                "next_checkpoint": "forfeit_ending",
                "checkpoint_scene": "center",
            },
            "option_five": {
                "Text": "use the vials",
                "id": 5,
                "follow_up_text": "You walk up closer to the statue and fountain, pulling the 3 "
                                  "vials of liquid out of your pocket...",
                "next_checkpoint": "statue_vials",
                "checkpoint_scene": "center",
                "is_displayed": False,
                "locked": {
                    "locked_checkpoint": "center_statue",
                    "locked_scene": "center",
                    "inventory_need": {
                        "red_vial": True,
                        "blue_vial": True,
                        "green_vial": True,

                    }
                }
            }
        }
    },
    "statue_vials": {
        "tag": "vials_choice",
        "dialogue": "You approach the statue holding the vials...",
        "choices": {
            "option_one": {
                "Text": "Pour into statues hands...",
                "id": 1,
                "follow_up_text": "You pour the vials into the statues hands one at a time...",
                "next_checkpoint": "vessel_ending",
                "checkpoint_scene": "center"
            },
            "option_two": {
                "Text": "Pour into the fountain...",
                "id": 2,
                "follow_up_text": "You pour the vials into the fountain one at a time...",
                "next_checkpoint": "cleansed_ending",
                "checkpoint_scene": "center"
            }
        }
    },
    # region Center Endings
    "cleansed_ending": {
        "dialogue": "The water drains from the fountain slowly, then cracks open, revealing a spiraling staircase. You descend "
                    "and are placed in a sewer, a sign reads city with an arrow. You follow it. Youve escaped the village",
        "ending_key": "cleansed"
    },
    "vessel_ending": {
        "dialogue": "You pour the vials into the statues hands, each one instantly soaking in. Suddenly the statue combusts, "
                    "a faint sickly odor surrounds you, you cluth your throat as it burns and suffocates your lungs. "
                    "Your bones break and reform as your muscles expand. Youve become their beast. You are the village.",
        "ending_key": "vessel"
    },
    "forfeit_ending": {
        "dialogue": "You sit down by the statue and close your eyes, your exhaustion finally catching up to you. You keep your eyes closed as you hear footsteps surround you...",
        "ending_key": "forfeit"
    },
    # endregion
}

# Swamp Dictionary: Fog density is conditional [heavy, light, or none]
swamp_scene_dict = {
    "intro": {
        "dialogue": "After awhile, you come up on a open swampy area",
        "choices": {
            "option_one": {
                "Text": "walk into the swamp area",
                "id": 1,
                "follow_up_text": "Its just a swamp...",
                "next_checkpoint": "start_position",
                "checkpoint_scene": "swamp"
            },
            "option_two": {
                "Text": "turn around",
                "id": 2,
                "follow_up_text": "Dont like the look of this place, better go...",
                "next_checkpoint": "swamp_crossroads",
                "checkpoint_scene": "swamp"
            }
        }
    },
    # region Main Swamp Scenes
    "start_position": {
        "heavy_fog": {
            "dialogue": "As you get closer to the swamp, the fog begins to get heavy, its hard to see anything",
            "choices": {
                "option_one": {
                    "Text": "Walk aimlessly",
                    "id": 1,
                    "follow_up_text": "Despite the alarming silence around this swamp you decide to continue...",
                    "next_checkpoint": "inside_swamp",
                    "checkpoint_scene": "swamp"
                },
                "option_two": {
                    "Text": "Turn and Leave",
                    "id": 2,
                    "follow_up_text": "Not worth getting lost in here...",
                    "next_checkpoint": "swamp_crossroads",
                    "checkpoint_scene": "swamp"
                }
            }
        },
        "light_fog": {
            "dialogue": "As you walk more into the swamp, the fog gets a little heavier, you can faintly see the outline of a structure in the distance",
            "choices": {
                "option_one": {
                    "Text": "Continue Walking",
                    "id": 1,
                    "follow_up_text": "Its justa little fog, its not like your blind",
                    "next_checkpoint": "inside_swamp",
                    "checkpoint_scene": "swamp"
                },
                "option_two": {
                    "Text": "Turn and Leave",
                    "id": 2,
                    "follow_up_text": "Its not the fog that worries you, its what could be in the fog...",
                    "next_checkpoint": "swamp_crossroads",
                    "checkpoint_scene": "swamp"
                }
            }
        },
        "no_fog": {
            "dialogue": "As you get closer to the swamp you can see a large stone structure in the center. It looks to have a pedestal in the middle.",
            "choices": {
                "option_one": {
                    "Text": "keep walking",
                    "id": 1,
                    "follow_up_text": "you walk towards the stone structure...",
                    "next_checkpoint": "inside_swamp",
                    "checkpoint_scene": "swamp"
                },
                "option_two": {
                    "Text": "Turn and Leave",
                    "id": 2,
                    "follow_up_text": "Something about the energy here isn't right, you walk away...",
                    "next_checkpoint": "swamp_crossroads",
                    "checkpoint_scene": "swamp"
                }
            }
        }
    },
    "inside_swamp": {
        "heavy_fog": {
            "dialogue": "You walk forward with your hands stretched out, you hear rustling in the distance, you can only see 1 foot in front of you. "
                        "Suddenly you make contact with a stone structure, you can see some kind of cube on its pedestal.",
            "choices": {
                "option_one": {
                    "Text": "approach the cube",
                    "id": 1,
                    "follow_up_text": "The cube is small and metallic, you walk closer...",
                    "next_checkpoint": "approach_cube",
                    "checkpoint_scene": "swamp"
                },
                "option_two": {
                    "Text": "Turn and Leave",
                    "id": 2,
                    "follow_up_text": "This is too weird, time to go...",
                    "next_checkpoint": "swamp_crossroads",
                    "checkpoint_scene": "swamp"
                }
            }
        },
        "light_fog": {
            "dialogue": "You walk towards the structure. As you get closer you notice a pedestal in the center, it looks like a metal cube is on it...",
            "choices": {
                "option_one": {
                    "Text": "approach the metal cube",
                    "id": 1,
                    "follow_up_text": "Something special enough to be on a pedestal is worth taking a look at",
                    "next_checkpoint": "approach_cube",
                    "checkpoint_scene": "swamp"
                },
                "option_two": {
                    "Text": "Look around",
                    "id": 2,
                    "follow_up_text": "Maybe you should check the surrounding area before...",
                    "next_checkpoint": "swamp_key_items",
                    "checkpoint_scene": "swamp",
                    "locked": {
                        "locked_text": "You've already looked around. Theres nothing else worth getting",
                        "locked_checkpoint": "inside_swamp",
                        "locked_scene": "swamp",
                        "explore_flag": {
                            "snooped_swamp": False
                        }
                    },
                },
                "option_three": {
                    "Text": "Turn and Leave",
                    "id": 3,
                    "follow_up_text": "Its not the fog that worries you, its what could be in the fog...",
                    "next_checkpoint": "swamp_crossroads",
                    "checkpoint_scene": "swamp"
                }
            }
        },
        "no_fog": {
            "dialogue": "You walk closer to the stone structure. You can see footprints and dragging marks within the mud and "
                        "earth, someone or something put up a fight here. There are strange markings on the structure, symbols. "
                        "In the center of the stone structure is a pedestal with a metal like cube in the center.",
            "choices": {
                "option_one": {
                    "Text": "Approach the cube",
                    "id": 1,
                    "follow_up_text": "This could be interesting....",
                    "next_checkpoint": "approach_cube",
                    "checkpoint_scene": "swamp"
                },
                "option_two": {
                    "Text": "look around",
                    "id": 2,
                    "follow_up_text": "There could be more here to discover...",
                    "next_checkpoint": "swamp_key_items",
                    "checkpoint_scene": "swamp",
                    "locked": {
                        "locked_text": "You've already looked around. Theres nothing else worth looking at",
                        "locked_checkpoint": "inside_swamp",
                        "locked_scene": "swamp",
                        "explore_flag": {
                            "snooped_swamp": False
                        }
                    },
                },
                "option_three": {
                    "Text": "Turn and Leave",
                    "id": 3,
                    "follow_up_text": "Something about the energy here isn't right, you walk away...",
                    "next_checkpoint": "swamp_crossroads",
                    "checkpoint_scene": "swamp"
                }
            }
        }
    },
    "swamp_key_items": {
        "light_fog": {
            "dialogue": "You look around the surrounding area and spot a screwdriver",
            "choices": {
                "option_one": {
                    "Text": "take the screwdriver",
                    "id": 1,
                    "follow_up_text": "Could be useful...",
                    "next_checkpoint": "approach_cube",
                    "checkpoint_scene": "swamp",
                    "has_been": "snooped_swamp",
                    "locked": {
                        "locked_text": "You have already picked up these items",
                        "locked_checkpoint": "swamp_key_items",
                        "locked_scene": "swamp",
                        "inventory_need": {
                            "screwdriver": False
                        }
                    },
                },
                "option_two": {
                    "Text": "Leave the item",
                    "id": 2,
                    "follow_up_text": "its just a screwdriver...",
                    "next_checkpoint": "approach_cube",
                    "checkpoint_scene": "swamp"
                }
            }
        },
        "no_fog": {
            "dialogue": "You look around the surrounding area. You find a screwdriver and a rusty key. You also find strange"
                        "letters on the side of the structure, if only you could decipher them. ",
            "choices": {
                "option_one": {
                    "Text": "take the screwdriver and key",
                    "id": 1,
                    "follow_up_text": "This could be interesting....",
                    "next_checkpoint": "swamp_key_items",
                    "checkpoint_scene": "swamp",
                    "has_been": "snooped_swamp",
                    "locked": {
                        "locked_text": "You have already picked up these items",
                        "locked_checkpoint": "swamp_key_items",
                        "locked_scene": "swamp",
                        "inventory_need": {
                            "key": False,
                            "screwdriver": False
                        }
                    },
                },
                "option_two": {
                    "Text": "Use decoder",
                    "id": 2,
                    "follow_up_text": "you pocket the hammer and key, then use your decoder to read the strange "
                                      "words. (placeholder)",
                    "next_checkpoint": "approach_cube",
                    "checkpoint_scene": "swamp",
                    "has_been": "snooped_swamp",
                    "locked": {
                        "locked_text": "How could you decode these...",
                        "locked_checkpoint": "swamp_key_items",
                        "locked_scene": "swamp",
                        "inventory_need": {
                            "decoder": True
                        }
                    },
                },
                "option_three": {
                    "Text": "Leave",
                    "id": 3,
                    "follow_up_text": "Its a screwdriver and a rusty key, what could you possibly need these for...",
                    "next_checkpoint": "approach_cube",
                    "checkpoint_scene": "swamp"
                }
            }
        }
    },
    "swamp_crossroads": {  # crossroads to leave the scene *not finished*
        "dialogue": "Where do you want to go?",
        "choices": {
            "option_one": {
                "Text": "Go right [Church]",
                "id": 1,
                "follow_up_text": "you start walking right...",
                "next_checkpoint": "intro",
                "checkpoint_scene": "church"
            },
            "option_two": {
                "Text": "Go left [Farm]",
                "id": 2,
                "follow_up_text": "you start walking left...",
                "next_checkpoint": "intro",
                "checkpoint_scene": "farm"
            },
            "option_three": {
                "Text": "Go forward [Village Center]",
                "id": 3,
                "follow_up_text": "you start walking forward",
                "next_checkpoint": "intro",
                "checkpoint_scene": "center"
            }
        }
    },
    "approach_cube": {
        "tag": "cube_choice",
        "dialogue": "Suddenly, the cube flashes with a bright light...",
        "choices": {
            "option_one": {
                "Text": "get closer",
                "id": 1,
                "follow_up_text": "Its just a funny looking cube...",
                "next_checkpoint": "intuition_test",
                "checkpoint_scene": "swamp"
            },
            "option_two": {
                "Text": "back away",
                "id": 2,
                "follow_up_text": "The cube pulses with the light, it draws you close",
                "next_checkpoint": "intuition_test",
                "checkpoint_scene": "swamp"
            }
        }
    },
    # endregion
    # Intuition Test
    "intuition_test": {
        "question_1": {
            "tag": "intuition_1",
            "dialogue": "The cube hums...",
            "choices": {
                "option_one": {
                    "Text": "pick it up",
                    "id": 1,
                    "next_checkpoint": "question_2"
                },
                "option_two": {
                    "Text": "touch it",
                    "id": 2,
                    "next_checkpoint": "question_2"
                },
                "option_three": {
                    "Text": "hum with it",
                    "id": 3,
                    "next_checkpoint": "question_2"
                }
            }
        },
        "question_2": {
            "tag": "intuition_2",
            "dialogue": "A low frequency starts vibrating in your skull. You feel words that aren’t yours: 'What are you made of?'",
            "choices": {
                "option_one": {
                    "Text": "tell it to get out",
                    "id": 1,
                    "next_checkpoint": "question_3"
                },
                "option_two": {
                    "Text": "speak back",
                    "id": 2,
                    "next_checkpoint": "question_3"
                },
                "option_three": {
                    "Text": "stay silent",
                    "id": 3,
                    "next_checkpoint": "question_3"
                }
            }
        },
        "question_3": {
            "tag": "intuition_3",
            "dialogue": "A beam shines down on you...",
            "choices": {
                "option_one": {
                    "Text": "stay still",
                    "id": 1,
                    "next_checkpoint": "text"
                },
                "option_two": {
                    "Text": "run away",
                    "id": 2,
                    "next_checkpoint": "text"
                },
                "option_three": {
                    "Text": "stare up to it",
                    "id": 3,
                    "next_checkpoint": "text"
                }
            }
        }
    },
    # region After Intuition Test Scenes
    "make_choice": {  # choose for ending after test if you got the curious result
        "tag": "curious_choice",
        "dialogue": "The Aliens are captivated by your curiosity they wish for you to stay so they may study you",
        "choices": {
            "option_one": {
                "Text": "Stay on the ship",
                "id": 1,
                "next_checkpoint": "belong_ending",
                "checkpoint_scene": "swamp"
            },
            "option_two": {
                "Text": "Ask to leave",
                "id": 2,
                "next_checkpoint": "intuition_ending",
                "checkpoint_scene": "swamp"
            }
        }
    },
    "after_test_start": {
        "dialogue": "You return back to the swamp...",
        "choices": {
            "option_one": {
                "Text": "Keep walking",
                "id": 1,
                "follow_up_text": "Looks like any possible fog is going away...",
                "next_checkpoint": "after_test_swamp",
                "checkpoint_scene": "swamp"
            },
            "option_two": {
                "Text": "go back",
                "id": 2,
                "follow_up_text": "This place is creepy, with or without fog",
                "next_checkpoint": "swamp_crossroads",
                "checkpoint_scene": "swamp"
            }
        }
    },
    "after_test_swamp": {
        "dialogue": "You can clearly see the stone structure with scribbles of foreign words around it. Not only that, you can see marks and footprints along the ground",
        "choices": {
            "option_one": {
                "Text": "look around more",
                "id": 1,
                "follow_up_text": "Why not, the aliens are gone....right?",
                "next_checkpoint": "after_test_key_items",
                "checkpoint_scene": "swamp",
                "locked": {
                    "locked_text": "You've already looked around. Theres nothing else worth getting",
                    "locked_checkpoint": "after_test_swamp",
                    "locked_scene": "swamp",
                    "explore_flag": {
                        "snooped_swamp": False
                    }
                },
            },
            "option_two": {
                "Text": "leave",
                "id": 2,
                "follow_up_text": "On second though, maybe you should go, just to be safe.",
                "next_checkpoint": "swamp_crossroads",
                "checkpoint_scene": "swamp"
            }
        }
    },
    "after_test_key_items": {
        "dialogue": "You look around the surrounding area. You find a screwdriver and a rusty key. You also are able to see those strange"
                    "letters on the side of the structure better. If only you could decipher them.",
        "choices": {
            "option_one": {
                "Text": "take the screwdriver and key",
                "id": 1,
                "follow_up_text": "This could be interesting....",
                "next_checkpoint": "after_test_key_items",
                "checkpoint_scene": "swamp",
                "has_been": "snooped_swamp",
                "locked": {
                    "locked_text": "You have already picked up these items",
                    "locked_checkpoint": "after_test_key_items",
                    "locked_scene": "swamp",
                    "inventory_need": {
                        "key": False,
                        "screwdriver": False
                    }
                },
            },
            "option_two": {
                "Text": "Use decoder",
                "id": 2,
                "follow_up_text": "you pocket the hammer and key, then use your decoder to read the strange "
                                  "words. (placeholder)",
                "next_checkpoint": "after_test_key_items",
                "checkpoint_scene": "swamp",
                "has_been": "snooped_swamp",
                "locked": {
                    "locked_text": "How could you decode these...",
                    "locked_checkpoint": "after_test_key_items",
                    "locked_scene": "swamp",
                    "inventory_need": {
                        "decoder": True
                    }
                },
            },
            "option_three": {
                "Text": "Leave",
                "id": 3,
                "follow_up_text": "Its a screwdriver and a rusty key, what could you possibly need these for...",
                "next_checkpoint": "swamp_crossroads",
                "checkpoint_scene": "swamp"
            }
        }
    },
    # endregion
    # region Swamp Endings
    "rejected_ending": {
        "dialogue": "Your pathetic, the aliens probe you, dissect you, then discard you.",
        "ending_key": "rejected"
    },
    "probed_ending": {
        "dialogue": "Your average, the aliens probe you, wipe your memory and send you back to the forest.Your found by a farmer the next day...",
        "ending_key": "probed"
    },
    "belong_ending": {
        "dialogue": "The Aliens cheer as they usher you into the bridge. Their captain standing tall, with an outreached hand...",
        "ending_key": "you_belong"
    },
    "intuition_ending": {
        "dialogue": "The Aliens are sad to see you go but wish you all the best. They give you a vial filled with blue liquid as a parting gift",
        "ending_key": "intuition_pass",
        "next_checkpoint": "after_test_swamp",
        "checkpoint_scene": "swamp",
        "inventory_need": {
            "blue_vial": False,
        }
    },
    # endregion
}

# Church Dictionary: State of the church is conditional [priest inside the church, church is empty, the basement door is open]
church_scene_dict = {
    "intro": {
        "dialogue": "After awhile, you see a church among the trees, do you approach or "
                    "turn around?",
        "choices": {
            "option_one": {
                "Text": "Go to the Church",
                "id": 1,
                "follow_up_text": "You decide to walk towards the church...",
                "next_checkpoint": "start_position",
                "checkpoint_scene": "church"
            },
            "option_two": {
                "Text": "Turn Around",
                "id": 2,
                "follow_up_text": "You decide to turn around walking back to where you came from. "
                                  "Theres a crossroads...",
                "next_checkpoint": "church_crossroads",
                "checkpoint_scene": "church"
            }
        }
    },
    # region Main Church Scenes
    "start_position": {
        "church_is_empty": {
            "dialogue": "As you get closer to the church, you cant see any lights or hear any voices, it might be abandoned...",
            "choices": {
                "option_one": {
                    "Text": "Go in",
                    "id": 1,
                    "follow_up_text": "Despite the alarming silence around this church you decide to walk in the door",
                    "next_checkpoint": "inside_church",
                    "checkpoint_scene": "church"
                },
                "option_two": {
                    "Text": "Turn and Leave",
                    "id": 2,
                    "follow_up_text": "This church looks too creepy, best to walk away....",
                    "next_checkpoint": "church_crossroads",
                    "checkpoint_scene": "church"
                }
            }
        },
        "priest_inside": {
            "dialogue": "As you get closer to the church, you can faintly hear someone singing, theres a light emitting from one of the windows.",
            "choices": {
                "option_one": {
                    "Text": "Go in",
                    "id": 1,
                    "follow_up_text": "Its a church...how bad could it be",
                    "next_checkpoint": "inside_church",
                    "checkpoint_scene": "church"
                },
                "option_two": {
                    "Text": "Turn and Leave",
                    "id": 2,
                    "follow_up_text": "Perhaps small lights and faint singing does not equate to safety, you walk away...",
                    "next_checkpoint": "church_crossroads",
                    "checkpoint_scene": "church"
                }
            }
        },
        "basement_open": {
            "dialogue": "As you get closer to the church, you cant hear or see anything that would imply someone is there, but you have a feeling your not alone...",
            "choices": {
                "option_one": {
                    "Text": "Go in",
                    "id": 1,
                    "follow_up_text": "Im sure its just nerves, you head for the door...",
                    "next_checkpoint": "inside_church",
                    "checkpoint_scene": "church"
                },
                "option_two": {
                    "Text": "Turn and Leave",
                    "id": 2,
                    "follow_up_text": "Something about the energy here isn't right, you walk away...",
                    "next_checkpoint": "church_crossroads",
                    "checkpoint_scene": "church"
                }
            }
        }
    },
    "inside_church": {
        "church_is_empty": {
            "dialogue": "The church is surprisingly clean for looking so worn down on the outside. Doesnt look like anyone is here.",
            "choices": {
                "option_one": {
                    "Text": "Explore",
                    "id": 1,
                    "follow_up_text": "No harm in exploring a church, might find something useful",
                    "next_checkpoint": "snoop_church",
                    "checkpoint_scene": "church",
                },
                "option_two": {
                    "Text": "Leave",
                    "id": 2,
                    "follow_up_text": "Its a creepy empty church in the forest, you should not be in here.",
                    "next_checkpoint": "church_crossroads",
                    "checkpoint_scene": "church"
                }
            }
        },
        "priest_inside": {
            "dialogue": "The door is slightly ajar. When you walk in there is a priest facing the murals on the "
                        "back wall, hes lighting candles and singing a hymnn softly. doesnt seem like he heard you come in.",
            "choices": {
                "option_one": {
                    "Text": "Approach the priest",
                    "id": 1,
                    "follow_up_text": "You slowly approach the priest, just as your about to tap his shoulder he turns...",
                    "next_checkpoint": "faith_test",
                    "checkpoint_scene": "church"
                },
                "option_two": {
                    "Text": "Sit in the back pew",
                    "id": 2,
                    "follow_up_text": "he could be praying, maybe wait and let him finish...Once the priest finishes his song he turns and sees you sitting, he approaches...",
                    "next_checkpoint": "faith_test",
                    "checkpoint_scene": "church",
                },
                "option_three": {
                    "Text": "kill the priest",
                    "id": 3,
                    "checkpoint_scene": "church",
                    "follow_up_text": "You quietly sneak up on the priest, and kill him",
                    "next_checkpoint": "priest_death_ending",
                    "is_displayed": False,
                    "locked": {
                        "locked_text": "You instinctively reach for a weapon, you dont have...",
                        "locked_checkpoint": "inside_church",
                        "locked_scene": "church",
                        "inventory_need": {
                            "knife": True,
                            "hammer": True,
                            "screwdriver": True
                        },
                    }
                },
            }
        },
        "basement_open": {
            "tag": "basement_door_choice",
            "dialogue": "You enter the church cautiously, you were right, its abandoned, except for...that small light...emitting from the cellar door...",
            "choices": {
                "option_one": {
                    "Text": "Yell hello down the stairs",
                    "id": 1,
                    "follow_up_text": "No harm in calling out...right?. A couple of voices can be heard before a man ascends up the stairs, he looks like a priest.",
                    "next_checkpoint": "faith_test",
                    "checkpoint_scene": "church"
                },
                "option_two": {
                    "Text": "sit in the back pew and wait",
                    "id": 2,
                    "follow_up_text": "Someone is bound to come upstairs eventually...10 minutes later you hear someone ascend up the stairs, he looks like a priest. He walks towards you. ",
                    "next_checkpoint": "faith_test",
                    "checkpoint_scene": "church"
                },
                "option_three": {
                    "Text": "go downstairs",
                    "id": 3,
                    "follow_up_text": "its just a light....",
                    "next_checkpoint": "church_basement",
                    "checkpoint_scene": "church"
                }
            }
        }
    },
    "church_crossroads": {  # crossroads to leave the scene *not finished*
        "dialogue": "Where do you want to go?",
        "choices": {
            "option_one": {
                "Text": "Go left [Swamp]",
                "id": 1,
                "follow_up_text": "you decide to walk left...",
                "next_checkpoint": "intro",
                "checkpoint_scene": "swamp"
            },
            "option_two": {
                "Text": "Go forward [Village Center]",
                "id": 2,
                "follow_up_text": "you decide to walk forward...",
                "next_checkpoint": "intro",
                "checkpoint_scene": "center"
            }
        }
    },
    "church_basement": {
        "tag": "basement_choice",
        "dialogue": "As you descend the stairs you begin to smell a sickly burning odor. As you reach the bottom stair and "
                    "turn into the small room you see 2 people wearing robes and masks. They are holding a man on a stone table in place as another burns something into his skin",
        "choices": {
            "option_one": {
                "Text": "yell for them to stop",
                "id": 1,
                "follow_up_text": "This is cruel, you scream at them, they realize your not one of them...better run",
                "next_checkpoint": "altar_ending",
                "checkpoint_scene": "church"
            },
            "option_two": {
                "Text": "sneak back up the stairs",
                "id": 2,
                "follow_up_text": "your not supposed to see this, you attempt to quickly and silently go back up the stairs...",
                "next_checkpoint": "basement_ritual",
                "checkpoint_scene": "church"
            },
            "option_three": {
                "Text": "stand there in shock",
                "id": 3,
                "follow_up_text": "What did you just stumble upon?",
                "next_checkpoint": "basement_ritual",
                "checkpoint_scene": "church"
            },
            "option_four": {  # lore item
                "Text": "wear the farmhouse mask",
                "id": 4,
                "follow_up_text": "You place the mask on that you got from the farmhouse. The cloaked figures turn to face "
                                  "you, acknowledge you, then direct their attention back to the man on the table. The cloaked figures continue their"
                                  " barbaric branding, you inch closer to see what it is theyre branding on his skin. "
                                  "When you get close enough you see strange symbols, you can make out one though, a cube. ",
                "next_checkpoint": "basement_ritual",
                "checkpoint_scene": "church",
                "is_displayed": False,
                "locked": {
                    "locked_text": "if only you could blend in...",
                    "locked_checkpoint": "basement_ritual",
                    "locked_scene": "church",
                    "inventory_need": {
                        "mask": True,
                    }
                }
            }
        }
    },
    "basement_ritual": {
        "tag": "basement_two_choice",
        "dialogue": "The cloaked figures stop what they're doing and look at each-other, whispering in a strange dialect before slowly turning towards you.",
        "choices": {
            "option_one": {
                "Text": "apologize",
                "id": 1,
                "follow_up_text": "One of the figures approaches. they remove their mask and robe and lead you back up the stairs",
                "next_checkpoint": "faith_test",
                "checkpoint_scene": "church"
            },
            "option_two": {
                "Text": "'i dont want any trouble'",
                "id": 2,
                "follow_up_text": "One of the figures approaches. they remove their mask and robe and lead you back up the stairs",
                "next_checkpoint": "faith_test",
                "checkpoint_scene": "church"
            },
            "option_three": {
                "Text": "run",
                "id": 3,
                "follow_up_text": "You dont plan on sticking around",
                "next_checkpoint": "altar_ending",
                "checkpoint_scene": "church"
            }
        }
    },
    "snoop_church": {
        "dialogue": "The church looks cleanly upkept.",
        "choices": {
            "option_one": {
                "Text": "leave",
                "id": 1,
                "follow_up_text": "Doesnt look like anything worth looking at",
                "next_checkpoint": "church_crossroads",
                "checkpoint_scene": "church"
            },
            "option_two": {
                "Text": "explore",
                "id": 2,
                "follow_up_text": "You walk around the church, looking at everything",
                "next_checkpoint": "church_key_items",
                "checkpoint_scene": "church",
                "locked": {
                    "locked_text": "You've already explored this area",
                    "locked_checkpoint": "snoop_church",
                    "locked_scene": "church",
                    "explore_flag": {
                        "snooped_church": False
                    }
                },
            }
        }
    },
    "church_key_items": {
        "dialogue": "You explore around the church. Theres a cellar door but its locked. You find a bible and a paper with strange symbols and a translation...",
        "choices": {
            "option_one": {
                "Text": "take the bible and paper",
                "id": 1,
                "follow_up_text": "You take the items, no use in them collecting dust here",
                "next_checkpoint": "church_crossroads",
                "checkpoint_scene": "church",
                "has_been": "snooped_church",
                "locked": {
                    "locked_text": "You have already picked up these items",
                    "locked_checkpoint": "church_key_items",
                    "locked_scene": "church",
                    "inventory_need": {
                        "bible": False,
                        "decoder": False
                    }
                }
            },
            "option_two": {
                "Text": "leave",
                "id": 2,
                "follow_up_text": "whatever god is worshipped in here might not like us stealing, you leave the items",
                "next_checkpoint": "church_crossroads",
                "checkpoint_scene": "church"
            }
        }
    },
    # endregion
    # Faith Test
    "faith_test": {
        "question_1": {
            "tag": "faith_1",
            "dialogue": "The priest greets you with a warm smile. 'What is your name child?'",
            "choices": {
                "option_one": {
                    "Text": "ask for the priests name",
                    "id": 1,
                    "follow_up_text": "The priest smirks. 'My name is (placeholder), you have nothing to fear young star beam.",
                    "next_checkpoint": "question_2"
                },
                "option_two": {
                    "Text": "refuse to tell him your name",
                    "id": 2,
                    "follow_up_text": "The priest nods. Your mind is closed off, from fear?",
                    "next_checkpoint": "question_2"
                },
                "option_three": {
                    "Text": "tell the priest your name",
                    "id": 3,
                    "follow_up_text": "A name carved of stardust, how uniquely you.",
                    "next_checkpoint": "question_2"
                }
            }
        },
        "question_2": {
            "tag": "faith_2",
            "dialogue": "The priest walks to the pew in the first row and sits down. 'Will you join me?'",
            "choices": {
                "option_one": {
                    "Text": "'I'll stand'",
                    "id": 1,
                    "follow_up_text": "You walk to the front row but stand next to him instead of sitting.",
                    "next_checkpoint": "question_3"
                },
                "option_two": {
                    "Text": "'Sure, thanks'",
                    "id": 2,
                    "follow_up_text": "You join the priest and sit down, making sure theres ample space between you",
                    "next_checkpoint": "question_3"
                },
                "option_three": {
                    "Text": "'Id be honored'",
                    "id": 3,
                    "follow_up_text": "You join the priest and sit down next to him",
                    "next_checkpoint": "question_3"
                }
            }
        },
        "question_3": {
            "tag": "faith_3",
            "dialogue": "The priest glances down at your bare muddy feet. 'Youve walked far. Seeking something?'",
            "choices": {
                "option_one": {
                    "Text": "A way out",
                    "id": 1,
                    "follow_up_text": "The priest clutches his bible tighter",
                    "next_checkpoint": "question_4"
                },
                "option_two": {
                    "Text": "Enlightment",
                    "id": 2,
                    "follow_up_text": "The priest smiles warmly",
                    "next_checkpoint": "question_4"
                },
                "option_three": {
                    "Text": "Answers",
                    "id": 3,
                    "follow_up_text": "the priest nods slow",
                    "next_checkpoint": "question_4"
                }
            }
        },
        "question_4": {
            "tag": "faith_4",
            "dialogue": "Do you believe in signs from above",
            "choices": {
                "option_one": {
                    "Text": "Absolutely not",
                    "id": 1,
                    "follow_up_text": "The priest smiles, 'your will is strong'",
                    "next_checkpoint": "question_5"
                },
                "option_two": {
                    "Text": "sometimes, depends.",
                    "id": 2,
                    "follow_up_text": "Ah yes, the conditional believer...",
                    "next_checkpoint": "question_5"
                },
                "option_three": {
                    "Text": "of course",
                    "id": 3,
                    "follow_up_text": "The priest gazes at the murals before him",
                    "next_checkpoint": "question_5"
                }
            }
        },
        "question_5": {
            "tag": "faith_5",
            "dialogue": "he notices your gaze on his book. its covered in pale yellow leather, 'You may read?', he holds out the book for you to take.",
            "choices": {
                "option_one": {
                    "Text": "refuse to touch it",
                    "id": 1,
                    "follow_up_text": "The priests eye subtly twitches but he shrugs it off and smiles, 'thats alright'",
                    "next_checkpoint": "question_6"
                },
                "option_two": {
                    "Text": "glance through it",
                    "id": 2,
                    "follow_up_text": "You see glimpses of tall people, strange symbols, and a vial of liquid",
                    "next_checkpoint": "question_6"
                },
                "option_three": {
                    "Text": "read it carefully",
                    "id": 3,
                    "follow_up_text": "You see drawings of tall bipedal creatures, a cube, a statue, and 3 vials",
                    "next_checkpoint": "question_6"
                }
            }
        },
        "question_6": {
            "tag": "faith_6",
            "dialogue": "The priest stands up, gazing out the window, 'Will you stay for the ritual tomorrow?'",
            "choices": {
                "option_one": {
                    "Text": "no",
                    "id": 1,
                    "follow_up_text": "the priest begins to softly hum a hymnn",
                    "next_checkpoint": "text"
                },
                "option_two": {
                    "Text": "havent decided yet",
                    "id": 2,
                    "follow_up_text": "the priest speaks to himself, 'The beams will shine brightly, such a sight to see the chosen break free'",
                    "next_checkpoint": "text"
                },
                "option_three": {
                    "Text": "yes",
                    "id": 3,
                    "follow_up_text": "the priest turns to face you, smiling",
                    "next_checkpoint": "text"
                }
            }
        }
    },
    # region After Faith Test Scenes
    "after_test_start": {  # go to farm or barn
        "dialogue": "You return to the church...",
        "choices": {
            "option_one": {
                "Text": "Go inside",
                "id": 1,
                "follow_up_text": "You start making your way to the church...",
                "next_checkpoint": "after_test_church",
                "checkpoint_scene": "church"
            },
            "option_two": {
                "Text": "Leave",
                "id": 2,
                "follow_up_text": "You start making your way to the crossroads...",
                "next_checkpoint": "church_crossroads",
                "checkpoint_scene": "church"
            }
        }
    },
    "after_test_church": {  # after test explore
        "dialogue": "The priest is situated in the front, silently saying a prayer with outstretched arms, your free to explore the church",
        "choices": {
            "option_one": {
                "Text": "explore",
                "id": 1,
                "follow_up_text": "You decide to walk around...",
                "next_checkpoint": "after_test_key_items",
                "checkpoint_scene": "church",
                "locked": {
                    "locked_text": "You've already explored this area",
                    "locked_checkpoint": "after_test_church",
                    "locked_scene": "church",
                    "explore_flag": {
                        "snooped_church": False
                    }
                },
            },
            "option_two": {
                "Text": "leave",
                "id": 2,
                "follow_up_text": "You decide to turn around walking back to where you came from. "
                                  "Theres a crossroads...",
                "next_checkpoint": "church_crossroads",
                "checkpoint_scene": "church"
            }
        }
    },
    "after_test_key_items": {
        "dialogue": "You explore around the church. Theres a cellar door but its locked. You find a bible and a paper with strange symbols and a translation...",
        "choices": {
            "option_one": {
                "Text": "take the bible and paper",
                "id": 1,
                "follow_up_text": "You take the items, no use in them collecting dust here",
                "next_checkpoint": "church_crossroads",
                "checkpoint_scene": "church",
                "has_been": "snooped_church",
                "locked": {
                    "locked_text": "You have already picked up these items",
                    "locked_checkpoint": "after_test_key_items",
                    "locked_scene": "church",
                    "inventory_need": {
                        "bible": False,
                        "decoder": False
                    }
                }
            },
            "option_two": {
                "Text": "leave",
                "id": 2,
                "follow_up_text": "you leave the items, no use in a bible and paper.",
                "next_checkpoint": "church_crossroads",
                "checkpoint_scene": "church"
            }
        }
    },
    # endregion
    # region Church Endings
    "believer_ending": {
        "dialogue": "the priest sees light within your eyes, youve been asked to join the village",
        "ending_key": "believer"
    },
    "faith_ending": {
        "dialogue": "The priest respects your autonomy as you do his. Your free to explore the church respectfully. The Priest gives you a green vial from his pocket and tells you to seek answers in the center.",
        "ending_key": "faith_pass",
        "next_checkpoint": "after_test_church",
        "checkpoint_scene": "church",
        "inventory_need": {
            "green_vial": False,
        }
    },
    "heretics_ending": {
        "dialogue": "The priest is insulted by your disrespect. He opens the door to the basement ringing a bell. Your put in a cage to be sacrificed in the ritual.",
        "ending_key": "heretic"
    },
    "priest_death_ending": {
        "dialogue": "The priest falls to your feet, a pool of blood forming. A follower enters the church and yells for help. "
                    "Before you know it there are five figures dressed in robes wearing masks surrounding you. they beat you to death.",
        "ending_key": "priest_death"
    },
    "altar_ending": {
        "dialogue": "All 3 cloaked figures chase after you. they capture you and put you in a cage in the basement. One figure "
                    "takes off their mask and robe before approaching you, he looks like a priest. 'Blessed are the chosen. Youve been chosen for the ritual tomorrow",
        "ending_key": "altar"
    }
    # endregion
}

# Farm Dictionary: Farmer location is conditional [inside the house, sitting outside, inside the barn]
farm_scene_dict = {
    "intro": {
        "dialogue": "After awhile, you see a farm at the bottom of a hill in the distance, do you "
                    "approach or turn around?",
        "choices": {
            "option_one": {
                "Text": "Go to the Farm",
                "id": 1,
                "follow_up_text": "You decide to walk towards the farm...",
                "next_checkpoint": "start_position",
                "checkpoint_scene": "farm"
            },
            "option_two": {
                "Text": "Turn Around",
                "id": 2,
                "follow_up_text": "You decide to turn around walking back to where you came from. "
                                  "Theres a crossroads...",
                "next_checkpoint": "farm_crossroads",
                "checkpoint_scene": "farm"
            }
        }
    },
    # region Main farm Scene
    "start_position": {  # go to farm or barn
        "tag": "start_choice",
        "farmer_in_house": {
            "dialogue": "You walk forward getting closer to the farm, on one seems to be around.",
            "choices": None
        },
        "farmer_outside": {
            "dialogue": "You walk forward getting closer to the farm, you notice a man sitting on the porch",
            "choices": None
        },
        "farmer_in_barn": {
            "dialogue": "You walk forward getting closer to the farm, you notice a man walk into the barn",
            "choices": None
        },
        "choices": {
            "option_one": {
                "Text": "Walk to the Farmhouse",
                "id": 1,
                "follow_up_text": "You start making your way to the farmhouse...",
                "next_checkpoint": "choose_farmhouse",
                "checkpoint_scene": "farm"
            },
            "option_two": {
                "Text": "Walk to the Barn",
                "id": 2,
                "follow_up_text": "You start making your way to the barn...",
                "next_checkpoint": "choose_barn",
                "checkpoint_scene": "farm"
            }
        }
    },
    "choose_farmhouse": {  # you go to the farmhouse
        "farmer_in_house": {
            "tag": "knock_choice",
            "dialogue": "You walk up to the farmhouse door, you can hear someone on the other side of the door",
            "choices": {
                "option_one": {
                    "Text": "Knock on the door",
                    "id": 1,
                    "follow_up_text": " After a couple minutes a man opens the door greeting you",
                    "next_checkpoint": "meet_farmer",
                    "checkpoint_scene": "farm"
                },
                "option_two": {
                    "Text": "Bang on the door",
                    "id": 2,
                    "follow_up_text": "After a couple minutes a man swings the door open, visibly annoyed",
                    "next_checkpoint": "meet_farmer",
                    "checkpoint_scene": "farm"
                },
                "option_three": {
                    "Text": "Turn around and leave",
                    "id": 3,
                    "follow_up_text": "You turn and leave, maybe best not to bother whoever that is...",
                    "next_checkpoint": "house_crossroads",
                    "checkpoint_scene": "farm"
                }
            }
        },
        "farmer_outside": {
            "dialogue": "You walk towards the man sitting in a rocking chair on the porch he raises up a hand to greet you",
            "choices": {
                "option_one": {
                    "Text": "wave back",
                    "id": 1,
                    "follow_up_text": "The farmer smiles and stands up, beckoning you over",
                    "next_checkpoint": "meet_farmer",
                    "checkpoint_scene": "farm"
                },
                "option_two": {
                    "Text": "walk up to him without saying a word",
                    "id": 2,
                    "follow_up_text": "You silently walk towards the farmer, he stands up and crosses his arms looking down at you from the porch.",
                    "next_checkpoint": "meet_farmer",
                    "checkpoint_scene": "farm"
                }
            }
        },
        "farmer_in_barn": {
            "dialogue": "You walk up to the farmhouse door, doesnt sound like anyone is home",
            "choices": {
                "option_one": {
                    "Text": "go in",
                    "id": 1,
                    "follow_up_text": "You knock on the door and theres no answer, you open it slowly....",
                    "next_checkpoint": "snoop_house",
                    "checkpoint_scene": "farm",
                },
                "option_two": {
                    "Text": "Turn around",
                    "id": 2,
                    "follow_up_text": "You knock but theres no answer. No use in snooping, you turn and walk away.",
                    "next_checkpoint": "house_crossroads",
                    "checkpoint_scene": "farm"
                },
            }
        }
    },
    "choose_barn": {  # you go to the barn *not finished*
        "farmer_in_house": {  # random event condition
            "dialogue": "You walk up to the barn door. its quiet, doesnt sound like anyone is in there",
            "choices": {
                "option_one": {
                    "Text": "go in",
                    "id": 1,
                    "follow_up_text": "You call out, but theres no answer. You walk in slowly...",
                    "next_checkpoint": "snoop_barn",
                    "checkpoint_scene": "farm"
                },
                "option_two": {
                    "Text": "turn around and leave",
                    "id": 2,
                    "follow_up_text": "No one is here, no use in snooping.",
                    "next_checkpoint": "barn_crossroads",
                    "checkpoint_scene": "farm"
                }
            }
        },
        "farmer_outside": {
            "dialogue": "The farmer watches you walk over to the barn from the house. He calls you over to him",
            "choices": {
                "option_one": {
                    "Text": "Walk to the farmhouse",
                    "id": 1,
                    "follow_up_text": "You turn and make your way to the farmhouse, the farmer stands at the end of the porch for your arrival",
                    "next_checkpoint": "meet_farmer",
                    "checkpoint_scene": "farm"
                },
                "option_two": {
                    "Text": "ignore him and keep walking to the barn",
                    "id": 2,
                    "follow_up_text": "You keep walking to the barn, you see in the corner of your eye, the farmer getting up and making his way to you.",
                    "next_checkpoint": "butcher_ending",
                    "checkpoint_scene": "farm"
                }
            }
        },
        "farmer_in_barn": {
            "dialogue": "You walk up to the barn door, and see a man sharpening a knife",
            "choices": {
                "option_one": {
                    "Text": "back away slowly",
                    "id": 1,
                    "follow_up_text": "The man looks up at you, suspiciously",
                    "next_checkpoint": "meet_farmer",
                    "checkpoint_scene": "farm"
                },
                "option_two": {
                    "Text": "knock on the barn door",
                    "id": 2,
                    "follow_up_text": "The farmer looks up at you slightly confused, waiting...",
                    "next_checkpoint": "meet_farmer",
                    "checkpoint_scene": "farm"
                },
            }
        }
    },
    "snoop_house": {
        "dialogue": "The house is decorated, looks old and lived in.",
        "choices": {
            "option_one": {
                "Text": "leave",
                "id": 1,
                "follow_up_text": "Doesnt look like anything worth looking at",
                "next_checkpoint": "house_crossroads",
                "checkpoint_scene": "farm"
            },
            "option_two": {
                "Text": "explore",
                "id": 2,
                "follow_up_text": "You walk around the house, looking at everything",
                "next_checkpoint": "house_key_items",
                "checkpoint_scene": "farm",
                "locked": {
                    "locked_text": "You've already explored this area",
                    "locked_checkpoint": "snoop_house",
                    "locked_scene": "farm",
                    "explore_flag": {
                        "snooped_house": False
                    }
                },
            }
        }
    },
    "snoop_barn": {
        "dialogue": "The barn is decorated, besides a wall of tools theres not much, not even animals...",
        "choices": {
            "option_one": {
                "Text": "leave",
                "id": 1,
                "follow_up_text": "Doesnt look like anything worth looking at",
                "next_checkpoint": "barn_crossroads",
                "checkpoint_scene": "farm"
            },
            "option_two": {
                "Text": "explore",
                "id": 2,
                "follow_up_text": "You walk around the barn, looking at everything",
                "next_checkpoint": "barn_key_items",
                "checkpoint_scene": "farm",
                "locked": {
                    "locked_text": "You've already explored this area",
                    "locked_checkpoint": "snoop_barn",
                    "locked_scene": "farm",
                    "explore_flag": {
                        "snooped_barn": False
                    }
                },
            }
        }
    },
    "barn_key_items": {
        "dialogue": "While exploring the barn you stumble upon an old hammer and a mask",
        "choices": {
            "option_one": {
                "Text": "leave the items",
                "id": 1,
                "follow_up_text": "you leave the items, theyre not yours to take.",
                "next_checkpoint": "barn_crossroads",
                "checkpoint_scene": "farm"
            },
            "option_two": {
                "Text": "take the items",
                "id": 2,
                "follow_up_text": "you take the items, finders keepers.",
                "next_checkpoint": "barn_crossroads",
                "checkpoint_scene": "farm",
                "has_been": "snooped_barn",
                "locked": {
                    "locked_text": "You have already picked up these items",
                    "locked_checkpoint": "barn_key_items",
                    "locked_scene": "farm",
                    "inventory_need": {
                        "mask": False,
                        "hammer": False
                    }
                },
            }
        }
    },
    "house_key_items": {
        "dialogue": "While exploring the house you stumble upon a letter and a large butcher knife",
        "choices": {
            "option_one": {
                "Text": "leave the items",
                "id": 1,
                "follow_up_text": "you leave the items, theyre not yours to take.",
                "next_checkpoint": "house_crossroads",
                "checkpoint_scene": "farm"
            },
            "option_two": {
                "Text": "take the items",
                "id": 2,
                "follow_up_text": "you take the items, finders keepers.",
                "next_checkpoint": "house_crossroads",
                "checkpoint_scene": "farm",
                "has_been": "snooped_house",
                "locked": {
                    "locked_text": "You have already picked up these items",
                    "locked_checkpoint": "house_key_items",
                    "locked_scene": "farm",
                    "inventory_need": {
                        "letter": False,
                        "knife": False
                    }
                },
            }
        }
    },
    # endregion
    # region Crossroads
    "farm_crossroads": {  # crossroads to leave the scene
        "dialogue": "Where do you want to go?",
        "choices": {
            "option_one": {
                "Text": "Go right [Swamp]",
                "id": 1,
                "follow_up_text": "you start walking right...",
                "next_checkpoint": "intro",
                "checkpoint_scene": "swamp"
            },
            "option_two": {
                "Text": "Go forward [Village Center]",
                "id": 2,
                "follow_up_text": "you start walking forward...",
                "next_checkpoint": "intro",
                "checkpoint_scene": "center"
            }
        }
    },
    "house_crossroads": {  # crossroads when leaving the house
        "dialogue": "Where do you want to go?",
        "choices": {
            "option_one": {
                "Text": "Go to the crossroads",
                "id": 1,
                "follow_up_text": "You turn around and walk back up the hill to the crossroads...",
                "next_checkpoint": "farm_crossroads",
                "checkpoint_scene": "farm"
            },
            "option_two": {
                "Text": "Go to barn",
                "id": 2,
                "follow_up_text": "You turn and walk towards the barn...",
                "next_checkpoint": "choose_barn",
                "checkpoint_scene": "farm"
            }
        }
    },
    "barn_crossroads": {  # crossroads when leaving the barn
        "dialogue": "Where do you want to go?",
        "choices": {
            "option_one": {
                "Text": "Go to the crossroads",
                "id": 1,
                "follow_up_text": "You turn around and walk back up the hill to the crossroads...",
                "next_checkpoint": "farm_crossroads",
                "checkpoint_scene": "farm"
            },
            "option_two": {
                "Text": "Go to the farmhouse",
                "id": 2,
                "follow_up_text": "You turn and walk towards the house...",
                "next_checkpoint": "choose_farmhouse",
                "checkpoint_scene": "farm"
            }
        }
    },
    "meet_farmer": {
        "tag": "meet_choice",
        "dialogue": 'The farmer stands there, waiting...',
        "choices": {
            "option_one": {
                "Text": "Greet him politely.",
                "id": 1,
                "follow_up_text": "You say hello to the farmer. The farmer smiles...",
                "next_checkpoint": "trust_test",
                "checkpoint_scene": "farm"
            },
            "option_two": {
                "Text": "kill the farmer.",
                "id": 2,
                "follow_up_text": "You reach for a weapon...",
                "next_checkpoint": "farmer_death_ending",
                "checkpoint_scene": "farm",
                "is_displayed": False,
                "locked": {
                    "locked_text": "You reach for a weapon you don't have...",
                    "locked_checkpoint": "meet_farmer",
                    "locked_scene": "farm",
                    "inventory_need": {
                        "knife": True,
                        "hammer": True,
                        "screwdriver": True
                    }
                }
            }
        }
    },
    # endregion
    # Trust Test
    "trust_test": {
        "question_1": {
            "tag": "trust_1",
            "dialogue": "Howdy there stranger whats your name",
            "choices": {
                "option_one": {
                    "Text": "ignore him and ask for his name",
                    "id": 1,
                    "follow_up_text": "The farmer looks at you suspiciously. My name is (placeholder).",
                    "next_checkpoint": "question_2"
                },
                "option_two": {  # trust pt
                    "Text": "tell the farmer your name",
                    "id": 2,
                    "follow_up_text": "Why that's a great name, my name is (placeholder), welcome to my farm",
                    "next_checkpoint": "question_2"
                }
            }
        },
        "question_2": {
            "tag": "trust_2",
            "dialogue": "You alright partner? the farmer looks down at your bare feet covered in mud",
            "choices": {
                "option_one": {  # trust point
                    "Text": "ask for help",
                    "id": 1,
                    "follow_up_text": "The farmers face softens. Why dont you come in and i'll help you get all sorted",
                    "next_checkpoint": "question_3"
                },
                "option_two": {
                    "Text": "ask where you are",
                    "id": 2,
                    "follow_up_text": "I got a map you can look at. Why dont you come in and i'll help you get all sorted.",
                    "next_checkpoint": "question_3"
                },
            }
        },
        "question_3": {
            "tag": "trust_3",
            "dialogue": "The farmer welcomes you into his home, gesturing to a nearby dining table for you to sit at. Like some ice tea, friend?",
            "choices": {
                "option_one": {
                    "Text": "decline the ice tea",
                    "id": 1,
                    "follow_up_text": "the farmer turns to stare you down before smiling and pouring himself a glass and sitting down with you.",
                    "next_checkpoint": "question_4"
                },
                "option_two": {  # trust pt
                    "Text": "accept the ice tea",
                    "id": 2,
                    "follow_up_text": "The farmer pours you both a glass of ice tea setting it in front of you. Its my gammies famous recipe, generational ice tea right there",
                    "next_checkpoint": "question_4"
                }
            }
        },
        "question_4": {
            "tag": "trust_4",
            "dialogue": "The farmer takes a sip, savoring the taste before smacking his lips. Yep, nothing beats good "
                        "old fashioned sweet tea. Yknow it was actually my grandpappi that started this farm here.",
            "choices": {
                "option_one": {  # trust point
                    "Text": "ask him more about his family",
                    "id": 1,
                    "follow_up_text": "The farmer smiles wide. His name was (placeholder)He helped discover this here village, course back then it was just a meateor site",
                    "next_checkpoint": "question_5"
                },
                "option_two": {
                    "Text": "remind him about helping you",
                    "id": 2,
                    "follow_up_text": "The farmer takes another slow sip, staring you down. Y'know my great grandpappi was a founder of this here town, respect outta be in order for you.",
                    "next_checkpoint": "question_5"
                },
            }
        },
        "question_5": {
            "tag": "trust_5",
            "dialogue": "My family helped keep this town fed. Back then we didn't have all the tools and knowledge we did, but food preparation has always been what it once was. The farmer gives you a big gummy smile",
            "choices": {
                "option_one": {
                    "Text": "change the subject",
                    "id": 1,
                    "follow_up_text": "The farmer slowly drops his smile. You look hungry.",
                    "next_checkpoint": "question_6"
                },
                "option_two": {  # trust pt
                    "Text": "smile as well",
                    "id": 2,
                    "follow_up_text": "The farmer looks at you as if studying your physique. You look like you could use a meal",
                    "next_checkpoint": "question_6"
                }
            }
        },
        "question_6": {
            "tag": "trust_6",
            "dialogue": "The farmer stands up and walks into the kitchen. You hear sounds of dishes and cutlery. After awhile "
                        "the farmer comes back with 2 steaming bowls of stew. He sets the bowl in front of you. Cant help ya on an empty stomach, go ahead and dig in",
            "choices": {
                "option_one": {  # trust point
                    "Text": "accept and start eating the stew",
                    "id": 1,
                    "follow_up_text": "The farmer smiles as you start eating, enjoying his own bowl.",
                    "next_checkpoint": "question_7"
                },
                "option_two": {
                    "Text": "refuse the stew",
                    "id": 2,
                    "follow_up_text": "The farmer pushes the bowl closer to you. I didnt ask if you wanted it. The farmer "
                                      "watches you as you reluctantly start eating the stew, a small smile tugs at the corner of his lips as he continues eating his bowl",
                    "next_checkpoint": "question_7"
                },
            }
        },
        "question_7": {
            "tag": "trust_7",
            "dialogue": "You remind me of a boy I met once. Tasted just like this. Shame what happened to him. Real shame.",
            "choices": {
                "option_one": {  # trust point
                    "Text": "stay silent",
                    "id": 1,
                    "follow_up_text": "The farmer looks back up at you smiling. Some people dont know how to accept such generous hospitality",
                    "next_checkpoint": "question_8"
                },
                "option_two": {
                    "Text": "ask him whats in the stew",
                    "id": 2,
                    "follow_up_text": "Nothing that aint good for you",
                    "next_checkpoint": "question_8"
                },
            }
        },
        "question_8": {
            "tag": "trust_8",
            "dialogue": "The farmer tries to fish something out of his stew. 'Damn i just love these things', he holds up what looks to be a small human toe, tossing it in his mouth and chewing.",
            "choices": {
                "option_one": {
                    "Text": "spit it out",
                    "id": 1,
                    "follow_up_text": "You spit out the stew, pushing th bowl away in disgust. The farmer stares you down darkly, taking your stew and pouring it into his bowl. his voice low, 'Thou shall waste not'",
                    "next_checkpoint": "question_9"
                },
                "option_two": {  # trust pt
                    "Text": "finish the stew",
                    "id": 2,
                    "follow_up_text": "You both finish your stew in silence, the farmer humming a song that sound like a hymnn.",
                    "next_checkpoint": "question_9"
                }
            }
        },
        "question_9": {
            "tag": "trust_9",
            "dialogue": "After the farmer finishes his stew he stands up and circles you, then suddenly holds a knife up to "
                        "your throat. 'Blessed are the divine meat' he inhales your scent deeply",
            "choices": {
                "option_one": {  # trust pt
                    "Text": "stay still",
                    "id": 1,
                    "follow_up_text": "The farmer licks your cheek and pulls the knife away, setting it on the counter. 'Good meat never fights back'",
                    "next_checkpoint": "text"
                },
                "option_two": {
                    "Text": "reach for his knife",
                    "id": 2,
                    "follow_up_text": "The farmer moves the knife away quickly before you can grab it, but not before barely"
                                      " nicking your skin. He licks the blood off the knife and stares you down, 'Wickedness soaks deep into the marrow' ",
                    "next_checkpoint": "text"
                    # need checkpoint for when scene is over to calculate points and pick ending
                },
            }
        },
    },
    # region After Trust Test Scenes
    "fail_choice": {  # failed the test, might have a weapon
        "dialogue": "The farmer smiles and shakes his head walking back into the kitchen, when he returns hes wearing a mask and holding a "
                    "butcher knife. 'Grandmami used to always say the wicked are packed with FLAVOUR' ",
        "choices": {
            "option_one": {
                "Text": "try to run",
                "id": 1,
                "follow_up_text": "You stand suddenly, running for the front door...",
                "next_checkpoint": "tainted_ending",
                "checkpoint_scene": "farm"
            },
            "option_two": {
                "Text": "Attack Him",
                "id": 2,
                "follow_up_text": "You reach for your weapon...",
                "next_checkpoint": "defense_ending",
                "checkpoint_scene": "farm",
                "is_displayed": False,
                "locked": {
                    "locked_text": "You reach for a weapon you dont have...",
                    "locked_checkpoint": "tainted_ending",
                    "locked_scene": "farm",
                    "inventory_need": {
                        "knife": True,
                        "hammer": True,
                        "screwdriver": True
                    }
                }
            }
        }
    },
    "after_test_start": {  # go to farm or barn
        "dialogue": "You return to the farm...",
        "choices": {
            "option_one": {
                "Text": "Walk to the Farmhouse",
                "id": 1,
                "follow_up_text": "You start making your way to the farmhouse...",
                "next_checkpoint": "after_test_house",
                "checkpoint_scene": "farm"
            },
            "option_two": {
                "Text": "Walk to the Barn",
                "id": 2,
                "follow_up_text": "You start making your way to the barn...",
                "next_checkpoint": "after_test_barn",
                "checkpoint_scene": "farm"
            }
        }
    },
    "after_test_house": {  # conditions = ending_key
        "self_defense": {
            "dialogue": "You walk up to the farmhouse, the door is still wide open with the farmer dead just passed the doorway",
            "choices": {
                "option_one": {
                    "Text": "Look at farmer",
                    "id": 1,
                    "follow_up_text": "The farmer has a large gash in his throat of where you....yknow",
                    "next_checkpoint": "after_test_house",
                    "checkpoint_scene": "farm"
                },
                "option_two": {
                    "Text": "Turn around and leave",
                    "id": 2,
                    "follow_up_text": "You turn and leave, its starting to stink...",
                    "next_checkpoint": "after_test_house_crossroads",
                    "checkpoint_scene": "farm"
                }
            }
        },
        "trust_pass": {
            "tag": "break_choice",
            "dialogue": "You walk back to the farmhouse. the farmer is sitting in his rocking chair, watching the trees.",
            "choices": {
                "option_one": {
                    "Text": "sit on the porch",
                    "id": 1,
                    "follow_up_text": "You sit on the porch steps for awhile enjoying the breeze, taking a break from everything.",
                    "next_checkpoint": "after_test_house",
                    "checkpoint_scene": "farm"
                },
                "option_two": {
                    "Text": "Turn around and leave",
                    "id": 2,
                    "follow_up_text": "You turn and leave, its starting to stink...",
                    "next_checkpoint": "after_test_house_crossroads",
                    "checkpoint_scene": "farm"
                }
            }
        },
        "farmer_death": {
            "dialogue": "You walk towards the farmhouse, the house looks spotless, someone stopped by...it doesnt seem like the farmers body is here.",
            "choices": {
                "option_one": {
                    "Text": "Look around",
                    "id": 1,
                    "follow_up_text": "Youve checked the house, the farmers body isnt in here.",
                    "next_checkpoint": "after_test_house",
                    "checkpoint_scene": "farm"
                },
                "option_two": {
                    "Text": "Turn around and leave",
                    "id": 2,
                    "follow_up_text": "You turn and leave, its starting to stink...",
                    "next_checkpoint": "after_test_house_crossroads",
                    "checkpoint_scene": "farm"
                }
            }
        }
    },
    "after_test_barn": {  # conditions = ending_key
        "self_defense": {
            "dialogue": "You walk to the barn, its quiet in here...",
            "choices": {
                "option_one": {
                    "Text": "See what you can find",
                    "id": 1,
                    "follow_up_text": "Not like that psycho is gonna need anything in here...",
                    "next_checkpoint": "after_test_key_items",
                    "checkpoint_scene": "farm",
                    "locked": {
                        "locked_text": "You already looked, no use looking again...",
                        "locked_checkpoint": "after_test_barn",
                        "locked_scene": "farm",
                        "explore_flag": {
                            "snooped_barn": False
                        }
                    }
                },
                "option_two": {
                    "Text": "Turn around and leave",
                    "id": 2,
                    "follow_up_text": "You turn and leave, its too quiet",
                    "next_checkpoint": "after_test_barn_crossroads",
                    "checkpoint_scene": "farm"
                }
            }
        },
        "trust_pass": {
            "dialogue": "The farmer watches you from the porch, and waves. He trusts you...",
            "choices": {
                "option_one": {
                    "Text": "Look around",
                    "id": 1,
                    "follow_up_text": "You head into the barn...",
                    "next_checkpoint": "after_test_key_items",
                    "checkpoint_scene": "farm",
                    "locked": {
                        "locked_text": "You already looked, no use looking again...",
                        "locked_checkpoint": "after_test_barn",
                        "locked_scene": "farm",
                        "explore_flag": {
                            "snooped_barn": False
                        }
                    }
                },
                "option_two": {
                    "Text": "Turn around and leave",
                    "id": 2,
                    "follow_up_text": "You turn and leave...",
                    "next_checkpoint": "after_test_barn_crossroads",
                    "checkpoint_scene": "farm"
                }
            }
        },
        "farmer_death": {
            "dialogue": "You walk towards the barn, its quiet...it doesnt seem like the farmers body is here.",
            "choices": {
                "option_one": {
                    "Text": "Look around",
                    "id": 1,
                    "follow_up_text": "You check every part of the barn, the farmers body isnt in here",
                    "next_checkpoint": "after_test_barn",
                    "checkpoint_scene": "farm"
                },
                "option_two": {
                    "Text": "Turn around and leave",
                    "id": 2,
                    "follow_up_text": "You turn and leave, its too quiet in here",
                    "next_checkpoint": "after_test_barn_crossroads",
                    "checkpoint_scene": "farm"
                }
            }
        }
    },
    "after_test_key_items": {
        "dialogue": "While exploring the barn you stumble upon an old hammer and a mask",
        "choices": {
            "option_one": {
                "Text": "leave the items",
                "id": 1,
                "follow_up_text": "you leave the items, theyre not yours to take.",
                "next_checkpoint": "after_test_barn_crossroads",
                "checkpoint_scene": "farm"
            },
            "option_two": {
                "Text": "take the items",
                "id": 2,
                "follow_up_text": "you take the items, the farmer wont mind...",
                "next_checkpoint": "after_test_barn_crossroads",
                "checkpoint_scene": "farm",
                "has_been": "snooped_barn",
                "locked": {
                    "locked_text": "You have already picked up these items",
                    "locked_checkpoint": "after_test_key_items",
                    "locked_scene": "farm",
                    "inventory_need": {
                        "mask": False,
                        "hammer": False
                    }
                },
            }
        }
    },
    "after_test_house_crossroads": {
        "dialogue": "Where do you want to go?",
        "choices": {
            "option_one": {
                "Text": "Go to the crossroads",
                "id": 1,
                "follow_up_text": "You turn around and walk back up the hill to the crossroads...",
                "next_checkpoint": "after_test_crossroads",
                "checkpoint_scene": "farm"
            },
            "option_two": {
                "Text": "Go to barn",
                "id": 2,
                "follow_up_text": "You turn and walk towards the barn...",
                "next_checkpoint": "after_test_barn",
                "checkpoint_scene": "farm"
            }
        }
    },
    "after_test_barn_crossroads": {
        "dialogue": "Where do you want to go?",
        "choices": {
            "option_one": {
                "Text": "Go to the crossroads",
                "id": 1,
                "follow_up_text": "You turn around and walk back up the hill to the crossroads...",
                "next_checkpoint": "after_test_crossroads",
                "checkpoint_scene": "farm"
            },
            "option_two": {
                "Text": "Go to Farmhouse",
                "id": 2,
                "follow_up_text": "You turn and walk towards the house...",
                "next_checkpoint": "after_test_house",
                "checkpoint_scene": "farm"
            }
        }
    },
    "after_test_crossroads": {  # crossroads to leave the scene
        "dialogue": "Where do you want to go?",
        "choices": {
            "option_one": {
                "Text": "Go right [Swamp]",
                "id": 1,
                "follow_up_text": "you start walking right...",
                "next_checkpoint": "intro",
                "checkpoint_scene": "swamp"
            },
            "option_two": {
                "Text": "Go forward [Village Center]",
                "id": 2,
                "follow_up_text": "you start walking forward...",
                "next_checkpoint": "intro",
                "checkpoint_scene": "center"
            }
        }
    },
    # endregion
    # region Farm Endings
    "butcher_ending": {
        "dialogue": "Before your able to make your way into the barn you feel a sharp pain in your back. "
                    "When you look down you see youve been stabbed",
        "ending_key": "butcher"
    },
    "kindness_ending": {
        "dialogue": "The farmer is amazed by your polite manners. He offers to drive you to the main road. You escape the village",
        "ending_key": "kindness"
    },
    "defense_ending": {
        "dialogue": "The farmer attacks you but you have a weapon. Its a tedious fight but you overcome him, you did what you had to do",
        "ending_key": "self_defense",
        "next_checkpoint": "after_test_house_crossroads",
        "checkpoint_scene": "farm"
    },
    "farmer_death_ending": {
        "dialogue": "You kill the farmer, his body lies at your feet.",
        "ending_key": "farmer_death",
        "next_checkpoint": "after_test_house_crossroads",
        "checkpoint_scene": "farm"
    },
    "tainted_ending": {
        "dialogue": "The farmer lunges at you and attacks you. He kills you. You shoudve been more trusting of his hospitality",
        "ending_key": "tainted_meat"
    },
    "trust_ending": {
        "dialogue": "The farmer trusts you. he hands you a vial of red liquid and tells you the answers you seek are in the center",
        "ending_key": "trust_pass",
        "next_checkpoint": "after_test_house_crossroads",
        "checkpoint_scene": "farm",
        "inventory_need": {
            "red_vial": False,
        }

    }
    # endregion
}

# endregion
