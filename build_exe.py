"""
Build script to create an executable from the uwuifier Python app with embedded resources
"""
import os
import subprocess
import sys

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
        return True
    except ImportError:
        print("📦 Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install PyInstaller: {e}")
            return False

def create_executable():
    """Create the executable using PyInstaller with embedded resources"""
    print("🚀 Building uwuifier.exe with embedded resources...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create single executable file
        "--windowed",                   # Hide console window
        "--name=uwuifier",             # Name of the executable
        "--distpath=dist",             # Output directory
        "--workpath=build",            # Build directory
        "--specpath=.",                # Spec file location
        "--clean",                     # Clean build cache for fresh build
    ]
    
    # Add icon if it exists
    if os.path.exists("icon.ico"):
        cmd.extend(["--icon=icon.ico"])
        print("🎨 Using custom icon: icon.ico")
    else:
        print("⚠️  No icon.ico found - executable will use default icon")
    
    # Add version info for Windows
    version_info = '''# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
filevers=(1,0,0,0),
prodvers=(1,0,0,0),
mask=0x3f,
flags=0x0,
OS=0x40004,
fileType=0x1,
subtype=0x0,
date=(0, 0)
),
kids=[
StringFileInfo(
[
StringTable(
u'040904B0',
[StringStruct(u'CompanyName', u'uwuifier'),
StringStruct(u'FileDescription', u'uwuifier'),
StringStruct(u'FileVersion', u'1.0.0'),
StringStruct(u'InternalName', u'uwuifier'),
StringStruct(u'LegalCopyright', u'uwuifier'),
StringStruct(u'OriginalFilename', u'uwuifier.exe'),
StringStruct(u'ProductName', u'uwuifier'),
StringStruct(u'ProductVersion', u'1.0.0')])
]),
VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
]
)'''
    
    # Write version info to file
    with open("version_info.py", "w", encoding='utf-8') as f:
        f.write(version_info)
    
    cmd.extend(["--version-file=version_info.py"])
    
    # Add hidden imports for libraries that PyInstaller might miss
    hidden_imports = [
        "--hidden-import=pygame",
        "--hidden-import=keyboard", 
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=resource_helper"
    ]
    cmd.extend(hidden_imports)
    
    # EMBED FILES DIRECTLY INTO THE EXECUTABLE
    embedded_files = []
    
    # Embed config file
    if os.path.exists("config.json"):
        embedded_files.append("--add-data=config.json;.")
        print("📄 EMBEDDING config.json into executable")
    
    # Embed icon as data file (for runtime access)
    if os.path.exists("icon.ico"):
        embedded_files.append("--add-data=icon.ico;.")
        print("🎨 EMBEDDING icon.ico into executable")
    
    # EMBED AUDIO FILE - This will be inside the .exe file
    if os.path.exists("audio.mp3"):
        embedded_files.append("--add-data=audio.mp3;.")
        print("🎵 EMBEDDING audio.mp3 into executable")
    
    # EMBED OVERLAY IMAGE - This will be inside the .exe file  
    if os.path.exists("overlay.png"):
        embedded_files.append("--add-data=overlay.png;.")
        print("🖼️ EMBEDDING overlay.png into executable")
    
    # Add all embedded files to command
    cmd.extend(embedded_files)
    
    # Main script
    cmd.append("main.py")
    
    print(f"📝 PyInstaller Command: {' '.join(cmd)}")
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ Build completed successfully!")
        print(f"📁 Executable location: dist/uwuifier.exe")
        
        # Only copy icon.ico to dist for taskbar display (audio/overlay are embedded)
        import shutil
        
        if os.path.exists("icon.ico"):
            dist_icon_path = os.path.join("dist", "icon.ico")
            shutil.copy2("icon.ico", dist_icon_path)
            print("🎨 Copied icon.ico to dist folder for taskbar display")
        
        print("   📄 config.json, overlay and audio have been embedded.")
        
        # Check if file was created
        exe_path = os.path.join("dist", "uwuifier.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"✅ Final executable size: {size_mb:.1f} MB")
            return True
        else:
            print("❌ Executable file not found after build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Uh oh! The build failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    """Main build process"""
    print("😳 uwuifier Executable Builder")
    print("=" * 50)
    print("🎯 Building portable single-file executable")
    print("📦 Audio and images will be EMBEDDED inside the .exe")
    print("=" * 50)
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️  Not in virtual environment - make sure all dependencies are installed.")
    
    # Install PyInstaller
    if not install_pyinstaller():
        return
    
    # Check for required files
    if not os.path.exists("main.py"):
        print("❌ main.py not found in current directory")
        return
        
    if not os.path.exists("resource_helper.py"):
        print("❌ resource_helper.py not found - needed for embedded resources")
        return
    
    # Create executable
    if create_executable():
        print("\n" + "="*50)
        print("🎉 SUCCESS! Your uwuifier.exe is ready!")
        print("💡 Just distribute the single uwuifier.exe file")
        print("🚀 No external audio/image files needed - everything is embedded (besides .ico)")
        print("🎵 Troll mode audio will work from embedded resource")
        print("🖼️  Troll mode overlay will work from embedded resource")
        print("="*50)
    else:
        print("\n❌ Build failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
