# MiniCode IDE ✦

> A lightweight, portable, and powerful Python IDE — built with PyQt6.


---

## ✨ Features

| Feature | Description |
|---|---|
| 🖊 **Syntax Highlighting** | Python, HTML, CSS highlighting via custom lexers |
| 📁 **File Explorer** | Dockable tree view — open folders and files instantly |
| 🖥 **Integrated Terminal** | Run Python scripts directly inside the IDE |
| 👁 **Live Web Preview** | Real-time HTML/CSS/JS preview — updates as you type |
| 🎨 **SuperUI™ Customizer** | Full QSS (Qt Style Sheets) editor with preset themes |
| 💾 **Session Persistence** | Re-opens your last files on next launch |
| 📦 **Portable EXE** | Single-file executable — no installation required |

---

## 🚀 Quick Start

### Run from Source
```bash
# 1. Install dependencies
pip install PyQt6 PyQt6-WebEngine

# 2. Launch
python main.py
```

### Use the Portable Executables (Windows, Linux, macOS)
No Python installation required! Download the pre-compiled version for your operating system from the **Releases** section of this repository:
- **Windows**: Download `MiniCode-windows.exe` and run.
- **Linux**: Download `MiniCode-linux.tar.gz`, extract it, and run the `MiniCode` binary.
- **macOS**: Download `MiniCode-macos.zip`, extract it, and run the `MiniCode.app` bundle.

---

## 🎨 SuperUI™ Themes

Open **Help → SuperUI™** to customize the entire IDE with Qt Style Sheets. 

You can find awesome community themes in the `themes/` directory:
- 🌸 **girly_pink.css**: Cute pink and lavender accents
- 💻 **mascular_charcoal.css**: A rugged, dark orange and steel-charcoal setup
- 🌌 **tokyo_night.css**: Deep indigo/blue inspired by Tokyo Night
- ⚽ **football_core.css**: Classic pitch green with gold accents

To apply a theme:
1. Open the `.css` theme file of your choice from the `themes/` folder.
2. Copy all the code.
3. Open **Help → SuperUI™** in MiniCode, paste the code, and click **Apply Changes**.

You can also write **your own QSS** directly in the editor, or use `url(https://...)` to apply web images as backgrounds or icons.

---

## 👁 Live Preview

1. Open an HTML/CSS/JS file
2. Click the **Preview** button in the toolbar (or **View → Web Preview**)
3. The preview panel appears on the right — it **updates instantly as you type**

> No need to save — changes reflect in real-time.

---

## ⌨ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+N` | New File |
| `Ctrl+O` | Open File |
| `Ctrl+S` | Save |
| `Ctrl+Shift+S` | Save As |
| `F5` | Run Python |

---

## 🏗 Building the EXE

```bash
# Install PyInstaller
pip install pyinstaller

# Build (single file, with icon)
pyinstaller --onefile --windowed --icon=icon.ico \
    --add-data "icon.ico;." \
    --name MiniCode main.py
```

> **Important:** Always include `--add-data "icon.ico;."` so the EXE can find the icon at runtime. The `resource_path()` helper in `main.py` handles this automatically.

The output EXE will be in the `dist/` folder.

---

## 📂 Project Structure

```
MiniCode/
├── main.py             # Application entry point
├── icon.ico            # App icon (included in EXE)
├── session.json        # Auto-saved session (created at runtime)
└── ui/
    ├── editor.py       # CodeEditor with line numbers
    ├── explorer.py     # File tree widget
    ├── highlighter.py  # Python syntax highlighter
    ├── preview.py      # WebEngine live preview panel
    ├── styles.py       # Default dark QSS theme
    ├── super_ui.py     # SuperUI™ customizer dialog
    └── terminal.py     # Embedded terminal widget
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `PyQt6` | Core GUI framework |
| `PyQt6-WebEngine` | Live HTML/CSS/JS preview panel |
| `pyinstaller` | (Build only) Package as portable EXE |

Install all:
```bash
pip install PyQt6 PyQt6-WebEngine
```

---

## 🪲 Known Issues / FAQ

**Q: The EXE shows a default icon instead of my custom icon.**  
A: Make sure you build with both `--icon=icon.ico` **and** `--add-data "icon.ico;."`. The `--icon` flag sets the file/taskbar icon, while `--add-data` ensures the app can load it at runtime via `resource_path()`.

**Q: Preview panel shows nothing.**  
A: Install `PyQt6-WebEngine`: `pip install PyQt6-WebEngine`

**Q: Terminal doesn't work.**  
A: The terminal uses the system shell. On Windows, make sure Python is on your `PATH`.

---

## 📄 License

MIT — Free to use, modify, and distribute.

---

*Built with ❤️ and PyQt6*
