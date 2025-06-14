# This file holds all the endings of the game

#type = survived, secret, good, test, failed, death

endings = {

    # Center Endings
    "cleansed": {
        "name": "The Cleansed",
        "scene": "center",
        "type": "secret",
        "summary": "escaped village using fountain",
        "description": "You bathed in ancient light, trusted the unknown, and walked free with stars in your footsteps."
    },
    "vessel": {
        "name": "The Vessel",
        "scene": "center",
        "type": "secret",
        "summary": "became village beast",
        "description": "You gave yourself completely. The village took root in your bones, and you became its monstrous guardian."
    },
    "forfeit": {
        "name": "Give in to the Village",
        "scene": "center",
        "type": "failed",
        "summary": "Gave up",
        "description": "The village was too much for you, your only option was to give in, so you did."
    },

    #region Swamp Endings
    "rejected": {
        "name": "The Rejected Specimen",
        "scene": "swamp",
        "type": "failed",
        "summary": "didnt pass intuition test",
        "description": "The cube found you lacking. Cast out, altered, a puzzle unsolved. The swamp forgets your name."
    },
    "probed": {
        "name": "Probed and Confused",
        "scene": "swamp",
        "type": "survived",
        "summary": "survived the intuition test",
        "description": "You endured the test. Something inside you changed, but the cube let you go… for now."
    },
    "you_belong": {
        "name": "You Belong With Us",
        "scene": "swamp",
        "type": "good",
        "summary": "passed test, choose to stay",
        "description": "The cube recognized you. You stayed, not out of fear, but because something called you home."
    },
    "intuition_pass": {
        "name": "Passed Intuition Test",
        "scene": "swamp",
        "type": "test",
        "summary": "passed test, choose to leave",
        "description": "The cube accepted you, but you walked away. Clarity is costly—but you kept your soul intact."
    },
    #endregion

    #region Church Endings
    "believer": {
        "name": "A True Believer",
        "scene": "church",
        "type": "good",
        "summary": "asked to join cult",
        "description": "You listened, believed, and were welcomed into the fold. Faith became your light—and your chains."
    },
    "faith_pass": {
        "name": "Passed Faith Test",
        "scene": "church",
        "type": "test",
        "summary": "passed the faith test",
        "description": "You were measured by the eyes of the divine. You held steady, and the stars blinked in approval."
    },
    "heretic": {
        "name": "A Heretic's Fate",
        "scene": "church",
        "type": "failed",
        "summary": "failed faith test",
        "description": "Your doubt echoed too loud. The walls listened. You were judged, and judgment was not kind."
    },
    "priest_death": {
        "name": "Thou Shalt Not Kill",
        "scene": "church",
        "type": "death",
        "summary": "killed priest",
        "description": "The blade met flesh in sacred halls. Blood soaked the scriptures. The beams do not forgive."
    },
    "altar": {
        "name": "Altar Bound",
        "scene": "church",
        "type": "survived",
        "summary": "tried to run from/stop the men in the church basement",
        "description": "You fled, you fought—but the hymn was louder. Bound and broken, you became part of the ritual."
    },
    #endregion

    #region Farm Endings
    "butcher": {
        "name": "The Butcher's Choice",
        "scene": "farm",
        "type": "death",
        "summary": "ignored farmer",
        "description": "You turned away from the humble farmer. He did not return the favor."
    },
    "kindness": {
        "name": "Kindness is Earned Not Given",
        "scene": "farm",
        "type": "good",
        "summary": "scored perfectly on trust test",
        "description": "You saw the man, not the monster. In a land of wolves, you offered your throat—and were spared."
    },
    "self_defense": {
        "name": "You Did What You Had To Do",
        "scene": "farm",
        "type": "survived",
        "summary": "attack farmer after test",
        "description": "The cleaver sang before the test could end. You survived by instinct. But survival is not salvation."
    },
    "farmer_death": {
        "name": "Strike First, Rot Later",
        "scene": "farm",
        "type": "survived",
        "summary": "killed farmer first",
        "description": "You didn't wait. You saw a threat and acted fast. Brutal and final."
    },
    "tainted_meat": {
        "name": "You Smell Tainted",
        "scene": "farm",
        "type": "failed",
        "summary": "failed trust test",
        "description": "You hesitated, lied, or looked away. The farmer saw your soul and deemed it spoiled."
    },
    "trust_pass": {
        "name": "Trust Test Passed",
        "scene": "farm",
        "type": "test",
        "summary": "You passed the trust test",
        "description": "You earned his nod and his silence. Trust was the blade you did not see, and it spared you."
    }
    #endregion
}
