import curses
import os
import subprocess

def check_path(path):
    if os.path.isfile(path):
        return "File found", curses.color_pair(1)  # Green
    elif os.path.isdir(path):
        return "Folder found", curses.color_pair(1)  # Green
    else:
        return "Path not found", curses.color_pair(2)  # Red

def execute_script(script_name, path, key_file=None):
    try:
        if key_file:
            result = subprocess.run(['python3', script_name, path, key_file], capture_output=True, text=True)
        else:
            result = subprocess.run(['python3', script_name, path], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error: {str(e)}"

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # Hide the blinking cursor
    curses.curs_set(0)  # Disable cursor blinking

    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Green for paths
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Red for errors
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Cyan for titles
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)    # Red for author name

    while True:
        # Display title
        stdscr.addstr(0, 0, "=== Encryption/Decryption Tool ===", curses.color_pair(3) | curses.A_BOLD)

        # Position "Tool by: Mr_Root" on the bottom-right side
        height, width = stdscr.getmaxyx()
        author_name = "Tool by: Mr_Root"
        x = width - len(author_name) - 5  # Align it towards the right with padding
        y = height - 4                    # Push it down a bit more
        
        stdscr.addstr(y, x, author_name, curses.color_pair(4) | curses.A_BOLD)

        stdscr.refresh()

        # Display instructions
        stdscr.addstr(3, 0, "Enter the path of the file or folder (Press 'q' to quit):", curses.A_BOLD)
        stdscr.addstr(4, 0, "Enter 1 for Encryption or 2 for Decryption:", curses.A_BOLD)
        stdscr.refresh()

        path = ""
        action = None
        row = 6
        action_row = row + 1
        feedback_row = row + 2

        while True:
            # Get user input
            ch = stdscr.getch()

            if ch == ord('q'):
                return  # Exit the program

            if ch == curses.KEY_BACKSPACE or ch == 127:  # Handle backspace
                path = path[:-1]
            elif ch == curses.KEY_ENTER or ch == 10:
                # Handle Enter key
                if action == 1:
                    result = execute_script('Encrypt.py', path)
                elif action == 2:
                    # Prompt user for key file if decryption is selected
                    stdscr.addstr(feedback_row, 0, "Enter the path of the key file (Press Enter to finish):", curses.A_BOLD)
                    stdscr.refresh()
                    
                    key_file = ""
                    key_file_row = feedback_row + 1
                    while True:
                        stdscr.addstr(key_file_row, 0, "Key file path: " + key_file, curses.color_pair(1))
                        stdscr.refresh()
                        ch = stdscr.getch()
                        if ch == curses.KEY_BACKSPACE or ch == 127:  # Handle backspace
                            key_file = key_file[:-1]
                        elif ch == curses.KEY_ENTER or ch == 10:
                            break
                        elif ch >= 32 and ch <= 126:  # Printable characters
                            key_file += chr(ch)
                        
                        # Clear and refresh key file input area
                        stdscr.addstr(key_file_row, 0, " " * (len("Key file path: " + key_file) + 12))
                        stdscr.addstr(key_file_row, 0, "Key file path: " + key_file, curses.color_pair(1))
                        stdscr.refresh()

                    result = execute_script('Decrypt.py', path, key_file)
                else:
                    result = "Select a valid action (1 for Encryption, 2 for Decryption)"
                
                # Clear previous lines
                stdscr.clear()
                stdscr.addstr(0, 0, "=== Encryption/Decryption Tool ===", curses.color_pair(3) | curses.A_BOLD)
                stdscr.addstr(y, x, author_name, curses.color_pair(4) | curses.A_BOLD)
                
                # Display result
                stdscr.addstr(6, 0, result, curses.color_pair(1))
                stdscr.refresh()

                # Display exit message centered at the bottom
                height, width = stdscr.getmaxyx()
                exit_message = "Press any key to exit..."
                x = (width // 2) - (len(exit_message) // 2)
                y = height - 2  # Position it near the bottom
                stdscr.addstr(y, x, exit_message, curses.A_BOLD)
                stdscr.refresh()

                stdscr.getch()  # Wait for user input to exit
                return  # Exit the program
            elif ch == ord('1'):
                action = 1
                stdscr.addstr(action_row, 0, "Encryption selected", curses.color_pair(3))
                stdscr.refresh()
            elif ch == ord('2'):
                action = 2
                stdscr.addstr(action_row, 0, "Decryption selected", curses.color_pair(3))
                stdscr.refresh()
            else:
                if ch >= 32 and ch <= 126:  # Printable characters
                    path += chr(ch)

            # Clear previous lines
            stdscr.addstr(row, 0, " " * 80)
            stdscr.addstr(action_row, 0, " " * 80)
            stdscr.addstr(feedback_row, 0, " " * 80)

            # Display current path and feedback
            prompt = "Enter the path of the file or folder: "
            feedback, color = check_path(path)
            
            stdscr.addstr(row, 0, prompt, curses.A_BOLD)
            stdscr.addstr(row, len(prompt), path, curses.color_pair(1))
            stdscr.addstr(feedback_row, 0, feedback, color)
            stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
