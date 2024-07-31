import datetime
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate, QSettings, QTime, Qt, QByteArray, QDateTime
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication, QTextEdit, QPushButton, QDialog, QFormLayout, QLineEdit
from PyQt6.QtPrintSupport import QPrintDialog

import tracker_config as tkc

#############################################################################
# UI
from ui.main_ui.gui import Ui_MainWindow

#############################################################################
# LOGGER
#############################################################################
from logger_setup import logger

#############################################################################
# NAVIGATION
#############################################################################
from navigation.master_navigation import change_mainStack
#############################################################################
# UTILITY
#############################################################################
from utility.app_operations.diet_calc import (
    calculate_calories)
from utility.app_operations.save_generic import (
    TextEditSaver)
from utility.widgets_set_widgets.slider_spinbox_connections import (
    connect_slider_spinbox)

# Window geometry and frame
from utility.app_operations.frameless_window import (
    FramelessWindow)
from utility.app_operations.window_controls import (
    WindowController)
from utility.app_operations.current_date_highlighter import (
    DateHighlighter)
from utility.widgets_set_widgets.line_connections import (
    line_edit_times)

from utility.widgets_set_widgets.slider_timers import (
    connect_slider_timeedits)
from utility.widgets_set_widgets.buttons_set_time import (
    btn_times)

from utility.app_operations.show_hide import (
    toggle_views)

from utility.widgets_set_widgets.buttons_set_time import (
    btn_times)
from database.add_data.teethbrushing import (
    add_teethbrush_data)
from database.add_data.exercise import (
    add_exercise_data)
from database.add_data.shower import (
    add_shower_data)

##############################################################################
# DATABASE Magicks w/ Wizardry & Necromancy
##############################################################################
# Database connections
from database.database_manager import (
    DataManager)

# Delete Records
from database.database_utility.delete_records import (
    delete_selected_rows)

# setup Models
from database.database_utility.model_setup import (
    create_and_set_model)
# Add personal diet
from database.add_data.diet import add_diet_data
from database.add_data.hydration import add_hydration_data
# Basics add sleep and basics
from database.add_data.woke_up_like_data import add_woke_up_like_data
from database.add_data.total_hours_slept import add_total_hours_slept_data
from database.add_data.sleep_data import add_sleep_data
from database.add_data.sleep_quality_data import add_sleep_quality_data
from database.add_data.wefe_add_data import add_wefe_data
from database.add_data.mental_mental import add_mentalsolo_data
from database.add_data.cspr import add_cspr_data
from database.add_data.time_in_room import add_time_in_room_data
from database.add_data.mood import add_lily_mood_data
from database.add_data.lily_diet import add_lily_diet_data
from database.add_data.walks import add_lily_walk_data
from database.add_data.lily_notes import add_lily_note_data
from database.add_data.walk_notes import add_lily_walk_notes


