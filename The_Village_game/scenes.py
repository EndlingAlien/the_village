#file will contain all scene dicts for the game

#dynamic variable for player_state_dict =
# farmer_location (inside, outside, barn)
# church_state (empty, priest, basement)
# fog_density (heavy, light, none)

# need a last location variable to know where your coming from in swamp or keep track of where player been
#tags for analysis later?
#NEW key in dict locked = hidden until condition met

#dict key and values will change, below is foundation

#dict template
"checkpoint": {
        "dialogue": "text",
        "choices": {
            "option_one": {
                "Text": "text",
                "id": 1,
                "follow_up_text": "text",
                "next_checkpoint": "text"
            },
            "option_two": {
                "Text": "text",
                "id": 2,
                "follow_up_text": "text",
                "next_checkpoint": "text"
            },
            "option_three": {
                "Text": "text",
                "id": 3,
                "follow_up_text": "text",
                "next_checkpoint": "text"
            }
        }
    },

#purely for secret endings
center_scene_dict = {
    "intro": {
            "dialogue": "You decide to go forward and come up on a small circle of houses, with an organic statue in the center. You cant see people, could it be abandoned?",
            "choices": {
                "option_one": {
                    "Text": "Walk to the center",
                    "id": 1,
                    "follow_up_text": "You decide to continue on...",
                    "next_checkpoint": "village_center"
                },
                "option_two": {
                    "Text": "Leave",
                    "id": 2,
                    "follow_up_text": "You decide to head back to the crossroads",
                    "next_checkpoint": "center_crossroads"
                }
            }
    },
    "center_crossroads": {  # crossroads to leave the scene *not finished*
        "dialogue": "Where do you want to go?",
        "choices": {
            "option_one": {
                "Text": "Go right [Farm]",
                "id": 1
            },
            "option_two": {
                "Text": "Go left [Church]",
                "id": 2
            },
            "option_three": {
                "Text": "Go forward [Swamp]",
                "id": 3
            }
        }
    },
    "village_center": {
        "dialogue": "The place looks empty. There are houses surrounding a small courtyard. There is a large statue in the middle of the courtyard, littered by strange letters on it.",
        "choices": {
            "option_one": {
                "Text": "Try the houses",
                "id": 1,
                "follow_up_text": "You knock on some doors and try opening them. The curtains are drawn. You swear you can hear something behind a couple doors but no one answers.",
            },
            "option_two": {
                "Text": "Go to the statue",
                "id": 2,
                "follow_up_text": "You walk towards the statue in the square...",
                "next_checkpoint": "center_statue"
            },
            "option_three": {
                "Text": "Turn and leave",
                "id": 3,
                "follow_up_text": "You turn around leaving the small village center behind",
                "next_checkpoint": "center_crossroads"
            }
        }
    },
    "center_statue": {
        "dialogue": "You walk towards the statue in the middle of the courtyard, there is a small fountain at its feet. "
                    "The statue looks to be made of organic material, plants, roots and vines. It has strange words engraved into it...",
        "choices": {
            "option_one": {
                "Text": "touch statue",
                "id": 1,
                "follow_up_text": "You touch the statue. Its made of intertwined sticks and mud. Its covered in plants and flowers and moss.",
            },
            "option_two": {
                "Text": "use decoder",
                "id": 2,
                "follow_up_text": "You use the decoder to read the strange words. the first engraving across the base of the statue reads,"
                                  " 'Quench the hands, heal the spring—One binds flesh to fury, the other frees the soul'"
                                  "The second engraving running along the base of the fountain reads, 'Blood of the forest, tears of the sky, veins of the earth'",
                "locked_text": "If only you could read these...",
            },
            "option_three": {
                "Text": "leave",
                "id": 3,
                "follow_up_text": "You turn and leave, walking back to the crossroads...",
                "next_checkpoint": "center_crossroads"
            },
            "option_four": {
                "Text": "use the vials",
                "id": 4,
                "follow_up_text": "You walk up closer to the statue and fountain, pulling the 3 vials of liquid out of your pocket...",
                "next_checkpoint": "statue_vials"
            }
        }
    },
    "statue_vials": {
        "dialogue": "You approach the statue holding the vials...",
        "choices": {
            "option_one": {
                "Text": "Pour into statues hands...",
                "id": 1,
                "follow_up_text": "You pour the vials into the statues hands one at a time...",
                "next_checkpoint": "vessel_ending"
            },
            "option_two": {
                "Text": "Pour into the fountain...",
                "id": 2,
                "follow_up_text": "You pour the vials into the fountain one at a time...",
                "next_checkpoint": "cleansed_ending"
            }
        }
    },
    "cleansed_ending": {
    "dialogue": "The water drains from the fountain slowly, then cracks open, revealing a spiraling staircase. You descend "
                "and are placed in a sewer, a sign reads city with an arrow. You follow it. Youve escaped the village",
    "ending_key": "cleansed_secret"
    },
    "vessel_ending": {
    "dialogue": "You pour the vials into the statues hands, each one instantly soaking in. Suddenly the statue combusts, "
                "a faint sickly odor surrounds you, you cluth your throat as it burns and suffocates your lungs. "
                "Your bones break and reform as your muscles expand. Youve become their beast. You are the village.",
    "ending_key": "the_vessel_secret"
    }

}

