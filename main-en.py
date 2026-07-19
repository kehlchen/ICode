#!/usr/bin/env python3
"""
WhiseByte - Invisible Data Encoder & Decoder
Uses ASCII control characters \x02 and \x03 for absolute invisibility.
"""

import os
import sys

# Invisible control characters as separators
START_CHAR = "\x02"
END_CHAR = "\x03"

def clear_screen():
    """Clears the terminal screen across platforms."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_key():
    """Reads a single keypress without external libraries."""
    if os.name == 'nt':
        import msvcrt
        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):
            ch = msvcrt.getch()
            if ch == b'H': return 'up'
            if ch == b'P': return 'down'
        if ch in (b'\r', b'\n'): return 'enter'
        return None
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(2)
                if ch2 == '[A': return 'up'
                if ch2 == '[B': return 'down'
            if ch in ('\n', '\r'): return 'enter'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None

def terminal_menu(options):
    """Interactive terminal menu using arrow keys."""
    selected_index = 0
    while True:
        clear_screen()
        print("=== WhiseByte System ===")
        print("Use [Up/Down] and confirm with [Enter]\n")
        
        for idx, option in enumerate(options):
            if idx == selected_index:
                print(f" > \033[1m\033[36m[{option}]\033[0m")
            else:
                print(f"   {option}")
        
        key = get_key()
        if key == 'up':
            selected_index = (selected_index - 1) % len(options)
        elif key == 'down':
            selected_index = (selected_index + 1) % len(options)
        elif key == 'enter':
            return options[selected_index]

def get_file_path(prompt):
    """Reads paths and cleans Drag & Drop quotation marks."""
    while True:
        path = input(prompt).strip().strip('"\'')
        if not path:
            print("Path cannot be empty.")
            continue
        return path

# --- CORE FUNCTIONS ---

def encode_file(input_path, output_path, base_file_path=None):
    """
    Encodes the ICode into whitespace. 
    If a carrier file (base_file_path) is provided, 
    the invisible data is appended to it.
    """
    try:
        # If we use a host program, read its content first
        base_content = ""
        if base_file_path and os.path.exists(base_file_path):
            with open(base_file_path, 'r', encoding='utf-8', errors='ignore') as base_file:
                base_content = base_file.read()
                # Ensure the carrier file ends with a newline
                if base_content and not base_content.endswith('\n'):
                    base_content += '\n'

        with open(input_path, 'rb') as infile:
            binary_data = infile.read()

        # Generate whitespace stream
        encoded_bits = []
        for byte in binary_data:
            bits = f"{byte:08b}"
            encoded_bits.append("".join(['\t' if bit == '1' else ' ' for bit in bits]))
        
        # Every byte gets a newline for structure
        payload = "\n".join(encoded_bits) + "\n"

        # Final structure: [Carrier] + [Invisible Start] + [Payload] + [Invisible End]
        with open(output_path, 'w', encoding='utf-8') as outfile:
            if base_content:
                outfile.write(base_content)
            outfile.write(START_CHAR + payload + END_CHAR + "\n")
            
        print(f"\n[Success] File invisibly encoded to: {output_path}")
    except Exception as e:
        print(f"\n[Error] An error occurred during encoding: {e}")

def decode_and_execute_file(input_path, output_path=None, execute=False):
    """
    Isolates the whitespace between \x02 and \x03.
    Restores the file bit-accurately and optionally executes it directly.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as infile:
            content = infile.read()
            
        if START_CHAR not in content or END_CHAR not in content:
            print("\n[Error] No hidden WhiseByte data stream found.")
            return
            
        start_idx = content.find(START_CHAR) + len(START_CHAR)
        end_idx = content.find(END_CHAR)
        
        # Strict isolation: Everything outside these indices is discarded
        payload = content[start_idx:end_idx]
        
        # Extract bits exclusively from the isolated area
        filtered_bits = [('0' if char == ' ' else '1') for char in payload if char in (' ', '\t')]
        
        # Reconstruct bytes
        byte_chunks = bytearray()
        for i in range(0, len(filtered_bits), 8):
            bit_str = "".join(filtered_bits[i:i+8])
            if len(bit_str) == 8:
                byte_chunks.append(int(bit_str, 2))
                
        # Export path if requested
        if output_path:
            with open(output_path, 'wb') as outfile:
                outfile.write(byte_chunks)
            print(f"[Success] File restored under: {output_path}")

        # In-Memory execution of the hidden code via exec()
        if execute:
            try:
                icode_text = byte_chunks.decode('utf-8')
                print("\n--- [START INVISIBLE CODE EXECUTION] ---")
                exec(icode_text, globals())
                print("--- [END INVISIBLE CODE EXECUTION] ---")
            except Exception as script_error:
                print(f"\n[Error during ICode execution]: {script_error}")
                
    except Exception as e:
        print(f"\n[Error] An error occurred during decoding: {e}")

# --- MAIN CONTROLLER ---

def main():
    options = ["Encode File (Hidden)", "Decode & Extract File", "Decode & Execute (Memory)", "Exit"]
    
    while True:
        choice = terminal_menu(options)
        
        if choice == "Exit":
            clear_screen()
            print("WhiseByte stopped. See you next time!")
            break
            
        clear_screen()
        print(f"=== {choice} Mode ===\n")
        
        if choice == "Encode File (Hidden)":
            input_file = get_file_path("Path to the secret file (Input): ")
            if not os.path.exists(input_file):
                print("[Error] File does not exist!")
                input("\nPress Enter...")
                continue
                
            use_base = input("Should the code be embedded into a visible carrier program (e.g. harmless .py/.bat)? (y/N): ").lower()
            base_file = None
            if use_base == 'y':
                base_file = get_file_path("Path to the existing carrier file: ")
                if not os.path.exists(base_file):
                    print("[Error] Carrier file does not exist!")
                    input("\nPress Enter...")
                    continue
            
            output_file = get_file_path("Save location for the output file: ")
            encode_file(input_file, output_file, base_file)
            
        elif choice == "Decode & Extract File":
            input_file = get_file_path("Path to the prepared WhiseByte file: ")
            if not os.path.exists(input_file):
                print("[Error] File does not exist!")
                input("\nPress Enter...")
                continue
            output_file = get_file_path("Save location for the restored file: ")
            decode_and_execute_file(input_file, output_path=output_file, execute=False)
            
        elif choice == "Decode & Execute (Memory)":
            input_file = get_file_path("Path to the prepared WhiseByte file: ")
            if not os.path.exists(input_file):
                print("[Error] File does not exist!")
                input("\nPress Enter...")
                continue
            decode_and_execute_file(input_file, output_path=None, execute=True)
            
        # FIX: The standard interaction prompt at the end of the loop
        input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\nProgram terminated by user.")