import sqlite3
from datetime import date
import pandas as pd
import os


#TODO: !!!!!!!!!____________SUPER IMPORTANT_____________!!!!!!!!!!
# This is what our 'final_stats' needs to look like at end of game to make everything easy!
final_data = {
    "cond_data": {},
    "player_data": {},
    "test_data": {},
    "archetype_data": {}
}

#example of final_data
final_data = {
    "cond_data": {
        "farm": None,
        "swamp": None,
        "church": None
    },
    "player_data": {
        "explore_flag": {  # all start as False, game changes them to True
            "snooped_house": False,
            "snooped_barn": True,
            "snooped_church": True,
            "snooped_swamp": False,
        },
        "inventory": {  # Needs to be empty when game starts /// Below is for testing
            "decoder": True,
            "bible": True,
            "hammer": True,
            "key": True,

        },
        "choices": {  # all will stay as None, final check will ask: if choices[key] =! None -> save to db
            "vials_choice": 1,
            "cube_choice": 2,
            "curious_choice": None,
            "basement_door_choice": 1,
            "basement_choice": None,
            "basement_two_choice": None,
            "start_choice": 2,
            "knock_choice": None,
            "meet_choice": 1,
            "break_choice": None
        },
        "ending_key": {
            "rejected": True,
            "faith_pass": True,
            "priest_death": True,
            "self_defense": True,
            "trust_pass": True
        },
    },
    "test_data": {
        "trust_answers": {
            "question_1": 2,
            "question_2": 1,
            "question_3": 2,
            "question_4": 1,
            "question_5": 2,
            "question_6": 1,
            "question_7": 1,
            "question_8": 2,
            "question_9": 1},
        "faith_answers": {
            "question_1": 3,
            "question_2": 2,
            "question_3": 1,
            "question_4": 3,
            "question_5": 2,
            "question_6": 2},
        "intuition_answers": {
            "question_1": 2,
            "question_2": 1,
            "question_3": 3},
    },
    "archetype_data": {
        "trust_archetype": 'chosen',
        "faith_archetype": 'unbending',
        "intuition_archetype": 'curious',
        "choice_archetype": 'observant',
    }
}



