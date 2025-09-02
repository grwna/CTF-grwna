#!/usr/bin/env python3
"""
Examples of running shell commands in Python
"""

import subprocess
import os
import sys

print("=== Different ways to run shell commands in Python ===\n")

# Method 1: subprocess.run() - RECOMMENDED (Python 3.5+)
print("1. Using subprocess.run() - Most recommended:")
try:
    result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
    print(f"Return code: {result.returncode}")
    print(f"Output:\n{result.stdout}")
    if result.stderr:
        print(f"Error:\n{result.stderr}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Method 2: subprocess.run() with shell=True
print("2. Using subprocess.run() with shell=True:")
try:
    result = subprocess.run('echo "Hello from shell"', shell=True, capture_output=True, text=True)
    print(f"Output: {result.stdout.strip()}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Method 3: subprocess.check_output() - For when you only need output
print("3. Using subprocess.check_output():")
try:
    output = subprocess.check_output(['whoami'], text=True)
    print(f"Current user: {output.strip()}")
except subprocess.CalledProcessError as e:
    print(f"Command failed with return code {e.returncode}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Method 4: subprocess.Popen() - For more control
print("4. Using subprocess.Popen() for real-time output:")
try:
    process = subprocess.Popen(['ping', '-c', '3', 'localhost'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, 
                              text=True)
    
    # Read output line by line
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(f"Ping output: {output.strip()}")
    
    # Get the return code
    rc = process.poll()
    print(f"Return code: {rc}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Method 5: os.system() - Simple but less secure (NOT recommended for production)
print("5. Using os.system() - Simple but less secure:")
return_code = os.system('echo "Hello from os.system"')
print(f"Return code: {return_code}")

print("\n" + "="*50 + "\n")

# Method 6: os.popen() - Gets output but deprecated
print("6. Using os.popen() - Deprecated but still works:")
with os.popen('date') as f:
    output = f.read()
    print(f"Current date: {output.strip()}")

print("\n" + "="*50 + "\n")

# Practical examples for security challenges
print("=== Practical examples for security challenges ===\n")

def run_command_safe(cmd_list):
    """Safely run a command and return output"""
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True, timeout=10)
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", -1
    except Exception as e:
        return "", str(e), -1

def run_command_with_input(cmd_list, input_data):
    """Run command with input data"""
    try:
        result = subprocess.run(cmd_list, input=input_data, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), -1

# Example: Get file permissions
print("7. Getting file permissions:")
stdout, stderr, rc = run_command_safe(['ls', '-la', __file__])
if rc == 0:
    print(f"File info:\n{stdout}")
else:
    print(f"Error: {stderr}")

print("\n" + "="*30 + "\n")

# Example: Running a binary with input
print("8. Running binary with input (example):")
# This would be useful for pwn challenges
# stdout, stderr, rc = run_command_with_input(['./binary'], b"AAAA\n")

print("\n" + "="*30 + "\n")

# Example: Environment variables
print("9. Running command with custom environment:")
env = os.environ.copy()
env['CUSTOM_VAR'] = 'hello_world'
try:
    result = subprocess.run(['env'], env=env, capture_output=True, text=True)
    # Look for our custom variable
    for line in result.stdout.split('\n'):
        if 'CUSTOM_VAR' in line:
            print(f"Found: {line}")
            break
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Security considerations
print("=== Security Tips ===")
print("1. Always use subprocess.run() with a list of arguments instead of shell=True when possible")
print("2. Validate and sanitize any user input before passing to shell commands")
print("3. Use timeout parameter to prevent hanging")
print("4. Handle exceptions properly")
print("5. Be careful with shell injection when using shell=True")

# Example of shell injection vulnerability (DON'T DO THIS)
print("\n⚠️  DANGEROUS EXAMPLE (for educational purposes):")
print("# NEVER do this with user input:")
print("# user_input = '; rm -rf /'")
print("# os.system(f'echo {user_input}')  # This could delete everything!")

print("\n✅ SAFE ALTERNATIVE:")
print("# subprocess.run(['echo', user_input])  # Safe - no shell interpretation")
