# ICode

ICode is an experimental steganography tool written in Python. It allows you to encode files or scripts entirely into invisible trailing whitespace (tabs and spaces) and append them to a visible carrier script (like a harmless `.py` or `.bat` file). 

The project features an interactive CLI menu that supports both bit-accurate data recovery and direct in-memory execution (`exec()`) without writing the hidden payload to the disk.

## 🚀 Features

* **Absolute Invisibility:** Uses ASCII control characters (`\x02` and `\x03`) to securely isolate the hidden payload from the visible host code.
* **Carrier Integration:** Append invisible payloads to existing functional scripts without breaking their original logic.
* **In-Memory Execution:** Directly decode and run hidden Python scripts straight into the RAM using dynamic execution contexts.
* **Pure Python:** Built entirely using native Python components and built-in libraries.
* **Interactive CLI:** A keyboard-driven terminal menu with cross-platform arrow-key support.

## 🛠️ How it Works

The tool translates binary file data into a stream of tab (`\t`) and space (` `) characters representing `1`s and `0`s. 


```
[ Carrier / Visible Code ]
\n
\x02 (Invisible Start Marker)
\t   \t\t   ... (Encoded Bits)
\x03 (Invisible End Marker)
```

During execution, the script targets the exact indices between the markers, ignoring both the host code and any standard trailing characters, reconstructing the original byte sequence flawlessly.

## 💻 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/WhiseByte.git](https://github.com/kehlchen/ICode.git)
   cd WhiseByte
   ```
 2. **Run the application:**
   ```
   python main-en.py
   
   ```
   **or**
   ```
   python main-de.py
   ```
   for the german version
   
 3. **Navigate the Menu:**
   * Use the **[Up / Down]** arrow keys to move the selection.
   * Press **[Enter]** to confirm your choice.

## Languages
The project currently only supports English (`main-en.py`) and German (`main-de.py`) as a language, if you want to support this project, you can help translate it to other languages.

## ⚠️ Disclaimer
This project is intended strictly for educational purposes, experimental software engineering, and studying steganographic concepts. Always ensure you comply with applicable software licenses when modifying open-source codebases.
