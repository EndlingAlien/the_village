import sqlite3
from datetime import date
import pandas as pd
import os
import analysis


# TODO: Change to GameDatabase when done testing
class MockDatabase:
    def __init__(self):
        self.db_name = 'mock_stats.db'
        self.conn = sqlite3.connect(self.db_name)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        commands = {
            'command_1': """CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                user_name TEXT
            )
            """,
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
            'command_3': """CREATE TABLE IF NOT EXISTS test_results (
                run_id INTEGER PRIMARY KEY,
                trust_archetype TEXT,
                faith_archetype TEXT,
                intuition_archetype TEXT,
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id) ON DELETE CASCADE
            )
            """,
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
            'command_6': """CREATE TABLE IF NOT EXISTS intuition_test_answers (
                run_id INTEGER PRIMARY KEY,
                question_1 INTEGER,
                question_2 INTEGER,
                question_3 INTEGER,
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id) ON DELETE CASCADE
            )
            """,
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
            'command_8': """CREATE TABLE IF NOT EXISTS explore_flags (
                run_id INTEGER PRIMARY KEY,
                snooped_house BOOLEAN,
                snooped_barn BOOLEAN,
                snooped_church BOOLEAN,
                snooped_swamp BOOLEAN,
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id) ON DELETE CASCADE
            )
            """,
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

    def create_user(self, user_name):
        user_name = user_name.lower()
        df = pd.read_sql_query('SELECT * FROM users', self.conn)
        if self.check_if_user_exists(user_name):
            result = pd.read_sql_query("""SELECT user_id FROM users WHERE user_name = ? LIMIT 1""", self.conn, params=(user_name,))
            if not result.empty:
                user_id = result.iloc[0]['user_id']
                return user_id
        else:
            self.cursor.execute("""
            INSERT INTO users (user_name) VALUES (?)""", (user_name,))
            return self.cursor.lastrowid

    def add_run(self, user_id, final_archetype, cond_dict):
        user_id = int(user_id)
        today = date.today().isoformat()
        farm_cond = cond_dict.get('farm')
        church_cond = cond_dict.get('church')
        swamp_cond = cond_dict.get('swamp')
        self.cursor.execute("""
        INSERT INTO player_runs (user_id, run_date, final_archetype, farm_condition, church_condition, swamp_condition) VALUES (?, ?, ?, ?, ?, ?)""",
                            (user_id, today, final_archetype, farm_cond, church_cond, swamp_cond,))
        return self.cursor.lastrowid

    def add_choices(self, run_id, choices_dict):
        columns = ','.join(['run_id'] + list(choices_dict.keys()))
        placeholders = ','.join(['?'] * (len(choices_dict) + 1))
        values = [run_id] + list(choices_dict.values())

        if self.check_if_run_exists('choices', run_id):
            result = pd.read_sql_query("""SELECT run_id FROM choices WHERE run_id = ? LIMIT 1""", self.conn, params=(run_id,))
            if not result.empty:
                print(f'Stats for this run_id of: {run_id}. Are already available.')
        else:
            self.cursor.execute(
                f"INSERT INTO choices ({columns}) VALUES ({placeholders})",
                values
            )

    def add_explore_flags(self, run_id, explore_dict):
        columns = ','.join(['run_id'] + list(explore_dict.keys()))
        placeholders = ','.join(['?'] * (len(explore_dict) + 1))
        values = [run_id] + list(explore_dict.values())

        if self.check_if_run_exists('explore_flags', run_id):
            result = pd.read_sql_query("""SELECT run_id FROM explore_flags WHERE run_id = ? LIMIT 1""", self.conn, params=(run_id,))
            if not result.empty:
                print(f'Stats for this run_id of: {run_id}. Are already available.')
        else:
            self.cursor.execute(
                f"INSERT INTO explore_flags ({columns}) VALUES ({placeholders})",
                values
            )

    def add_faith_answers(self, run_id, faith_answers_dict):
        columns = ('run_id',) + tuple(f'question_{i}' for i in range(1, 7))
        column_str = ','.join(columns)
        placeholders = ','.join(['?'] * (len(faith_answers_dict) + 1))
        values = [run_id] + list(faith_answers_dict.values())

        if self.check_if_run_exists('faith_test_answers', run_id):
            result = pd.read_sql_query("""SELECT run_id FROM faith_test_answers WHERE run_id = ? LIMIT 1""", self.conn, params=(run_id,))
            if not result.empty:
                print(f'Stats for this run_id of: {run_id}. Are already available.')
        else:
            self.cursor.execute(f"INSERT INTO faith_test_answers ({column_str}) VALUES ({placeholders})", values)

    def add_intuition_answers(self, run_id, intuition_answers_dict):
        columns = ('run_id',) + tuple(f'question_{i}' for i in range(1, 4))
        column_str = ','.join(columns)
        placeholders = ','.join(['?'] * (len(intuition_answers_dict) + 1))
        values = [run_id] + list(intuition_answers_dict.values())

        if self.check_if_run_exists('intuition_test_answers', run_id):
            result = pd.read_sql_query("""SELECT run_id FROM intuition_test_answers WHERE run_id = ? LIMIT 1""", self.conn, params=(run_id,))
            if not result.empty:
                print(f'Stats for this run_id of: {run_id}. Are already available.')
        else:
            self.cursor.execute(
                f"INSERT INTO intuition_test_answers ({column_str}) VALUES ({placeholders})",
                values
            )

    def add_trust_answers(self, run_id, trust_answers_dict):
        columns = ('run_id',) + tuple(f'question_{i}' for i in range(1, 10))
        column_str = ','.join(columns)
        placeholders = ','.join(['?'] * (len(trust_answers_dict) + 1))
        values = [run_id] + list(trust_answers_dict.values())

        if self.check_if_run_exists('trust_test_answers', run_id):
            result = pd.read_sql_query("""SELECT run_id FROM trust_test_answers WHERE run_id = ? LIMIT 1""", self.conn, params=(run_id,))
            if not result.empty:
                print(f'Stats for this run_id of: {run_id}. Are already available.')
        else:
            self.cursor.execute(
                f"INSERT INTO trust_test_answers ({column_str}) VALUES ({placeholders})",
                values
            )

    def add_end_keys(self, run_id, ending_keys_dict):
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
        for key in ending_flags:
            if key in ending_keys_dict:
                ending_flags[key] = ending_keys_dict[key]

        columns = ','.join(['run_id'] + list(ending_flags.keys()))
        placeholders = ','.join(['?'] * (len(ending_flags) + 1))
        values = [run_id] + list(ending_flags.values())

        if self.check_if_run_exists('end_keys', run_id):
            result = pd.read_sql_query("""SELECT run_id FROM end_keys WHERE run_id = ? LIMIT 1""", self.conn, params=(run_id,))
            if not result.empty:
                print(f'Stats for this run_id of: {run_id}. Are already available.')
        else:
            self.cursor.execute(
                f"INSERT INTO end_keys ({columns}) VALUES ({placeholders})",
                values
            )

    def add_inventory(self, run_id, inventory_dict):
        inventory_flags = {
            "decoder": False,
            "mask": False,
            "bible": False,
            "letter": False,
            "hammer": False,
            "key": False,
            "screwdriver": False,
            "knife": False,
            "red_vial": False,
            "blue_vial": False,
            "green_vial": False,
        }
        for key in inventory_flags:
            if key in inventory_dict:
                inventory_flags[key] = inventory_dict[key]

        columns = ','.join(['run_id'] + list(inventory_flags.keys()))
        placeholders = ','.join(['?'] * (len(inventory_flags) + 1))
        values = [run_id] + list(inventory_flags.values())

        if self.check_if_run_exists('inventory', run_id):
            result = pd.read_sql_query("""SELECT run_id FROM inventory WHERE run_id = ? LIMIT 1""", self.conn, params=(run_id,))
            if not result.empty:
                print(f'Stats for this run_id of: {run_id}. Are already available.')
        else:
            self.cursor.execute(
                f"INSERT INTO inventory ({columns}) VALUES ({placeholders})",
                values
            )

    def add_test_results(self, run_id, trust_arch, faith_arch, intuition_arch):
        if self.check_if_run_exists('test_results', run_id):
            result = pd.read_sql_query("""SELECT run_id FROM test_results WHERE run_id = ? LIMIT 1""", self.conn, params=(run_id,))
            if not result.empty:
                print(f'Stats for this run_id of: {run_id}. Are already available.')
        else:
            self.cursor.execute(
                f"INSERT INTO test_results (run_id, trust_archetype, faith_archetype, intuition_archetype) VALUES (? ,?, ?, ?)",
                (run_id, trust_arch, faith_arch, intuition_arch,)
            )

    def close_connection(self):
        self.conn.commit()
        self.conn.close()

    # region Checks
    def check_if_user_exists(self, user_name):
        self.cursor.execute("""
                SELECT 1 FROM users WHERE user_name = (?) LIMIT 1""", (user_name,))
        return self.cursor.fetchone() is not None

    def check_if_run_exists(self, table_name, run_id):
        query = f"SELECT 1 FROM {table_name} WHERE run_id = ? LIMIT 1"
        self.cursor.execute(query, (run_id,))
        return self.cursor.fetchone() is not None

    # endregion
    def insert_full_run(self, user_name, run_data):
        try:
            self.conn.execute("BEGIN")  # Start transaction

            # === Step-by-step inserts ===
            user_id = self.create_user(user_name)  # Insert or fetch user
            run_id = self.add_run(user_id, run_data['archetype_data']['choice_archetype'], run_data['cond_data'])

            self.add_trust_answers(run_id, run_data['test_data']['trust_answers'])
            self.add_faith_answers(run_id, run_data['test_data']['faith_answers'])
            self.add_intuition_answers(run_id, run_data['test_data']['intuition_answers'])
            self.add_inventory(run_id, run_data['player_data']['inventory'])
            self.add_explore_flags(run_id, run_data['player_data']['explore_flag'])
            self.add_choices(run_id, run_data['player_data']['choices'])
            self.add_end_keys(run_id, run_data['player_data']['ending_key'])
            self.add_test_results(run_id, run_data['archetype_data']['trust_archetype'], run_data['archetype_data']['faith_archetype'],
                                  run_data['archetype_data']['intuition_archetype'])

            self.conn.commit()  # If everything worked, save it
            print(f"Successfully inserted full run for {user_name}")

        except Exception as e:
            self.conn.rollback()  # Revert everything if one thing fails
            print(f"Failed to insert full run: {e}")


    # TODO: Use this when done with testing to remove testing data and reset db
    def reset_database(self):
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
        self.cursor.execute("DROP TABLE IF EXISTS player_runs;")
        self.cursor.execute("DROP TABLE IF EXISTS users;")
        self.create_tables()


# for testing
test_db = MockDatabase()

#TODO: !!!!!!!!!____________SUPER IMPORTANT_____________!!!!!!!!!!
# This is what our 'final_stats' needs to look like at end of game to make everything easy!
final_data = {
    "cond_data": {
        "farm": 'farmer_outside',
        "swamp": 'no_fog',
        "church": 'priest_inside'
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


test_db.insert_full_run('Patty', final_data)

# _______________TESTING AREA __________________________
'''#current_user_id = test_db.create_user("michelle")
arch_func = analysis.calc_choice_archetype(analysis.choices_list)
#run_id = test_db.add_run(current_user_id, arch_func, test_dict)
a = analysis

faith_archetype = a.calc_faith_test_archetype(test_answers_dict['faith'])
intuition_archetype = a.calc_intuition_test_archetype(test_answers_dict['intuition'])
trust_archetype = a.calc_trust_test_archetype(8)
test_db.add_test_results(3, trust_archetype,faith_archetype, intuition_archetype)'''