#fog density is conditional
swamp_scene_dict = {
    "intro": {
        "dialogue": { #or later on, change follow-up text to feel dynamic
            "from_church": "You decide to take a left and come up on a open swampy area",
            "from_farm": "You decide to take a right and come up on a open swampy area"
        },
        "choices": {
            "option_one": {
                "Text": "walk into the swamp area",
                "id": 1,
                "follow_up_text": "Its just a swamp...",
                "next_checkpoint": "start_position"
            },
            "option_two": {
                "Text": "turn around",
                "id": 2,
                "follow_up_text": "Dont like the look of this place, better go...",
                "next_checkpoint": "swamp_crossroads"
            }
        }
    },
    "swamp_crossroads": {  # crossroads to leave the scene *not finished*
        "dialogue": "Where do you want to go?",
        "choices": {
            "option_one": {
                "Text": "Go right [Church]",
                "id": 1
            },
            "option_two": {
                "Text": "Go left [Farm]",
                "id": 2
            },
            "option_three": {
                "Text": "Go forward [Village Center]",
                "id": 3
            }
        }
    },
    "start_position": {
        "dialogue": {
            "heavy_fog": {
                "dialogue": "As you get closer to the swamp, the fog begins to get heavy, its hard to see anything",
                "choices": {
                    "option_one": {
                        "Text": "Walk aimlessly",
                        "id": 1,
                        "follow_up_text": "Despite the alarming silence around this church you decide to walk in the door",
                        "next_checkpoint": "inside_swamp"
                    },
                    "option_two": {
                        "Text": "Turn and Leave",
                        "id": 2,
                        "follow_up_text": "Not worth getting lost in here...",
                        "next_checkpoint": "swamp_crossroads"
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
                        "next_checkpoint": "inside_swamp"
                    },
                    "option_two": {
                        "Text": "Turn and Leave",
                        "id": 2,
                        "follow_up_text": "Its not the fog that worries you, its what could be in the fog...",
                        "next_checkpoint": "swamp_crossroads"
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
                        "next_checkpoint": "inside_swamp"
                    },
                    "option_two": {
                        "Text": "Turn and Leave",
                        "id": 2,
                        "follow_up_text": "Something about the energy here isn't right, you walk away...",
                        "next_checkpoint": "swamp_crossroads"
                    }
                }
            }
        }
    },
    "inside_swamp": {
        "dialogue": {
            "heavy_fog": {
                "dialogue": "You walk forward with your hands stretched out, you hear rustling in the distance, you can only see 1 foot in front of you. "
                            "Suddenly you make contact with a stone structure, you can see some kind of cube on its pedestal.",
                "choices": {
                    "option_one": {
                        "Text": "approach the cube",
                        "id": 1,
                        "follow_up_text": "The cube is small and metallic, it flashes with a bright light...",
                        "next_checkpoint": "intuition_test"
                    },
                    "option_two": {
                        "Text": "Turn and Leave",
                        "id": 2,
                        "follow_up_text": "This is too weird, time to go...",
                        "next_checkpoint": "swamp_crossroads"
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
                        "next_checkpoint": "intuition_test"
                    },
                    "option_two": {
                        "Text": "Look around",
                        "id": 2,
                        "follow_up_text": "Maybe you should check the surrounding area before...",
                        "next_checkpoint": "swamp_key_items"
                    },
                    "option_three": {
                        "Text": "Turn and Leave",
                        "id": 3,
                        "follow_up_text": "Its not the fog that worries you, its what could be in the fog...",
                        "next_checkpoint": "swamp_crossroads"
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
                        "next_checkpoint": "intuition_test"
                    },
                    "option_two": {
                        "Text": "look around",
                        "id": 2,
                        "follow_up_text": "There could be more here to discover...",
                        "next_checkpoint": "swamp_key_items"
                    },
                    "option_three": {
                        "Text": "Turn and Leave",
                        "id": 3,
                        "follow_up_text": "Something about the energy here isn't right, you walk away...",
                        "next_checkpoint": "swamp_crossroads"
                    }
                }
            }
        }
    },
    "swamp_key_items": {
        "dialogue": {
            "light_fog": {
                "dialogue": "You look around the surrounding area and spot a hammer",
                "choices": {
                    "option_one": {
                        "Text": "take the hammer",
                        "id": 1,
                        "follow_up_text": "Could be useful...",
                        "next_checkpoint": "approach_cube"
                    },
                    "option_two": {
                        "Text": "Leave the hammer",
                        "id": 2,
                        "follow_up_text": "its just a hammer",
                        "next_checkpoint": "approach_cube"
                    }
                }
            },
            "no_fog": {
                "dialogue": "You look around the surrounding area. You find a hammer and a rusty key. You also find strange "
                            "letters on the side of the structure, if only you could decipher them. ",
                "choices": {
                    "option_one": {
                        "Text": "take the hammer and key",
                        "id": 1,
                        "follow_up_text": "This could be interesting....",
                        "next_checkpoint": "approach_cube"
                    },
                    "option_two": {
                        "Text": "Take the items and use decoder",
                        "id": 2,
                        "condition": "has_decoder",
                        "locked_text": "How could you decode these...",
                        "follow_up_text": "you pocket the hammer and key, then use your decoder to read the strange words. (placeholder)",
                        "next_checkpoint": "approach_cube"
                    },
                    "option_three": {
                        "Text": "Leave the hammer and key",
                        "id": 3,
                        "follow_up_text": "Its a hammer and a rusty key, what could you possibly need these for...",
                        "next_checkpoint": "approach_cube"
                    }
                }
            }
        }
    },
    "approach_cube": {
        "dialogue": "After collecting your items you see the cube flash with a bright light...",
        "choices": {
            "option_one": {
                "Text": "approach",
                "id": 1,
                "follow_up_text": "Its just a funny looking cube...",
                "next_checkpoint": "intuition_test"
            },
            "option_two": {
                "Text": "back away",
                "id": 1,
                "follow_up_text": "The cube pulses with the light, it draws you close",
                "next_checkpoint": "intuition_test"
            }
        }
    },
    "intuition_test": {
        "question_1": {
            "dialogue": "The cube hums...",
            "choices": {
                "option_one": {
                    "Text": "hum with it",
                    "id": 1,
                    "next_checkpoint": "question_2"
                },
                "option_two": {
                    "Text": "touch it",
                    "id": 2,
                    "next_checkpoint": "question_2"
                },
                "option_three": {
                    "Text": "pick it up",
                    "id": 3,
                    "next_checkpoint": "question_2"
                }
            }
        },
        "question_2": {
            "dialogue": "A low frequency starts vibrating in your skull. You feel words that aren’t yours:"
                            "'What are you made of?'",
            "choices": {
                "option_one": {
                    "Text": "speak back",
                    "id": 1,
                    "next_checkpoint": "question_3"
                },
                "option_two": {
                    "Text": "stay silent",
                    "id": 2,
                    "next_checkpoint": "question_3"
                },
                "option_three": {
                    "Text": "tell it to get out",
                    "id": 3,
                    "next_checkpoint": "question_3"
                }
            }
        },
        "question_3": {# *not finished*
            "dialogue": "A beam shines down on you...",
            "choices": {
                "option_one": {
                    "Text": "stare up to it",
                    "id": 1,
                    "next_checkpoint": "text"
                },
                "option_two": {
                    "Text": "stay still",
                    "id": 2,
                    "next_checkpoint": "text"
                },
                "option_three": {
                    "Text": "run away",
                    "id": 3,
                    "next_checkpoint": "text"
                }
            }
        }
    },
    "make_choice": { #choose for ending after test if you got the curious result
        "dialogue": "The Aliens are captivated by your curiosity they wish for you to stay so they may study you",
        "choices": {
            "option_one": {
                "Text": "Stay on the ship",
                "id": 1,
                "next_checkpoint": "belong_ending"
            },
            "option_two": {
                "Text": "Ask to leave",
                "id": 2,
                "next_checkpoint": "intuition_ending"
            }
        }
    },
    #endings
    "rejected_ending": {
    "dialogue": "Your pathetic, the aliens probe you, dissect you, then discard you.",
    "ending_key": "rejected_specimen"
    },
    "probed_ending": {
    "dialogue": "Your average, the aliens probe you, wipe your memory and send you back to the forest",
    "ending_key": "probed_and_confused"
    },
    "belong_ending": {
    "dialogue": "The Aliens cheer as they usher you into the bridge. Their captain standing tall, with an outreached hand...",
    "ending_key": "you_belong_with_us"
    },
    "intuition_ending": {
    "dialogue": "The Aliens are sad to see you go but wish you all the best",
    "ending_key": "intuition_test_passed"
    },

}

