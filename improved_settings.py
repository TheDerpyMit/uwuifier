import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QButtonGroup, QRadioButton, QGroupBox, QGridLayout,
                            QCheckBox, QScrollArea, QWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class HotkeySelector(QGroupBox):
    """Custom hotkey selector with radio buttons"""
    
    hotkey_changed = pyqtSignal(str)
    
    def __init__(self, current_hotkey="ctrl+shift+u", parent=None):
        super().__init__("Global Hotkey", parent)
        self.current_hotkey = current_hotkey
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the hotkey selection UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 25, 20, 20)
        layout.setSpacing(12)
        
        # Create button group for exclusive selection
        self.button_group = QButtonGroup(self)
        
        # Define hotkey options
        self.hotkey_options = [
            ("Ctrl + Shift + U", "ctrl+shift+u"),
            ("Ctrl + Shift + W", "ctrl+shift+w"),
            ("Ctrl + Alt + U", "ctrl+alt+u"),
            ("Alt + Shift + U", "alt+shift+u"),
            ("Ctrl + U", "ctrl+u"),
            ("Alt + U", "alt+u"),
            ("F9", "f9"),
            ("F10", "f10"),
            ("F11", "f11"),
            ("F12", "f12")
        ]
        
        # Create radio buttons in a grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(8)
        
        for i, (display_name, hotkey_value) in enumerate(self.hotkey_options):
            radio_btn = QRadioButton(display_name)
            radio_btn.setObjectName(hotkey_value)
            
            # Check if this is the current hotkey
            if hotkey_value == self.current_hotkey:
                radio_btn.setChecked(True)
            
            # Connect signal
            radio_btn.toggled.connect(self._on_hotkey_selected)
            
            # Add to button group and layout
            self.button_group.addButton(radio_btn)
            
            # Arrange in 2 columns
            row = i // 2
            col = i % 2
            grid_layout.addWidget(radio_btn, row, col)
        
        layout.addLayout(grid_layout)
        
    def _on_hotkey_selected(self):
        """Handle hotkey selection"""
        sender = self.sender()
        if sender.isChecked():
            hotkey_value = sender.objectName()
            self.current_hotkey = hotkey_value
            self.hotkey_changed.emit(hotkey_value)
    
    def get_selected_hotkey(self):
        """Get the currently selected hotkey"""
        return self.current_hotkey

