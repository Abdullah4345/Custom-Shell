import os
import sys
import subprocess
import time
import shutil
import getpass
import signal
import readline 
from collections import deque




command_history = deque(maxlen=100) 
background_jobs = [] 
environment_variables = os.environ.copy()  


history_file = os.path.expanduser("~/.python_shell_history")




if os.path.exists(history_file):
    readline.read_history_file(history_file)
readline.set_history_length(100) 

def save_history():
    """Save the history to the file."""
    readline.write_history_file(history_file)

def execute_command(command):
    """Execute a command using subprocess."""
    try:
        if shutil.which(command[0]) is None:
            print(f"Error: Command '{command[0]}' not found.")
        else:
            subprocess.run(command, check=True, env=environment_variables)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

def builtin_commands(command):
    """Handle built-in commands like cd, exit, etc."""
    if command[0] == "exit":
        print("Exiting the shell.")
        save_history() 
        sys.exit()
    elif command[0] == "clear":
        os.system("clear")
    elif command[0] == "whoami":
        print(getpass.getuser())
    elif command[0] == "cd":
        if len(command) < 2:
            print(os.getcwd()) 
        else:
            try:
                os.chdir(command[1])
            except Exception as e:
                print(f"cd: {e}")
    elif command[0] == "mkdir":
        if len(command) < 2:
            print("Error: Please specify the folder name.")
        else:
            try:
                os.makedirs(command[1])
                print(f"Directory '{command[1]}' created successfully.")
            except Exception as e:
                print(f"Error creating directory: {e}")
    
    elif command[0] == "copy":
        if len(command) < 3:
            print("Error: Please specify the source and destination.")
        else:
            source = command[1]
            destination = command[2]
            try:
                shutil.copy(source, destination)
                print(f"Copied '{source}' to '{destination}'.")
            except Exception as e:
                print(f"Error copying file: {e}")
    elif command[0] == "tree":
        # Display the directory tree
        print("\nDirectory Tree:")
        display_directory_tree(os.getcwd())
    elif command[0] == "move":
        if len(command) < 3:
            print("Error: Please specify the source and destination.")
        else:
            source = command[1]
            destination = command[2]
            try:
                shutil.move(source, destination)
                print(f"Moved '{source}' to '{destination}'.")
            except Exception as e:
                print(f"Error moving file: {e}")
    elif command[0] == "set":
       
        if len(command) < 2:
            print("Error: Please specify a variable in the format VAR=VALUE.")
        else:
            key, value = command[1].split("=", 1)
            environment_variables[key] = value
            print(f"Set {key} to {value}")

    elif command[0] == "top":
        print("Displaying real-time system processes. Refreshing every 2 seconds.")
        try:
            while True:
                
                os.system("clear")  
                subprocess.run(["top", "-n", "1"]) 
                time.sleep(2) 
        except KeyboardInterrupt:
            print("Exiting 'top' command.")

    elif command[0] == "del":
        if len(command) < 2:
            print("Error: Please specify the file or directory to delete.")
        else:
            target = command[1]
            if os.path.isfile(target):
                try:
                    os.remove(target)
                    print(f"Deleted file '{target}'.")
                except Exception as e:
                    print(f"Error deleting file: {e}")
            elif os.path.isdir(target):
                try:
                    shutil.rmtree(target)
                    print(f"Deleted directory '{target}' and all its contents.")
                except Exception as e:
                    print(f"Error deleting directory: {e}")
            else:
                print(f"Error: '{target}' does not exist.")
    elif command[0] == "echo":
        if command[1].startswith("$"):
            var_name = command[1][1:]
            print(environment_variables.get(var_name, ""))
        else:
            print(" ".join(command[1:]))
    elif command[0] == "history":
        for i, cmd in enumerate(command_history):
            print(f"{i + 1}: {cmd}")
    elif command[0] == "help":
        print("Available commands:")
        print("  exit            - Exit the shell")
        print("  clear           - Clear the screen")
        print("  whoami          - Display the current user")
        print("  cd <path>       - Change the current directory")
        print("  mkdir <name>    - Create a new directory")
        print("  set VAR=VALUE   - Set an environment variable")
        print("  echo $VAR       - Display an environment variable's value")
        print("  history         - Show command history")
        print("  help            - Display this help message")
        print("  copy            - example.txt ./test2/example.txt")
        print("  move            - move example.txt ../test2")
        print("  del             - example.txt")
        print("  ps              - Display the list of running processes")
        print("  ps a            - Show processes for all users")
        print("  ps au           - Show detailed information about all processes")
        print("  ps aux          - List all processes with detailed user and system stats")
        print("  top             - Display a real-time view of system processes")
        print("  ifconfig        - Show or configure network interfaces")
        print("  kill            - Terminate a process by its ID")
        print("  ping            - Test connectivity to a network host")
        print("  nslookup        - Query DNS for a domain's IP address")
        print("  traceroute      - Trace the path packets take to a destination")
        print("  tree            - Display a directory structure in a tree format")


    elif command[0] == "jinx":
        print('''
███████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▓▓▒▒▓▒▓████████████▓█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▓▓▒▒▓▓▒▓▒▒░▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
███▓█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▓▓▓░▒▒▓█▓█▓████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▒▒▒▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒
██████▓████████████▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒░░░░▒▓▒░░▓█▓▓▓█▓█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
█████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▓▓▓▒▒▒▒▒░░░▒▒░▒▓▓▓▓▓█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒
█████████▓▓█▓▓▓▓▓▓▓███▓██▓▓▒▒▒▒▒▒▒██▒▒▒▒▒▒░▒▓▒▒▓▓▓░░░▒▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▒▒▒▓▓▓▓▓▓▒▒▓▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▓▒▒▓▒▒▒▒▒▒▒▒▒▒▓
████████▓▓▓█▓▓▓██▓███▓█▓▒▒▒▒▒▒▒▒▒▓█▓▒▒▒▒░▓▓▓▒▒▒▓▓▓▓▓▒░░▓▓▓▓▓▓▓▓▓▓▒▒▓▓█▓▓▒▒▒▓▓▓▓▓▓▒▒▓▒▒▓▓█▓▓▓▒▒▓▓▓▓▓▒▒▓▓▓▓▓▒▒▓▒▒▓▓▓▓▓▓▓▒▓
███████▓▓▓██▓▓▓▓▓████▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒░▓▓▓▒▒▒▓▒▒▓▓▓▒▒░░░▒▓▓▓▓▓▓▓▒▒▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▓▓█▓▓▒▒▒▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓
███████▓▓▓█▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▓▓▓▓▓▒▒▓▓▓▓▓▓░▒░░▒▓▓▓▓▓▓▓░░▓▓▓▓▓▒▒▒▓▓███▓▒▒▓▒▒▓▓▓▒▓▒▒▒▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓▒▓▓▓▓▓▓▓▒▒▓
███████▓▓█▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▓▒▒▓▓▒▒▓▓▓▓▓▓▓▓▒▒▒▒░░░▓▓▓▓▓░░▓▓▓▓▓▒▒▒▓████▓▒▒▓▒▒▓▓▓▓▒▓▒▒▒▒▓▓▒▒░▓▓▓▓▓▒▓▓▒▒▒▒▒▒▒▒▒▒▓
██████▓▓▓█▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒███▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░▒▒▒░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓██████▓▓▒▒▓██▓▒▒▒▓▒▒▓▓▓▓▒▒▓▓▒▓▓▓▓▒▓▓▓▓▓▓▓▓▒▒▓
██████▓▓▓█▓▓▓▓▓▓▓▒▒▒▒▒▒▒▓██▓▒▒▒▒▒▒▒▒░▒░▒▒▓▓▒▓▒▒▒▒▒░▒▓▒▒░░░▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓▓▒▓▓▒▓▓▓▓▓▓▓▓▓▓▓▒▓▓▓▓▓▓▒▓▓▓▒▒▒░
██████▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▓▓▓▒░░▒░░░▒▒▓▒▓▓▒▒░▒█▓▓▓▓▒▓▓▓▒▒▒▒▒░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▒▒▓▓▒▒▒
██████▓▓▓▓▓▓▓▓▓▓▓▒▒▒▓▓█▒▓▓▓▓▓▓▓▓▓░▒▓▓▒░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒▒▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▒▒░░░░░
███████▓▓▓▓▓▓▓▓██▒▒▓▒█░█▓▓▓▓▓▓▓▓▓▓▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓█▒▒▓▓███▓▒▒▒██▒▒▒▒█▓██▓▓█▓▓▓▓▓▓▓▓▓▓▒░▒▒▒▒▒▒
███████▓█▓▓▓▓▓▓██▓▒█▒▓██▓▓▓▓▓░▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒░▒▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒▓▓▓▓▓▓▓▓▒▒▒▓▓██▓▓▓▓████▓▓▓██▓▓▓▓████▓▓▓▓▓▓▓▓▓▓▓▓█▓▓▒▒▒▒▒▒
███████▓█▓▓▓▓▓▓███▓█▒▒███▓▒▒▓▓▓▓▓▓▓▒▓▒▒▒▒▒▒▒▒▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒░▒▒▒▒▓▓▓▓▓▓▒▒▒▒███▒▒▒▓███▓▓▓▓██▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█▓▓▓▓▓▓▓▒
███████▓█▓█▓▓▓▓█████▓▓▒███▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▓▓▓▓▒▒▒▒▒▓▓▓▓▒▒▒▒▒░░▒▓▒▒▒▒▓▓▓▒▒▒▒▓▓█▒▒▒▓████▒▓▓██▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▓
████████████▓▓█████▓▓▓▓▒██▓█▓▓▓▓▓▓▓▓▒▒▒▒▒▓▓▒▒▒▒▒▓▓▓▒▒▓▓▒▒▒▒▒▒░▓▓▓▓▓▓▓▓▓▒▒▒▒███▒▒▒▒███▓▒▒▓██▓▓▓▒▓███████▓▓▓▓▓▓▒▒▒▒░░▒▒▒▒▒
████████████▓▓█████▓▓▒▓▓█░░▓▓▓▒░▓██▒▒▒▒▒▒▒▒▒▒▒▓▓▓▒▒▒▒▓▓▒▒▒▒▒▒░▓▓▓▒▒▒▓▓▓▒▒▒▒▓▓█▒▒▒▒████▒▒▒██▓▓▓▓▓██████▓▓▓▓▓▓█▒▒▒▓▒░▒░░▒▒
████████████▓▓████████▓██▓▓█▓▓██▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▒░▓▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▒▒▒▒▓▓█▒▒▒▒███▓▒▒▒██▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓░░░░░▓░
█████████████████████▓██▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▓▒▒▓▓▓▒▒▒▒▒▒▒▒▓▓▒▓▒▒▒▓▓▓▒▒▒▒▓▓▓▒▒▒▒▓▓▓▓▒▒▒▓▓▓█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▒▒▒▒▒▒
█████████████████████▓█▓██▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒██▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓▓█▓▓▒▒▒
███████████████████████████▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████▒▒▒▒▒▒
████████████████████████▓██▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒███████▓▓▒▒▒▒▓▓
███████████████████████▓▓█▓██▓█▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒░░▓▓▓▓▓▓▓▓▓▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▒▒▒▒▒▒▒▒███████▒░▒▓▓▓▒▒
█████████████████████████▓▓▓▓▒▒▒▒███▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▓▓▓▓▓▓▒▒▒░▒▓▓▓▓▓▓▓▓▓▓█▓▓▓▓▓▓▓▓▓▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▓█████▒░▒▓▓▓▒░▒
█████████████████████████████▓██████████████▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒░▒░▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▓▓▓▓▒▓▓▓▓▓▓▓▓▓▓▓▓▓██░░▒▒▓▒▒▒
███████████████████████████████▓█████████████▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▒▒▒▒░░▒▒▓▓▓▓▓▓███████▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████▓▓▒▓▓▓
███████████████████████████████████████████████▓▒▒▒▒▒▒▒▒▒▒▓▓██▓▓▓▓▓▓▓▒▒▒▒▒▒▓▓▓▒▓█▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▒▒▓▒▓▓▓▓▓▒▓███████▓█▓▓▓
███████████████████████████████████████████████████████████▓▓▒▒░▒▒▓▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▒▓▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒██████████▓▓
█████████████████████████████████████████████▒▓████▓▓▓▒▒▒▒▒▒▒▒▒▓▓▓▓▓▒▒▒▒▒▒▒▒▓▒▒▓▓▓▓▒▒▒▒▓▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓███████
████████████████████████████████████████████▒▓▒▒▒█████████████▓▓░░░░░░░░░▓▒▓▓▓▓▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒
████████████████████████████████████████████████████████████████▓▓▓▓▓████▓▓█████████████████████████████████████████████''')
    else:
        return False
    return True