#state of the church is conditional
church_scene_dict = {
    "intro": {  # entered the scene
        "dialogue": "You decide to take a left and see a church among the trees, do you approach or turn around?",
        "choices": {
            "option_one": {
                "Text": "Go to the Church",
                "id": 1,
                "follow_up_text": "You decide to walk towards the church...",
                "next_checkpoint": "start_position"
            },
            "option_two": {
                "Text": "Turn Around",
                "id": 2,
                "follow_up_text": "You decide to turn around walking back to where you came from. Theres a crossroads...",
                "next_checkpoint": "church_crossroads"
            }
        }
    },
    "church_crossroads": {#crossroads to leave the scene *not finished*
        "dialogue": "Where do you want to go?",
        "choices": {
            "option_one": {
                "Text": "Go right [Forest]",
                "id": 1
            },
            "option_two": {
                "Text": "Go left [Swamp]",
                "id": 2
            },
            "option_three": {
                "Text": "Go forward [Village Center]",
                "id": 3
            }
        }
    },
    "start_position": {
        "dialogue": {
            "church_is_empty": {
                "dialogue": "As you get closer to the church, you cant see any lights or hear any voices, it might be abandoned...",
                "choices": {
                    "option_one": {
                        "Text": "Go in",
                        "id": 1,
                        "follow_up_text": "Despite the alarming silence around this church you decide to walk in the door",
                        "next_checkpoint": "inside_church"
                    },
                    "option_two": {
                        "Text": "Turn and Leave",
                        "id": 2,
                        "follow_up_text": "This church looks too creepy, best to walk away....",
                        "next_checkpoint": "church_crossroads"
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
                        "next_checkpoint": "inside_church"
                    },
                    "option_two": {
                        "Text": "Turn and Leave",
                        "id": 2,
                        "follow_up_text": "Perhaps small lights and faint singing does not equate to safety, you walk away...",
                        "next_checkpoint": "church_crossroads"
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
                        "next_checkpoint": "inside_church"
                    },
                    "option_two": {
                        "Text": "Turn and Leave",
                        "id": 2,
                        "follow_up_text": "Something about the energy here isn't right, you walk away...",
                        "next_checkpoint": "church_crossroads"
                    }
                }
            }
        }
    },
    "inside_church": {
        "dialogue": {
            "church_is_empty": {
                "dialogue": "The church is surprisingly clean for looking so worn down on the outside. Doesnt look like anyone is here.",
                "choices": {
                    "option_one": {
                        "Text": "Explore",
                        "id": 1,
                        "follow_up_text": "No harm in exploring a church, might find something useful",
                        "next_checkpoint": "church_key_items"
                    },
                    "option_two": {
                        "Text": "Leave",
                        "id": 2,
                        "follow_up_text": "Its a creepy empty church in the forest, you should not be in here.",
                        "next_checkpoint": "church_crossroads"
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
                        "next_checkpoint": "faith_test"
                    },
                    "option_two": {
                        "Text": "Sit in the back pew",
                        "id": 2,
                        "follow_up_text": "he could be praying, maybe wait and let him finish...Once the priest finishes his song he turns and sees you sitting, he approaches...",
                        "next_checkpoint": "faith_test"
                    },
                    "option_three": {
                        "Text": "kill the priest",
                        "id": 3,
                        "condition": "has_weapon",
                        "locked_text": "You reach for a weapon you don’t have.",
                        "follow_up_text": "You quietly sneak up on the priest, and kill him",
                        "next_checkpoint": "priest_death_ending"
                    },
                }
            },
            "basement_open": {
                "dialogue": "You enter the church cautiously, you were right, its abandoned, except for...that small light...emitting from the cellar door...",
                "choices": {
                    "option_one": {
                        "Text": "Yell hello down the stairs",
                        "id": 1,
                        "follow_up_text": "No harm in calling out...right?. A couple of voices can be heard before a man ascends up the stairs, he looks like a priest.",
                        "next_checkpoint": "faith_test"
                    },
                    "option_two": {
                        "Text": "sit in the back pew and wait",
                        "id": 2,
                        "follow_up_text": "Someone is bound to come upstairs eventually...10 minutes later you hear someone ascend up the stairs, he looks like a priest. He walks towards you. ",
                        "next_checkpoint": "faith_test"
                    },
                    "option_three": {
                        "Text": "go downstairs",
                        "id": 2,
                        "follow_up_text": "its just a light....",
                        "next_checkpoint": "church_basement"
                    }
                }
            }
        }
    },
    "church_basement": {
        "dialogue": "As you descend the stairs you begin to smell a sickly burning odor. As you reach the bottom stair and "
                    "turn into the small room you see 2 people wearing robes and masks. They are holding a man on a stone table in place as another burns something into his skin",
        "choices": {
            "option_one": {
                "Text": "yell for them to stop",
                "id": 1,
                "follow_up_text": "This is cruel, you scream at them, they realize your not one of them...better run",
                "next_checkpoint": "altar_ending"
            },
            "option_two": {
                "Text": "sneak back up the stairs",
                "id": 2,
                "follow_up_text": "your not supposed to see this, you quickly and silently go back up the stairs",
                "next_checkpoint": "inside_church"
            },
            "option_three": {
                "Text": "stand there in shock",
                "id": 3,
                "follow_up_text": "What did you just stumble upon?",
                "next_checkpoint": "basement_ritual"
            },
            "option_four": { #lore item
                "Text": "wear the farmhouse mask",
                "id": 3,
                "condition": "has_mask",
                "locked_text": "if only you could blend in...",
                "follow_up_text": "You place the mask on that you got from the farmhouse. The cloaked figures turn to face "
                                  "you, acknowledge you, then direct their attention back to the man on the table ",
                "additional_dialogue": "The cloaked figures continue their barbaric branding, you inch closer to see what it is theyre branding on his skin. "
                                       "When you get close enough you see strange symbols, you can make out one though, a cube.",
                "next_checkpoint": "basement_ritual"
            }
        }
    },
    "basement_ritual": {
        "dialogue": "The cloaked figures stop what they're doing and look at each-other, whispering in a strange dialect before slowly turning towards you.",
        "choices": {
            "option_one": {
                "Text": "apologize",
                "id": 1,
                "follow_up_text": "One of the figures approaches. they remove their mask and robe and lead you back up the stairs",
                "next_checkpoint": "faith_test"
            },
            "option_two": {
                "Text": "'i dont want any trouble'",
                "id": 2,
                "follow_up_text": "One of the figures approaches. they remove their mask and robe and lead you back up the stairs",
                "next_checkpoint": "faith_test"
            },
            "option_three": {
                "Text": "run",
                "id": 3,
                "follow_up_text": "You dont plan on sticking around",
                "next_checkpoint": "altar_ending"
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
                "next_checkpoint": "church_crossroads"
            },
            "option_two": {
                "Text": "leave the items",
                "id": 2,
                "follow_up_text": "whatever god is worshipped in here might not like us stealing, you leave the items",
                "next_checkpoint": "church_crossroads"
            }
        }
    },
    "faith_test": {
        "question_1": {
            "dialogue": "The priest greets you with a warm smile. 'What is your name child?'",
            "choices": {
                "option_one": {
                    "Text": "tell the priest your name",
                    "id": 1,
                    "follow_up_text": "A name carved of stardust, how uniquely you. ",
                    "next_checkpoint": "question_2"
                },
                "option_two": {
                    "Text": "ask for the priests name",
                    "id": 2,
                    "follow_up_text": "The priest smirks. 'My name is (placeholder), you have nothing to fear young star beam.",
                    "next_checkpoint": "question_2"
                },
                "option_three": {
                    "Text": "refuse to tell him your name",
                    "id": 3,
                    "follow_up_text": "The priest nods. Your mind is closed off, from fear?",
                    "next_checkpoint": "question_2"
                }
            }
        },
        "question_2": {
            "dialogue": "The priest walks to the pew in the first row and sits down. 'Will you join me?'",
            "choices": {
                "option_one": {
                    "Text": "'Id be honored'",
                    "id": 1,
                    "follow_up_text": "You join the priest and sit down next to him",
                    "next_checkpoint": "question_3"
                },
                "option_two": {
                    "Text": "'Sure, thanks'",
                    "id": 2,
                    "follow_up_text": "You join the priest and sit down, making sure theres ample space between you",
                    "next_checkpoint": "question_3"
                },
                "option_three": {
                    "Text": "'I'll stand'",
                    "id": 3,
                    "follow_up_text": "You walk to the front row but stand next to him instead of sitting.",
                    "next_checkpoint": "question_3"
                }
            }
        },
        "question_3": {
            "dialogue": "The priest glances down at your bare muddy feet. 'Youve walked far. Seeking something?'",
            "choices": {
                "option_one": {
                    "Text": "Enlightment",
                    "id": 1,
                    "follow_up_text": "The priest smiles warmly",
                    "next_checkpoint": "question_4"
                },
                "option_two": {
                    "Text": "Answers",
                    "id": 2,
                    "follow_up_text": "the priest nods slow",
                    "next_checkpoint": "question_4"
                },
                "option_three": {
                    "Text": "A way out",
                    "id": 3,
                    "follow_up_text": "The priest clutches his bible tighter",
                    "next_checkpoint": "question_4"
                }
            }
        },
        "question_4": {
            "dialogue": "Do you believe in signs from above",
            "choices": {
                "option_one": {
                    "Text": "of course",
                    "id": 1,
                    "follow_up_text": "The priest gazes at the murals before him",
                    "next_checkpoint": "question_5"
                },
                "option_two": {
                    "Text": "sometimes, depends.",
                    "id": 2,
                    "follow_up_text": "Ah yes, the conditional believer...",
                    "next_checkpoint": "question_5"
                },
                "option_three": {
                    "Text": "Absolutely not",
                    "id": 3,
                    "follow_up_text": "The priest smiles, 'your will is strong'",
                    "next_checkpoint": "question_5"
                }
            }
        },
        "question_5": {
            "dialogue": "he notices your gaze on his book. its covered in pale yellow leather, 'You may read?', he holds out the book for you to take.",
            "choices": {
                "option_one": {
                    "Text": "read it carefully",
                    "id": 1,
                    "follow_up_text": "You see drawings of tall bipedal creatures, a cube, a statue, and 3 vials",
                    "next_checkpoint": "question_6"
                },
                "option_two": {
                    "Text": "glance through it",
                    "id": 2,
                    "follow_up_text": "You see glimpses of tall people, strange symbols, and a vial of liquid",
                    "next_checkpoint": "question_6"
                },
                "option_three": {
                    "Text": "refuse to touch it",
                    "id": 3,
                    "follow_up_text": "The priests eye subtly twitches but he shrugs it off and smiles, 'thats alright'",
                    "next_checkpoint": "question_6"
                }
            }
        },
        "question_6": {# *not finished*
            "dialogue": "The priest stands up, gazing out the window, 'Will you stay for the ritual tomorrow?'",
            "choices": {
                "option_one": {
                    "Text": "yes",
                    "id": 1,
                    "follow_up_text": "the priest turns to face you, smiling",
                    "next_checkpoint": "text"
                },
                "option_two": {
                    "Text": "havent decided yet",
                    "id": 2,
                    "follow_up_text": "the priest speaks to himself, 'The beams will shine brightly, such a sight to see the chosen break free'",
                    "next_checkpoint": "text"
                },
                "option_three": {
                    "Text": "no",
                    "id": 3,
                    "follow_up_text": "the priest begins to softly hum a hymnn",
                    "next_checkpoint": "text"
                }
            }
        },
    },
    #endings
    "believer_ending": {
    "dialogue": "the priest sees light within your eyes, youve been asked to join the village",
    "ending_key": "true_believer"
    },
    "faith_ending": {
    "dialogue": "The priest respects your autonomy as you do his. Your free to explore the church respectfully. Priest tells you to seek answers in the center.",
    "ending_key": "faith_test_passed",
    "next_checkpoint": "church_key_items"#or items added to inventory
    },
    "heretics_ending": {
    "dialogue": "The priest is insulted by your disrespect. He opens the door to the basement ringing a bell. Your put in a cage to be sacrificed in the ritual.",
    "ending_key": "heretics_fate"
    },
    "priest_death_ending": {
        "dialogue": "The priest falls to your feet, a pool of blood forming. A follower enters the church and yells for help. "
                    "Before you know it there are five figures dressed in robes wearing masks surrounding you. they beat you to death.",
        "ending_key": "thou_shalt_not"
    },
    "altar_ending": {
    "dialogue": "All 3 cloaked figures chase after you. they capture you and put you in a cage in the basement. One figure "
                    "takes off their mask and robe before approaching you, he looks like a priest. 'Blessed are the chosen. Youve been chosen for the ritual tomorrow",
    "ending_key": "altar_bound"
    }
}