class ImprovedSettingsDialog(QDialog):
    """Improved settings dialog with sliders and modern design"""
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """Setup the improved settings dialog UI"""
        self.setWindowTitle("uwuifier Settings")
        self.setFixedSize(600, 600)  # Made wider to accommodate buttons better
        self.setModal(True)
        
        # Set window flags to remove the help button (question mark)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
        # Set the same icon as the main window
        import os
        from PyQt5.QtGui import QIcon
        if os.path.exists("icon.ico"):
            self.setWindowIcon(QIcon("icon.ico"))
        
        # Apply modern dark theme styling
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                font-weight: 600;
                border: 2px solid #404040;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 15px;
                color: #ff69b4;
                font-size: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                background-color: #1e1e1e;
            }
            QRadioButton {
                color: white;
                padding: 8px;
                font-size: 13px;
                spacing: 8px;
                min-height: 20px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #555;
                border-radius: 9px;
                background-color: #2d2d2d;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #ff69b4;
                border-radius: 9px;
                background-color: #ff69b4;
            }
            QRadioButton:hover {
                background-color: #2d2d2d;
                border-radius: 6px;
            }
            QCheckBox {
                color: white;
                padding: 10px 15px;
                font-size: 14px;
                font-weight: 500;
                spacing: 12px;
                min-height: 25px;
                background-color: transparent;
            }
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
            }
            QCheckBox::indicator:unchecked {
                border: 3px solid #555;
                border-radius: 6px;
                background-color: #2d2d2d;
            }
            QCheckBox::indicator:checked {
                border: 3px solid #ff69b4;
                border-radius: 6px;
                background-color: #ff69b4;
            }
            QCheckBox:hover {
                background-color: #2a2a2a;
                border-radius: 8px;
            }
            QPushButton {
                background-color: #ff69b4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 12px;
                min-height: 18px;
            }
            QPushButton:hover {
                background-color: #ff1493;
            }
            QPushButton:pressed {
                background-color: #dc143c;
            }
            QPushButton#cancelButton {
                background-color: #404040;
            }
            QPushButton#cancelButton:hover {
                background-color: #505050;
            }
            QLabel {
                color: #cccccc;
                font-size: 13px;
            }
            QLabel#sectionTitle {
                color: #ff69b4;
                font-size: 18px;
                font-weight: bold;
                padding: 15px 0px;
            }
            QLabel#titleLabel {
                color: #ff69b4;
                font-size: 22px;
                font-weight: bold;
                padding: 10px 0px;
            }
            QLabel#optionDescription {
                color: #888888;
                font-size: 11px;
                font-style: italic;
                padding-left: 35px;
                margin-bottom: 3px;
                margin-top: 2px;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollArea QWidget {
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #ff69b4;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #ff1493;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QToolTip {
                background-color: #2d2d2d;
                color: white;
                border: 2px solid #ff69b4;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
                font-weight: 500;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Content widget for scroll area
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel("🎀 uwuifier Settings")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)
        
        # Add some space after title
        layout.addSpacing(10)
        
        # Hotkey section
        self.hotkey_selector = HotkeySelector()
        layout.addWidget(self.hotkey_selector)
        
        # UwUify Options section
        options_group = QGroupBox("🎀 UwUify Transform Options")
        options_layout = QVBoxLayout(options_group)
        options_layout.setSpacing(15)
        options_layout.setContentsMargins(25, 35, 25, 30)
        
        # Create checkboxes with tooltips instead of descriptions
        self.smiley_cb = QCheckBox("🙂 Emoticons")
        self.smiley_cb.setToolTip("Adds cute emoticons and kaomoji to the text (◕‿◕) ✨\nMakes your text more expressive with adorable faces!")
        
        self.yu_cb = QCheckBox("💫 YU Substitution")
        self.yu_cb.setToolTip("Replaces 'you' with 'yu' for extra cuteness\nExample: 'How are you?' → 'How are yu?'")
        
        self.stutter_cb = QCheckBox("😊 Stuttering")
        self.stutter_cb.setToolTip("Adds  stuttering to some words (l-like this!) \nMakes characters seem shy and cute")
        
        self.nouwu_cb = QCheckBox("🚫 No UwU Mode")
        self.nouwu_cb.setToolTip("Disables the main 'r'→'w' and 'l'→'w' transformations\nUse this to keep some original pronunciation")
        
        # Add checkboxes to layout
        options_layout.addWidget(self.smiley_cb)
        options_layout.addWidget(self.yu_cb)
        options_layout.addWidget(self.stutter_cb)
        options_layout.addWidget(self.nouwu_cb)
        
        layout.addWidget(options_group)
        
        # Troll Mode section
        troll_group = QGroupBox("🦹‍♀️ DANGER ZONE")
        troll_layout = QVBoxLayout(troll_group)
        troll_layout.setSpacing(15)
        troll_layout.setContentsMargins(25, 35, 25, 30)
        
        # Troll mode button
        self.troll_btn = QPushButton("😈 ACTIVATE TROLL MODE")
        self.troll_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc143c;
                color: white;
                border: 2px solid #ff1493;
                border-radius: 8px;
                padding: 15px 25px;
                font-weight: bold;
                font-size: 14px;
                min-height: 25px;
            }
            QPushButton:hover {
                background-color: #b91c3c;
                border-color: #ff69b4;
            }
            QPushButton:pressed {
                background-color: #a0122a;
            }
        """)
        self.troll_btn.setToolTip("⚠️ WARNING: This will hijack your computer!\nOnly activate if you want chaos! Can only be stopped via Task Manager!")
        self.troll_btn.clicked.connect(self.activate_troll_mode)
        
        # Warning label
        warning_label = QLabel("⚠️ WARNING: Troll mode will completely hijack your computer!\nKeyboard, mouse, screen overlay, and audio chaos!\nOnly kill from Task Manager can stop it!")
        warning_label.setStyleSheet("color: #ff6666; font-weight: bold; text-align: center;")
        warning_label.setAlignment(Qt.AlignCenter)
        warning_label.setWordWrap(True)
        
        troll_layout.addWidget(warning_label)
        troll_layout.addWidget(self.troll_btn)
        
        layout.addWidget(troll_group)
        
        # Info section
        layout.addStretch(10)
        info_label = QLabel("💡 Hover over options to see detailed descriptions\n⚡ Changes are applied immediately when you save settings")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #888888; font-style: italic; line-height: 1.4;")
        layout.addWidget(info_label)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)  # Reduced spacing between buttons
        button_layout.addStretch()
        
        # How to Use button
        self.help_btn = QPushButton("❓ How to Use")
        self.help_btn.clicked.connect(self.show_instructions)
        self.help_btn.setToolTip("Show step-by-step instructions")
        button_layout.addWidget(self.help_btn)
        
        # Save button
        self.save_btn = QPushButton("💾 Save Settings")
        self.save_btn.clicked.connect(self.save_settings)
        self.save_btn.setToolTip("Save all changes and apply new settings")
        button_layout.addWidget(self.save_btn)
        
        # Cancel button
        self.cancel_btn = QPushButton("❌ Cancel")
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.clicked.connect(self.reject)
        self.cancel_btn.setToolTip("Close without saving changes")
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        # Set the content widget to scroll area and add to main layout
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
    def load_settings(self):
        """Load current settings"""
        current_hotkey = self.config_manager.get('hotkey', 'ctrl+shift+u')
        
        # Update hotkey selector
        self.hotkey_selector.current_hotkey = current_hotkey
        
        # Find and check the correct radio button
        for btn in self.hotkey_selector.button_group.buttons():
            if btn.objectName() == current_hotkey:
                btn.setChecked(True)
                break
        
        # Load uwuify flag settings
        self.smiley_cb.setChecked(self.config_manager.get('smiley', False))
        self.yu_cb.setChecked(self.config_manager.get('yu', False))
        self.stutter_cb.setChecked(self.config_manager.get('stutter', False))
        self.nouwu_cb.setChecked(self.config_manager.get('nouwu', False))
                
    def save_settings(self):
        """Save settings and close"""
        # Get selected hotkey
        selected_hotkey = self.hotkey_selector.get_selected_hotkey()
        
        # Save to config
        self.config_manager.set('hotkey', selected_hotkey)
        
        # Save uwuify flags
        self.config_manager.set('smiley', self.smiley_cb.isChecked())
        self.config_manager.set('yu', self.yu_cb.isChecked())
        self.config_manager.set('stutter', self.stutter_cb.isChecked())
        self.config_manager.set('nouwu', self.nouwu_cb.isChecked())
        
        print("Settings saved successfully!")
        
        # Close dialog
        self.accept()
    
    def show_instructions(self):
        """Show mini instruction dialog"""
        from PyQt5.QtWidgets import QMessageBox
        
        msg = QMessageBox(self)
        msg.setWindowTitle("How to Use uwuifier")
        msg.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
        instructions = """
