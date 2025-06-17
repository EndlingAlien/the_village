import sqlite3
from datetime import date

import analysis


# TODO: Change to GameDatabase when done testing
class MockDatabase:
    def __init__(self, db_name='game_stats.db'):
        self.conn = sqlite3.connect(db_name)
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
                run_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                run_date DATE,
                final_archetype TEXT,
                farm_condition TEXT,
                church_condition TEXT,
                swamp_condition TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
            """,
            'command_3': """CREATE TABLE IF NOT EXISTS test_results (
                run_id INTEGER PRIMARY KEY,
                trust_archetype TEXT,
                faith_archetype TEXT,
                intuition_archetype TEXT,
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id)
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
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id)
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
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id)
            )
            """,
            'command_6': """CREATE TABLE IF NOT EXISTS intuition_test_answers (
                run_id INTEGER PRIMARY KEY,
                question_1 INTEGER,
                question_2 INTEGER,
                question_3 INTEGER,
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id)
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
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id)
            )
            """,
            'command_8': """CREATE TABLE IF NOT EXISTS explore_flags (
                run_id INTEGER PRIMARY KEY,
                snooped_house BOOLEAN,
                snooped_barn BOOLEAN,
                snooped_church BOOLEAN,
                snooped_swamp BOOLEAN,
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id)
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
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id)
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
                FOREIGN KEY(run_id) REFERENCES player_runs(run_id)
            )
            """
        }
        for name, sql in commands.items():
            try:
                self.cursor.execute(sql)
            except sqlite3.Error as e:
                print(f"Failed to create {name}: {e}")

    def create_user(self, user_name):
        self.cursor.execute("""
        INSERT INTO users (user_name) VALUES (?)""", (user_name,))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_run(self, user_id, final_archetype, farm_cond, church_cond, swamp_cond):
        today = date.today()
        self.cursor.execute("""
        INSERT INTO player_runs (user_id, run_date, final_archetype, farm_condition, church_condition, swamp_condition) VALUES (?, ?, ?, ?, ?, ?)""",
                            (user_id, today, final_archetype, farm_cond, church_cond, swamp_cond,))
        self.conn.commit()
        return self.cursor.lastrowid


    def add_choices(self,run_id ,choices_dict):
        columns = ','.join(['run_id'] + list(choices_dict.keys()))
        placeholders = ','.join(['?'] * (len(choices_dict) + 1))
        values = [run_id] + list(choices_dict.values())

        self.cursor.execute(
            f"INSERT INTO choices ({columns}) VALUES ({placeholders})",
            values
        )
        self.conn.commit()

    def add_end_keys(self, run_id, ending_keys):
        pass



    def close(self):
        self.conn.commit()
        self.conn.close()


test_db = MockDatabase()


test_db.add_choices(analysis.choices_list)
