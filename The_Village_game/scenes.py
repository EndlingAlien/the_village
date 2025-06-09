#file will contain all scene dicts for the game

#dynamic variable for player_state_dict = farmer_location (inside, outside, barn)


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



#dict key and values will change, below is foundation
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
                "Text": "Stab the farmer.",
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