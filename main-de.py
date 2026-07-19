#!/usr/bin/env python3
"""
WhiseByte - Unsichtbarer Daten-Encoder & Decoder
Verwendet ASCII-Steuerzeichen \x02 und \x03 für absolute Unsichtbarkeit.
"""

import os
import sys

# Unsichtbare Steuerzeichen als Trenner
START_CHAR = "\x02"
END_CHAR = "\x03"

def clear_screen():
    """Löscht den Terminal-Bildschirm plattformunabhängig."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_key():
    """Liest einen einzelnen Tastendruck ohne externe Bibliotheken ein."""
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
    """Interaktives Terminal-Menü mit Pfeiltasten."""
    selected_index = 0
    while True:
        clear_screen()
        print("=== WhiseByte System ===")
        print("Nutze [Hoch/Runter] und bestätige mit [Enter]\n")
        
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
    """Liest Pfade ein und säubert Drag & Drop Anführungszeichen."""
    while True:
        path = input(prompt).strip().strip('"\'')
        if not path:
            print("Pfad darf nicht leer sein.")
            continue
        return path

# --- CORE FUNCTIONS ---

def encode_file(input_path, output_path, base_file_path=None):
    """
    Kodiert den ICode in Whitespace. 
    Falls eine Trägerdatei (base_file_path) angegeben wird, 
    werden die unsichtbaren Daten an diese angehängt.
    """
    try:
        # Falls wir ein Wirtsprogramm nutzen, lesen wir dessen Inhalt zuerst
        base_content = ""
        if base_file_path and os.path.exists(base_file_path):
            with open(base_file_path, 'r', encoding='utf-8', errors='ignore') as base_file:
                base_content = base_file.read()
                # Sicherstellen, dass die Trägerdatei mit einem Zeilenumbruch endet
                if base_content and not base_content.endswith('\n'):
                    base_content += '\n'

        with open(input_path, 'rb') as infile:
            binary_data = infile.read()

        # Whitespace-Stream generieren
        encoded_bits = []
        for byte in binary_data:
            bits = f"{byte:08b}"
            encoded_bits.append("".join(['\t' if bit == '1' else ' ' for bit in bits]))
        
        # Jedes Byte kriegt der Struktur halber einen Zeilenumbruch (\n wird von Python toleriert)
        payload = "\n".join(encoded_bits) + "\n"

        # Finale Struktur: [Trägerprogramm] + [Unsichtbarer Start] + [Payload] + [Unsichtbares Ende]
        with open(output_path, 'w', encoding='utf-8') as outfile:
            if base_content:
                outfile.write(base_content)
            outfile.write(START_CHAR + payload + END_CHAR + "\n")
            
        print(f"\n[Erfolg] Datei unsichtbar kodiert in: {output_path}")
    except Exception as e:
        print(f"\n[Fehler] Beim Kodieren ist ein Fehler aufgetreten: {e}")

def decode_and_execute_file(input_path, output_path=None, execute=False):
    """
    Isoliert den Whitespace zwischen \x02 und \x03.
    Stellt die Datei bitgenau wieder her und führt sie optional direkt aus.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as infile:
            content = infile.read()
            
        if START_CHAR not in content or END_CHAR not in content:
            print("\n[Fehler] Kein verdeckter WhiseByte-Datenstrom gefunden.")
            return
            
        start_idx = content.find(START_CHAR) + len(START_CHAR)
        end_idx = content.find(END_CHAR)
        
        # Strikte Isolation: Alles außerhalb dieser Indizes wird verworfen
        payload = content[start_idx:end_idx]
        
        # Extrahiere Bits ausschließlich aus dem isolierten Bereich
        filtered_bits = [('0' if char == ' ' else '1') for char in payload if char in (' ', '\t')]
        
        # Rekonstruktion der Bytes
        byte_chunks = bytearray()
        for i in range(0, len(filtered_bits), 8):
            bit_str = "".join(filtered_bits[i:i+8])
            if len(bit_str) == 8:
                byte_chunks.append(int(bit_str, 2))
                
        # Pfad-Export falls gewünscht
        if output_path:
            with open(output_path, 'wb') as outfile:
                outfile.write(byte_chunks)
            print(f"[Erfolg] Datei wiederhergestellt unter: {output_path}")

        # In-Memory Ausführung des verdeckten Codes via exec()
        if execute:
            try:
                icode_text = byte_chunks.decode('utf-8')
                print("\n--- [START INVISIBLE CODE EXECUTION] ---")
                exec(icode_text, globals())
                print("--- [ENDE INVISIBLE CODE EXECUTION] ---")
            except Exception as script_error:
                print(f"\n[Fehler bei der ICode-Ausführung]: {script_error}")
                
    except Exception as e:
        print(f"\n[Fehler] Beim Dekodieren ist ein Fehler aufgetreten: {e}")

# --- MAIN CONTROLLER ---

def main():
    options = ["Encode File (Hidden)", "Decode & Extract File", "Decode & Execute (Memory)", "Exit"]
    
    while True:
        choice = terminal_menu(options)
        
        if choice == "Exit":
            clear_screen()
            print("WhiseByte beendet. Bis zum nächsten Mal!")
            break
            
        clear_screen()
        print(f"=== {choice} Mode ===\n")
        
        if choice == "Encode File (Hidden)":
            input_file = get_file_path("Pfad zur geheimen Datei (Eingabe): ")
            if not os.path.exists(input_file):
                print("[Fehler] Datei existiert nicht!")
                input("\nDrücke Enter...")
                continue
                
            use_base = input("Soll der Code in ein sichtbares Trägerprogramm (z.B. harmlose .py/.bat) eingebettet werden? (j/N): ").lower()
            base_file = None
            if use_base == 'j':
                base_file = get_file_path("Pfad zur existierenden Trägerdatei: ")
                if not os.path.exists(base_file):
                    print("[Fehler] Trägerdatei existiert nicht!")
                    input("\nDrücke Enter...")
                    continue
            
            output_file = get_file_path("Speicherort für die Ausgabedatei: ")
            encode_file(input_file, output_file, base_file)
            
        elif choice == "Decode & Extract File":
            input_file = get_file_path("Pfad zur präparierten WhiseByte-Datei: ")
            if not os.path.exists(input_file):
                print("[Fehler] Datei existiert nicht!")
                input("\nDrücke Enter...")
                continue
            output_file = get_file_path("Speicherort für die wiederhergestellte Datei: ")
            decode_and_execute_file(input_file, output_path=output_file, execute=False)
            
        elif choice == "Decode & Execute (Memory)":
            input_file = get_file_path("Pfad zur präparierten WhiseByte-Datei: ")
            if not os.path.exists(input_file):
                print("[Fehler] Datei existiert nicht!")
                input("\nDrücke Enter...")
                continue
            decode_and_execute_file(input_file, output_path=None, execute=True)
            
        input("\nDrücke Enter, um zum Hauptmenü zurückzukehren...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\nProgramm durch Benutzer abgebrochen.")