class MainWindow(FramelessWindow, QtWidgets.QMainWindow, Ui_MainWindow):
    """
    The main window of the application.

    This class represents the main window of the application. It inherits from FramelessWindow,
    QtWidgets.QMainWindow, and Ui_MainWindow. It contains various models, setup functions,
    and operations related to the application.

    Attributes:
    - exercise_model: The exercise model.
    - tooth_model: The tooth model.
    - shower_model: The shower model.
    - hydro_model: The hydro model.
    - diet_model: The diet model.
    - lily_walk_note_model: The lily walk note model.
    - lily_note_model: The lily note model.
    - lily_room_model: The lily room model.
    - lily_walk_model: The lily walk model.
    - lily_mood_model: The lily mood model.
    - lily_diet_model: The lily diet model.
    - mental_mental_model: The mental mental model.
    - cspr_model: The cspr model.
    - wefe_model: The wefe model.
    - btn_times: The button times.
    - sleep_quality_model: The sleep quality model.
    - woke_up_like_model: The woke up like model.
    - sleep_model: The sleep model.
    - total_hours_slept_model: The total hours slept model.
    - total_hrs_slept: The total hours slept.
    - basics_model: The basics model.
    - ui: The UI object.
    - db_manager: The database manager.
    - settings: The QSettings object.
    - window_controller: The WindowController object.

    Methods:
    - __init__: Initializes the MainWindow object.
    - commits_setup: Sets up the commits.
    - slider_set_spinbox: Connects sliders to spinboxes.
    - update_time: Updates the time displayed on the time_label widget.
    - update_beck_summary: Updates the averages of the sliders in the wellbeing and pain module.
    - init_hydration_tracker: Initializes the hydration tracker buttons.
    - switch_bds_page: Switches to the bds page.
    - switch_sleep_data_page: Switches to the sleep data page.
    - switch_to_diet_data_page: Switches to the diet data page.
    - switch_to_basics_data_page: Switches to the basics data page.
    - switch_to_mmdm_measures: Switches to the mmdm measures page.
    - switch_to_wefe_measures: Switches to the wefe measures page.
    - cspr_measures: Switches to the cspr measures page.
    - mmwefecspr_datapage: Switches to the mmwefecspr datapage.
    - switch_lilys_mod: Switches to the lilys mod page.
    - switch_to_lilys_dataviews: Switches to the lilys dataviews page.
    - auto_date_setters: Automatically sets the date for various widgets.
    - auto_time_setters: Automatically sets the time for various widgets.
    - app_operations: Performs various operations related to the application.
    """
    def __init__(self,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.exercise_model = None
        self.tooth_model = None
        self.shower_model = None
        self.hydro_model = None
        self.diet_model = None
        self.lily_walk_note_model = None
        self.lily_note_model = None
        self.lily_room_model = None
        self.lily_walk_model = None
        self.lily_mood_model = None
        self.lily_diet_model = None
        self.mental_mental_model = None
        self.cspr_model = None
        self.wefe_model = None
        self.btn_times = None
        self.sleep_quality_model = None
        self.woke_up_like_model = None
        self.sleep_model = None
        self.total_hours_slept_model = None
        self.total_hrs_slept = None
        self.basics_model = None
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        # Database init
        self.db_manager = DataManager()
        self.setup_models()
        # QSettings settings_manager setup
        self.settings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)
        self.window_controller = WindowController()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.restore_state()
        self.app_operations()
        self.auto_date_setters()
        self.calculate_total_hours_slept()
        self.stack_navigation()
        self.delete_actions()
        self.switch_page_view_setup()
        self.init_hydration_tracker()
        self.commits_setup()
        self.update_beck_summary()
        
        self.summing_box.setEnabled(False)
        for slider in [self.wellbeing_slider, self.excite_slider, self.focus_slider,
                       self.energy_slider]:
            slider.setRange(0, 10)
        
        self.wellbeing_slider.valueChanged.connect(self.update_beck_summary)
        self.excite_slider.valueChanged.connect(self.update_beck_summary)
        self.focus_slider.valueChanged.connect(self.update_beck_summary)
        self.energy_slider.valueChanged.connect(self.update_beck_summary)
    
    def commits_setup(self):
        """
        Sets up the commits for various activities.

        This method calls several other methods to set up commits for different activities,
        such as sleep, total hours, woke up like, sleep quality, diet data, shower, exercise,
        teethbrush, lily diet data, lily mood data, lily walk, lily in room, lily notes data,
        lily walk notes data, mental mental table, cspr, wefe, and slider set spinbox.
        """
        self.sleep_commit()
        self.total_hours_commit()
        self.woke_up_like_commit()
        self.sleep_quality_commit()
        self.diet_data_commit()
        self.shower_commit()
        self.exercise_commit()
        self.teethbrush_commit()
        self.lily_diet_data_commit()
        self.add_lily_mood_data()
        self.lily_walk_commit()
        self.lily_in_room_commit()
        self.add_lily_notes_data()
        self.add_lily_walk_notes_data()
        self.mental_mental_table_commit()
        self.cspr_commit()
        self.wefe_commit()
        self.slider_set_spinbox()
    
    # ////////////////////////////////////////////////////////////////////////////////////////
    # SLIDER UPDATES SPINBOX/VICE VERSA SETUP
    # ////////////////////////////////////////////////////////////////////////////////////////
    def slider_set_spinbox(self):
        """
        Connects sliders to their corresponding spinboxes.

        This method establishes a connection between sliders and spinboxes
        by mapping each slider to its corresponding spinbox. It then calls
        the `connect_slider_spinbox` function to establish the connection.

        Returns:
            None
        """
        connect_slider_to_spinbox = {
            self.wellbeing_slider: self.wellbeing_spinbox,
            self.excite_slider: self.excite_spinbox,
            self.focus_slider: self.focus_spinbox,
            self.energy_slider: self.energy_spinbox,
            self.mood_slider: self.mood,
            self.mania_slider: self.mania,
            self.depression_slider: self.depression,
            self.mixed_risk_slider: self.mixed_risk,
            self.calm_slider: self.calm_spinbox,
            self.stress_slider: self.stress_spinbox,
            self.rage_slider: self.rage_spinbox,
            self.pain_slider: self.pain_spinbox,
            self.lily_time_in_room_slider: self.lily_time_in_room,
            self.lily_mood_slider: self.lily_mood,
            self.lily_mood_activity_slider: self.lily_activity,
            self.lily_gait_slider: self.lily_gait,
            self.lily_behavior_slider: self.lily_behavior,
            self.lily_energy_slider: self.lily_energy,
            self.woke_up_like_slider: self.woke_up_like,
            self.sleep_quality_slider: self.sleep_quality,
        }
        
        for slider, spinbox in connect_slider_to_spinbox.items():
            connect_slider_spinbox(slider, spinbox)

    @staticmethod
    def update_time(state, time_label):
        """
        Update the time displayed on the time_label widget based on the given state.

        Parameters:
        state (int): The state of the time_label widget. If state is 2, the time will be updated.
        time_label (QLabel): The QLabel widget to display the time.

        Raises:
        Exception: If there is an error updating the time.

        Returns:
        None
        """
        try:
            if state == 2:  # checked state
                current_time = QTime.currentTime()
                time_label.setTime(current_time)
        except Exception as e:
            logger.error(f"Error updating time. {e}", exc_info=True)
    
    def update_beck_summary(self):
        """
        Updates the averages of the sliders in the wellbeing and pain module such that
        the overall is the average of the whole.

        :return: None
        """
        try:
            values = [slider.value() for slider in
                      [self.wellbeing_slider, self.excite_slider, self.focus_slider,
                       self.energy_slider] if
                      slider.value() > 0]

            s = sum(values)

            self.summing_box.setValue(int(s))

        except Exception as e:
            logger.error(f"{e}", exc_info=True)
    
    def init_hydration_tracker(self):
        """
        Initializes the hydration tracker buttons.

        This method connects the click events of the hydration tracker buttons
        to the `commit_hydration` method with the corresponding hydration amount.

        Raises:
            Exception: If there is an error initializing the hydration tracker buttons.

        """
        try:
            self.eight_ounce_cup.clicked.connect(lambda: self.commit_hydration(8))
            self.sixteen_ounce_cup.clicked.connect(lambda: self.commit_hydration(16))
            self.twenty_four_ounce_cup.clicked.connect(lambda: self.commit_hydration(24))
            self.thirty_two_ounce_cup.clicked.connect(lambda: self.commit_hydration(32))
        except Exception as e:
            logger.error(f"Error initializing hydration tracker buttons: {e}", exc_info=True)
    
    def switch_bds_page(self):
        """
        Switches the current widget to the BDS page and resizes the window to 300x300 pixels.

        This method sets the current widget of the mainStack to the BDS page widget and resizes the window
        to a fixed size of 300x300 pixels.

        Parameters:
        None

        Returns:
        None
        """
        self.mainStack.setCurrentWidget(self.bds_page)
        self.resize(300, 300)
        self.setFixedSize(300, 300)
    
    def switch_sleep_data_page(self):
        """
        Switches to the sleep data page and adjusts the window size.

        This method sets the current widget of the mainStack to the sleep_data_page,
        and resizes the window to a fixed size of 540x540.

        Parameters:
            None

        Returns:
            None
        """
        self.mainStack.setCurrentWidget(self.sleep_data_page)
        self.resize(540, 540)
        self.setFixedSize(540, 540)
    
    def switch_to_diet_data_page(self):
        """
        Switches to the diet data page and adjusts the window size.

        This method sets the current widget of the mainStack to the diet_data_page,
        and resizes the window to a width of 800 pixels and a height of 540 pixels.

        Parameters:
        None

        Returns:
        None
        """
        self.mainStack.setCurrentWidget(self.diet_data_page)
        self.resize(800, 540)
        self.setFixedSize(800, 540)
    
    def switch_to_basics_data_page(self):
        """
        Switches the current widget to the basics data page and sets the window size to 540x540.

        This method sets the current widget of the mainStack to the basics_data_page, which is responsible for displaying
        the basics data. It also resizes the window to a fixed size of 540x540.

        Parameters:
            None

        Returns:
            None
        """
        self.mainStack.setCurrentWidget(self.basics_data_page)
        self.resize(540, 540)
        self.setFixedSize(540, 540)
    
    def switch_to_mmdm_measures(self):
        """
        Switches the current widget to the 'mmdm_measures' widget and resizes the window.

        This method sets the current widget of the mainStack to the 'mmdm_measures' widget,
        and resizes the window to a width of 175 and height of 270. It also sets the window
        size to a fixed size of 175x270.

        Parameters:
            None

        Returns:
            None
        """
        self.mainStack.setCurrentWidget(self.mmdm_measures)
        self.resize(175, 270)
        self.setFixedSize(175, 270)
    
    def switch_to_wefe_measures(self):
        """
        Switches the current widget to the WEFE measurements widget and adjusts the window size.

        This method sets the current widget of the `mainStack` to the `wefe_measurements` widget.
        It also resizes the window to a width of 175 pixels and a height of 270 pixels, and fixes the window size to these dimensions.

        Parameters:
            None

        Returns:
            None
        """
        self.mainStack.setCurrentWidget(self.wefe_measurements)
        self.resize(175, 270)
        self.setFixedSize(175, 270)
    
    def cspr_measures(self):
        """
        Switches the current widget to cspr_measurements and adjusts the window size.

        This method sets the current widget of the mainStack to cspr_measurements,
        and resizes the window to a width of 175 and height of 270. It also fixes
        the window size to prevent further resizing.

        Parameters:
            None

        Returns:
            None
        """
        self.mainStack.setCurrentWidget(self.cspr_measurements)
        self.resize(175, 270)
        self.setFixedSize(175, 270)
    
    def mmwefecspr_datapage(self):
        """
        Switches the current widget to the mmwefecspr_dataviews widget and sets the window size to 800x460.

        This method is responsible for displaying the data page in the main window.

        Parameters:
            None

        Returns:
            None
        """
        self.mainStack.setCurrentWidget(self.mmwefecspr_dataviews)
        self.resize(800, 460)
        self.setFixedSize(800, 460)
    
    def switch_lilys_mod(self):
        """
        Switches the current widget to the 'lilys_mod' widget and adjusts the window size.

        This method sets the current widget of the mainStack to the 'lilys_mod' widget and resizes the window
        to a width of 250 pixels and a height of 314 pixels. The window size is then fixed to prevent further resizing.

        Parameters:
            None

        Returns:
            None
        """
        self.mainStack.setCurrentWidget(self.lilys_mod)
        self.resize(250, 314)
        self.setFixedSize(250, 314)
    
    def switch_to_lilys_dataviews(self):
        """
        Switches to the Lily's DataViews widget and adjusts the window size.

        This method sets the current widget of the mainStack to the Lily's DataViews widget,
        and resizes the window to a width of 800 pixels and a height of 456 pixels.

        Parameters:
        None

        Returns:
        None
        """
        self.mainStack.setCurrentWidget(self.lilys_dataviews)
        self.resize(800, 456)
        self.setFixedSize(800, 456)
    
    def auto_date_setters(self) -> None:
        """
        Sets the date for various widgets to the current date.

        This method sets the date for the following widgets to the current date:
        - diet_date
        - sleep_date
        - basics_date
        - mental_mental_date
        - wefe_date
        - cspr_date
        - lily_date

        If any exception occurs during the process, it will be logged with the error message.

        Returns:
            None
        """
        try:
            self.diet_date.setDate(QDate.currentDate())
            self.sleep_date.setDate(QDate.currentDate())
            self.basics_date.setDate(QDate.currentDate())
            self.mental_mental_date.setDate(QDate.currentDate())
            self.wefe_date.setDate(QDate.currentDate())
            self.cspr_date.setDate(QDate.currentDate())
            self.lily_date.setDate(QDate.currentDate())
        except Exception as e:
            logger.error(f"Probs with auto dates, {e}", exc_info=True)
    
    def auto_time_setters(self) -> None:
        """
        Sets the time for various components in the UI to the current system time.

        This method sets the time for the following components to the current system time:
        - diet_time
        - sleep_time
        - mental_mental_time
        - basics_time
        - wefe_time
        - cspr_time
        - lily_time

        If any exception occurs during the process, it will be logged with the appropriate error message.

        Returns:
            None
        """
        try:
            self.diet_time.setTime(QTime.currentTime())
            self.sleep_time.setTime(QTime.currentTime())
            self.mental_mental_time.setTime(QTime.currentTime())
            self.basics_time.setTime(QTime.currentTime())
            self.wefe_time.setTime(QTime.currentTime())
            self.cspr_time.setTime(QTime.currentTime())
            self.lily_time.setTime(QTime.currentTime())
        except Exception as e:
            logger.error(f"Probs with auto time, {e}", exc_info=True)
    
    ##########################################################################################
    # APP-OPERATIONS setup
    ##########################################################################################
    def app_operations(self):
        """
        Performs the necessary operations for setting up the application.

        This method connects the currentChanged signal of the mainStack to the on_page_changed slot,
        hides the check frame, connects the triggered signal of the actionTotalHours to the
        calculate_total_hours_slept slot, and sets the current index of the mainStack based on the
        last saved index.

        Raises:
            Exception: If an error occurs while setting up the app_operations.

        """
        try:
            self.mainStack.currentChanged.connect(self.on_page_changed)
            self.hide_check_frame.setVisible(False)
            self.actionTotalHours.triggered.connect(self.calculate_total_hours_slept)
            last_index = self.settings.value("lastPageIndex", 0, type=int)
            self.mainStack.setCurrentIndex(last_index)
        except Exception as e:
            logger.error(f"Error occurred while setting up app_operations : {e}", exc_info=True)
    
    def commits_set_times(self):
        """
        Sets the times for various buttons in the UI.

        The times are stored in a dictionary where the keys are the buttons and the values are the corresponding times.
        The buttons and times are connected using the `btn_times` dictionary.

        Example:
            self.btn_times = {
                self.shower_c: self.basics_time,
                self.exercise_commit: self.basics_time,
                self.teethbrush_commit: self.basics_time,
            }

        The lineEdits are then connected to the centralized function `btn_times` using a for loop.

        Args:
            None

        Returns:
            None
        """
        self.btn_times = {
            self.shower_c: self.basics_time,
            self.exercise_commit: self.basics_time,
            self.teethbrush_commit: self.basics_time,
        }
        
        # Connect lineEdits to the centralized function
        for app_btns, times_edit in self.btn_times.items():
            btn_times(app_btns, times_edit)
    
    def on_page_changed(self, index):
        """
        Callback method triggered when the page is changed in the UI.

        Args:
            index (int): The index of the new page.
        """
        self.settings.setValue("lastPageIndex", index)
    
    def calculate_total_hours_slept(self) -> None:
        """
        Calculates the total hours slept based on the awake time and asleep time.

        This method calculates the total hours slept by subtracting the awake time from the
        asleep time.
        If the time spans past midnight, it adds 24 hours worth of minutes to the total.
        The result is then converted to hours and minutes and displayed in the
        total_hours_slept_lineedit.

        Raises:
            Exception: If an error occurs while calculating the total hours slept.

        """
        
        try:
            time_asleep = self.time_awake.time()
            time_awake = self.time_asleep.time()
            
            # Convert time to total minutes since the start of the day
            minutes_asleep = (time_asleep.hour() * 60 + time_asleep.minute())
            minutes_awake = (time_awake.hour() * 60 + time_awake.minute())
            
            # Calculate the difference in minutes
            total_minutes = minutes_asleep - minutes_awake
            
            # Handle case where the time spans past midnight
            if total_minutes < 0:
                total_minutes += (24 * 60)  # Add 24 hours worth of minutes
            
            # Convert back to hours and minutes
            hours = total_minutes // 60
            minutes = total_minutes % 60
            
            # Create the total_hours_slept string in HH:mm format
            self.total_hrs_slept = f"{hours:02}:{minutes:02}"
            
            # Update the lineEdit with the total hours slept
            self.total_hours_slept.setText(self.total_hrs_slept)
        
        except Exception as e:
            logger.error(f"Error occurred while calculating total hours slept {e}", exc_info=True)
    
    #############################################################################################
    # Agenda Journal Navigation
    #############################################################################################
    def stack_navigation(self):
        """
        Handles the stack navigation for the main window.

        This method maps actions and buttons to stack page indices for the agenda journal.
        It connects the actions to the corresponding pages in the stack.

        Raises:
            Exception: If an error occurs during the stack navigation.

        """
        try:
            # Mapping actions and buttons to stack page indices for the agenda journal
            mainStackNavvy = {
                self.actionBDSInput: 0, self.actionSleepDataView: 1,
                self.actionDietDataView: 2, self.actionBasicsDataView: 3,
                self.actionMMDMView: 4, self.actionWEFEView: 5,
                self.actionCSPRView: 6, self.actionExamDataViews: 7,
                self.actionLilysPage: 8, self.actionLilyDataView: 9,
            }
            
            # Main Stack Navigation
            for action, page in mainStackNavvy.items():
                action.triggered.connect(
                    lambda _, p=page: change_mainStack(self.mainStack, p))
        
        except Exception as e:
            logger.error(f"An error has occurred: {e}", exc_info=True)
    
    def switch_page_view_setup(self):
        """
        Connects the various actions to their corresponding methods for switching pages/views.

        This method sets up the connections between the menu actions and the methods that handle
        switching to different pages/views in the application.

        """
        self.actionBDSInput.triggered.connect(self.switch_bds_page)
        self.actionSleepDataView.triggered.connect(self.switch_sleep_data_page)
        self.actionDietDataView.triggered.connect(self.switch_to_diet_data_page)
        self.actionBasicsDataView.triggered.connect(self.switch_to_basics_data_page)
        self.actionMMDMView.triggered.connect(self.switch_to_mmdm_measures)
        self.actionWEFEView.triggered.connect(self.switch_to_wefe_measures)
        self.actionCSPRView.triggered.connect(self.cspr_measures)
        self.actionExamDataViews.triggered.connect(self.mmwefecspr_datapage)
        self.actionLilysPage.triggered.connect(self.switch_lilys_mod)
        self.actionLilyDataView.triggered.connect(self.switch_to_lilys_dataviews)
    
    def mental_mental_table_commit(self) -> None:
        """
        Connects the 'commit' action to the 'add_mentalsolo_data' function and inserts data into the mental_mental_table.

        This method connects the 'commit' action to the 'add_mentalsolo_data' function, which is responsible for inserting data into the mental_mental_table. It sets up the connection using the `triggered.connect()` method and passes the necessary data to the `add_mentalsolo_data` function.

        Raises:
            Exception: If an error occurs during the process.
        """
        try:
            self.actionCommitMMDM.triggered.connect(
                lambda: add_mentalsolo_data(
                    self, {
                        "mental_mental_date": "mental_mental_date",
                        "mental_mental_time": "mental_mental_time",
                        "mood_slider": "mood_slider",
                        "mania_slider": "mania_slider",
                        "depression_slider": "depression_slider",
                        "mixed_risk_slider": "mixed_risk_slider",
                        "model": "mental_mental_model"
                    },
                    self.db_manager.insert_into_mental_mental_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def cspr_commit(self) -> None:
        """
        Connects the 'Commit CSPR' action to the 'add_cspr_data' function and inserts the CSPR exam data into the database.

        Raises:
            Exception: If an error occurs during the execution of the method.
        """
        try:
            self.actionCommitCSPR.triggered.connect(
                lambda: add_cspr_data(
                    self, {
                        "cspr_date": "cspr_date",
                        "cspr_time": "cspr_time",
                        "calm_slider": "calm_slider",
                        "stress_slider": "stress_slider",
                        "pain_slider": "pain_slider",
                        "rage_slider": "rage_slider",
                        "model": "cspr_model"
                    },
                    self.db_manager.insert_into_cspr_exam, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def wefe_commit(self) -> None:
        """
        Connects the actionCommitWEFE signal to the add_wefe_data function with the specified parameters.
        Inserts the WEFE data into the WEFE table using the db_manager.

        Raises:
            Exception: If an error occurs during the execution of the method.
        """
        try:
            self.actionCommitWEFE.triggered.connect(
                lambda: add_wefe_data(
                    self, {
                        "wefe_date": "wefe_date",
                        "wefe_time": "wefe_time",
                        "wellbeing_slider": "wellbeing_slider",
                        "excite_slider": "excite_slider",
                        "focus_slider": "focus_slider",
                        "energy_slider": "energy_slider",
                        "summing_box": "summing_box",
                        "model": "wefe_model"
                    },
                    self.db_manager.insert_into_wefe_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    # SLEEP COMMIT
    #######################################################################################
    def sleep_commit(self):
        """
        Connects the 'Commit Sleep' action to the 'add_sleep_data' function and inserts the sleep data into the sleep table.

        Raises:
            Exception: If an error occurs during the connection or insertion process.
        """
        try:
            self.actionCommitSleep.triggered.connect(lambda: add_sleep_data(self, {
                "sleep_date": "sleep_date", "time_asleep": "time_asleep", "time_awake":
                    "time_awake", "model": "sleep_model",
            },
                                                                            self.db_manager.insert_into_sleep_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def total_hours_commit(self):
        """
        Connects the 'CommitSleep' action to the 'add_total_hours_slept_data' function and inserts data into the 
        'total_hours_slept_table' in the database.

        Raises:
            Exception: If an error occurs during the execution of the method.

        """
        try:
            self.actionCommitSleep.triggered.connect(lambda: add_total_hours_slept_data(self, {
                "sleep_date": "sleep_date", "total_hours_slept": "total_hours_slept", "model":
                    "total_hours_slept_model",
            },
                                                                                        self.db_manager.insert_into_total_hours_slept_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def woke_up_like_commit(self):
        """
        Connects the 'Commit Sleep' action to the 'add_woke_up_like_data' function.

        This method connects the 'triggered' signal of the 'actionCommitSleep' QAction to the 'add_woke_up_like_data'
        function. It passes the necessary parameters to the function and inserts the data into the 'woke_up_like' table
        using the 'db_manager' object.

        Raises:
            Exception: If an error occurs during the connection or data insertion, an exception is raised.

        """
        try:
            self.actionCommitSleep.triggered.connect(lambda: add_woke_up_like_data(self, {
                "sleep_date": "sleep_date", "woke_up_like": "woke_up_like", "model": "woke_up_like_model",
            },
                                                                                   self.db_manager.insert_woke_up_like_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def sleep_quality_commit(self):
        """
        Connects the 'Commit Sleep' action to the 'add_sleep_quality_data' function and inserts the sleep quality data
        into the sleep quality table in the database.

        Raises:
            Exception: If an error occurs during the execution of the method.

        """
        try:
            self.actionCommitSleep.triggered.connect(lambda: add_sleep_quality_data(self, {
                "sleep_date": "sleep_date", "sleep_quality": "sleep_quality", "model":
                    "sleep_quality_model",
            },
                                                                                    self.db_manager.insert_into_sleep_quality_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    # MY DIET Commit Method
    #########################################################################
    def diet_data_commit(self):
        """
        Connects the 'Commit Diet' action to the 'add_diet_data' function and inserts the diet data into the database.

        Raises:
            Exception: If an error occurs during the process.

        """
        try:
            self.actionCommitDiet.triggered.connect(lambda: add_diet_data(self, {
                "diet_date": "diet_date", "diet_time": "diet_time", "food_eaten": "food_eaten",
                "calories": "calories", "model": "diet_model",
            }, self.db_manager.insert_into_diet_table, ))
        except Exception as e:
            logger.error(f"An error has occurred: {e}", exc_info=True)
    
    def commit_hydration(self, amount):
        """
        Commits the hydration data to the database.

        Args:
            amount (int): The amount of water in ounces.

        Raises:
            Exception: If an error occurs while committing the hydration data.

        Returns:
            None
        """
        try:
            date = QDate.currentDate().toString("yyyy-MM-dd")
            time = QTime.currentTime().toString("hh:mm:ss")
            self.db_manager.insert_into_hydration_table(date, time, amount)
            logger.info(f"Committed {amount} oz of water at {date} {time}")
            self.hydro_model.select()
        except Exception as e:
            logger.error(f"Error committing hydration data: {e}", exc_info=True)
    
    def shower_commit(self):
        """
        Connects the 'clicked' signal of the 'shower_c' button to the 'add_shower_data' function,
        passing the necessary parameters and calling the 'insert_into_shower_table' method of the 'db_manager' object.

        Raises:
            Exception: If an error occurs during the process.

        """
        try:
            self.shower_c.clicked.connect(lambda: add_shower_data(self, {
                "basics_date": "basics_date", "basics_time": "basics_time",
                "shower_check": "shower_check", "model": "shower_model",
            },
                                                                  self.db_manager.insert_into_shower_table, ))
        except Exception as e:
            logger.error(f"An error occurred: {e}", exc_info=True)
    
    def exercise_commit(self):
        """
        Connects the `yoga_commit` button to the `add_exercise_data` function with the specified arguments.

        This method is responsible for setting up the connection between the `yoga_commit` button and the `add_exercise_data` function.
        It passes the necessary arguments to the `add_exercise_data` function, which is responsible for inserting exercise data into the exercise table.

        Args:
            self: The instance of the class.

        Returns:
            None
        """
        self.yoga_commit.clicked.connect(lambda: add_exercise_data(self, {
            "basics_date": "basics_date", "basics_time": "basics_time",
            "exerc_check": "exerc_check", "model": "exercise_model",
        }, self.db_manager.insert_into_exercise_table, ))
    
    def teethbrush_commit(self):
        """
        Connects the `clicked` signal of the `teeth_commit` button to the `add_teethbrush_data` function.

        The `add_teethbrush_data` function is called with the following parameters:
        - `self`: The instance of the main window class.
        - A dictionary containing the data to be passed to the `add_teethbrush_data` function.
        - `self.db_manager.insert_into_tooth_table`: The method to be called when inserting data into the tooth table.

        This method is responsible for handling the commit action when the `teeth_commit` button is clicked.
        """
        self.teeth_commit.clicked.connect(lambda: add_teethbrush_data(self, {
            "basics_date": "basics_date", "basics_time": "basics_time",
            "tooth_check": "tooth_check", "model": "tooth_model",
        }, self.db_manager.insert_into_tooth_table, ))
    
    def lily_diet_data_commit(self):
        """
        Connects the `lily_ate_check` button click event to the `add_lily_diet_data` function.

        The `add_lily_diet_data` function is called with the following parameters:
        - `self`: The current instance of the class.
        - A dictionary containing the data to be passed to the `add_lily_diet_data` function:
            - "lily_date": The value of the "lily_date" attribute.
            - "lily_time": The value of the "lily_time" attribute.
            - "model": The value of the "lily_diet_model" attribute.
        - `self.db_manager.insert_into_lily_diet_table`: The function to be called when the button is clicked.

        Raises:
            Exception: If an error occurs during the execution of the method.

        """
        try:
            self.lily_ate_check.clicked.connect(lambda: add_lily_diet_data(self, {
                "lily_date": "lily_date", "lily_time": "lily_time",
                "model": "lily_diet_model",
            }, self.db_manager.insert_into_lily_diet_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_lily_mood_data(self):
        """
        Connects the 'commit_mood' action to the 'add_lily_mood_data' function and passes the necessary data to it.

        This method connects the 'commit_mood' action to the 'add_lily_mood_data' function, which is responsible for inserting
        Lily's mood data into the database. It sets up the necessary data and connects the action to the function using a lambda
        function. The lambda function passes the required data and the function to be called when the action is triggered.

        Parameters:
            self (MainWindow): The instance of the main window.

        Returns:
            None
        """
        try:
            self.actionCommitLilyMood.triggered.connect(lambda: add_lily_mood_data(self, {
                "lily_date": "lily_date",
                "lily_time": "lily_time",
                "lily_mood_slider": "lily_mood_slider",
                "lily_energy_slider": "lily_energy_slider",
                "lily_mood_activity_slider": "lily_mood_activity_slider",
                "model": "lily_mood_model",
            }, self.db_manager.insert_into_lily_mood_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_lily_notes_data(self):
        """
        Connects the 'commit_lily_notes' action to the 'add_lily_note_data' function.

        This method connects the 'commit_lily_notes' action to the 'add_lily_note_data' function,
        passing the necessary parameters. It handles any exceptions that occur and logs an error message.

        Parameters:
        - self: The instance of the main window.

        Returns:
        - None
        """
        try:
            self.lily_note_commit_btn.clicked.connect(lambda: add_lily_note_data(self, {
                "lily_date": "lily_date", "lily_time": "lily_time",
                "lily_notes": "lily_notes",
                "model": "lily_note_model",
            }, self.db_manager.insert_into_lily_notes_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def lily_walk_commit(self):
        """
        Connects the `lily_walk_btn` button to the `add_lily_walk_data` function with specified arguments.

        This method is responsible for setting up the connection between the `lily_walk_btn` button and the `add_lily_walk_data` function.
        It passes a dictionary of data and a callback function to the `add_lily_walk_data` function.

        Args:
            self: The instance of the class.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the connection setup.

        """
        try:
            self.lily_walk_btn.clicked.connect(lambda: add_lily_walk_data(self, {
                "lily_date": "lily_date", "lily_time": "lily_time",
                "lily_behavior_slider": "lily_behavior_slider",
                "lily_gait_slider": "lily_gait_slider",
                "model": "lily_walk_model"
            }, self.db_manager.insert_into_wiggles_walks_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def lily_in_room_commit(self):
        """
        Connects the 'commit_room_time' action to the 'add_time_in_room_data' function,
        passing the necessary parameters and inserting the data into the time in room table.

        Raises:
            Exception: If an error occurs during the commit process.

        """
        try:
            self.actionCommitLilysTimeInRoom.triggered.connect(lambda: add_time_in_room_data(self, {
                "lily_date": "lily_date", "lily_time": "lily_time", "lily_time_in_room_slider":
                    "lily_time_in_room_slider", "model": "lily_room_model"
            }, self.db_manager.insert_into_time_in_room_table))
        except Exception as e:
            logger.error(f"Error occurring during in_room commit main_window.py loc. {e}",
                         exc_info=True)
    
    def add_lily_walk_notes_data(self):
        """
        Connects the `lily_walk_btn` button to the `add_lily_walk_notes` function with specified arguments.

        This method sets up the connection between the `lily_walk_btn` button and the `add_lily_walk_notes` function.
        When the button is clicked, it calls the `add_lily_walk_notes` function with the provided arguments.

        Args:
            self: The instance of the main window class.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the connection setup.

        """
        try:
            self.lily_walk_note_commit_btn.clicked.connect(lambda: add_lily_walk_notes(self, {
                "lily_date": "lily_date", "lily_time": "lily_time",
                "lily_walk_note": "lily_walk_note", "model": "lily_walk_note_model"
            }, self.db_manager.insert_into_lily_walk_notes_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def delete_actions(self):
        """
        Connects the `actionDelete` trigger to multiple `delete_selected_rows` functions for different tables and models.
        """
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'wefe_tableview',
                    'wefe_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)    
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'cspr_tableview',
                    'cspr_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'mental_mental_table',
                    'mental_mental_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'sleep_tableview',
                    'sleep_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'total_hours_slept_tableview',
                    'total_hours_slept_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'woke_up_like_tableview',
                    'woke_up_like_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'sleep_quality_tableview',
                    'sleep_quality_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'shower_table',
                    'shower_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'teethbrushed_table',
                    'tooth_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'yoga_table',
                    'exercise_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'diet_table',
                    'diet_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'hydration_table',
                    'hydro_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'lily_walk_table',
                    'lily_walk_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'lily_diet_table',
                    'lily_diet_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'lily_mood_table',
                    'lily_mood_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'time_in_room_table',
                    'lily_room_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'lily_notes_table',
                    'lily_note_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'lily_walk_note_table',
                    'lily_walk_note_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
    
    def setup_models(self) -> None:
        """
        Set up models for various tables in the main window.

        This method creates and sets models for different tables in the main window.
        It uses the `create_and_set_model` function to create and set the models.

        Raises:
            Exception: If there is an error setting up the models.

        """
        try:
            self.wefe_model = create_and_set_model(
                "wefe_table",
                self.wefe_tableview
            )
            
            self.cspr_model = create_and_set_model(
                "cspr_table",
                self.cspr_tableview
            )
            
            self.mental_mental_model = create_and_set_model(
                "mental_mental_table",
                self.mental_mental_table
            )
            
            self.sleep_model = create_and_set_model(
                "sleep_table",
                self.sleep_tableview
            )
            
            self.total_hours_slept_model = create_and_set_model(
                "total_hours_slept_table",
                self.total_hours_slept_tableview
            )
            
            self.woke_up_like_model = create_and_set_model(
                "woke_up_like_table",
                self.woke_up_like_tableview)
            
            self.sleep_quality_model = create_and_set_model(
                "sleep_quality_table",
                self.sleep_quality_tableview)
            
            self.shower_model = create_and_set_model(
                "shower_table",
                self.shower_table
            )
            # SLEEP: model creates and set
            
            self.tooth_model = create_and_set_model(
                "tooth_table",
                self.teethbrushed_table
            )
            
            self.exercise_model = create_and_set_model(
                "exercise_table",
                self.yoga_table
            )
            
            self.diet_model = create_and_set_model(
                "diet_table",
                self.diet_table
            )
            
            self.hydro_model = create_and_set_model(
                "hydration_table",
                self.hydration_table
            )
            
            self.lily_diet_model = create_and_set_model(
                "lily_diet_table",
                self.lily_diet_table)
            
            self.lily_mood_model = create_and_set_model(
                "lily_mood_table",
                self.lily_mood_table)
            
            self.lily_walk_model = create_and_set_model(
                "lily_walk_table",
                self.lily_walk_table)
            
            self.lily_room_model = create_and_set_model(
                "lily_in_room_table",
                self.time_in_room_table)
            
            self.lily_note_model = create_and_set_model(
                "lily_notes_table",
                self.lily_notes_table)
            
            self.lily_walk_note_model = create_and_set_model(
                "lily_walk_notes_table",
                self.lily_walk_note_table)
        except Exception as e:
            logger.error(f"Error setting up models: {e}", exc_info=True)
    
    def save_state(self):
        """
        Saves the state of the main window.

        This method saves the values of various sliders, inputs, and other UI elements
        as well as the window geometry and state to the application settings.

        Raises:
            Exception: If there is an error while saving the state.

        """
        try:
            self.settings.setValue(
                'lily_time_in_room_slider',
                self.lily_time_in_room_slider.value())
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.settings.setValue(
                'lily_mood_slider',
                self.lily_mood_slider.value())
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.settings.setValue(
                'lily_mood_activity_slider',
                self.lily_mood_activity_slider.value())
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.settings.setValue('lily_energy_slider', self.lily_energy_slider.value())
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.settings.setValue('lily_time_in_room', self.lily_time_in_room.value())
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.settings.setValue('lily_mood', self.lily_mood.value())
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.settings.setValue('lily_activity', self.lily_activity.value())
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.settings.setValue('lily_energy', self.lily_energy.value())
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.settings.setValue('lily_notes', self.lily_notes.toHtml())
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.settings.setValue("geometry", self.saveGeometry())
        except Exception as e:
            logger.error(f"Geometry not good fail. {e}", exc_info=True)
        
        try:
            self.settings.setValue("windowState", self.saveState())
        except Exception as e:
            logger.error(f"Geometry not good fail. {e}", exc_info=True)
            
    def restore_state(self) -> None:
        """
        Restores the state of the main window by retrieving values from the settings.

        This method restores the values of various sliders, text fields, and window geometry
        from the settings. If an error occurs during the restoration process, it is logged
        with the corresponding exception.

        Returns:
            None
        """
        try:
            self.lily_time_in_room_slider.setValue(
                self.settings.value(
                    'lily_time_in_room_slider',
                    0,
                    type=int
                )
            )
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.lily_mood_slider.setValue(self.settings.value('lily_mood_slider', 0, type=int))
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.lily_mood_activity_slider.setValue(
                self.settings.value(
                    'lily_mood_activity_slider',
                    0,
                    type=int
                )
            )
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.lily_energy_slider.setValue(self.settings.value('lily_energy_slider', 0, type=int))
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.lily_time_in_room.setValue(self.settings.value('lily_time_in_room', 0, type=int))
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.lily_mood.setValue(self.settings.value('lily_mood', 0, type=int))
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.lily_activity.setValue(self.settings.value('lily_activity', 0, type=int))
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.lily_energy.setValue(self.settings.value('lily_energy', 0, type=int))
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            self.lily_notes.setHtml(self.settings.value('lily_notes', "", type=str))
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        
        try:
            # restore window geometry state
            self.restoreGeometry(self.settings.value("geometry", QByteArray()))
        except Exception as e:
            logger.error(f"Error restoring the minds module : stress state {e}")
        
        try:
            self.restoreState(self.settings.value("windowState", QByteArray()))
        except Exception as e:
            logger.error(f"Error restoring WINDOW STATE {e}", exc_info=True)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Event handler for the close event of the main window.

        This method is called when the user tries to close the main window.
        It saves the state of the application before closing.

        Args:
            event (QCloseEvent): The close event object.

        Returns:
            None
        """
        try:
            self.save_state()
        except Exception as e:
            logger.error(f"error saving state during closure: {e}", exc_info=True)