<h3>🦄 How to Use uwuifier</h3>

<p><b>Step 1:</b> Select any text in any application</p>
<p><b>Step 2:</b> Press <b>F12</b> (or your custom hotkey)</p>
<p><b>Step 3:</b> Watch the text get uwuified! ✨</p>

<hr>

<p><b>💡 Tips:</b></p>
<p>• Works in any app: browsers, text editors, chat apps</p>
<p>• Change hotkey in Settings if F12 doesn't work</p>
<p>• Customize uwuify style with checkboxes in Settings</p>
<p>• Look for overlay notifications in top-right corner</p>
        """
        
        msg.setText(instructions)
        msg.setTextFormat(Qt.RichText)
        msg.setIcon(QMessageBox.Information)
        
        # Custom styling for the message box
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1e1e1e;
                color: white;
                font-family: 'Segoe UI';
            }
            QMessageBox QLabel {
                color: white;
                min-width: 400px;
                max-width: 500px;
            }
            QPushButton {
                background-color: #ff69b4;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 6px;
                font-weight: 600;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #ff1493;
            }
        """)
        
        msg.exec_()
    
    def activate_troll_mode(self):
        """Activate the ultimate troll mode with warning"""
        try:
            # Import the troll mode module
            from troll_mode import show_troll_mode_warning, TrollModeManager
            
            # Show warning dialog
            if show_troll_mode_warning():
                print("😈 User confirmed troll mode activation!")
                
                # Close settings dialog first
                self.accept()
                
                # Get the main window from parent
                main_window = self.parent()
                if main_window:
                    # Create and activate troll mode
                    troll_manager = TrollModeManager(main_window)
                    troll_manager.activate_troll_mode()
                else:
                    print("❌ Could not get main window reference")
            else:
                print("🛑 User cancelled troll mode activation")
                
        except ImportError as e:
            print(f"❌ Error importing troll mode: {e}")
        except Exception as e:
            print(f"❌ Error activating troll mode: {e}")
            import traceback
            traceback.print_exc()
        
    def get_selected_hotkey(self):
        """Get the selected hotkey value"""
        return self.hotkey_selector.get_selected_hotkey()
