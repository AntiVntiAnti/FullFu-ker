# from sexy_logger import logger
import tracker_config as tkc
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import os
import shutil
from logger_setup import logger

user_dir = os.path.expanduser('~')
db_path = os.path.join(os.getcwd(), tkc.DB_NAME)  # Database Name
target_db_path = os.path.join(user_dir, tkc.DB_NAME)  # Database Name


def initialize_database():
    try:
        if not os.path.exists(target_db_path):
            if os.path.exists(db_path):
                shutil.copy(db_path, target_db_path)
            else:
                db = QSqlDatabase.addDatabase('QSQLITE')
                db.setDatabaseName(target_db_path)
                if not db.open():
                    logger.error("Error: Unable to create database")
                db.close()
    except Exception as e:
        logger.error("Error: Unable to create database", str(e))


class DataManager:
    
    def __init__(self,
                 db_name=target_db_path):
        try:
            self.db = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(db_name)
            
            if not self.db.open():
                logger.error("Error: Unable to open database")
            logger.info("DB INITIALIZING")
            self.query = QSqlQuery()
            self.setup_tables()
        except Exception as e:
            logger.error(f"Error: Unable to open database {e}", exc_info=True)
    
    def setup_tables(self):
        self.setup_sleep_table()
        self.setup_total_hours_slept_table()
        self.setup_woke_up_like_table()
        self.setup_sleep_quality_table()
        self.setup_shower()
        self.setup_exercise()
        self.setup_teethbrush()
        self.setup_diet_table()
        self.setup_hydration_table()
        self.setup_wefe_table()
        self.setup_into_cspr_exam()
        self.setup_mental_mental_table()
        self.setup_lily_diet_table()
        self.setup_lily_mood_table()
        self.setup_wiggles_walks_table()
        self.setup_time_in_room_table()
        self.setup_lily_notes_table()
        self.setup_lily_walk_notes_table()
    
    def setup_lily_notes_table(self) -> None:
        """
        Sets up the 'lily_notes_table' in the database if it doesn't already exist.

        This method creates a table named 'lily_notes_table' with the following columns:
        - id: INTEGER (Primary Key, Auto Increment)
        - lily_date: TEXT
        - lily_time: TEXT
        - lily_notes: TEXT

        Returns:
        - None if the table is created successfully.
        - Logs an error message if there's an error creating the table.
        """
        if not self.query.exec(f"""
                        CREATE TABLE IF NOT EXISTS lily_notes_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lily_date TEXT,
                        lily_time TEXT,
                        lily_notes TEXT
                        )"""):
            logger.error(f"Error creating table: lily_notes_table", self.query.lastError().text())
    
    def insert_into_lily_notes_table(self,
                                     lily_date: str,
                                     lily_time: str,
                                     lily_notes: str) -> None:
        """
        Inserts a new record into the lily_notes_table.

        Args:
            lily_date (str): The date of the Lily note.
            lily_time (str): The time of the Lily note.
            lily_notes (str): The content of the Lily note.

        Raises:
            ValueError: If the number of bind values does not match the number of placeholders in the SQL query.

        Returns:
            None
        """
        sql: str = f"""INSERT INTO lily_notes_table(lily_date, lily_time, lily_notes) VALUES (?, ?, ?)"""
        bind_values: List[str] = [lily_date, lily_time, lily_notes]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: lily_notes_table Expected {sql.count('?')}
                            bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(f"Error inserting data: lily_notes_table - {self.query.lastError().text()}")
        except ValueError as e:
            logger.error(f"ValueError lily_notes_table: {e}")
        except Exception as e:
            logger.error(f"Error during data insertion: lily_notes_table {e}", exc_info=True)
        
        ##################################################################################################################
        # Lily Diet Table
        ##################################################################################################################
    
    def setup_time_in_room_table(self) -> None:
        """
        Sets up the 'lily_in_room_table' table in the database if it doesn't exist.

        This method creates the 'lily_in_room_table' table with the following columns:
        - id: INTEGER (Primary Key, Autoincrement)
        - lily_date: TEXT
        - lily_time: TEXT
        - time_in_room_slider: INTEGER

        Returns:
        None
        """
        if not self.query.exec(f"""
                        CREATE TABLE IF NOT EXISTS lily_in_room_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lily_date TEXT,
                        lily_time TEXT,
                        time_in_room_slider INTEGER
                        )"""):
            logger.error(f"Error creating table: lily_in_room_table", self.query.lastError().text())
    
    def insert_into_time_in_room_table(self,
                                       lily_date: str,
                                       lily_time: str,
                                       time_in_room_slider: int) -> None:
        """
        Inserts a new record into the lily_in_room_table.

        Args:
            lily_date (str): The date of the record.
            lily_time (str): The time of the record.
            time_in_room_slider (int): The value of the time_in_room_slider.

        Raises:
            ValueError: If the number of bind values does not match the expected number of placeholders in the SQL query.

        Returns:
            None
        """
        sql: str = f"""INSERT INTO lily_in_room_table(lily_date, lily_time,
                                               time_in_room_slider) VALUES (?, ?, ?)"""
        bind_values: List[Union[str, int]] = [lily_date, lily_time, time_in_room_slider]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: lily_in_room_table Expected {sql.count('?')}
                            bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: lily_in_room_table - {self.query.lastError().text()}")
        except ValueError as e:
            logger.error(f"ValueError lily_in_room_table: {e}")
        except Exception as e:
            logger.error(f"Error during data insertion: lily_in_room_table {e}", exc_info=True)
        
        ##################################################################################################################
        # Lily Diet Table
        ##################################################################################################################
    
    def setup_lily_diet_table(self) -> None:
        """
        Sets up the 'lily_diet_table' in the database if it doesn't already exist.

        This method creates a table named 'lily_diet_table' with the following columns:
        - id: INTEGER (Primary Key, Auto Increment)
        - lily_date: TEXT
        - lily_time: TEXT

        Returns:
        None
        """
        if not self.query.exec(f"""
                        CREATE TABLE IF NOT EXISTS lily_diet_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lily_date TEXT,
                        lily_time TEXT
                        )"""):
            logger.error(f"Error creating table: lily_diet_table", self.query.lastError().text())
    
    def insert_into_lily_diet_table(self,
                                    lily_date: str,
                                    lily_time: str) -> None:
        """
        Inserts a new record into the lily_diet_table.

        Args:
            lily_date (str): The date of the record.
            lily_time (str): The time of the record.

        Raises:
            ValueError: If the number of bind values does not match the expected number of placeholders in the SQL query.

        Returns:
        None
        """
        sql: str = f"""INSERT INTO lily_diet_table(lily_date, lily_time) VALUES (?, ?)"""
        bind_values: List[str] = [lily_date, lily_time]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: lily_eats_table Expected {sql.count('?')}
                            bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: lily_eats_table - {self.query.lastError().text()}")
        except ValueError as e:
            logger.error(f"ValueError lily_eats_table: {e}")
        except Exception as e:
            logger.error(f"Error during data insertion: lily_eats_table {e}", exc_info=True)
        
        ##################################################################################################################
        #       Lily MOOD table
        ##################################################################################################################
    
    def setup_lily_mood_table(self) -> None:
        if not self.query.exec(f"""
                        CREATE TABLE IF NOT EXISTS lily_mood_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lily_date TEXT,
                        lily_time TEXT,
                        lily_mood_slider INTEGER,
                        lily_mood_activity_slider INTEGER,
                        lily_energy_slider INTEGER
                            )"""):
            logger.error(f"Error creating table: lily_mood_table", self.query.lastError().text())
    
    def insert_into_lily_mood_table(self,
                                    lily_date: str,
                                    lily_time: str,
                                    lily_mood_slider: int,
                                    lily_mood_activity_slider: int,
                                    lily_energy_slider: int) -> None:
        """
        Inserts a new record into the lily_mood_table.

        Args:
            lily_date (str): The date of the record.
            lily_time (str): The time of the record.
            lily_mood_slider (int): The mood slider value.
            lily_mood_activity_slider (int): The mood activity slider value.
            lily_energy_slider (int): The energy slider value.

        Raises:
            ValueError: If the number of bind values does not match the expected number in the SQL query.

        Returns:
        None
        """
        sql: str = f"""INSERT INTO lily_mood_table(
                lily_date, lily_time, lily_mood_slider, lily_mood_activity_slider, lily_energy_slider)
                VALUES (?, ?, ?, ?, ?)"""
        bind_values: List[Union[str, int]] = [lily_date, lily_time, lily_mood_slider,
                                              lily_mood_activity_slider, lily_energy_slider]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: lily_mood_table Expected
                            {sql.count('?')} bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: lily_mood_table - {self.query.lastError().text()}")
        except ValueError as ve:
            logger.error(f"ValueError lily_mood_table: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during data insertion: lily_mood_table {e}", exc_info=True)
        
        # Lily WALKS table
    
    def setup_wiggles_walks_table(self) -> None:
        """
        Sets up the 'lily_walk_table' in the database if it doesn't already exist.

        This method creates a table named 'lily_walk_table' with the following columns:
        - id: INTEGER (Primary Key, Autoincrement)
        - lily_date: TEXT
        - lily_time: TEXT
        - lily_behavior: INTEGER
        - lily_gait: INTEGER

        Returns:
        None
        """
        if not self.query.exec(f"""
                        CREATE TABLE IF NOT EXISTS lily_walk_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lily_date TEXT,
                        lily_time TEXT,
                        lily_behavior INTEGER,
                        lily_gait INTEGER
                        )"""):
            logger.error(f"Error creating table: lily_walk_table", self.query.lastError().text())
    
    def insert_into_wiggles_walks_table(self,
                                        lily_date: str,
                                        lily_time: str,
                                        lily_behavior: int,
                                        lily_gait: int) -> None:
        """
        Inserts a new record into the lily_walk_table.

        Args:
            lily_date (str): The date of the walk.
            lily_time (str): The time of the walk.
            lily_behavior (str): The behavior during the walk.
            lily_gait (str): The gait during the walk.

        Raises:
            ValueError: If the number of bind values does not match the number of placeholders in the SQL query.

        Returns:
        None
        """
        sql: str = f"""INSERT INTO lily_walk_table(
                    lily_date, lily_time, lily_behavior, lily_gait)
                    VALUES (?, ?, ?, ?)"""
        
        bind_values: List[Union[str, int]] = [lily_date, lily_time, lily_behavior, lily_gait]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(
                    f"Mismatch: lily_walk_table Expected {sql.count('?')} bind values, got "
                    f"{len(bind_values)}.")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: lily_walk_table - {self.query.lastError().text()}")
        except ValueError as ve:
            logger.error(f"ValueError lily_walk_table: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during data insertion: lily_walk_table", str(e))
    
    def setup_lily_walk_notes_table(self) -> None:
        """
        Sets up the 'lily_walk_table' in the database if it doesn't already exist.

        This method creates a table named 'lily_walk_table' with the following columns:
        - id: INTEGER (Primary Key, Autoincrement)
        - lily_date: TEXT
        - lily_time: TEXT
        - lily_walk_note: TEXT

        Returns:
        None
        """
        if not self.query.exec(f"""
                        CREATE TABLE IF NOT EXISTS lily_walk_notes_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lily_date TEXT,
                        lily_time TEXT,
                        lily_walk_note TEXT
                        )"""):
            logger.error(f"Error creating table: lily_walk_notes_table",
                         self.query.lastError().text())
    
    def insert_into_lily_walk_notes_table(self,
                                          lily_date: str,
                                          lily_time: str,
                                          lily_walk_note: str) -> None:
        """
        Inserts a new record into the lily_walk_notes_table.

        Args:
            lily_date (str): The date of the walk.
            lily_time (str): The time of the walk.
            lily_walk_note (str): Additional notes about the walk.

        Raises:
            ValueError: If the number of bind values does not match the number of placeholders in the SQL query.

        Returns:
        None
        """
        sql: str = f"""INSERT INTO lily_walk_notes_table(
                    lily_date, lily_time, lily_walk_note)
                    VALUES (?, ?, ?)"""
        
        bind_values: List[Union[str, int]] = [lily_date, lily_time, lily_walk_note]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(
                    f"Mismatch: lily_walk_notes_table Expected {sql.count('?')} bind values, got "
                    f"{len(bind_values)}.")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: lily_walk_notes_table - {self.query.lastError().text()}")
        except ValueError as ve:
            logger.error(f"ValueError lily_walk_notes_table: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during data insertion: lily_walk_notes_table", str(e))
    
    def setup_mental_mental_table(self) -> None:
        """
        Sets up the 'mental_mental_table' in the database if it doesn't already exist.

        This method creates a table named 'mental_mental_table' in the database with the following columns:
        - id: INTEGER (Primary Key, Autoincrement)
        - mental_mental_date: TEXT
        - mental_mental_time: TEXT
        - mood_slider: INTEGER
        - mania_slider: INTEGER
        - depression_slider: INTEGER
        - mixed_risk_slider: INTEGER

        If the table already exists, this method does nothing.

        Returns:
            None
        """
        if not self.query.exec(f"""
                                    CREATE TABLE IF NOT EXISTS mental_mental_table (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    mental_mental_date TEXT,
                                    mental_mental_time TEXT,
                                    mood_slider INTEGER,
                                    mania_slider INTEGER,
                                    depression_slider INTEGER,
                                    mixed_risk_slider INTEGER
                                    )"""):
            logger.error(f"Error creating table: mental_mental_table",
                         self.query.lastError().text())
    
    def insert_into_mental_mental_table(self,
                                        mental_mental_date: int,
                                        mental_mental_time: int,
                                        mood_slider: int,
                                        mania_slider: int,
                                        depression_slider: int,
                                        mixed_risk_slider: int) -> None:
        """
        Inserts data into the mental_mental_table.

        Args:
            mental_mental_date (int): The date of the mental_mental record.
            mental_mental_time (int): The time of the mental_mental record.
            mood_slider (int): The value of the mood slider.
            mania_slider (int): The value of the mania slider.
            depression_slider (int): The value of the depression slider.
            mixed_risk_slider (int): The value of the mixed risk slider.

        Returns:
            None

        Raises:
            ValueError: If the number of bind values does not match the number of placeholders in the SQL query.
            Exception: If there is an error during data insertion.

        """
        sql: str = f"""INSERT INTO mental_mental_table(
                    mental_mental_date,
                    mental_mental_time,
                    mood_slider,
                    mania_slider,
                    depression_slider,
                    mixed_risk_slider) VALUES (?, ?, ?, ?, ?, ?)"""
        
        bind_values: List[Union[str, int]] = [mental_mental_date, mental_mental_time,
                                              mood_slider, mania_slider, depression_slider,
                                              mixed_risk_slider]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: mental_mental_table Expected {sql.count('?')}
                                bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: mental_mental_table - {self.query.lastError().text()}")
        except ValueError as e:
            logger.error(f"ValueError mental_mental_table: {e}")
        except Exception as e:
            logger.error(f"Error during data insertion: mental_mental_table {e}", exc_info=True)
    
    def setup_into_cspr_exam(self) -> None:
        if not self.query.exec(f"""
                                    CREATE TABLE IF NOT EXISTS cspr_table (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    cspr_date TEXT,
                                    cspr_time TEXT,
                                    calm_slider INTEGER,
                                    stress_slider INTEGER,
                                    pain_slider INTEGER,
                                    rage_slider INTEGER
                                    )"""):
            logger.error(f"Error creating table: cspr_table",
                         self.query.lastError().text())
    
    def insert_into_cspr_exam(self,
                              cspr_date: str,
                              cspr_time: str,
                              calm_slider: int,
                              stress_slider: int,
                              pain_slider: int,
                              rage_slider: int
                              ) -> None:
        
        sql: str = f"""INSERT INTO cspr_table(
                    cspr_date,
                    cspr_time,
                    calm_slider,
                    stress_slider,
                    pain_slider,
                    rage_slider) VALUES (?, ?, ?, ?, ?, ?)"""
        
        bind_values: List[Union[str, int]] = [cspr_date, cspr_time,
                                              calm_slider, stress_slider, pain_slider, rage_slider]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: cspr_table Expected {sql.count('?')}
                                bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: cspr_table - {self.query.lastError().text()}")
        except ValueError as e:
            logger.error(f"ValueError cspr_table: {e}")
        except Exception as e:
            logger.error(f"Error during data insertion: cspr_table {e}", exc_info=True)
    
    def setup_wefe_table(self) -> None:
        if not self.query.exec(f"""
                                CREATE TABLE IF NOT EXISTS wefe_table (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                wefe_date TEXT,
                                wefe_time TEXT,
                                wellbeing_slider INTEGER,
                                excite_slider INTEGER,
                                focus_slider INTEGER,
                                energy_slider INTEGER,
                                summing_box INTEGER
                                )"""):
            logger.error(f"Error creating table: wefe_table",
                         self.query.lastError().text())
    
    def insert_into_wefe_table(self,
                               wefe_date: str,
                               wefe_time: str,
                               wellbeing_slider: int,
                               excite_slider: int,
                               focus_slider: int,
                               energy_slider: int,
                               summing_box: int
                               ) -> None:
        
        sql: str = f"""INSERT INTO wefe_table(
                wefe_date,
                wefe_time,
                wellbeing_slider,
                excite_slider,
                focus_slider,
                energy_slider,
                summing_box) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        
        bind_values: List[Union[str, int]] = [wefe_date,
                                              wefe_time,
                                              wellbeing_slider,
                                              excite_slider,
                                              focus_slider,
                                              energy_slider,
                                              summing_box]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: wefe_table Expected {sql.count('?')}
                            bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: wefe_table - {self.query.lastError().text()}")
        except ValueError as e:
            logger.error(f"ValueError wefe_table: {e}")
        except Exception as e:
            logger.error(f"Error during data insertion: wefe_table {e}", exc_info=True)
    
    def setup_diet_table(self):
        if not self.query.exec(f"""
                        CREATE TABLE IF NOT EXISTS diet_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        diet_date TEXT,
                        diet_time TEXT,
                        food_eaten TEXT,
                        calories INTEGER
                        )"""):
            logger.error(f"Error creating table: diet_table", self.query.lastError().text())
    
    def insert_into_diet_table(self,
                               diet_date,
                               diet_time,
                               food_eaten,
                               calories):
        
        sql = f"""INSERT INTO diet_table(diet_date, diet_time, food_eaten, calories) VALUES
                (?, ?, ?, ?)"""
        
        bind_values = [diet_date, diet_time, food_eaten, calories]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"Mismatch: diet_table Expected {sql.count('?')} bind values, got "
                                 f"{len(bind_values)}.")
            if not self.query.exec():
                logger.error(f"Error inserting data: diet_table - {self.query.lastError().text()}")
        except ValueError as ve:
            logger.error(f"ValueError diet_table: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during data insertion: diet_table", str(e))
    
    def setup_hydration_table(self):
        if not self.query.exec(f"""
                        CREATE TABLE IF NOT EXISTS hydration_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        diet_date TEXT,
                        diet_time TEXT,
                        hydration INTEGER
                        )"""):
            logger.error(f"Error creating table: hydration_table", self.query.lastError().text())
        
        # database_manager.py
    
    def insert_into_hydration_table(self,
                                    diet_date,
                                    diet_time,
                                    hydration):
        sql = """INSERT INTO hydration_table(diet_date, diet_time, hydration) VALUES (?, ?, ?)"""
        
        bind_values = [diet_date, diet_time, hydration]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"Mismatch: hydration_table Expected {sql.count('?')} bind values, got {len(bind_values)}.")
            if not self.query.exec():
                logger.error(f"Error inserting data: hydration_table - {self.query.lastError().text()}")
        except ValueError as ve:
            logger.error(f"ValueError hydration_table: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during data insertion: hydration_table", str(e))
        
        # -:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-
        # SLEEP table
        # -:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-
    
    def setup_shower(self) -> None:
        if not self.query.exec(f"""
                                CREATE TABLE IF NOT EXISTS shower_table (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                basics_date TEXT,
                                basics_time TEXT,
                                shower_check BOOL
                                )"""):
            logger.error(f"Error creating table: shower_table", self.query.lastError().text())
    
    def insert_into_shower_table(self,
                                 basics_date: str,
                                 basics_time: str,
                                 shower_check: int) -> None:
        
        sql: str = f"""INSERT INTO shower_table(basics_date, basics_time,
                shower_check) VALUES (?, ?, ?)"""
        
        bind_values: List[Union[str, bool]] = [basics_date, basics_time,
                                               shower_check]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: shower_table Expected {sql.count('?')}
                            bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: shower_table - {self.query.lastError().text()}")
        except ValueError as e:
            logger.error(f"ValueError shower_table: {e}")
        except Exception as e:
            logger.error(f"Error during data insertion: shower_table {e}", exc_info=True)
    
    def setup_exercise(self) -> None:
        if not self.query.exec(f"""
                                CREATE TABLE IF NOT EXISTS exercise_table (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                basics_date TEXT,
                                basics_time TEXT,
                                exerc_check BOOL
                                )"""):
            logger.error(f"Error creating table: exercise_table", self.query.lastError().text())
    
    def insert_into_exercise_table(self,
                                   basics_date: str,
                                   basics_time: str,
                                   exerc_check: int) -> None:
        
        sql: str = f"""INSERT INTO exercise_table(basics_date, basics_time,
                exerc_check) VALUES (?, ?, ?)"""
        
        bind_values: List[Union[str, bool]] = [basics_date, basics_time,
                                               exerc_check]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: exercise_table Expected {sql.count('?')}
                            bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: exercise_table - {self.query.lastError().text()}")
        except ValueError as e:
            logger.error(f"ValueError exercise_table: {e}")
        except Exception as e:
            logger.error(f"Error during data insertion: exercise_table {e}", exc_info=True)
        
        # Teethbrushing Table
    
    def setup_teethbrush(self) -> None:
        if not self.query.exec(f"""
                                CREATE TABLE IF NOT EXISTS tooth_table (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                basics_date TEXT,
                                basics_time TEXT,
                                tooth_check BOOL
                                )"""):
            logger.error(f"Error creating table: tooth_table", self.query.lastError().text())
    
    def insert_into_tooth_table(self,
                                basics_date: str,
                                basics_time: str,
                                tooth_check: int) -> None:
        
        sql: str = f"""INSERT INTO tooth_table(basics_date, basics_time,
                tooth_check) VALUES (?, ?, ?)"""
        
        bind_values: List[Union[str, bool]] = [basics_date, basics_time,
                                               tooth_check]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: tooth_table Expected {sql.count('?')}
                            bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: tooth_table - {self.query.lastError().text()}")
        except ValueError as e:
            logger.error(f"ValueError tooth_table: {e}")
        except Exception as e:
            logger.error(f"Error during data insertion: tooth_table {e}", exc_info=True)
    
    # SLEEP TIMES TABLE 
    def setup_sleep_table(self):
        if not self.query.exec(f"""
                CREATE TABLE IF NOT EXISTS sleep_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sleep_date TEXT,
                time_asleep TEXT,
                time_awake TEXT
                )"""):
            logger.error(f"Error creating table: sleep_table", self.query.lastError().text())
    
    def insert_into_sleep_table(self,
                                sleep_date,
                                time_asleep,
                                time_awake):
        sql = f"""INSERT INTO sleep_table(sleep_date, time_asleep, time_awake) VALUES (?, ?, ?)"""
        bind_values = [sleep_date, time_asleep, time_awake]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(
                    f"Mismatch: sleep_table Expected {sql.count('?')} bind values, got "
                    f"{len(bind_values)}.")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: sleep_table - {self.query.lastError().text()}")
        except ValueError as ve:
            logger.error(f"ValueError sleep_table: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during data insertion: sleep_table", str(e))
    
    # -:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-
    # BASICS table
    # -:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-
    def setup_total_hours_slept_table(self):
        if not self.query.exec(f"""
                CREATE TABLE IF NOT EXISTS total_hours_slept_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                sleep_date TEXT,
                total_hours_slept TEXT                                
                )"""):
            logger.error(f"Error creating table: total_hours_slept", self.query.lastError().text())
    
    def insert_into_total_hours_slept_table(self,
                                            sleep_date,
                                            total_hours_slept):
        # Prepare the SQL statement
        sql = f"""INSERT INTO total_hours_slept_table(sleep_date, total_hours_slept) VALUES (?, ?)"""
        bind_values = [sleep_date, total_hours_slept]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(
                    f"Mismatch: total_hours_slept Expected {sql.count('?')} bind values, got "
                    f"{len(bind_values)}.")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: total_hours_slept - {self.query.lastError().text()}")
        except ValueError as ve:
            logger.error(f"ValueError total_hours_slept: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during data insertion: total_hours_slept", str(e))
    
    def setup_woke_up_like_table(self):
        if not self.query.exec(f"""
                CREATE TABLE IF NOT EXISTS woke_up_like_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sleep_date TEXT,
                woke_up_like TEXT
                )"""):
            logger.error(f"Error creating table: woke_up_like", self.query.lastError().text())
    
    def insert_woke_up_like_table(self,
                                  sleep_date,
                                  woke_up_like):
        # Prepare the SQL statement
        sql = f"""INSERT INTO woke_up_like_table(sleep_date, woke_up_like) VALUES (?, ?)"""
        bind_values = [sleep_date, woke_up_like]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(
                    f"Mismatch: woke_up_like Expected {sql.count('?')} bind values, got "
                    f"{len(bind_values)}.")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: woke_up_like - {self.query.lastError().text()}")
        except ValueError as ve:
            logger.error(f"ValueError woke_up_like: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during data insertion: woke_up_like", str(e))
    
    def setup_sleep_quality_table(self):
        if not self.query.exec(f"""
                CREATE TABLE IF NOT EXISTS sleep_quality_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sleep_date TEXT,
                sleep_quality TEXT
                )"""):
            logger.error(f"Error creating table: sleep_quality", self.query.lastError().text())
    
    def insert_into_sleep_quality_table(self,
                                        sleep_date,
                                        sleep_quality):
        # Prepare the SQL statement
        sql = f"""INSERT INTO sleep_quality_table(sleep_date, sleep_quality) VALUES (?, ?)"""
        bind_values = [sleep_date, sleep_quality]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(
                    f"Mismatch: sleep_quality Expected {sql.count('?')} bind values, got "
                    f"{len(bind_values)}.")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: sleep_quality - {self.query.lastError().text()}")
        except ValueError as ve:
            logger.error(f"ValueError sleep_quality: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during data insertion: sleep_quality", str(e))


def close_database(self):
    try:
        logger.info("if database is open")
        if self.db.isOpen():
            logger.info("the database is closed successfully")
            self.db.close()
    except Exception as e:
        logger.exception(f"Error closing database: {e}")
