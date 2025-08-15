import sys
import os
import subprocess
import time
import threading
from typing import Optional
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel, QDialog,
                            QLineEdit, QFormLayout, QSystemTrayIcon, QMenu, QAction)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont, QPainterPath, QBrush, QColor
from config_manager import ConfigManager
from overlay import OverlayManager
from selection_keyboard import SelectionKeyboardHook, SelectionUwuTextProcessor
from improved_settings import ImprovedSettingsDialog

class MainWindow(QMainWindow):
    toggle_requested = pyqtSignal()
    overlay_requested = pyqtSignal(str)  # Signal for overlay messages
    
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        
        # Connect the overlay signal to the handler
        self.overlay_requested.connect(self.show_overlay_on_main_thread)
        self.overlay_manager = OverlayManager()
        self.text_processor = SelectionUwuTextProcessor(self.config_manager)
        self.keyboard_hook = None
        
        self.setup_ui()
        self.setup_system_tray()
        self.setup_keyboard_hook()
        
        # Load initial state
        self.text_processor.enabled = self.config_manager.is_enabled()
        self.update_toggle_button()
    
    def setup_ui(self):
        """Setup main window UI with borderless design"""
        self.setWindowTitle("uwuifier")
        self.setFixedSize(320, 320)  # Made taller to fix button scaling issues
        
        # Set window icon if available
        if os.path.exists("icon.ico"):
            self.setWindowIcon(QIcon("icon.ico"))
        
        # Create borderless window with custom controls
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        # Dark theme styling with custom title bar
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                border: 1px solid #ff69b4;
            }
            QWidget {
                background-color: transparent;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QWidget#titleBar {
                background-color: #2d2d2d;
                border-bottom: 1px solid #3d3d3d;
            }
            QWidget#contentArea {
                background-color: #1e1e1e;
            }
            QPushButton {
                background-color: #ff69b4;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #ff1493;
            }
            QPushButton:pressed {
                background-color: #dc143c;
            }
            QPushButton#toggleButton {
                font-size: 16px;
                min-height: 30px;
            }
            QPushButton#settingsButton, QPushButton#exitButton {
                background-color: #3b3b3b;
                font-size: 12px;
                min-height: 15px;
                padding: 8px 16px;
            }
            QPushButton#settingsButton:hover, QPushButton#exitButton:hover {
                background-color: #4b4b4b;
            }
            QPushButton#closeButton {
                background-color: #e81123;
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 12px;
                font-weight: bold;
                min-height: 12px;
                max-width: 30px;
            }
            QPushButton#closeButton:hover {
                background-color: #f1707a;
            }
            QPushButton#minimizeButton {
                background-color: #404040;
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 12px;
                font-weight: bold;
                min-height: 12px;
                max-width: 30px;
            }
            QPushButton#minimizeButton:hover {
                background-color: #505050;
            }
            QLabel {
                color: #cccccc;
                font-size: 14px;
                font-weight: 500;
            }
            QLabel#titleLabel {
                color: #ff69b4;
                font-size: 18px;
                font-weight: bold;
            }
            QLabel#windowTitle {
                color: white;
                font-size: 12px;
                font-weight: 600;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Custom title bar
        title_bar = self.create_title_bar()
        main_layout.addWidget(title_bar)
        
        # Content area
        content_area = QWidget()
        content_area.setObjectName("contentArea")
        content_layout = QVBoxLayout(content_area)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(25, 25, 25, 25)
        
        # App title
        title_label = QLabel("uwuifier")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title_label)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.status_label)
        
        # Toggle button
        self.toggle_button = QPushButton()
        self.toggle_button.setObjectName("toggleButton")
        self.toggle_button.clicked.connect(self.toggle_uwuifier)
        content_layout.addWidget(self.toggle_button)
        
        # Add some stretch space
        content_layout.addStretch(10)
        
        # Button row
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # Settings button
        settings_button = QPushButton("⚙️ Settings")
        settings_button.setObjectName("settingsButton")
        settings_button.clicked.connect(self.show_settings)
        button_layout.addWidget(settings_button)
        
        # Exit button
        exit_button = QPushButton("❌ Exit")
        exit_button.setObjectName("exitButton")
        exit_button.clicked.connect(self.close_application)
        button_layout.addWidget(exit_button)
        
        content_layout.addLayout(button_layout)
        
        # Made by text at the bottom
        made_by_label = QLabel("made with 🩷 by mit")
        made_by_label.setAlignment(Qt.AlignCenter)
        made_by_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 10px;
                font-family: 'Segoe UI';
                margin-top: 8px;
                margin-bottom: 4px;
            }
        """)
        content_layout.addWidget(made_by_label)
        
        main_layout.addWidget(content_area)
        
        # Center the window
        self.center_window()
        
        # Enable dragging
        self.drag_position = None
    
    def create_title_bar(self):
        """Create custom title bar with minimize and close buttons"""
        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(35)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(15, 8, 8, 8)
        layout.setSpacing(8)
        
        # Window title
        title_label = QLabel("uwuifier")
        title_label.setObjectName("windowTitle")
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # Minimize button
        minimize_btn = QPushButton("−")
        minimize_btn.setObjectName("minimizeButton")
        minimize_btn.clicked.connect(self.showMinimized)
        minimize_btn.setToolTip("Minimize")
        layout.addWidget(minimize_btn)
        
        # Close button
        close_btn = QPushButton("×")
        close_btn.setObjectName("closeButton")
        close_btn.clicked.connect(self.close)
        close_btn.setToolTip("Close")
        layout.addWidget(close_btn)
        
        return title_bar
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        self.drag_position = None
    
    def paintEvent(self, event):
        """Custom paint event for rounded corners"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create rounded rectangle path
        rect = self.rect()
        path = QPainterPath()
        path.addRoundedRect(rect.x(), rect.y(), rect.width(), rect.height(), 12, 12)
        
        # Fill background
        painter.fillPath(path, QBrush(QColor(30, 30, 30)))
        
        # Draw border
        painter.setPen(QColor(255, 105, 180))
        painter.drawPath(path)
    
    def center_window(self):
        """Center the window on screen"""
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)
    
    def setup_system_tray(self):
        """Setup system tray icon"""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Create tray icon (simple colored circle)
        icon = self.create_tray_icon()
        self.tray_icon.setIcon(icon)
        
        # Show welcome instructions on first run
        self.show_welcome_if_first_run()
        
        # Tray menu
        tray_menu = QMenu()
        
        # Toggle action
        self.toggle_action = QAction("Enable uwuifier", self)
        self.toggle_action.triggered.connect(self.toggle_uwuifier)
        tray_menu.addAction(self.toggle_action)
        
        tray_menu.addSeparator()
        
        # Settings action
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        tray_menu.addAction(settings_action)
        
        # Show/Hide window action
        show_action = QAction("Show/Hide Window", self)
        show_action.triggered.connect(self.toggle_window_visibility)
        tray_menu.addAction(show_action)
        
        tray_menu.addSeparator()
        
        # Quit action
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close_application)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
    
    def setup_keyboard_hook(self):
        """Setup selection-based keyboard hook"""
        def start_hook():
            # Load hotkey from config
            saved_hotkey = self.config_manager.get('hotkey', 'ctrl+shift+u')
            
            self.keyboard_hook = SelectionKeyboardHook(
                self.text_processor, 
                overlay_callback=self.on_overlay_trigger
            )
            
            # Set the saved hotkey before starting
            self.keyboard_hook.set_hotkey(saved_hotkey)
            self.keyboard_hook.start()
            
            print(f"✅ Selection-based keyboard hook ready!")
            print(f"🔥 Use '{self.keyboard_hook.get_hotkey()}' to uwuify selected text")
            
            # Update UI to show ready
            if hasattr(self, 'status_label'):
                hotkey = self.keyboard_hook.get_hotkey()
                if self.text_processor.enabled:
                    self.status_label.setText(f"Status: Ready - Use {hotkey} to uwuify!")
                else:
                    self.status_label.setText("Status: Ready (Disabled)")
        
        threading.Thread(target=start_hook, daemon=True).start()
    
    def on_overlay_trigger(self, message: str):
        """Handle overlay trigger from keyboard hook - ensure it runs on main thread"""
        # Emit signal to show overlay on main thread
        self.overlay_requested.emit(message)
    
    def show_overlay_on_main_thread(self, message: str):
        """Show overlay on the main thread"""
        try:
            self.overlay_manager.show_custom_overlay(message)
        except Exception as e:
            print(f"Error showing overlay: {e}")
    
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
    
    def show_welcome_if_first_run(self):
        """Show welcome instructions if this is the first time using the app"""
        first_run = self.config_manager.get('first_run', True)
        if first_run:
            # Mark as not first run anymore
            self.config_manager.set('first_run', False)
            
            # Show welcome message with a delay so the main window appears first
            QTimer.singleShot(800, self.show_welcome_message)
    
    def show_welcome_message(self):
        """Show the welcome message"""
        from PyQt5.QtWidgets import QMessageBox
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Welcome to uwuifier! 🦄")
        msg.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
        welcome_text = """
<h2>🦄 Welcome to uwuifier!</h2>

<p>Ready to make your text cuter? Here's how:</p>

<p><b>1.</b> Select any text anywhere (browser, Discord, etc.)</p>
<p><b>2.</b> Press <b>F12</b> to uwuify it instantly! ✨</p>
<p><b>3.</b> Watch for overlay notifications in the top-right corner</p>

<hr>

<p><b>💡 Pro Tips:</b></p>
<p>• Change hotkey in Settings if F12 conflicts</p>
<p>• Customize uwuify style with checkboxes</p>
<p>• Click "❓ How to Use" in Settings for help anytime</p>

<p><b>Try it now!</b> Select this text and press F12! 🎯</p>
        """
        
        msg.setText(welcome_text)
        msg.setTextFormat(Qt.RichText)
        msg.setIcon(QMessageBox.Information)
        
        # Custom styling
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1e1e1e;
                color: white;
                font-family: 'Segoe UI';
            }
            QMessageBox QLabel {
                color: white;
                min-width: 450px;
                max-width: 500px;
            }
            QPushButton {
                background-color: #ff69b4;
                color: white;
                border: none;
                padding: 10px 24px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 12px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #ff1493;
            }
        """)
        
        msg.exec_()

    def test_overlay(self):
        """Test method to trigger overlay manually"""
        self.overlay_manager.show_overlay("Test overlay message! 🧪")
    
    def create_tray_icon(self):
        """Create a tray icon - use the same custom icon as the main window"""
        # Try to use custom icon first (same as window icon)
        if os.path.exists("icon.ico"):
            return QIcon("icon.ico")  # Use the icon directly for consistency
        
        # Fallback: create simple icon if custom one doesn't exist
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw a pink circle
        painter.setBrush(Qt.magenta)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(2, 2, 28, 28)
        
        # Draw "u" in the center
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "u")
        
        painter.end()
        return QIcon(pixmap)
    
    def toggle_uwuifier(self):
        """Toggle uwuifier state"""
        new_state = not self.text_processor.enabled
        
        # Update state
        self.config_manager.set('enabled', new_state)
        self.text_processor.enabled = new_state
        
        # Show overlay
        if new_state:
            self.overlay_manager.show_enabled_overlay()
        else:
            self.overlay_manager.show_disabled_overlay()
        
        self.update_toggle_button()
    
    def update_toggle_button(self):
        """Update toggle button appearance"""
        if self.text_processor.enabled:
            self.toggle_button.setText("💖 Disable uwuifier")
            if hasattr(self, 'keyboard_hook') and self.keyboard_hook:
                hotkey = self.keyboard_hook.get_hotkey()
                self.status_label.setText(f"Status: Enabled - Use {hotkey} to uwuify!")
            else:
                self.status_label.setText("Status: Enabled")
            self.toggle_action.setText("Disable uwuifier")
        else:
            self.toggle_button.setText("😿 Enable uwuifier") 
            self.status_label.setText("Status: Disabled")
            self.toggle_action.setText("Enable uwuifier")
    
    def show_settings(self):
        """Show settings dialog"""
        try:
            print("Opening settings dialog...")
            dialog = ImprovedSettingsDialog(self.config_manager, self)
            print("Settings dialog created successfully")
            result = dialog.exec_()
            print(f"Settings dialog closed with result: {result}")
            
            if result == QDialog.Accepted:
                # Get the new hotkey from the dialog
                new_hotkey = dialog.get_selected_hotkey()
                
                # Update the keyboard hook with the new hotkey
                if self.keyboard_hook:
                    self.keyboard_hook.set_hotkey(new_hotkey)
                    
                # Update status label to show new hotkey
                if self.text_processor.enabled:
                    self.status_label.setText(f"Status: Enabled - Use {new_hotkey} to uwuify!")
                
                print(f"Settings saved - New hotkey: {new_hotkey}")
        except Exception as e:
            print(f"Error opening settings dialog: {e}")
            import traceback
            traceback.print_exc()
    
    def tray_icon_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_window_visibility()
    
    def toggle_window_visibility(self):
        """Toggle main window visibility"""
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            event.accept()
    
    def close_application(self):
        """Close the entire application"""
        # Stop keyboard hook
        if self.keyboard_hook:
            self.keyboard_hook.stop()
        
        self.tray_icon.hide()
        QApplication.quit()

class UwuifierApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        
        # Set application icon globally (affects taskbar, alt+tab, etc.)
        if os.path.exists("icon.ico"):
            app_icon = QIcon("icon.ico")
            self.setWindowIcon(app_icon)
            # Also set as application icon explicitly
            QApplication.setWindowIcon(app_icon)
        
        # Set application properties for better Windows integration
        self.setOrganizationName("uwuifier")
        self.setApplicationName("uwuifier")
        self.setApplicationVersion("1.0")
        
        # Windows-specific: Set application user model ID for taskbar grouping
        try:
            import ctypes
            myappid = 'uwuifier.app.1.0'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass  # Ignore if ctypes fails
        
        # Ensure single instance
        self.setQuitOnLastWindowClosed(False)
        
        # Create main window
        self.main_window = MainWindow()
        
        # Show window initially (will be hidden to tray after first run)
        self.main_window.show()

def main():
    """Main entry point"""
    app = UwuifierApp()
    
    # Check if system tray is available
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("System tray is not available on this system.")
        return 1
    
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
