from PySide6 import QtWidgets, QtCore, QtGui
from src.utils import (
    setup_combobox,
    employee_data_info_error,
    employee_data_info_success,
    criteria_export,
    show_empty_widget,
)
from src.components.customlabel import CustomLabel
import resources
from src.components.workerclass import Worker
from src.components.threadpool_manager import global_threadpool
from src.database.db import SessionLocal
from src.crud.crud_user import get_user, update_user
from src.components.logoutdialog import LogoutDialog
import os
from platformdirs import user_data_dir
from pathlib import Path
import shutil
from datetime import datetime


class AccountScreen(QtWidgets.QMainWindow):
    previous_screen = QtCore.Signal(object)
    display_splashscreen = QtCore.Signal(object)

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_account_screen()

    def setup_window(self):
        self.setWindowIcon(QtGui.QIcon(":/assets/icons/unitrack_icon"))
        self.setWindowTitle("UniTrack")
        self.setFixedSize(QtCore.QSize(950, 550))

    def setup_container(self):
        self.container_widget = QtWidgets.QWidget()
        self.container_widget.setContentsMargins(0, 0, 0, 0)

        self.container_layout = QtWidgets.QVBoxLayout(self.container_widget)
        self.container_layout.setContentsMargins(0, 10, 0, 0)

        self.setCentralWidget(self.container_widget)

    def setup_top_row(self):
        self.top_row_widget = QtWidgets.QWidget()
        self.top_row_widget.setContentsMargins(0, 0, 0, 0)

        self.top_row_layout = QtWidgets.QHBoxLayout(self.top_row_widget)
        self.top_row_layout.setContentsMargins(20, 0, 0, 0)

        self.button_text_widget = QtWidgets.QWidget()
        self.button_text_widget.setContentsMargins(0, 0, 0, 0)

        self.button_widget_layout = QtWidgets.QHBoxLayout(self.button_text_widget)
        self.button_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.button_widget_layout.setSpacing(50)

        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.setObjectName("BackButton")
        self.back_button.setFixedSize(QtCore.QSize(52, 22))
        self.back_button.setStyleSheet(
            """QPushButton#BackButton {
                    background-color: #8B4513;
                    color: white;
                    font-weight: bold;
                    border-radius: 5;
                    font-size: 10px;   
                }
                
                QPushButton#BackButton:hover {
                    background-color: #67330E;
                    color: white;
                }
                
                QPushButton#BackButton:pressed {
                    background-color: #B85B19;
                    color: white;
                }"""
        )
        self.back_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.back_button.clicked.connect(self.back_to_dashboard)
        self.button_widget_layout.addWidget(self.back_button)

        self.account_text = QtWidgets.QLabel(
            "Account", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.account_text.setFixedSize(QtCore.QSize(125, 40))
        self.account_text.setStyleSheet(
            """
                background-color: #ADADAD;
                padding: 0 10 0 10;
                color: #3B3B3B; 
                font-weight: bold; 
                border-radius: 10;
            """
        )
        self.button_widget_layout.addWidget(self.account_text)

        self.top_row_layout.addWidget(
            self.button_text_widget, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )

        self.logout_container = CustomLabel()
        self.logout_container.setStyleSheet("margin-right: 25;")
        self.logout_icon = QtGui.QPixmap(":/assets/icons/logout-small")
        self.logout_container.setPixmap(self.logout_icon)
        self.logout_container.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.logout_container.clicked.connect(self.open_logout_dialog)

        self.top_row_layout.addWidget(
            self.logout_container, alignment=QtCore.Qt.AlignmentFlag.AlignRight
        )

        self.container_layout.addWidget(self.top_row_widget)

    def setup_edit_profile_widgets(self):
        self.edit_profile_container_widget = QtWidgets.QWidget()
        self.edit_profile_container_widget.setContentsMargins(0, 0, 0, 0)

        self.edit_profile_container_layout = QtWidgets.QVBoxLayout(
            self.edit_profile_container_widget
        )
        self.edit_profile_container_layout.setContentsMargins(20, 0, 0, 0)

        self.edit_profile_grid_widget = QtWidgets.QWidget()
        self.edit_profile_grid_widget.setContentsMargins(0, 0, 0, 0)

        self.edit_profile_grid = QtWidgets.QGridLayout(self.edit_profile_grid_widget)
        self.edit_profile_grid.setContentsMargins(0, 20, 0, 0)
        self.edit_profile_grid.setHorizontalSpacing(20)
        self.edit_profile_grid.setVerticalSpacing(40)

        self.username_label = QtWidgets.QLabel("Username")
        self.username_label.setStyleSheet("color: #3B3B3B; font-weight: bold;")
        self.edit_profile_grid.addWidget(self.username_label, 0, 0)
        self.username_textbox = QtWidgets.QLineEdit()
        self.username_textbox.setFixedSize(QtCore.QSize(250, 35))
        self.username_textbox.setStyleSheet(
            """
            background-color: #ADADAD;
            color: #3B3B3B;
            font-weight: bold;
            border-radius: 5;
            padding-left: 8px;
            """
        )
        self.edit_profile_grid.addWidget(self.username_textbox, 0, 1)

        self.current_password_label = QtWidgets.QLabel("Current Password")
        self.current_password_label.setStyleSheet("color: #3B3B3B; font-weight: bold;")
        self.edit_profile_grid.addWidget(self.current_password_label, 0, 2)
        self.current_password_textbox = QtWidgets.QLineEdit()
        self.current_password_textbox.setFixedSize(QtCore.QSize(250, 35))
        self.current_password_textbox.setStyleSheet(
            """
            background-color: #ADADAD;
            color: #3B3B3B;
            font-weight: bold;
            border-radius: 5;
            padding-left: 8px;
            """
        )

        self.visible_icon = QtGui.QIcon(":/assets/icons/visible")
        self.hidden_icon = QtGui.QIcon(":/assets/icons/not_visible")

        self.current_password_action = self.current_password_textbox.addAction(
            self.hidden_icon, QtWidgets.QLineEdit.TrailingPosition
        )
        self.current_password_action.triggered.connect(
            self.toggle_password_visibility_current
        )
        self.current_password_textbox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.edit_profile_grid.addWidget(self.current_password_textbox, 0, 3)

        self.new_password_label = QtWidgets.QLabel("New Password")
        self.new_password_label.setStyleSheet("color: #3B3B3B; font-weight: bold;")
        self.edit_profile_grid.addWidget(self.new_password_label, 1, 0)

        self.new_password_textbox = QtWidgets.QLineEdit()
        self.new_password_textbox.setFixedSize(QtCore.QSize(250, 35))
        self.new_password_textbox.setStyleSheet(
            """
            background-color: #ADADAD;
            color: #3B3B3B;
            font-weight: bold;
            border-radius: 5; 
            padding-left: 8px;
            """
        )

        self.new_password_action = self.new_password_textbox.addAction(
            self.hidden_icon, QtWidgets.QLineEdit.TrailingPosition
        )
        self.new_password_action.triggered.connect(self.toggle_password_visibility_new)
        self.new_password_textbox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.edit_profile_grid.addWidget(self.new_password_textbox, 1, 1)

        self.buttons_widget = QtWidgets.QWidget()
        self.buttons_widget.setContentsMargins(0, 0, 0, 0)

        self.buttons_layout = QtWidgets.QHBoxLayout(self.buttons_widget)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setSpacing(30)

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setObjectName("SaveButton")
        self.save_button.setFixedSize(QtCore.QSize(140, 45))
        self.save_button.setStyleSheet(
            """
                QPushButton#SaveButton {
                    background-color: #8B4513;
                    color: white;
                    font-weight: bold;
                    border-radius: 5;   
                }
                
                QPushButton#SaveButton:hover {
                    background-color: #67330E;
                    color: white;
                }
                
                QPushButton#SaveButton:pressed {
                    background-color: #B85B19;
                    color: white;
                }
            """
        )
        self.save_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.save_button.clicked.connect(self.get_user_credentials)
        self.buttons_layout.addWidget(self.save_button)

        self.discard_button = QtWidgets.QPushButton("Discard")
        self.discard_button.setObjectName("DiscardButton")
        self.discard_button.setFixedSize(QtCore.QSize(140, 45))
        self.discard_button.setStyleSheet(
            """
                QPushButton#DiscardButton {
                    background-color: white;
                    color: #8B4513;
                    font-weight: bold;
                    border-radius: 5;
                    border: 2pt solid #8B4513;
                }
                
                QPushButton#DiscardButton:hover {
                    color: #B85B19;
                }
                
                QPushButton#DiscardButton:pressed {
                    color: #67330E;
                    background-color: white;
                }
                
            """
        )
        self.discard_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.discard_button.clicked.connect(self.discard_changes)
        self.buttons_layout.addWidget(self.discard_button)
        self.edit_profile_grid.addWidget(
            self.buttons_widget,
            1,
            2,
            1,
            2,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )

        self.edit_profile_container_layout.addWidget(
            self.edit_profile_grid_widget, stretch=1
        )

        # Filter Export Section
        self.filtered_export_widgets = QtWidgets.QWidget()
        self.filtered_export_widgets.setContentsMargins(0, 0, 0, 0)

        self.filtered_export_layout = QtWidgets.QVBoxLayout(
            self.filtered_export_widgets
        )
        self.filtered_export_layout.setContentsMargins(20, 30, 0, 0)

        # Separate Layout and Widget for the "Filtered Export" Title
        self.filtered_export_text_widget = QtWidgets.QWidget()
        self.filtered_export_text_widget.setContentsMargins(0, 0, 0, 0)

        self.filtered_export_text_layout = QtWidgets.QHBoxLayout(
            self.filtered_export_text_widget
        )
        self.filtered_export_text_layout.setContentsMargins(0, 0, 0, 0)

        self.filtered_export_text = QtWidgets.QLabel(
            "Filtered Export", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.filtered_export_text.setFixedSize(QtCore.QSize(150, 40))
        self.filtered_export_text.setStyleSheet(
            """
                background-color: #ADADAD;
                padding: 0 10 0 10;
                color: #3B3B3B; 
                font-weight: bold; 
                border-radius: 10;
            """
        )
        self.filtered_export_text_layout.addWidget(
            self.filtered_export_text, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.filtered_export_layout.addWidget(self.filtered_export_text_widget)

        self.criteria_export_button_widget = QtWidgets.QWidget()
        self.criteria_export_button_widget.setContentsMargins(0, 0, 0, 0)

        self.criteria_export_button_layout = QtWidgets.QGridLayout(
            self.criteria_export_button_widget
        )
        self.criteria_export_button_layout.setContentsMargins(0, 0, 0, 0)
        self.criteria_export_button_layout.setSpacing(30)

        self.criteria_label = QtWidgets.QLabel("Criteria")
        self.criteria_label.setStyleSheet("color: #3B3B3B; font-weight: bold;")
        self.criteria_export_button_layout.addWidget(self.criteria_label, 0, 0)
        self.criteria_dropdown = QtWidgets.QComboBox()
        self.criteria_dropdown.setStyleSheet(
            """
            background-color: #ADADAD;
            color: #3B3B3B;
            font-weight: bold;
            padding-left: 8px;
            """
        )
        self.criteria_dropdown = setup_combobox(
            self.criteria_dropdown, "filter_export_criteria"
        )

        # Setting retrieved value
        index = self.criteria_dropdown.findText("")
        self.criteria_dropdown.setCurrentIndex(index)

        self.criteria_dropdown.setFixedSize(QtCore.QSize(250, 35))
        self.criteria_export_button_layout.addWidget(
            self.criteria_dropdown, 0, 1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )

        self.export_button = QtWidgets.QPushButton("Export")
        self.export_button.setObjectName("ExportButton")
        self.export_button.setFixedSize(QtCore.QSize(140, 45))
        self.export_button.setStyleSheet(
            """
                QPushButton#ExportButton {
                    background-color: white;
                    color: #8B4513;
                    font-weight: bold;
                    border-radius: 5;
                    border: 2pt solid #8B4513;
                }
                
                QPushButton#ExportButton:hover {
                    color: #B85B19;
                }
                
                QPushButton#ExportButton:pressed {
                    color: #67330E;
                    background-color: white;
                }
                
            """
        )
        self.export_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.export_button.clicked.connect(self.open_export_dialog)
        self.criteria_export_button_layout.addWidget(
            self.export_button, 0, 2, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )

        self.filtered_export_layout.addWidget(self.criteria_export_button_widget)

        self.back_up_button_container = QtWidgets.QWidget()
        self.back_up_button_container.setContentsMargins(0, 0, 0, 0)

        self.back_up_button_layout = QtWidgets.QHBoxLayout(
            self.back_up_button_container
        )
        self.back_up_button_layout.setContentsMargins(0, 10, 10, 0)

        self.back_up_button = QtWidgets.QPushButton("Back Up Database")
        self.back_up_button.setObjectName("BackUpButton")
        self.back_up_button.setFixedSize(QtCore.QSize(170, 40))
        self.back_up_button.setStyleSheet(
            """
                QPushButton#BackUpButton {
                    background-color: #8B4513;
                    color: white;
                    font-weight: bold;
                    border-radius: 5;   
                }
                
                QPushButton#BackUpButton:hover {
                    background-color: #67330E;
                    color: white;
                }
                
                QPushButton#BackUpButton:pressed {
                    background-color: #B85B19;
                    color: white;
                }
            """
        )
        self.back_up_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.back_up_button.clicked.connect(self.select_db_backup_file_location)
        self.back_up_button_layout.addWidget(
            self.back_up_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight
        )

        self.container_layout.addWidget(
            self.edit_profile_container_widget,
            stretch=2,
            alignment=QtCore.Qt.AlignmentFlag.AlignLeft,
        )

        self.container_layout.addWidget(
            self.filtered_export_widgets,
            stretch=2,
            alignment=QtCore.Qt.AlignmentFlag.AlignLeft,
        )

        self.container_layout.addWidget(self.back_up_button_container, stretch=1)

    def setup_footer_area(self):
        self.footer_widget = QtWidgets.QWidget()
        self.footer_widget.setContentsMargins(0, 0, 0, 0)
        self.footer_widget.setStyleSheet(
            """
            background-color: #ADADAD;
            padding-left: 5px;
            padding-right: 5px;
            """
        )

        self.footer_layout = QtWidgets.QHBoxLayout(self.footer_widget)
        self.footer_layout.setContentsMargins(0, 0, 0, 0)

        self.stack_widget = QtWidgets.QWidget()
        self.stack_widget.setContentsMargins(10, 10, 0, 10)
        self.progress_employee_data_stack = QtWidgets.QStackedLayout(self.stack_widget)
        self.progress_employee_data_stack.setContentsMargins(0, 0, 0, 0)

        self.empty_widget = QtWidgets.QWidget()

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(15)
        self.progress_bar.setTextVisible(True)

        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 3px solid white;
                border-radius: 5px;
                text-align: center;
                color: #3B3B3B;
                font-size: 10pt;
                font-weight: bold;
                background-color: white;
            }
            
            QProgressBar::chunk {
                background-color: #ADADAD;
                border-radius: 5px;
            }
            """
        )

        self.employee_data_info = QtWidgets.QLabel()
        self.employee_data_info.setFixedWidth(420)
        self.employee_data_info.setWordWrap(True)

        self.progress_employee_data_stack.addWidget(self.empty_widget)
        self.progress_employee_data_stack.addWidget(self.progress_bar)
        self.progress_employee_data_stack.addWidget(self.employee_data_info)
        self.progress_employee_data_stack.setCurrentIndex(0)

        self.loading_indicator_box = QtWidgets.QLabel()
        self.loading_indicator_box.setFixedSize(45, 45)

        self.loading_indicator = QtGui.QMovie(":/assets/icons/spinner-account")
        self.loading_indicator.setScaledSize(self.loading_indicator_box.size())
        self.loading_indicator_box.setMovie(self.loading_indicator)

        self.product_version_info = QtWidgets.QLabel("UniTrack v1.0.0")
        self.product_version_info.setStyleSheet("color: #3B3B3B; font-weight: bold;")

        self.footer_layout.addWidget(self.stack_widget, stretch=1)
        self.footer_layout.addWidget(
            self.loading_indicator_box,
            alignment=QtCore.Qt.AlignmentFlag.AlignVCenter,
            stretch=1,
        )
        self.footer_layout.addWidget(
            self.product_version_info,
            alignment=QtCore.Qt.AlignmentFlag.AlignRight,
            stretch=1,
        )

        self.container_layout.addWidget(self.footer_widget, stretch=1)

    def prefill_username_textbox(self):
        self.get_username_from_db()

    def preset_username_textbox(self, result):
        self.loading_indicator.stop()
        self.loading_indicator_box.setVisible(False)

        user = result
        self.username = user.get("username")
        self.username_textbox.setText(self.username)

    def get_username(self):
        with SessionLocal() as db:
            result = get_user(db)
            return result

    def get_username_from_db(self):
        self.loading_indicator.start()
        self.loading_indicator_box.setVisible(True)

        worker = Worker(self.get_username)
        worker.signals.result.connect(self.preset_username_textbox)
        global_threadpool.start(worker)

    def discard_changes(self):
        self.username_textbox.setText(self.username)
        self.new_password_textbox.clear()
        self.current_password_textbox.clear()

    def show_user_update_status(self, response):
        self.loading_indicator.stop()
        self.loading_indicator_box.setVisible(False)

        self.progress_employee_data_stack.setCurrentIndex(2)

        if not response:
            self.employee_data_info.setText(
                "User credentials update failed. Password mismatch"
            )
            employee_data_info_error(self.employee_data_info)
            self.username_textbox.setText(self.username)
            self.current_password_textbox.clear()
            self.new_password_textbox.clear()
            show_empty_widget(self.progress_employee_data_stack)
            return

        self.employee_data_info.setText("User credentials updated")
        employee_data_info_success(self.employee_data_info)
        show_empty_widget(self.progress_employee_data_stack)
        return

    def update_user_credentials(self, user):
        with SessionLocal() as db:
            result = update_user(db, user)
            db.commit()
            return result

    def get_user_credentials(self):
        self.loading_indicator.start()
        self.loading_indicator_box.setVisible(True)

        username = self.username_textbox.text()
        current_password = self.current_password_textbox.text()
        new_password = self.new_password_textbox.text()
        user = {}

        if not username:
            self.loading_indicator.stop()
            self.loading_indicator_box.setVisible(False)

            self.progress_employee_data_stack.setCurrentIndex(2)
            self.employee_data_info.setText("Please enter Username")
            employee_data_info_error(self.employee_data_info)
            show_empty_widget(self.progress_employee_data_stack)
            return

        if not current_password:
            self.loading_indicator.stop()
            self.loading_indicator_box.setVisible(False)

            self.progress_employee_data_stack.setCurrentIndex(2)
            self.employee_data_info.setText("Please enter Current Password")
            employee_data_info_error(self.employee_data_info)
            show_empty_widget(self.progress_employee_data_stack)
            return

        if not new_password:
            self.loading_indicator.stop()
            self.loading_indicator_box.setVisible(False)

            self.progress_employee_data_stack.setCurrentIndex(2)
            self.employee_data_info.setText("Please enter New Password")
            employee_data_info_error(self.employee_data_info)
            show_empty_widget(self.progress_employee_data_stack)
            return

        user["username"] = username
        user["current_password"] = current_password
        user["new_password"] = new_password

        worker = Worker(self.update_user_credentials, user)
        worker.signals.result.connect(self.show_user_update_status)
        global_threadpool.start(worker)

    def start_logout(self):
        self.get_username_from_db()
        self.current_password_textbox.clear()
        self.new_password_textbox.clear()
        self.progress_employee_data_stack.setCurrentIndex(0)

        self.exit_dialog()

        self.display_splashscreen.emit(True)

    def exit_dialog(self):
        self.logout_dialog.close()

    def open_logout_dialog(self):
        self.logout_dialog = LogoutDialog(
            self.start_logout, self.exit_dialog, parent=self
        )
        self.logout_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.logout_dialog.show()

    def export_data_result(self, response):
        # Re-enable window
        self.setEnabled(True)

        self.progress_employee_data_stack.setCurrentIndex(2)

        if response is False:
            self.employee_data_info.setText(f"No data to export")
            employee_data_info_error(self.employee_data_info)
            show_empty_widget(self.progress_employee_data_stack)
            return

        elif isinstance(response, dict):
            error = response.get("error")
            self.employee_data_info.setText(f"{error}")
            employee_data_info_error(self.employee_data_info)
            show_empty_widget(self.progress_employee_data_stack)
            return

        number_of_exported_records = response
        self.employee_data_info.setText(
            f"Export complete: {number_of_exported_records} records"
        )
        employee_data_info_success(self.employee_data_info)
        show_empty_widget(self.progress_employee_data_stack)

    def export_data(self, file_name, criteria, progress_callback=None):
        progress_callback_function_received = progress_callback

        with SessionLocal() as db:
            result = criteria_export(
                db, file_name, criteria, progress_callback_function_received
            )
            return result

    def start_export(self, file_name, criteria):

        # Disable window
        self.setEnabled(False)

        self.progress_bar.setValue(0)
        self.progress_employee_data_stack.setCurrentIndex(1)

        self.export_worker = Worker(self.export_data, file_name, criteria)
        self.export_worker.kwargs["progress_callback"] = (
            self.export_worker.signals.progress
        )
        self.export_worker.signals.result.connect(self.export_data_result)
        self.export_worker.signals.progress.connect(self.progress_bar.setValue)
        global_threadpool.start(self.export_worker)

    def open_export_dialog(self):
        FILTER_EXPORT_CRITERIA = [
            "Full Deduction",
            "Partial Deduction",
            "Exceeded Deduction",
            "No Deduction",
        ]

        criteria = self.criteria_dropdown.currentText()

        if not criteria:
            self.progress_employee_data_stack.setCurrentIndex(2)
            self.employee_data_info.setText(f"Select a criteria")
            employee_data_info_error(self.employee_data_info)
            return

        elif criteria not in FILTER_EXPORT_CRITERIA:
            self.progress_employee_data_stack.setCurrentIndex(2)
            self.employee_data_info.setText(f"Invalid criteria: {criteria}")
            employee_data_info_error(self.employee_data_info)
            return

        self.desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export Data", self.desktop_path, "Excel Files (*.xlsx *.xls)"
        )
        if not file_name:
            return

        self.start_export(file_name, criteria)

    def select_db_backup_file_location(self):
        self.desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Backup Database", self.desktop_path, "Database Files (*.db)"
        )

        self.loading_indicator.start()
        self.loading_indicator_box.setVisible(True)

        if not file_path:
            return

        APP_NAME, APP_AUTHOR = "UniTrack", "UniTrack"

        data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
        data_dir.mkdir(parents=True, exist_ok=True)
        db_path = data_dir / "unitrack.db"

        if not db_path.exists():
            self.loading_indicator.stop()
            self.loading_indicator_box.setVisible(False)

            self.progress_employee_data_stack.setCurrentIndex(2)
            self.employee_data_info.setText(f"Database not found")
            employee_data_info_error(self.employee_data_info)
            show_empty_widget(self.progress_employee_data_stack)
            return

        # Create BackUp Folder in the user's system accounts folder
        secret_backup_folder = Path(user_data_dir("UniTrack Backups"))
        secret_backup_folder.mkdir(parents=True, exist_ok=True)

        # Create backup folder in user's selected backup file destination folder
        backup_destination_folder = os.path.dirname(file_path)
        os.chdir(backup_destination_folder)
        os.makedirs("UniTrack Backups", exist_ok=True)
        file_name = os.path.basename(file_path)

        backup_datetime = datetime.strftime(datetime.now(), "%d-%m-%Y_%H-%M-%S")

        file_name_without_extension = file_name.split(".db")[0]
        new_file_name = f"{file_name_without_extension}_{backup_datetime}.db"
        backup_file_destination = os.path.join(
            backup_destination_folder, "UniTrack Backups", new_file_name
        )

        shutil.copy2(db_path, backup_file_destination)

        # Copy backup to secret BackUp Folder on user's system
        secret_backup_folder_path = secret_backup_folder / new_file_name
        shutil.copy2(db_path, secret_backup_folder_path)

        self.loading_indicator.stop()
        self.loading_indicator_box.setVisible(False)

        self.progress_employee_data_stack.setCurrentIndex(2)
        self.employee_data_info.setText(f"Backup created successfully")
        employee_data_info_success(self.employee_data_info)
        show_empty_widget(self.progress_employee_data_stack)

    def toggle_password_visibility_current(self):
        if self.current_password_textbox.echoMode() == QtWidgets.QLineEdit.Password:
            self.current_password_textbox.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.current_password_action.setIcon(self.visible_icon)
        else:
            self.current_password_textbox.setEchoMode(QtWidgets.QLineEdit.Password)
            self.current_password_action.setIcon(self.hidden_icon)

    def toggle_password_visibility_new(self):
        if self.new_password_textbox.echoMode() == QtWidgets.QLineEdit.Password:
            self.new_password_textbox.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.new_password_action.setIcon(self.visible_icon)
        else:
            self.new_password_textbox.setEchoMode(QtWidgets.QLineEdit.Password)
            self.new_password_action.setIcon(self.hidden_icon)

    def setup_account_screen(self):
        self.setup_container()
        self.setup_top_row()
        self.setup_edit_profile_widgets()
        self.setup_footer_area()
        self.prefill_username_textbox()

    def back_to_dashboard(self):
        self.previous_screen.emit(True)
