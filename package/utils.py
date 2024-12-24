import platform
import os

def base10_to_base64(num):
    if num == 0:
        return 'A'
    
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    base64_string = ""
    while num > 0:
        remainder = num % 64
        base64_string = base64_chars[remainder] + base64_string
        num = num // 64
    
    return base64_string

def check_platform():
    os_platform = platform.system()
    if os_platform == "Linux":
        # Check for Android-specific details if on Linux
        if "ANDROID_ARGUMENT" in os.environ:
            return "Android"
        else:
            return "Linux"
    elif os_platform == "Windows":
        return "Windows"
    elif os_platform == "Darwin":
        return "PC macOS"
    else:
        return "Unknown platform"


def MakeSample():
    return {"File Name":[f"file_{i+1}" for i in range(10)],
          'Sheet Name': [f"sheet_{i+1}" for i in range(10)],
          'Number Of Rows': [f"row_{i+1}" for i in range(10)], 
          'Number Of Columns': [f"col_{i+1}" for i in range(10)]}