#farmer location is conditional
farm_scene_dict = {
    "intro": {#entered the scene
        "dialogue": "You decide to take a right and see a farm at the bottom of a hill in the distance, do you approach or turn around?",
        "choices": {
            "option_one": {
                "Text": "Go to the Farm",
                "id": 1,
                "follow_up_text": "You decide to walk towards the farm...",
                "next_checkpoint": "start_position"
            },
            "option_two": {
                "Text": "Turn Around",
                "id": 2,
                "follow_up_text": "You decide to turn around walking back to where you came from. Theres a crossroads...",
                "next_checkpoint": "farm_crossroads"
            }
        }
    },
    #crossroads
    "farm_crossroads": {#crossroads to leave the scene *not finished*
        "dialogue": "Where do you want to go?",
        "choices": {
            "option_one": {
                "Text": "Go right [Swamp]",
                "id": 1
            },
            "option_two": {
                "Text": "Go left [Forest]",
                "id": 2
            },
            "option_three": {
                "Text": "Go forward [Village Center]",
                "id": 3
            }
        }
    },
    "house_crossroads": {#crossroads when leaving the house
        "dialogue": "Where do you want to go?",
        "choices": {
            "option_one": {
                "Text": "Go to the crossroads",
                "id": 1,
                "follow_up_text": "You turn around and walk back up the hill to the crossroads...",
                "next_checkpoint": "farm_crossroads"
            },
            "option_two": {
                "Text": "Go to barn",
                "id": 2,
                "follow_up_text": "You turn and walk towards the barn...",
                "next_checkpoint": "choose_barn"
            }
        }
    },
    "barn_crossroads": {#crossroads when leaving the barn
        "dialogue": "Where do you want to go?",
        "choices": {
            "option_one": {
                "Text": "Go to the crossroads",
                "id": 1,
                "follow_up_text": "You turn around and walk back up the hill to the crossroads...",
                "next_checkpoint": "farm_crossroads"
            },
            "option_two": {
                "Text": "Go to the farmhouse",
                "id": 2,
                "follow_up_text": "You turn and walk towards the house...",
                "next_checkpoint": "choose_farmhouse"
            }
        }
    },

    "start_position": {#go to farm or barn
        "farmer_in_house": {#random event condition
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
            "next_checkpoint": "choose_farmhouse"
            },
            "option_two": {
                "Text": "Walk to the Barn",
                "id": 2,
                "follow_up_text": "You start making your way to the barn...",
                "next_checkpoint": "choose_barn"
            }
        }
    },
    "choose_farmhouse": {#you go to the farmhouse
        "farmer_in_house": {
            "dialogue": "You walk up to the farmhouse door, you can hear someone on the other side of the door",
            "choices": {
                "option_one": {
                    "Text": "Knock on the door",
                    "id": 1,
                    "follow_up_text": " After a couple minutes a man opens the door greeting you",
                    "next_checkpoint": "meet_farmer"
                },
                "option_two": {
                    "Text": "Bang on the door",
                    "id": 2,
                    "follow_up_text": "After a couple minutes a man swings the door open, visibly annoyed",
                    "next_checkpoint": "meet_farmer"
                },
                "option_three": {
                    "Text": "Turn around and leave",
                    "id": 3,
                    "follow_up_text": "You turn and leave, maybe best not to bother whoever that is...",
                    "next_checkpoint": "house_crossroads"
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
                    "next_checkpoint": "meet_farmer"
                },
                "option_two": {
                    "Text": "walk up to him without saying a word",
                    "id": 2,
                    "follow_up_text": "You silently walk towards the farmer, he stands up and crosses his arms looking down at you from the porch.",
                    "next_checkpoint": "meet_farmer"
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
                    "next_checkpoint": "snoop_house"
                },
                "option_two": {
                    "Text": "Turn around",
                    "id": 2,
                    "follow_up_text": "You knock but theres no answer. No use in snooping, you turn and walk away.",
                    "next_checkpoint": "house_crossroads"
                },
            }
        }
    },
    "choose_barn": {#you go to the barn *not finished*
        "farmer_in_house": {#random event condition
            "dialogue": "You walk up to the barn door. its quiet, doesnt sound like anyone is in there",
            "choices": {
                "option_one": {
                    "Text": "go in",
                    "id": 1,
                    "follow_up_text": "You call out, but theres no answer. You walk in slowly...",
                    "next_checkpoint": "snoop_barn"
                },
                "option_two": {
                    "Text": "turn around and leave",
                    "id": 2,
                    "follow_up_text": "No one is here, no use in snooping.",
                    "next_checkpoint": "barn_crossroads"
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
                    "next_checkpoint": "meet_farmer"
                },
                "option_two": {
                    "Text": "ignore him and keep walking to the barn",
                    "id": 2,
                    "follow_up_text": "You keep walking to the barn, you see in the corner of your eye, the farmer getting up and making his way to you.",
                    "next_checkpoint": "butcher_ending" #death
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
                    "next_checkpoint": "meet_farmer"
                },
                "option_two": {
                    "Text": "knock on the barn door",
                    "id": 2,
                    "follow_up_text": "The farmer looks up at you slightly confused, waiting...",
                    "next_checkpoint": "meet_farmer"
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
                "next_checkpoint": "house_crossroads"
            },
            "option_two": {
                "Text": "explore",
                "id": 2,
                "follow_up_text": "You walk around the house, looking at everything",
                "condition" : "has_snooped_house", # needs to be false to snoop (avoid dupe items)
                "next_checkpoint": "house_key_items"
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
                "next_checkpoint": "barn_crossroads"
            },
            "option_two": {
                "Text": "explore",
                "id": 2,
                "follow_up_text": "You walk around the barn, looking at everything",
                "condition" : "has_snooped_barn", # needs to be false to snoop (avoid dupe items)
                "next_checkpoint": "barn_key_items"
            }
        }
    },
    "barn_key_items": {
        "dialogue": "While exploring the barn you stumble upon an old screwdriver and a mask",
        "choices": {
            "option_one": {
                "Text": "leave the items",
                "id": 1,
                "follow_up_text": "you leave the items, theyre not yours to take.",
                "next_checkpoint": "barn_crossroads"
            },
            "option_two": {
                "Text": "take the items",
                "id": 2,
                "follow_up_text": "you take the items, finders keepers.",
                "next_checkpoint": "barn_crossroads"
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
                "next_checkpoint": "house_crossroads"
            },
            "option_two": {
                "Text": "take the items",
                "id": 2,
                "follow_up_text": "you take the items, finders keepers.",
                "next_checkpoint": "house_crossroads"
            }
        }
    },
    "meet_farmer": {#option to kill before test *not finished*
        "dialogue": None,
        "choices": {
            "option_kill": {
                "Text": "kill the farmer.",
                "id": 1,
                "condition": "has_weapon",
                "locked_text": "You reach for a weapon you don’t have.",
                "next_checkpoint": "text" #ending
            },
            "option_talk": {
                "Text": "Greet him politely.",
                "id": 2,
                "follow_up_text": "You say hello to the farmer.The farmer smiles...",
                "next_checkpoint": "trust_test"
            }
        }
    },
    "trust_test": {
        "question_1": {
            "dialogue": "Howdy there stranger whats your name",
            "choices": {
                "option_one": {#trust point
                    "Text": "tell the farmer your name",
                    "id": 1,
                    "follow_up_text": "Why thats a great name, my name is (placeholder), welcome to my farm",
                    "next_checkpoint": "question_2"
                },
                "option_two": {
                    "Text": "ignore him and ask for his name",
                    "id": 2,
                    "follow_up_text": "The farmer looks at you suspiciously. My name is (placeholder).",
                    "next_checkpoint": "question_2"
                },
            }
        },
        "question_2": {
            "dialogue": "You alright partner? the farmer looks down at your bare feet covered in mud",
            "choices": {
                "option_one": {#trust point
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
            "dialogue": "The farmer welcomes you into his home, gesturing to a nearby dining table for you to sit at. Like some ice tea, friend?",
            "choices": {
                "option_one": {#trust point
                    "Text": "accept the ice tea",
                    "id": 1,
                    "follow_up_text": "The farmer pours you both a glass of ice tea setting it in front of you. Its my gammies famous recipe, generational ice tea right there",
                    "next_checkpoint": "question_4"
                },
                "option_two": {
                    "Text": "decline the ice tea",
                    "id": 2,
                    "follow_up_text": "the farmer turns to stare you down before smiling and pouring himself a glass and sitting down with you.",
                    "next_checkpoint": "question_4"
                },
            }
        },
        "question_4": {
            "dialogue": "The farmer takes a sip, savoring the taste before smacking his lips. Yep, nothing beats good "
                        "old fashioned sweet tea. Yknow it was actually my grandpappi that started this farm here.",
            "choices": {
                "option_one": {#trust point
                    "Text": "ask him more about his family",
                    "id": 1,
                    "follow_up_text": "The farmer smiles wide. His name was (placeholder)He helped discover this here village, course back then it was just a meateor site",
                    "next_checkpoint": "question_5"
                },
                "option_two": {
                    "Text": "remind him about helping you",
                    "id": 2,
                    "follow_up_text": "The farmer takes another slow sip, staring you down. Y'know my grandpappi was a founder of this here town, respect outta be in order for you.",
                    "next_checkpoint": "question_5"
                },
            }
        },
        "question_5": {
            "dialogue": "My family helped keep this town fed. Back then we didn't have all the tools and knowledge we did, "
                        "but food preparation has always been what it once was. The farmer gives you a big gummy smile",
            "choices": {
                "option_one": {#trust point
                    "Text": "smile as well",
                    "id": 1,
                    "follow_up_text": "The farmer looks at you as if studying your physique. You look like you could use a meal",
                    "next_checkpoint": "question_6"
                },
                "option_two": {
                    "Text": "change the subject",
                    "id": 2,
                    "follow_up_text": "The farmer slowly drops his smile. You look hungry.",
                    "next_checkpoint": "question_6"
                },
            }
        },
        "question_6": {
            "dialogue": "The farmer stands up and walks into the kitchen. You hear sounds of dishes and cutlery. After awhile "
                        "the farmer comes back with 2 steaming bowls of stew. He sets the bowl in front of you. Cant help ya on an empty stomach, go ahead and dig in",
            "choices": {
                "option_one": {#trust point
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
            "dialogue": "You remind me of a boy I met once. Tasted just like this. Shame what happened to him. Real shame.",
            "choices": {
                "option_one": {#trust point
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
            "dialogue": "The farmer tries to fish something out of his stew. 'Damn i just love these things', he holds up "
                        "what looks to be a small human toe, tossing it in his mouth and chewing.",
            "choices": {
                "option_one": {#trust point
                    "Text": "finish the stew",
                    "id": 1,
                    "follow_up_text": "You both finish your stew in silence, the farmer humming a song that sound like a hymnn.",
                    "next_checkpoint": "question_9"
                },
                "option_two": {
                    "Text": "spit it out",
                    "id": 2,
                    "follow_up_text": "You spit out the stew, pushing th bowl away in disgust. The farmer stares you down darkly, "
                                      "taking your stew and pouring it into his bowl. his voice low, 'Thou shall waste not'",
                    "next_checkpoint": "question_9"
                },
            }
        },
        "question_9": {
            "dialogue": "After the farmer finishes his stew he stands up and circles you, then suddenly holds a knife up to "
                        "your throat. 'Blessed are the divine meat' he inhales your scent deeply",
            "choices": {
                "option_one": {#trust point
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
                    "next_checkpoint": "text" #need checkpoint for when scene is over to calculate points and pick ending
                },
            }
        },
    },

    #endings
    "butcher_ending": {
        "dialogue": "Before your able to make your way into the barn you feel a sharp pain in your back. "
                    "When you look down you see youve been stabbed",
        "ending_key": "butcher_choice"
    },
    "kindness_ending": {
        "dialogue": "The farmer is amazed by your polite manners. He offers to drive you to the main road. You escape the village",
        "ending_key": "kindness_pays"
    },
    "defense_ending": {
        "dialogue": "The farmer attacks you but you have a weapon. Its a tedious fight but you overcome him, you did what you had to do",
        "ending_key": "self_defense"
    },
    "tainted_ending": {
        "dialogue": "The farmer lunges at you and attacks you. He kills you. You shoudve been more trusting of his hospitality",
        "ending_key": "tainted_meat"
    },
    "trust_ending": {
        "dialogue": "The farmer trusts you. he hands you a vial of red liquid and tells you the answers you seek are in the center",
        "ending_key": "trust_test_passed"
    }
}