def parse_input(input_command):
    """Parse and execute a user's input command."""
    global command_history, background_jobs
    background = False
    input_command = input_command.strip()
    command_history.append(input_command) 
    readline.add_history(input_command)  


    if input_command.endswith("&"):
        input_command = input_command[:-1].strip()
        background = True

   
    if "|" in input_command:
        commands = [cmd.strip() for cmd in input_command.split("|")]
        processes = []
        prev_pipe = None
        for i, cmd in enumerate(commands):
            cmd_parts = cmd.split()
            if i == 0:
                prev_pipe = subprocess.Popen(cmd_parts, stdout=subprocess.PIPE)
            elif i == len(commands) - 1:
                subprocess.run(cmd_parts, stdin=prev_pipe.stdout)
                prev_pipe.stdout.close()
            else:
                prev_pipe = subprocess.Popen(cmd_parts, stdin=prev_pipe.stdout, stdout=subprocess.PIPE)
        return


    if ">" in input_command or "<" in input_command:
        if ">>" in input_command:
            parts = input_command.split(">>", 1)
            command = parts[0].strip().split()
            output_file = parts[1].strip()
            with open(output_file, "a") as f:
                subprocess.run(command, stdout=f, env=environment_variables)
        elif ">" in input_command:
            parts = input_command.split(">", 1)
            command = parts[0].strip().split()
            output_file = parts[1].strip()
            with open(output_file, "w") as f:
                subprocess.run(command, stdout=f, env=environment_variables)
        elif "<" in input_command:
            parts = input_command.split("<", 1)
            command = parts[0].strip().split()
            input_file = parts[1].strip()
            with open(input_file, "r") as f:
                subprocess.run(command, stdin=f, env=environment_variables)
        return


    command_parts = input_command.split()
    if builtin_commands(command_parts):
        return


    if background:
        try:
            pid = os.fork()
            if pid == 0: 
                os.execvp(command_parts[0], command_parts)  
            else:  
                background_jobs.append(pid)  
                print(f"Command '{input_command}' is running in the background with PID {pid}.")
        except Exception as e:
            print(f"Error running background command: {e}")
    else:
        
        execute_command(command_parts)

