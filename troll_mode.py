"""
Troll Mode Implementation - Use with caution! 🦹‍♀️
This module implements chaotic troll features including:
- Global keyboard hijacking
- Screen overlay
- Mouse cursor shaking
- Audio loop
"""
import sys
import os
import threading
import time
import random
import subprocess
from typing import Optional
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor, QCursor
import keyboard
import pygame
from resource_helper import get_resource_path, extract_resource_to_temp, cleanup_temp_file

class TrollModeManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.is_active = False
        self.keyboard_thread = None
        self.mouse_shake_timer = None
        self.overlay_widget = None
        self.audio_thread = None
        self.popup_timer = None
        self.active_popups = []  # Keep track of all popups
        self.glitch_timer = None  # For screen glitching
        self.temp_files = []  # Keep track of temporary files for cleanup
        
        # Initialize pygame mixer for audio
        try:
            pygame.mixer.init()
            self.audio_available = True
        except:
            self.audio_available = False
            print("⚠️ Audio not available for troll mode")
    
    def activate_troll_mode(self):
        """Activate the ultimate troll mode! 👹"""
        if self.is_active:
            return
        
        print("🦹‍♀️ ACTIVATING TROLL MODE...")
        self.is_active = True
        
        # 1. Hide main window and system tray
        self.hide_application()
        
        # 2. Start keyboard hijacking
        self.start_keyboard_hijacking()
        
        # 3. Show permanent screen overlay
        self.show_screen_overlay()
        
        # 4. Start mouse cursor shaking
        self.start_mouse_shaking()
        
        # 5. Start audio loop
        self.start_audio_loop()
        
        # 6. Start random popup spam
        self.start_popup_spam()
        
        # 7. Start screen glitching
        self.start_screen_glitch()
        
        print("😈 TROLL MODE ACTIVATED! Only Task Manager can save you now...")
    
    def deactivate_troll_mode(self):
        """Deactivate troll mode (usually only called on app exit)"""
        if not self.is_active:
            return
        
        print("🛑 Deactivating troll mode...")
        self.is_active = False
        
        # Stop all troll activities
        self.stop_keyboard_hijacking()
        self.stop_mouse_shaking()
        self.hide_screen_overlay()
        self.stop_audio_loop()
        self.stop_popup_spam()
        self.stop_screen_glitch()
        
        # Clean up temporary files
        self.cleanup_temp_files()
        
        # Show application again
        self.show_application()
    
    def hide_application(self):
        """Hide the main window and system tray completely"""
        try:
            # Hide main window
            self.main_window.hide()
            
            # Hide system tray icon
            if hasattr(self.main_window, 'tray_icon'):
                self.main_window.tray_icon.hide()
            
            print("👻 Application hidden from user")
        except Exception as e:
            print(f"Error hiding application: {e}")
    
    def show_application(self):
        """Show the application again"""
        try:
            # Show system tray icon
            if hasattr(self.main_window, 'tray_icon'):
                self.main_window.tray_icon.show()
            
            # Show main window
            self.main_window.show()
            
            print("👋 Application restored")
        except Exception as e:
            print(f"Error showing application: {e}")
    
    def start_keyboard_hijacking(self):
        """Hijack all keyboard input to type 'uwu kawaii!!' instead"""
        def keyboard_hijack():
            try:
                # Block all keys and replace with our message
                target_text = "uwu kawaii!! i love you!! love!! "
                text_index = 0
                
                def on_key_event(event):
                    nonlocal text_index
                    
                    if not self.is_active:
                        return True  # Allow key through if not active
                    
                    if event.event_type == keyboard.KEY_DOWN:
                        # Type our troll message instead of the pressed key
                        if text_index < len(target_text):
                            char = target_text[text_index]
                            # Use threading to avoid blocking
                            threading.Thread(
                                target=lambda: keyboard.write(char), 
                                daemon=True
                            ).start()
                            text_index += 1
                        else:
                            # Reset to beginning of message
                            text_index = 0
                        
                        # Block the original key
                        return False  # Suppress original key
                
                # Hook all keyboard events
                keyboard.hook(on_key_event, suppress=True)
                
                # Keep the hook active while troll mode is on
                while self.is_active:
                    time.sleep(0.1)
                
                # Unhook when done
                keyboard.unhook_all()
                
            except Exception as e:
                print(f"Error in keyboard hijacking: {e}")
        
        self.keyboard_thread = threading.Thread(target=keyboard_hijack, daemon=True)
        self.keyboard_thread.start()
        print("⌨️ Keyboard hijacking started")
    
    def stop_keyboard_hijacking(self):
        """Stop keyboard hijacking"""
        try:
            keyboard.unhook_all()
            if self.keyboard_thread:
                self.keyboard_thread = None
            print("⌨️ Keyboard hijacking stopped")
        except Exception as e:
            print(f"Error stopping keyboard hijacking: {e}")
    
    def show_screen_overlay(self):
        """Show a permanent kawaii overlay over the entire screen"""
        try:
            self.overlay_widget = TrollOverlayWidget()
            self.overlay_widget.show()
            print("🖼️ Screen overlay activated")
        except Exception as e:
            print(f"Error showing screen overlay: {e}")
    
    def hide_screen_overlay(self):
        """Hide the screen overlay"""
        try:
            if self.overlay_widget:
                self.overlay_widget.hide()
                self.overlay_widget.deleteLater()
                self.overlay_widget = None
            print("🖼️ Screen overlay hidden")
        except Exception as e:
            print(f"Error hiding screen overlay: {e}")
    
    def start_mouse_shaking(self):
        """Make the mouse cursor shake violently like it's having a seizure"""
        def shake_cursor():
            if not self.is_active:
                return
            
            try:
                # Get current cursor position
                current_pos = QCursor.pos()
                
                # Add violent random shake - much stronger than before
                shake_x = random.randint(-15, 15)  # Increased from -3,3 to -15,15
                shake_y = random.randint(-15, 15)  # Much more violent shaking
                
                # Move cursor violently
                QCursor.setPos(current_pos.x() + shake_x, current_pos.y() + shake_y)
            except Exception as e:
                print(f"Error shaking cursor: {e}")
        
        # Shake cursor every 25ms for ultra jittery effect (increased from 50ms)
        self.mouse_shake_timer = QTimer()
        self.mouse_shake_timer.timeout.connect(shake_cursor)
        self.mouse_shake_timer.start(25)  # Faster and more violent
        print("mouse shaking started")
    
    def stop_mouse_shaking(self):
        """Stop mouse cursor shaking"""
        try:
            if self.mouse_shake_timer:
                self.mouse_shake_timer.stop()
                self.mouse_shake_timer = None
            print("🐭 Mouse shaking stopped")
        except Exception as e:
            print(f"Error stopping mouse shaking: {e}")
    
    def start_audio_loop(self):
        """Start looping custom audio file"""
        if not self.audio_available:
            print("🔇 Audio not available")
            return
        
        def audio_loop():
            try:
                # Try to load and play custom audio file using resource helper
                audio_temp_path = extract_resource_to_temp("audio.mp3")
                if audio_temp_path:
                    print(f"🎵 Loading custom audio from embedded resource")
                    self.temp_files.append(audio_temp_path)
                    
                    pygame.mixer.music.load(audio_temp_path)
                    pygame.mixer.music.set_volume(0.7)  # volume to 70
                    
                    # Loop the audio indefinitely while troll mode is active
                    pygame.mixer.music.play(-1)  # -1 means loop forever
                    
                    while self.is_active:
                        time.sleep(0.5)
                        # Check if music stopped and restart if needed
                        if not pygame.mixer.music.get_busy() and self.is_active:
                            pygame.mixer.music.play(-1)
                    
                    # Stop music when troll mode ends
                    pygame.mixer.music.stop()
                    print("🎵 Custom audio stopped")
                else:
                    print(f"⚠️ Audio file 'audio.mp3' not found, falling back to system beeps")
                    # Fallback to system beeps if audio file not found
                    while self.is_active:
                        try:
                            import winsound
                            # Fallback beep pattern
                            frequencies = [800, 1000, 1200, 1000, 600, 1400]  
                            for freq in frequencies:
                                if not self.is_active:
                                    break
                                winsound.Beep(freq, 150)
                                time.sleep(0.05)
                            time.sleep(0.5)
                        except ImportError:
                            time.sleep(2)
                        
            except Exception as e:
                print(f"Error in audio loop: {e}")
        
        self.audio_thread = threading.Thread(target=audio_loop, daemon=True)
        self.audio_thread.start()
        print("🔊 Audio loop started")
    
    def stop_audio_loop(self):
        """Stop audio loop"""
        try:
            # Stop pygame music
            if self.audio_available:
                pygame.mixer.music.stop()
            
            if self.audio_thread:
                self.audio_thread = None
            print("🔇 Audio loop stopped")
        except Exception as e:
            print(f"Error stopping audio loop: {e}")
    
    def start_popup_spam(self):
        """Start spawning random popup messages every 2-5 seconds"""
        def show_random_popup():
            if not self.is_active:
                return
            
            try:
                # Random kawaii/chaotic messages
                popup_messages = [
                    "uwu Notice me senpai! (◕‿◕)",
                    "KAWAII OVERLOAD! 🌸✨💕",
                    "You've been uwuified! There's no escape! >:3",
                    "owo what's this? *nuzzles your computer*",
                    "Troll mode is the best mode! uwu",
                    "Your computer is now 100% more kawaii! ✨",
                    "ERROR: Too much cuteness detected! 💕",
                    "Press Alt+F4 to make it stop! (just kidding uwu)",
                    "🦄 MAGICAL CHAOS ACTIVATED 🦄",
                    "This is what happens when you click random buttons! uwu",
                    "Congratulations! You're being trolled! 🎉",
                    "WARNING: Excessive kawaii levels detected! (≧◡≦)",
                    "Your productivity has been successfully destroyed! uwu",
                    "Remember: You asked for this! 😈",
                    "Friendship ended with normal computer, now uwu is my best friend!",
                    "Task Manager is your only savior now! uwu",
                    "🌈 RAINBOW CHAOS MODE ENGAGED 🌈",
                    "Beep boop! Your computer is now kawaii! owo",
                    "System Error: Too much uwu detected! 💖",
                    "This popup will self-destruct in... never! uwu"
                ]
                
                # Show popup with random message
                message = random.choice(popup_messages)
                popup = TrollPopupWidget(message)
                popup.show()
                
                # Keep track of the popup so we can close it later
                self.active_popups.append(popup)
                
                print(f"💥 Showed popup: {message}")
                
            except Exception as e:
                print(f"Error showing popup: {e}")
        
        def popup_timer_callback():
            if self.is_active:
                show_random_popup()
                # Schedule next popup in 2-5 seconds
                next_interval = random.randint(2000, 5000)  # 2-5 seconds in milliseconds
                self.popup_timer.singleShot(next_interval, popup_timer_callback)
        
        # Start the popup spam
        self.popup_timer = QTimer()
        first_interval = random.randint(2000, 5000)  # First popup in 2-5 seconds
        self.popup_timer.singleShot(first_interval, popup_timer_callback)
        print("💥 Random popup spam started")
    
    def stop_popup_spam(self):
        """Stop the popup spam and close all existing popups"""
        try:
            if self.popup_timer:
                self.popup_timer.stop()
                self.popup_timer = None
            
            # Close all active popups
            for popup in self.active_popups:
                try:
                    popup.close()
                    popup.deleteLater()
                except:
                    pass  # Ignore if popup already closed
            
            self.active_popups.clear()
            print("💥 Popup spam stopped and all popups closed")
        except Exception as e:
            print(f"Error stopping popup spam: {e}")
    
    def start_screen_glitch(self):
        """Start random screen glitching effects"""
        try:
            if self.glitch_timer:
                return  # Already running
            
            def create_glitch():
                if not self.is_active:
                    return
                
                try:
                    # Create a temporary glitch overlay
                    glitch_overlay = GlitchOverlayWidget()
                    glitch_overlay.show()
                    
                    # Remove glitch after short duration (100-300ms)
                    glitch_duration = random.randint(100, 300)
                    QTimer.singleShot(glitch_duration, glitch_overlay.close)
                    
                    print("⚡ Screen glitch triggered!")
                    
                except Exception as e:
                    print(f"Error creating glitch: {e}")
            
            def glitch_timer_callback():
                if self.is_active:
                    create_glitch()
                    # Schedule next glitch in 3-10 seconds
                    next_interval = random.randint(3000, 10000)
                    self.glitch_timer.singleShot(next_interval, glitch_timer_callback)
            
            # Start the glitch timer
            self.glitch_timer = QTimer()
            first_interval = random.randint(5000, 8000)  # First glitch in 5-8 seconds
            self.glitch_timer.singleShot(first_interval, glitch_timer_callback)
            print("⚡ Screen glitch system activated")
            
        except Exception as e:
            print(f"Error starting screen glitch: {e}")
    
    def stop_screen_glitch(self):
        """Stop the screen glitching"""
        try:
            if self.glitch_timer:
                self.glitch_timer.stop()
                self.glitch_timer = None
            print("⚡ Screen glitch system stopped")
        except Exception as e:
            print(f"Error stopping screen glitch: {e}")
    
    def cleanup_temp_files(self):
        """Clean up any temporary files created during troll mode"""
        try:
            for temp_path in self.temp_files:
                cleanup_temp_file(temp_path)
            self.temp_files.clear()
        except Exception as e:
            print(f"Error cleaning up temp files: {e}")

