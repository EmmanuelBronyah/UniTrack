from PySide6 import QtWidgets, QtCore, QtGui
from src.utils import setup_combobox


class AccountScreen(QtWidgets.QMainWindow):
    previous_screen = QtCore.Signal(object)

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
        self.top_row_layout.setSpacing(50)

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
                    background-color: #B85B19;
                    color: white;
                }
                
                QPushButton#BackButton:pressed {
                    background-color: white;
                    color: #8B4513;
                }"""
        )
        self.back_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.back_button.clicked.connect(self.back_to_dashboard)
        self.top_row_layout.addWidget(
            self.back_button, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )

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
        self.top_row_layout.addWidget(self.account_text)

        self.container_layout.addWidget(
            self.top_row_widget, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )

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
        self.edit_profile_grid.setHorizontalSpacing(30)
        self.edit_profile_grid.setVerticalSpacing(15)

        self.username_label = QtWidgets.QLabel("Username")
        self.username_label.setStyleSheet("color: #3B3B3B; font-weight: bold;")
        self.edit_profile_grid.addWidget(self.username_label, 0, 0)
        self.username_textbox = QtWidgets.QLineEdit()
        self.username_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.username_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; font-weight: bold;"
        )
        self.edit_profile_grid.addWidget(self.username_textbox, 1, 0)

        self.current_password_label = QtWidgets.QLabel("Current Password")
        self.current_password_label.setStyleSheet("color: #3B3B3B; font-weight: bold;")
        self.edit_profile_grid.addWidget(self.current_password_label, 0, 1)
        self.current_password_textbox = QtWidgets.QLineEdit()
        self.current_password_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.current_password_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; font-weight: bold;"
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

        self.edit_profile_grid.addWidget(self.current_password_textbox, 1, 1)

        self.new_password_label = QtWidgets.QLabel("New Password")
        self.new_password_label.setStyleSheet("color: #3B3B3B; font-weight: bold;")
        self.edit_profile_grid.addWidget(self.new_password_label, 2, 0)

        self.new_password_textbox = QtWidgets.QLineEdit()
        self.new_password_textbox.setFixedSize(QtCore.QSize(420, 35))
        self.new_password_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; font-weight: bold;"
        )

        self.new_password_action = self.new_password_textbox.addAction(
            self.hidden_icon, QtWidgets.QLineEdit.TrailingPosition
        )
        self.new_password_action.triggered.connect(self.toggle_password_visibility_new)
        self.new_password_textbox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.edit_profile_grid.addWidget(self.new_password_textbox, 3, 0, 1, 2)

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setObjectName("SaveButton")
        self.save_button.setFixedSize(QtCore.QSize(140, 35))
        self.save_button.setStyleSheet(
            """
                QPushButton#SaveButton {
                    background-color: #8B4513;
                    color: white;
                    font-weight: bold;
                    border-radius: 5;   
                }
                
                QPushButton#SaveButton:hover {
                    background-color: #B85B19;
                    color: white;
                }
                
                QPushButton#SaveButton:pressed {
                    background-color: white;
                    color: #8B4513;
                }
            """
        )
        self.save_button.setCursor(QtCore.Qt.PointingHandCursor)
        # self.save_button.clicked.connect(self.save_record)
        self.edit_profile_grid.addWidget(
            self.save_button, 1, 2, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )

        self.discard_button = QtWidgets.QPushButton("Discard")
        self.discard_button.setObjectName("DiscardButton")
        self.discard_button.setFixedSize(QtCore.QSize(140, 35))
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
                    color: white;
                    background-color: #B85B19;
                }
                
            """
        )
        self.discard_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.edit_profile_grid.addWidget(
            self.discard_button, 3, 2, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
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
        self.filtered_export_layout.setContentsMargins(0, 0, 0, 0)
        self.filtered_export_layout.setSpacing(0)

        # Separate Layout and Widget for the "Filtered Export" Title
        self.filtered_export_text_widget = QtWidgets.QWidget()
        self.filtered_export_text_widget.setContentsMargins(0, 0, 0, 0)

        self.filtered_export_text_layout = QtWidgets.QHBoxLayout(
            self.filtered_export_text_widget
        )
        self.filtered_export_text_layout.setContentsMargins(90, 0, 0, 0)

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
        self.criteria_export_button_layout.setHorizontalSpacing(50)

        self.criteria_label = QtWidgets.QLabel("Criteria")
        self.criteria_label.setStyleSheet("color: #3B3B3B; font-weight: bold;")
        self.criteria_export_button_layout.addWidget(self.criteria_label, 0, 0)
        self.criteria_dropdown = QtWidgets.QComboBox()
        self.criteria_dropdown.setStyleSheet("color: #3B3B3B; font-weight: bold;")
        self.criteria_dropdown = setup_combobox(
            self.criteria_dropdown, "filter_export_criteria"
        )

        # Setting retrieved value
        index = self.criteria_dropdown.findText("")
        self.criteria_dropdown.setCurrentIndex(index)

        self.criteria_dropdown.setFixedSize(QtCore.QSize(210, 35))
        self.criteria_dropdown.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.criteria_export_button_layout.addWidget(self.criteria_dropdown, 1, 0)

        self.export_button = QtWidgets.QPushButton("Export")
        self.export_button.setObjectName("ExportButton")
        self.export_button.setFixedSize(QtCore.QSize(140, 35))
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
                    color: white;
                    background-color: #B85B19;
                }
                
            """
        )
        self.export_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.criteria_export_button_layout.addWidget(
            self.export_button, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )

        self.filtered_export_layout.addWidget(self.criteria_export_button_widget)

        self.edit_profile_container_layout.addWidget(
            self.filtered_export_widgets, stretch=2
        )

        self.back_up_button_container = QtWidgets.QWidget()
        self.back_up_button_container.setContentsMargins(0, 0, 0, 0)

        self.back_up_button_layout = QtWidgets.QHBoxLayout(
            self.back_up_button_container
        )
        self.back_up_button_layout.setContentsMargins(0, 0, 10, 0)

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
                    background-color: #B85B19;
                    color: white;
                }
                
                QPushButton#BackUpButton:pressed {
                    background-color: white;
                    color: #8B4513;
                }
            """
        )
        self.back_up_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.back_up_button_layout.addWidget(
            self.back_up_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight
        )

        self.edit_profile_container_layout.addWidget(
            self.back_up_button_container, stretch=1
        )

        self.container_layout.addWidget(self.edit_profile_container_widget, stretch=6)

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
        self.employee_data_info.setStyleSheet(
            """
            background-color: #DBDBDB;
            color: white;
            font-weight: bold; 
            border-radius: 5; 
            padding: 3;
            """
        )

        self.progress_employee_data_stack.addWidget(self.empty_widget)
        self.progress_employee_data_stack.addWidget(self.progress_bar)
        self.progress_employee_data_stack.addWidget(self.employee_data_info)
        self.progress_employee_data_stack.setCurrentIndex(0)

        self.loading_indicator_box = QtWidgets.QLabel()
        self.loading_indicator_box.setFixedSize(45, 45)
        self.loading_indicator_box.setVisible(False)

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

    def back_to_dashboard(self):
        self.previous_screen.emit(True)