# TODO: Change to GameDatabase when done testing
class MockDatabase:
    """
        Simulates a database interface for storing and managing player stats and test results.
        Handles table creation, insertion of gameplay data, and transactional insert of a full player run.
    """
    def __init__(self):
        """Initialize database connection and create all necessary tables."""
        self.db_name = 'mock_stats.db'
        self.conn = sqlite3.connect(self.db_name)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create all tables if they don't already exist."""
        commands = {
            # Table for storing user information
            'command_1': """CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                user_name TEXT
            )
            """,
            # Table for each run a user completes
            'command_2': """CREATE TABLE IF NOT EXISTS player_runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            run_date DATE,
            final_archetype TEXT,
            farm_condition TEXT,
            church_condition TEXT,
            swamp_condition TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
            """,
            # Archetype results from player tests
            'command_3': """CREATE TABLE IF NOT EXISTS test_results (
                run_id INTEGER PRIMARY KEY,
                trust_archetype TEXT,
                faith_archetype TEXT,
                intuition_archetype TEXT,
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id) ON DELETE CASCADE
            )
            """,
            # Player's answers to the trust test
            'command_4': """CREATE TABLE IF NOT EXISTS trust_test_answers (
                run_id INTEGER PRIMARY KEY,
                question_1 INTEGER,
                question_2 INTEGER,
                question_3 INTEGER,
                question_4 INTEGER,
                question_5 INTEGER,
                question_6 INTEGER,
                question_7 INTEGER,
                question_8 INTEGER,
                question_9 INTEGER,
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id) ON DELETE CASCADE
            )
            """,
            # Player's answers to the faith test
            'command_5': """CREATE TABLE IF NOT EXISTS faith_test_answers (
                run_id INTEGER PRIMARY KEY,
                question_1 INTEGER,
                question_2 INTEGER,
                question_3 INTEGER,
                question_4 INTEGER,
                question_5 INTEGER,
                question_6 INTEGER,
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id) ON DELETE CASCADE
            )
            """,
            # Player's answers to the intuition test
            'command_6': """CREATE TABLE IF NOT EXISTS intuition_test_answers (
                run_id INTEGER PRIMARY KEY,
                question_1 INTEGER,
                question_2 INTEGER,
                question_3 INTEGER,
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id) ON DELETE CASCADE
            )
            """,
            # Items acquired in the playthrough
            'command_7': """CREATE TABLE IF NOT EXISTS inventory (
                run_id INTEGER PRIMARY KEY,
                decoder BOOLEAN,
                mask BOOLEAN,
                bible BOOLEAN,
                letter BOOLEAN,
                hammer BOOLEAN,
                key BOOLEAN,
                screwdriver BOOLEAN,
                knife BOOLEAN,
                red_vial BOOLEAN,
                green_vial BOOLEAN,
                blue_vial BOOLEAN,
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id) ON DELETE CASCADE
            )
            """,
            # Flags showing which areas the player explored
            'command_8': """CREATE TABLE IF NOT EXISTS explore_flags (
                run_id INTEGER PRIMARY KEY,
                snooped_house BOOLEAN,
                snooped_barn BOOLEAN,
                snooped_church BOOLEAN,
                snooped_swamp BOOLEAN,
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id) ON DELETE CASCADE
            )
            """,
            # All major in-game choices made
            'command_9': """CREATE TABLE IF NOT EXISTS choices (
                run_id INTEGER PRIMARY KEY,
                vials_choice INTEGER,
                cube_choice INTEGER,
                curious_choice INTEGER,
                basement_door_choice INTEGER,
                basement_choice INTEGER,
                basement_two_choice INTEGER,
                start_choice INTEGER,
                knock_choice INTEGER,
                meet_choice INTEGER,
                break_choice INTEGER,
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id) ON DELETE CASCADE
            )
            """,
            # Binary flags for endings reached
            'command_10': """CREATE TABLE IF NOT EXISTS end_keys (
                run_id INTEGER PRIMARY KEY,
                cleansed BOOLEAN,
                vessel BOOLEAN,
                rejected BOOLEAN,
                probed BOOLEAN,
                you_belong BOOLEAN,
                intuition_pass BOOLEAN,
                believer BOOLEAN,
                faith_pass BOOLEAN,
                heretic BOOLEAN,
                priest_death BOOLEAN,
                altar BOOLEAN,
                butcher BOOLEAN,
                kindness BOOLEAN,
                self_defense BOOLEAN,
                tainted_meat BOOLEAN,
                trust_pass BOOLEAN,
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id) ON DELETE CASCADE
            )
            """
        }
        for name, sql in commands.items():
            try:
                self.cursor.execute(sql)
            except sqlite3.Error as e:
                print(f"Failed to create {name}: {e}")

    #region Table Functions

    def create_user(self, user_name):
        """
        Creates a new user in the database or returns the existing user's ID.
        :param user_name: The name of the user to create or fetch (case-insensitive).
        :return: The user_id of the existing or newly created user.
        """
        user_name = user_name.strip().lower()  # Normalize username to lowercase for consistency

        # Check if the user already exists in the database
        if self.check_if_user_exists(user_name):
            # Fetch and return the existing user's ID
            result = pd.read_sql_query(
                """SELECT user_id FROM users WHERE user_name = ? LIMIT 1""",
                self.conn,
                params=(user_name,)
            )
            if not result.empty:
                user_id = result.iloc[0]['user_id']
                return user_id
        else:
            # Insert a new user record
            self.cursor.execute(
                """INSERT INTO users (user_name) VALUES (?)""",
                (user_name,)
            )
            return self.cursor.lastrowid

    def add_run(self, user_id, final_archetype, cond_dict):
        """
        Adds a new player run entry to the player_runs table.
        :param user_id: ID of the user who completed the run.
        :param final_archetype: The final archetype determined for this run.
        :param cond_dict: Dictionary containing scene conditions for farm, church, and swamp.
        :return: The run_id of the newly inserted run.
        """
        user_id = int(user_id)
        today = date.today().isoformat()  # Get current date in ISO format

        # Extract scene conditions
        farm_cond = str(cond_dict.get('farm')) if cond_dict.get('farm') is not None else None
        church_cond = str(cond_dict.get('church')) if cond_dict.get('church') is not None else None
        swamp_cond = str(cond_dict.get('swamp')) if cond_dict.get('swamp') is not None else None

        # Insert new run record with conditions and archetype
        self.cursor.execute(
            """
            INSERT INTO player_runs 
            (user_id, run_date, final_archetype, farm_condition, church_condition, swamp_condition) 
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, today, final_archetype, farm_cond, church_cond, swamp_cond)
        )
        return self.cursor.lastrowid

    def add_choices(self, run_id, choices_dict):
        """
        Adds player choice data for a run into the choice table.
        :param run_id: The run identifier this choice data belongs to.
        :param choices_dict: Dictionary of choice keys and their selected values.
        """
        # Prepare column names and SQL placeholders for insertion
        columns = ','.join(['run_id'] + list(choices_dict.keys()))
        placeholders = ','.join(['?'] * (len(choices_dict) + 1))
        values = [run_id] + list(choices_dict.values())

        if any(isinstance(v, dict) for v in choices_dict.values()):
            raise ValueError("Choices dict contains nested dicts. Expected flat key: value pairs.")

        # Check if choices for this run already exist
        if self.check_if_run_exists('choices', run_id):
            result = pd.read_sql_query(
                """SELECT run_id FROM choices WHERE run_id = ? LIMIT 1""",
                self.conn,
                params=(run_id,)
            )
            if not result.empty:
                print(f'Stats for this run_id of: {run_id} are already available.')
        else:
            # Insert new choices record
            self.cursor.execute(
                f"INSERT INTO choices ({columns}) VALUES ({placeholders})",
                values
            )

    def add_explore_flags(self, run_id, explore_dict):
        """
        Inserts explore flag data for a run into the explore_flags table.
        :param run_id: The run identifier this data belongs to.
        :param explore_dict: Dictionary of explore flags (e.g., snooped_house, snooped_barn).
        """
        # Prepare column names and placeholders for SQL insertion
        columns = ','.join(['run_id'] + list(explore_dict.keys()))
        placeholders = ','.join(['?'] * (len(explore_dict) + 1))
        values = [run_id] + list(explore_dict.values())

        for k, v in explore_dict.items():
            if isinstance(v, dict):
                raise TypeError(f"Explore flag '{k}' has invalid dict value: {v}")

        # Check if explore flags for this run already exist
        if self.check_if_run_exists('explore_flags', run_id):
            result = pd.read_sql_query(
                """SELECT run_id FROM explore_flags WHERE run_id = ? LIMIT 1""",
                self.conn,
                params=(run_id,)
            )
            if not result.empty:
                print(f'Stats for this run_id of: {run_id} are already available.')
        else:
            # Insert new explore flags record
            self.cursor.execute(
                f"INSERT INTO explore_flags ({columns}) VALUES ({placeholders})",
                values
            )

    def add_faith_answers(self, run_id, faith_answers_dict):
        """
        Inserts faith test answers for a run into the faith_test_answers table.
        :param run_id: The run identifier this data belongs to.
        :param faith_answers_dict: Dictionary of faith test question answers.
        """
        # Define columns: run_id plus question_1 to question_6
        columns = ('run_id',) + tuple(f'question_{i}' for i in range(1, 7))
        column_str = ','.join(columns)
        placeholders = ','.join(['?'] * (len(faith_answers_dict) + 1))
        values = [run_id] + [faith_answers_dict.get(f'question_{i}') for i in range(1, 7)]

        for k, v in faith_answers_dict.items():
            if isinstance(v, dict):
                raise TypeError(f"Faith answer '{k}' has invalid dict value: {v}")

        # Check if faith test answers for this run already exist
        if self.check_if_run_exists('faith_test_answers', run_id):
            result = pd.read_sql_query(
                """SELECT run_id FROM faith_test_answers WHERE run_id = ? LIMIT 1""",
                self.conn,
                params=(run_id,)
            )
            if not result.empty:
                print(f'Stats for this run_id of: {run_id} are already available.')
        else:
            # Insert new faith test answers record
            self.cursor.execute(
                f"INSERT INTO faith_test_answers ({column_str}) VALUES ({placeholders})",
                values
            )

    def add_intuition_answers(self, run_id, intuition_answers_dict):
        """
        Inserts intuition test answers for a run into the intuition_test_answers table.
        :param run_id: The run identifier this data belongs to.
        :param intuition_answers_dict: Dictionary of intuition test question answers.
        """
        # Define columns: run_id plus question_1 to question_3
        columns = ('run_id',) + tuple(f'question_{i}' for i in range(1, 4))
        column_str = ','.join(columns)
        placeholders = ','.join(['?'] * (len(intuition_answers_dict) + 1))
        values = [run_id] + [intuition_answers_dict.get(f'question_{i}') for i in range(1, 4)]

        for k, v in intuition_answers_dict.items():
            if isinstance(v, dict):
                raise TypeError(f"Intuition answer '{k}' has invalid dict value: {v}")


        # Check if intuition test answers for this run already exist
        if self.check_if_run_exists('intuition_test_answers', run_id):
            result = pd.read_sql_query(
                """SELECT run_id FROM intuition_test_answers WHERE run_id = ? LIMIT 1""",
                self.conn,
                params=(run_id,)
            )
            if not result.empty:
                print(f'Stats for this run_id of: {run_id} are already available.')
        else:
            # Insert new intuition test answers record
            self.cursor.execute(
                f"INSERT INTO intuition_test_answers ({column_str}) VALUES ({placeholders})",
                values
            )

    def add_trust_answers(self, run_id, trust_answers_dict):
        """
        Inserts trust test answers for a run into the trust_test_answers table.
        :param run_id: The run identifier this data belongs to.
        :param trust_answers_dict: Dictionary of trust test question answers.
        """
        # Define columns: run_id plus question_1 to question_9
        columns = ('run_id',) + tuple(f'question_{i}' for i in range(1, 10))
        column_str = ','.join(columns)
        placeholders = ','.join(['?'] * len(columns))
        values = [run_id] + [trust_answers_dict.get(f'question_{i}') for i in range(1, 10)]

        for k, v in trust_answers_dict.items():
            if isinstance(v, dict):
                raise TypeError(f"Trust answer '{k}' has invalid dict value: {v}")

        # Check if trust test answers for this run already exist
        if self.check_if_run_exists('trust_test_answers', run_id):
            result = pd.read_sql_query(
                """SELECT run_id FROM trust_test_answers WHERE run_id = ? LIMIT 1""",
                self.conn,
                params=(run_id,)
            )
            if not result.empty:
                print(f'Stats for this run_id of: {run_id} are already available.')
        else:
            # Insert new trust test answers record
            self.cursor.execute(
                f"INSERT INTO trust_test_answers ({column_str}) VALUES ({placeholders})",
                values
            )

    def add_end_keys(self, run_id, ending_keys_list):
        """
        Inserts or updates the end keys (flags representing game endings and statuses) for a given run.
        :param run_id: The identifier of the current run.
        :param ending_keys_list: List of strings representing end keys reached.
        """

        # Safety check: ensure input is a list of strings, no dicts sneaking in
        if not isinstance(ending_keys_list, list):
            raise TypeError(f"Expected ending_keys_list to be a list, got {type(ending_keys_list).__name__}")

        for item in ending_keys_list:
            if not isinstance(item, str):
                raise TypeError(f"Ending key list contains a non-string value: {item} ({type(item).__name__})")

        # Default all possible ending flags to False
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

        # Set flags based on what’s in the list
        for key in ending_flags:
            if key in ending_keys_list:
                ending_flags[key] = True

        # Define columns and values before the insert
        columns = ','.join(['run_id'] + list(ending_flags.keys()))
        placeholders = ','.join(['?'] * (len(ending_flags) + 1))
        values = [run_id] + list(ending_flags.values())

        # Check if end keys for this run already exist
        if self.check_if_run_exists('end_keys', run_id):
            result = pd.read_sql_query(
                """SELECT run_id FROM end_keys WHERE run_id = ? LIMIT 1""",
                self.conn,
                params=(run_id,)
            )
            if not result.empty:
                print(f'Stats for this run_id of: {run_id} are already available.')
        else:
            # Insert new end keys record
            self.cursor.execute(
                f"INSERT INTO end_keys ({columns}) VALUES ({placeholders})",
                values
            )

    def add_inventory(self, run_id, inventory_dict):
        """
        Inserts or updates the player's inventory items for a given run.
        :param run_id: The identifier of the current run.
        :param inventory_dict: Dictionary containing inventory item flags (boolean values).
        """

        # Prepare column names and placeholders for SQL insertion
        columns = ','.join(['run_id'] + list(inventory_dict.keys()))
        placeholders = ','.join(['?'] * (len(inventory_dict) + 1))
        values = [run_id] + list(inventory_dict.values())

        for k, v in inventory_dict.items():
            if isinstance(v, dict):
                raise TypeError(f"Inventory '{k}' has invalid dict value: {v}")

        # Check if inventory for this run already exists
        if self.check_if_run_exists('inventory', run_id):
            result = pd.read_sql_query(
                """SELECT run_id FROM inventory WHERE run_id = ? LIMIT 1""",
                self.conn,
                params=(run_id,)
            )
            if not result.empty:
                print(f'Stats for this run_id of: {run_id} are already available.')
        else:
            # Insert new inventory record
            self.cursor.execute(
                f"INSERT INTO inventory ({columns}) VALUES ({placeholders})",
                values
            )

    def add_test_results(self, run_id, trust_arch, faith_arch, intuition_arch):
        """
        Inserts the archetype results of tests (trust, faith, intuition) for a given run.
        :param run_id: The identifier of the current run.
        :param trust_arch: The trust archetype result as a string.
        :param faith_arch: The faith archetype result as a string.
        :param intuition_arch: The intuition archetype result as a string.
        """

        for name, arch in [('trust', trust_arch), ('faith', faith_arch), ('intuition', intuition_arch)]:
            if isinstance(arch, dict):
                raise TypeError(f"{name} archetype is a dict, expected string or None: {arch}")


        # Check if test results for this run already exist
        if self.check_if_run_exists('test_results', run_id):
            result = pd.read_sql_query(
                """SELECT run_id FROM test_results WHERE run_id = ? LIMIT 1""",
                self.conn,
                params=(run_id,)
            )
            if not result.empty:
                print(f'Stats for this run_id of: {run_id} are already available.')
        else:
            # Insert new test results record
            self.cursor.execute(
                f"INSERT INTO test_results (run_id, trust_archetype, faith_archetype, intuition_archetype) VALUES (?, ?, ?, ?)",
                (run_id, trust_arch, faith_arch, intuition_arch)
            )

    #endregion

    def close_connection(self):
        """
        Commits any pending transactions and closes the database connection.
        """
        self.conn.commit()
        self.conn.close()

    #region Table Checks

    def check_if_user_exists(self, user_name):
        """
        Checks if a user with the given username exists in the 'users' table.
        :param user_name: Username to check.
        :return: True if user exists, False otherwise.
        """
        self.cursor.execute(
            "SELECT 1 FROM users WHERE user_name = ? LIMIT 1",
            (user_name,)
        )
        return self.cursor.fetchone() is not None

    def check_if_run_exists(self, table_name, run_id):
        """
        Checks if a record with the given run_id exists in the specified table.
        :param table_name: Name of the table to query.
        :param run_id: The run identifier to check.
        :return: True if the run exists in the table, False otherwise.
        """
        query = f"SELECT 1 FROM {table_name} WHERE run_id = ? LIMIT 1"
        self.cursor.execute(query, (run_id,))
        return self.cursor.fetchone() is not None

    #endregion

    def insert_full_run(self, user_name, run_data):
        """
        Inserts a complete run's worth of data into all relevant tables within a single transaction.
        Rolls back all changes if any insertion fails to maintain data integrity.
        :param user_name: The player's username.
        :param run_data: Dictionary containing all run data structured with keys for archetypes, conditions,
                         test answers, inventory, exploration flags, choices, ending keys, etc.
        """
        try:
            self.conn.execute("BEGIN")  # Begin transaction

            # Insert or fetch user ID
            user_id = self.create_user(user_name)
            # Insert run metadata and get run ID
            run_id = self.add_run(user_id, run_data['archetype_data']['choice_archetype'], run_data['cond_data'])

            # Insert test answers
            self.add_trust_answers(run_id, run_data['test_data']['trust_answers'])
            self.add_faith_answers(run_id, run_data['test_data']['faith_answers'])
            self.add_intuition_answers(run_id, run_data['test_data']['intuition_answers'])

            # Insert player-related data
            self.add_inventory(run_id, run_data['player_data']['inventory'])
            self.add_explore_flags(run_id, run_data['player_data']['explore_flag'])
            self.add_choices(run_id, run_data['player_data']['choices'])
            self.add_end_keys(run_id, run_data['player_data']['ending_key'])

            # Insert archetype results
            self.add_test_results(
                run_id,
                run_data['archetype_data']['trust_archetype'],
                run_data['archetype_data']['faith_archetype'],
                run_data['archetype_data']['intuition_archetype']
            )

            self.conn.commit()  # Commit transaction if all inserts succeed
            print(f"Successfully inserted full run for {user_name}")

        except Exception as e:
            self.conn.rollback()  # Roll back all changes if any insert fails
            print(f"Failed to insert full run: {e}")

    # ________________________TESTING AREA _______________________

    def retrieve_all_users(self):
        query = "SELECT user_name FROM users"
        self.cursor.execute(query)
        return self.cursor.fetchall()


    # TODO: Use this when done with testing to remove testing data and reset db
    def reset_database(self):
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
        self.cursor.execute("DROP TABLE IF EXISTS player_runs;")
        self.cursor.execute("DROP TABLE IF EXISTS users;")
        self.create_tables()

# for testing
test_db = MockDatabase()

#example of function
#test_db.insert_full_run('Patty', final_data)