def fg():
    """Bring the most recent background job to the foreground."""
    if not background_jobs:
        print("No background jobs to bring to the foreground.")
        return

    pid = background_jobs.pop() 
    try:
        print(f"Bringing background job with PID {pid} to the foreground.")
        os.waitpid(pid, 0) 
    except ChildProcessError as e:
        print(f"Error: {e}")

def signal_handler(sig, frame):
    """Handle signals for SIGINT (Ctrl+C)."""
    print("\nUse 'exit' to quit the shell.")

def main():
    """Main function to run the shell."""
    signal.signal(signal.SIGINT, signal_handler) 

    while True:
        try:
            input_command = input("Basic Python Shell> ").strip()
            if not input_command:
                continue 
            if input_command == "fg":
                fg()  
            else:
                parse_input(input_command)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit the shell.")
        except EOFError:
            print("\nExiting shell.")
            save_history() 
            break




def display_directory_tree(path, indent=0, show_files=True):
    """
    Displays the directory tree in Windows style.
    If show_files is True, it will list files as well as directories.
    """
    if os.path.isdir(path):
        print(' ' * indent + f"{os.path.basename(path)}\\") 
        for item in sorted(os.listdir(path)):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                display_directory_tree(item_path, indent + 4, show_files)
            elif show_files:
                print(' ' * (indent + 4) + f"{item}")
    else:
        print(' ' * indent + f"{os.path.basename(path)}")





if __name__ == "__main__":
    main()
