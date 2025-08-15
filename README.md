# 🦄 uwuifier - The Ultimate Text Transformation Tool

<div align="center">
  <img src="icon.ico" alt="uwuifier Logo" width="128" height="128">
  
  [![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
  [![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green.svg)](https://pypi.org/project/PyQt5/)
  [![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
  [![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](README.md)
</div>

Transform any selected text into adorable uwu-speak with this feature-rich desktop application! uwuifier provides a seamless way to convert text with customizable hotkeys, beautiful overlays, and even includes a chaotic troll mode for maximum fun.

## ✨ Features

### 🎯 Core Features
- **🔥 Global Hotkey System**: Transform any selected text system-wide with customizable shortcuts
- **🌸 Beautiful Pink Overlays**: Elegant top-right notifications with kawaii styling  
- **⚙️ Advanced Settings**: Comprehensive configuration for uwuification behavior
- **💾 Persistent Configuration**: Settings saved automatically between sessions
- **📌 System Tray Integration**: Minimize to system tray with quick access
- **🖥️ Borderless Modern UI**: Clean, modern interface with custom styling

### 🔧 uwuification Options
- **😊 Smiley Mode**: Add cute emoticons to your text
- **🎌 Yu Mode**: Convert "you" to "yu" consistently  
- **😳 Stutter Mode**: Add adorable stuttering effects
- **🚫 NoUwU Mode**: Disable the classic "r/l→w" transformation

### ⌨️ Hotkey Customization
Choose from multiple hotkey combinations:
- `Ctrl + Shift + U` (default)
- `Ctrl + Shift + W`
- `Ctrl + Alt + U`
- `Ctrl + Alt + W`
- `Alt + Shift + U`
- `Alt + Shift + W`

### 🦹‍♀️ Troll Mode (Use Responsibly!)
**⚠️ WARNING: Ultimate Chaos Mode - Use Only for Pranks!**

When activated, troll mode unleashes complete mayhem:
- **⌨️ Keyboard Hijacking**: All keystrokes become "uwu kawaii!!" 
- **🖼️ Permanent Screen Overlay**: Kawaii image overlay across entire screen
- **🐭 Violent Mouse Shaking**: Cursor shakes uncontrollably
- **🔊 Endless Audio Loop**: Annoying sounds play continuously  
- **💥 Random Popup Spam**: Kawaii messages appear every 2-5 seconds
- **⚡ Screen Glitch Effects**: Random visual glitches for maximum chaos
- **👻 Complete App Hiding**: Application becomes invisible (even system tray!)

**🛑 The ONLY way to stop Troll Mode: Kill `uwuifier.exe` in Task Manager!**

## 🚀 Installation

### Option 1: Download Executable (Recommended)
1. Download the latest `uwuifierv1.zip` from the releases page
2. Unzip it to a folder and open the folder
3. Run the executable - no installation required!
4. All assets (audio, images) are embedded in the .exe file

### Option 2: Run from Source

#### Prerequisites
- Python 3.7 or higher
- pip package manager

#### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/uwuifier.git
   cd uwuifier
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## 📦 Building Executable

To compile your own executable with embedded resources:

### Prerequisites
```bash
pip install pyinstaller
```

### Build Process
```bash
python build_exe.py
```

This will create:
- `dist/uwuifier.exe` - Standalone executable
- All resources (audio, images) embedded inside the .exe
- Final executable size: ~50-60MB
- No external dependencies required for distribution

### Build Features
- **Single File Distribution**: Everything in one .exe file
- **Embedded Resources**: Audio and overlay images built-in
- **Windows Version Info**: Professional executable metadata
- **Custom Icon Support**: Branded application icon
- **Optimized Size**: Compressed for smaller file size

## 🎮 Usage Guide

### Basic Usage
1. **Launch the application** (uwuifier.exe or python main.py)
2. **Enable uwuifier** using the toggle button
3. **Select any text** anywhere on your computer
4. **Press your hotkey** (default: Ctrl+Shift+U)
5. **Watch the magic happen!** ✨

### Settings Configuration
- **Open Settings**: Click the gear icon in the main window
- **Customize Hotkey**: Choose from 6 different hotkey combinations
- **Configure uwuification**: Enable/disable smiley, yu, stutter, and nouwu modes
- **Visual Preferences**: Settings automatically save for next launch

### System Tray Usage
- **Minimize to Tray**: Close button minimizes to system tray
- **Quick Toggle**: Right-click tray icon to enable/disable quickly
- **Exit**: Right-click → Exit to fully close the application

## ⚠️ Troll Mode Safety Guide

**🚨 IMPORTANT: Troll Mode is designed for pranking friends and should be used responsibly!**

### Before Activating:
- ✅ Ensure you have access to Task Manager (Ctrl+Shift+Esc)
- ✅ Save any important work first
- ✅ Warn people nearby about potential chaos
- ✅ Make sure it's appropriate for the environment

### During Troll Mode:
- All keyboard input becomes "uwu kawaii!!"
- Mouse cursor will shake violently
- Random popups appear every 2-5 seconds
- Annoying audio plays continuously
- Screen overlay shows kawaii imagery
- Application becomes completely hidden

### Emergency Stop:
1. **Open Task Manager**: Ctrl+Shift+Esc (might require multiple attempts due to keyboard hijacking)
2. **Find uwuifier.exe** in the Processes tab
3. **End Task** to immediately stop all troll activities

## 📁 Project Structure

```
uwuifier/
├── main.py                 # Main application entry point
├── overlay.py              # Pink kawaii overlay system
├── selection_keyboard.py   # Global hotkey and text processing  
├── improved_settings.py    # Advanced settings dialog
├── troll_mode.py          # Chaos mode implementation
├── config_manager.py      # Configuration persistence
├── resource_helper.py     # Embedded resource management
├── build_exe.py          # Executable compilation script
├── requirements.txt      # Python dependencies
├── config.json          # User settings (auto-generated)
├── icon.ico            # Application icon
├── audio.mp3           # Troll mode audio (embedded)
├── overlay.png         # Troll mode image (embedded)
└── version_info.py     # Windows executable metadata
```

## 🛠️ Technical Details

### Dependencies
```
uwuify>=1.0.0        # Core text transformation library
PyQt5>=5.15.0        # GUI framework
pynput>=1.7.0        # Mouse control for troll mode  
keyboard>=0.13.0     # Global hotkey system
psutil>=5.8.0        # System process management
pyperclip>=1.8.0     # Clipboard operations
pygame>=2.0.0        # Audio playback system
```

### Architecture
- **PyQt5 GUI**: Modern, responsive interface with custom styling
- **Global Hotkeys**: System-wide keyboard hook for text transformation
- **Resource Embedding**: All assets compiled into single executable
- **Configuration Management**: JSON-based settings with automatic migration
- **Multi-threading**: Non-blocking operations for smooth performance
- **Memory Management**: Proper cleanup and resource disposal

### Compatibility
- **Operating System**: Windows 7/8/10/11
- **Python Version**: 3.7+ (for source code)
- **Architecture**: x64 (compiled executable)

## ❓ Troubleshooting

### Common Issues

**🔴 Hotkey not working:**
- Ensure no other application is using the same hotkey
- Try different hotkey combination in settings
- Run as administrator if needed

**🔴 Overlay not appearing:**
- Check if overlay is positioned off-screen
- Verify PyQt5 installation is complete
- Restart application to reset overlay position

**🔴 Troll mode won't stop:**
- Open Task Manager (Ctrl+Shift+Esc)
- Look for "uwuifier.exe" process
- End the process to immediately stop all activities

**🔴 Audio not playing in troll mode:**
- Ensure pygame is properly installed
- Check if audio.mp3 is embedded in executable
- Verify system audio is not muted

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **uwuify library**: Core text transformation functionality
- **PyQt5**: Excellent GUI framework
- **keyboard library**: Global hotkey system
- **pygame**: Audio playback capabilities
- **Troll Mode Audio**: [UwU Song, By Misutra.](https://www.youtube.com/watch?v=3sUGkclhvV8) Please support their work!

## ⚠️ Disclaimer

uwuifier is intended for entertainment purposes and harmless pranks among friends. The troll mode feature should be used responsibly and with consent. The developers are not responsible for any consequences arising from misuse of the troll mode functionality. Always ensure you have permission before pranking others and be mindful of appropriate environments for use. This whole project is made with Copilot, so expect shitty code if you're thinking of contributing.

---

<div align="center">
  <b>Made with 💕 and lots of uwu energy!</b><br>
  <i>Transform your text, spread the kawaii! 🌸</i>
</div>

