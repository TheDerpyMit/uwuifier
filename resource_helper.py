"""
Resource helper for handling embedded files in PyInstaller executables
"""
import os
import sys
import tempfile
import shutil

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource file.
    Works both in development and in PyInstaller bundled executable.
    For PyInstaller, files are extracted to a temporary directory.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        resource_path = os.path.join(base_path, relative_path)
        
        # Check if the file exists in the PyInstaller temp directory
        if os.path.exists(resource_path):
            return resource_path
            
    except AttributeError:
        # Not running in PyInstaller bundle
        pass
    
    # Development mode or file not found in bundle - check current directory
    current_dir_path = os.path.join(os.path.dirname(__file__), relative_path)
    if os.path.exists(current_dir_path):
        return current_dir_path
    
    # Check in the same directory as the script/executable
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir_path = os.path.join(script_dir, relative_path)
    if os.path.exists(script_dir_path):
        return script_dir_path
    
    # Last resort: check in current working directory
    cwd_path = os.path.join(os.getcwd(), relative_path)
    if os.path.exists(cwd_path):
        return cwd_path
        
    # File not found anywhere
    return None

def extract_resource_to_temp(relative_path):
    """
    Extract a resource to a temporary file and return the temp file path.
    This is useful for libraries that need actual file paths (like pygame.mixer.music.load).
    """
    resource_path = get_resource_path(relative_path)
    if not resource_path:
        return None
    
    # If it's already a regular file (not in PyInstaller temp), just return it
    try:
        if not hasattr(sys, '_MEIPASS') or not resource_path.startswith(sys._MEIPASS):
            return resource_path
    except AttributeError:
        return resource_path
    
    # Extract to a temporary file
    try:
        # Create temp file with same extension
        file_ext = os.path.splitext(relative_path)[1]
        temp_fd, temp_path = tempfile.mkstemp(suffix=file_ext)
        os.close(temp_fd)  # Close the file descriptor
        
        # Copy the resource to temp file
        shutil.copy2(resource_path, temp_path)
        
        print(f"📁 Extracted {relative_path} to temporary file: {temp_path}")
        return temp_path
        
    except Exception as e:
        print(f"❌ Failed to extract {relative_path}: {e}")
        return None

def cleanup_temp_file(temp_path):
    """Clean up a temporary file created by extract_resource_to_temp"""
    try:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"🧹 Cleaned up temp file: {temp_path}")
    except Exception as e:
        print(f"⚠️ Failed to cleanup temp file {temp_path}: {e}")
