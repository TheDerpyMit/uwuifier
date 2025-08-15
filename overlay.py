"""
Overlay Manager for the app
"""
import sys
import random
import math
from typing import Optional, Callable, List
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect, pyqtProperty
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QPainterPath, QBrush, QPen, QLinearGradient

class FloatingElement:
    def __init__(self, text: str, x: float, y: float, size: int = 16):
        self.text = text
        self.x = x
        self.y = y
        self.original_y = y
        self.size = size
        self.time_offset = random.uniform(0, math.pi * 2)
        self.float_amplitude = random.uniform(10, 20)
        self.float_speed = random.uniform(0.02, 0.05)

class KawaiiOverlayWidget(QWidget):
    def __init__(self, text: str, position: tuple, duration: int = 2000):
        super().__init__()
        self.text = text
        self.duration = duration
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_time = 0
        
        # Minimal floating elements for clean look
        self.floating_elements = [
            FloatingElement("✨", -15, -8, 10),   # Left sparkle
            FloatingElement("✨", 265, -8, 10),   # Right sparkle  
            FloatingElement("💫", 135, -12, 11),  # Center star
        ]
        
        self.setup_overlay(position)
        self.start_animations()
        
    def setup_overlay(self, position):
        # Window settings - make it stay on top and transparent
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.Tool |
            Qt.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Set compact size for top right corner
        self.setFixedSize(200, 40)  # Wider and more spacious
        self.move(position[0], position[1])  # Use exact position
        
    def paintEvent(self, event):
        """Pink kawaii-themed transparent overlay design"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Pink gradient background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(255, 182, 193, 180))  # Light pink
        gradient.setColorAt(1, QColor(255, 105, 180, 180))  # Hot pink
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(255, 20, 147, 120), 2))  # Deep pink border
        
        # Draw rounded rectangle
        rect = QRect(2, 2, self.width() - 4, self.height() - 4)
        painter.drawRoundedRect(rect, 10, 10)
        
        # Draw text with shadow for better readability
        font = QFont("Arial", 9, QFont.Normal)
        painter.setFont(font)
        
        # Text shadow
        painter.setPen(QPen(QColor(0, 0, 0, 100)))
        text_rect_shadow = QRect(5, 5, self.width() - 8, self.height() - 8)
        painter.drawText(text_rect_shadow, Qt.AlignCenter, self.text)
        
        # Main text in white
        painter.setPen(QPen(QColor(255, 255, 255, 240)))
        text_rect = QRect(4, 4, self.width() - 8, self.height() - 8)
        painter.drawText(text_rect, Qt.AlignCenter, self.text)
            
    def start_animations(self):
        """Start the kawaii animations"""
        self.animation_timer.start(16)  # ~60 FPS
        
        # Auto-close after duration
        QTimer.singleShot(self.duration, self.fade_out)
        
    def update_animation(self):
        """Update animation frame"""
        self.animation_time += 1
        self.update()  # Trigger repaint
        
    def fade_out(self):
        """Beautiful fade out animation"""
        self.animation_timer.stop()
        
        # Create fade out animation
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_animation.finished.connect(self.close)
        self.fade_animation.start()

class EnhancedOverlayManager:
    """Enhanced overlay manager with beautiful kawaii effects"""
    
    def __init__(self):
        self.active_overlays: List[KawaiiOverlayWidget] = []
        
    def show_overlay(self, text: str, position: tuple = None, duration: int = 2000):
        """Show a beautiful kawaii overlay with animations"""
        try:
            if not position:
                # Position in top right corner with better padding
                screen = QApplication.primaryScreen().availableGeometry()
                position = (
                    screen.width() - 290,
                    screen.y() + 30
                )
            
            # Create overlay
            overlay = KawaiiOverlayWidget(text, position, duration)
            overlay.show()
            
            # Track active overlay
            self.active_overlays.append(overlay)
            
            # Remove from list when closed
            QTimer.singleShot(duration + 600, lambda: self.remove_overlay(overlay))
            
            print(f"✨ Showed overlay: {text}")
            
        except Exception as e:
            print(f"Error showing overlay: {e}")
    
    def remove_overlay(self, overlay):
        """Remove overlay from tracking"""
        try:
            if overlay in self.active_overlays:
                self.active_overlays.remove(overlay)
        except Exception as e:
            print(f"Error removing overlay: {e}")
    
    def clear_all_overlays(self):
        """Clear all active overlays with fade effect"""
        try:
            for overlay in self.active_overlays[:]:
                overlay.fade_out()
            self.active_overlays.clear()
        except Exception as e:
            print(f"Error clearing overlays: {e}")
    
    def show_conversion_feedback(self, original_text: str, uwu_text: str):
        """Show conversion feedback with before/after in top right corner"""
        try:
            # Show overlays stacked vertically in top right
            screen = QApplication.primaryScreen().availableGeometry()
            pos1 = (screen.width() - 300, screen.y() + 20)      # Top overlay
            pos2 = (screen.width() - 300, screen.y() + 100)     # Second overlay  
            pos3 = (screen.width() - 220, screen.y() + 60)      # Center overlay
            
            # Show sequence of overlays
            self.show_overlay(f"Original: {original_text[:15]}...", pos1, 1500)
            QTimer.singleShot(800, lambda: self.show_overlay(f"UwU'd: {uwu_text[:15]}...", pos2, 2000))
            QTimer.singleShot(1200, lambda: self.show_overlay("✨ Kawaii! ✨", pos3, 1500))
            
        except Exception as e:
            print(f"Error showing conversion feedback: {e}")
    
    def show_enabled_overlay(self):
        """Show overlay when uwuifier is enabled"""
        try:
            screen = QApplication.primaryScreen().availableGeometry()
            position = (screen.width() - 200 - 10, screen.y() + 10)  # Top right with 10px padding
            self.show_overlay("😊 uwuifier enabled", position, 2000)
        except Exception as e:
            print(f"Error showing enabled overlay: {e}")
    
    def show_disabled_overlay(self):
        """Show overlay when uwuifier is disabled"""
        try:
            screen = QApplication.primaryScreen().availableGeometry()
            position = (screen.width() - 200 - 10, screen.y() + 10)  # Top right with 10px padding
            self.show_overlay("🥺 uwuifier disabled", position, 2000)
        except Exception as e:
            print(f"Error showing disabled overlay: {e}")
    
    def show_custom_overlay(self, message: str, position: tuple = None):
        """Show a custom overlay message"""
        try:
            if not position:
                screen = QApplication.primaryScreen().availableGeometry()
                position = (screen.width() - 200 - 10, screen.y() + 10)  # Top right with 10px padding
            
            self.show_overlay(f"✨ {message} ✨", position, 2500)
        except Exception as e:
            print(f"Error showing custom overlay: {e}")

# Maintain backward compatibility
OverlayWidget = KawaiiOverlayWidget
OverlayManager = EnhancedOverlayManager