class TrollOverlayWidget(QWidget):
    """Custom overlay widget that shows an image from overlay.png"""
    
    def __init__(self):
        super().__init__()
        self.setup_overlay()
        self.overlay_image = None
        self.load_overlay_image()
        
        # Animation for floating effects (optional)
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.start(100)
        self.animation_frame = 0
    
    def setup_overlay(self):
        """Setup the overlay widget"""
        # Make it cover all screens
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        self.setGeometry(geometry)
        
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.Tool |
            Qt.WindowTransparentForInput  # Allow clicks to pass through
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Create floating content
        self.kawaii_texts = [
            "uwu", "owo", "♡", "✨", "🌸", "💕", "kawaii!!", 
            "(◕‿◕)", "≧◡≦", "( ˘ ³˘)♥", "٩(◕‿◕)۶"
        ]
        
        # Random positions for floating text
        self.floating_texts = []
        for i in range(15):  # 15 floating kawaii elements
            self.floating_texts.append({
                'text': random.choice(self.kawaii_texts),
                'x': random.randint(0, geometry.width() - 100),
                'y': random.randint(0, geometry.height() - 50),
                'dx': random.uniform(-1, 1),
                'dy': random.uniform(-1, 1),
                'color': QColor(random.randint(200, 255), random.randint(100, 255), random.randint(200, 255))
            })
    
    def load_overlay_image(self):
        """Load the overlay image from overlay.png using resource helper"""
        try:
            overlay_path = get_resource_path("overlay.png")
            if overlay_path:
                self.overlay_image = QPixmap(overlay_path)
                print(f"🖼️ Loaded overlay image from embedded resource")
            else:
                print(f"⚠️ Overlay image 'overlay.png' not found, using text fallback")
                self.overlay_image = None
        except Exception as e:
            print(f"Error loading overlay image: {e}")
            self.overlay_image = None
    
    def paintEvent(self, event):
        """Paint the overlay: pink background + centered image + floating kawaii"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw semi-transparent pink overlay (old style)
        painter.fillRect(self.rect(), QColor(255, 182, 193, 50))  # Light pink with low alpha
        
        # Draw floating kawaii text
        for item in self.floating_texts:
            painter.setPen(item['color'])
            painter.setFont(QFont("Arial", 16, QFont.Bold))
            painter.drawText(int(item['x']), int(item['y']), item['text'])
        
        # Draw the custom overlay image centered if available
        if self.overlay_image and not self.overlay_image.isNull():
            screen_rect = self.rect()
            image_rect = self.overlay_image.rect()
            x = (screen_rect.width() - image_rect.width()) // 2
            y = (screen_rect.height() - image_rect.height()) // 2
            painter.drawPixmap(x, y, self.overlay_image)
    
    def animate(self):
        """Animate the floating kawaii elements"""
        geometry = self.geometry()
        
        for item in self.floating_texts:
            # Move the text
            item['x'] += item['dx']
            item['y'] += item['dy']
            
            # Bounce off edges
            if item['x'] <= 0 or item['x'] >= geometry.width() - 100:
                item['dx'] *= -1
            if item['y'] <= 20 or item['y'] >= geometry.height() - 50:
                item['dy'] *= -1
            
            # Occasionally change text
            if random.random() < 0.01:  # 1% chance per frame
                item['text'] = random.choice(self.kawaii_texts)
        
        self.animation_frame += 1
        self.update()  # Trigger repaint

class TrollPopupWidget(QWidget):
    """Annoying popup widget that shows random messages"""
    
    def __init__(self, message):
        super().__init__()
        self.message = message
        self.setup_popup()
    
    def setup_popup(self):
        """Setup the popup window"""
        width = random.randint(300, 500)
        height = random.randint(150, 250)
        self.setFixedSize(width, height)
        
        # Random position on screen
        screen = QApplication.primaryScreen().availableGeometry()
        x = random.randint(0, max(0, screen.width() - width))
        y = random.randint(0, max(0, screen.height() - height))
        self.move(x, y)
        
        # Window settings - make them more annoying and harder to close
        self.setWindowTitle("uwu Notification! ✨")
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.Dialog | 
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        # Create label with message
        from PyQt5.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setStyleSheet("""
            QLabel {
                color: #ff69b4;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: transparent;
            }
        """)
        layout.addWidget(message_label)
        
        # Kawaii styling
        self.setStyleSheet("""
            QWidget {
                background-color: #ffe0f0;
                border: 3px solid #ff69b4;
                border-radius: 15px;
            }
        """)

class GlitchOverlayWidget(QWidget):
    """Creates a temporary glitch effect overlay"""
    
    def __init__(self):
        super().__init__()
        self.setup_glitch()
        
    def setup_glitch(self):
        """Setup the glitch overlay"""
        # Make it fullscreen
        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(screen)
        
        # Window settings
        self.setWindowTitle("")
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Random glitch color
        glitch_colors = [
            "rgba(255, 0, 0, 80)",    # Red glitch
            "rgba(0, 255, 0, 80)",    # Green glitch  
            "rgba(0, 0, 255, 80)",    # Blue glitch
            "rgba(255, 255, 0, 80)",  # Yellow glitch
            "rgba(255, 0, 255, 80)",  # Magenta glitch
            "rgba(0, 255, 255, 80)",  # Cyan glitch
        ]
        
        glitch_color = random.choice(glitch_colors)
        
        # Random glitch pattern
        glitch_patterns = [
            # Horizontal lines
            f"""
            QWidget {{
                background-color: {glitch_color};
                background-image: repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 2px,
                    rgba(255,255,255,50) 2px,
                    rgba(255,255,255,50) 4px
                );
            }}
            """,
            # Vertical lines
            f"""
            QWidget {{
                background-color: {glitch_color};
                background-image: repeating-linear-gradient(
                    90deg,
                    transparent,
                    transparent 3px,
                    rgba(255,255,255,60) 3px,
                    rgba(255,255,255,60) 6px
                );
            }}
            """,
            # Diagonal stripes
            f"""
            QWidget {{
                background-color: {glitch_color};
                background-image: repeating-linear-gradient(
                    45deg,
                    transparent,
                    transparent 5px,
                    rgba(255,255,255,40) 5px,
                    rgba(255,255,255,40) 10px
                );
            }}
            """,
            # Random static effect
            f"""
            QWidget {{
                background-color: {glitch_color};
                background-image: 
                    radial-gradient(circle at 20% 50%, rgba(255,255,255,30) 1px, transparent 1px),
                    radial-gradient(circle at 80% 50%, rgba(255,255,255,30) 1px, transparent 1px),
                    radial-gradient(circle at 40% 20%, rgba(255,255,255,30) 1px, transparent 1px),
                    radial-gradient(circle at 60% 80%, rgba(255,255,255,30) 1px, transparent 1px);
                background-size: 50px 50px, 30px 30px, 70px 70px, 40px 40px;
            }}
            """
        ]
        
        pattern = random.choice(glitch_patterns)
        self.setStyleSheet(pattern)

def show_troll_mode_warning():
    """Show warning dialog before enabling troll mode"""
    from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFont, QPixmap, QPainter
    
    class TrollWarningDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("⚠️ TROLL MODE WARNING ⚠️")
            
            # Better window flags for proper movement and scaling
            self.setWindowFlags(
                Qt.Dialog | 
                Qt.WindowTitleHint | 
                Qt.WindowCloseButtonHint |
                Qt.WindowSystemMenuHint |
                Qt.MSWindowsFixedSizeDialogHint
            )
            
            # Set minimum size instead of fixed size for better scaling
            self.setMinimumSize(550, 450)  # Made wider: 480 -> 550
            self.setMaximumSize(700, 550)  # Allow more width: 600 -> 700
            self.resize(550, 450)  # Default size wider: 480 -> 550
            
            self.result_value = False
            
            # Center the dialog on screen
            self.center_on_screen()
            
            # Set up the UI
            self.setup_ui()
        
        def center_on_screen(self):
            """Center the dialog on the primary screen"""
            try:
                from PyQt5.QtWidgets import QApplication
                screen = QApplication.primaryScreen().availableGeometry()
                size = self.geometry()
                x = (screen.width() - size.width()) // 2
                y = (screen.height() - size.height()) // 2
                self.move(x, y)
            except:
                pass  # Fallback to default positioning
            
        def setup_ui(self):
            # Main layout with better margins and spacing
            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(20, 20, 20, 20)
            main_layout.setSpacing(15)
            
            # Header with warning icon and title
            header_layout = QHBoxLayout()
            header_layout.setSpacing(12)
            
            # Warning icon label - fixed size to prevent scaling issues
            icon_label = QLabel("⚠️")
            icon_label.setStyleSheet("font-size: 42px; color: #ff6666;")
            icon_label.setFixedSize(50, 50)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setScaledContents(False)  # Prevent scaling glitches
            header_layout.addWidget(icon_label)
            
            # Title with better text handling
            title_label = QLabel("DANGER: TROLL MODE ACTIVATION")
            title_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #ff6666;
                margin-top: 6px;
                padding: 4px;
            """)
            title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            title_label.setWordWrap(False)  # Prevent text wrapping issues
            header_layout.addWidget(title_label, 1)
            
            main_layout.addLayout(header_layout)
            
            # Warning text with better layout handling
            warning_text = """<b style="color: #ff6666;">WARNING!</b> You are about to activate <b>TROLL MODE</b>!

<br><br><b>This will:</b>
<br>• 🫥 <b>HIDE</b> this app completely (system tray too!)
<br>• ⌨️ <b>HIJACK</b> your keyboard - everything types "uwu kawaii!!"
<br>• 🖼️ Show <b>PERMANENT</b> kawaii overlay on your screen
<br>• 🐭 Make your <b>MOUSE SHAKE</b> violently
<br>• 🔊 Play <b>ANNOYING SOUNDS</b> on repeat
<br>• 💥 Spawn <b>RANDOM POPUPS</b> every 2-5 seconds

<br><br><b style="color: #ff6666;">⚠️ THE ONLY WAY TO STOP IT:</b>
<br>Kill "uwuifier.exe" in Task Manager!

<br><br><b>Are you ABSOLUTELY SURE you want to continue?</b>

<br><br><span style="color: #888888; font-size: 10px;">This is meant for pranking friends. Use responsibly! 😈</span>"""
            
            # Create scrollable text area to prevent layout issues
            text_label = QLabel(warning_text)
            text_label.setTextFormat(Qt.RichText)
            text_label.setWordWrap(True)
            text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            text_label.setSizePolicy(
                text_label.sizePolicy().Expanding, 
                text_label.sizePolicy().Expanding
            )
            text_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 12px;
                    line-height: 1.5;
                    padding: 12px;
                    background-color: rgba(255, 255, 255, 0.08);
                    border-radius: 6px;
                    margin: 2px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
            """)
            text_label.setMinimumHeight(220)
            text_label.setMaximumHeight(300)  # Prevent excessive growth
            main_layout.addWidget(text_label, 1)  # Allow expansion
            
            # Button layout with fixed sizing
            button_layout = QHBoxLayout()
            button_layout.setSpacing(12)
            button_layout.setContentsMargins(10, 10, 10, 0)
            button_layout.addStretch()
            
            # No button with larger size to fit text properly
            no_btn = QPushButton("🛑 no lol")
            no_btn.clicked.connect(self.reject_troll)
            no_btn.setFixedSize(160, 40)  # Wider: 150 -> 160
            no_btn.setStyleSheet("""
                QPushButton {
                    background-color: #404040;
                    color: white;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #505050;
                }
                QPushButton:pressed {
                    background-color: #353535;
                }
            """)
            button_layout.addWidget(no_btn)
            
            # Yes button with larger size to fit text properly
            yes_btn = QPushButton("😈 YES, ACTIVATE CHAOS!")
            yes_btn.clicked.connect(self.accept_troll)
            yes_btn.setFixedSize(180, 40)  # Much wider: 150 -> 180
            yes_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff1493;
                    color: white;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #dc143c;
                }
                QPushButton:pressed {
                    background-color: #b71c3c;
                }
            """)
            button_layout.addWidget(yes_btn)
            button_layout.addStretch()
            
            main_layout.addLayout(button_layout)
            
            # Set improved dark theme with better stability
            self.setStyleSheet("""
                QDialog {
                    background-color: #1e1e1e;
                    color: white;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    border: 2px solid #333333;
                    border-radius: 8px;
                }
                QLabel {
                    color: white;
                    background: transparent;
                }
                QVBoxLayout {
                    margin: 0px;
                }
                QHBoxLayout {
                    margin: 0px;
                }
            """)
            
            # Ensure proper sizing after setup
            self.adjustSize()
            self.setMinimumSize(self.size())  # Lock minimum to current size
        
        def accept_troll(self):
            self.result_value = True
            self.accept()
            
        def reject_troll(self):
            self.result_value = False
            self.reject()
    
    # Show the dialog
    dialog = TrollWarningDialog()
    dialog.exec_()
    return dialog.result_value
