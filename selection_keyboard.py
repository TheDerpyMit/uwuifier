"""
Selection-based UwUifier
Uses a customizable shortcut to uwuify currently selected text
"""
import threading
import time
from typing import Optional, Callable
import uwuify
import keyboard
import pyperclip

class SelectionUwuTextProcessor:
    """Processes selected text through uwuifier"""
    
    def __init__(self, config_manager=None):
        self.enabled = True
        self.config_manager = config_manager
        
    def process_text(self, text: str) -> str:
        """Process text through uwuifier with configured flags"""
        if not text.strip():
            return text
            
        try:
            # Get uwuify flags from config
            flags = uwuify.UwuifyFlag.NONE
            
            if self.config_manager:
                if self.config_manager.get('smiley', False):
                    flags |= uwuify.UwuifyFlag.SMILEY
                if self.config_manager.get('yu', False):
                    flags |= uwuify.UwuifyFlag.YU
                if self.config_manager.get('stutter', False):
                    flags |= uwuify.UwuifyFlag.STUTTER
                if self.config_manager.get('nouwu', False):
                    flags |= uwuify.UwuifyFlag.NOUWU
            
            # Use uwuify to transform the text with flags
            return uwuify.uwu(text, flags=flags)
        except Exception:
            return text

class SelectionKeyboardHook:
    """Keyboard hook that uwuifies selected text when shortcut is pressed"""
    
    def __init__(self, text_processor: SelectionUwuTextProcessor, overlay_callback: Optional[Callable] = None):
        self.text_processor = text_processor
        self.overlay_callback = overlay_callback
        self.running = False
        self.hotkey = 'ctrl+shift+u'  # Default shortcut
        self.processing = False
        
    def start(self):
        """Start the keyboard hook"""
        if self.running:
            return
            
        self.running = True
        
        try:
            # Set up hotkey for uwuifying selected text
            try:
                keyboard.add_hotkey(self.hotkey, self._uwuify_selection)
                print(f"UwUify shortcut '{self.hotkey}' set up successfully")
            except Exception as hotkey_error:
                print(f"Error setting hotkey: {hotkey_error}")
            
            print("Selection-based keyboard hook started successfully")
            
        except Exception as e:
            print(f"Failed to start keyboard hook: {e}")
            self.running = False
    
    def stop(self):
        """Stop the keyboard hook"""
        self.running = False
        try:
            keyboard.unhook_all()
            print("Keyboard hook stopped")
        except:
            pass
    
    def _uwuify_selection(self):
        """UwUify the currently selected text"""
        if not self.text_processor.enabled:
            # Show overlay for disabled state
            if self.overlay_callback:
                self.overlay_callback("uwuifier is disabled 😿")
            return
        
        # Prevent rapid multiple calls
        if self.processing:
            return
            
        self.processing = True
        
        try:
            print("🔄 Processing selected text...")
            
            # Store current clipboard content
            try:
                original_clipboard = pyperclip.paste()
            except:
                original_clipboard = ""
            
            # Longer wait for clipboard operations to work across more apps
            time.sleep(0.05)
            
            # Copy selected text to clipboard with multiple attempts
            selected_text = ""
            for attempt in range(3):
                keyboard.press_and_release('ctrl+c')
                time.sleep(0.15)  # Increased wait time
                
                # Get the selected text
                try:
                    selected_text = pyperclip.paste()
                except:
                    selected_text = ""
                
                # Check if we got new text (different from original clipboard)
                if selected_text and selected_text != original_clipboard:
                    break
                    
                if attempt == 2:  # Last attempt failed
                    print("⚠️ No text selected or clipboard unchanged after 3 attempts")
                    if self.overlay_callback:
                        self.overlay_callback("no text selected ⚠️")
                    return
            
            print(f"📝 Selected text: '{selected_text}'")
            
            # UwUify the text using the library function on the WHOLE text
            uwuified_text = self.text_processor.process_text(selected_text)
            
            print(f"🦄 UwUified text: '{uwuified_text}'")
            
            # Put uwuified text in clipboard
            pyperclip.copy(uwuified_text)
            time.sleep(0.1)  # Wait for clipboard to be set
            
            # Paste the uwuified text (replaces selection)
            keyboard.press_and_release('ctrl+v')
            
            # Show success overlay
            if self.overlay_callback:
                self.overlay_callback("text uwuified ✅")
            
            # Restore original clipboard after a delay (silently)
            def restore_clipboard():
                time.sleep(3)
                try:
                    pyperclip.copy(original_clipboard)
                except:
                    pass
            
            threading.Thread(target=restore_clipboard, daemon=True).start()
            
        except Exception as e:
            print(f"Error processing selection: {e}")
            if self.overlay_callback:
                self.overlay_callback("error uwuifying text ❌")
        finally:
            # Use a longer delay to prevent rapid successive calls
            def reset_processing():
                time.sleep(1.0)  # Longer delay to prevent multiple rapid calls
                self.processing = False
            
            threading.Thread(target=reset_processing, daemon=True).start()
    
    def set_hotkey(self, new_hotkey: str):
        """Update the hotkey"""
        try:
            # Remove old hotkey
            try:
                keyboard.unhook_all_hotkeys()
            except AttributeError:
                keyboard.unhook_all()
            
            self.hotkey = new_hotkey
            
            # Add new hotkey
            try:
                keyboard.add_hotkey(self.hotkey, self._uwuify_selection)
                print(f"Hotkey updated to: {new_hotkey}")
            except Exception as hotkey_error:
                print(f"Hotkey setup error: {hotkey_error}")
            
        except Exception as e:
            print(f"Error setting hotkey: {e}")
    
    def get_hotkey(self):
        return self.hotkey
