

# 🗣️ Python Text-to-Speech Tool

A simple yet powerful **Text-to-Speech (TTS)** utility built with Python.
Convert **text or PDFs** into high-quality speech using **offline system voices** or **Google TTS (gTTS)**.
Includes fun simulated voices like **🤖 Robot Mode** and **💻 Hacker Mode** — plus real-time voice previews!

---

## ✨ Features

* 🎧 **Multiple Output Formats** – Save speech as `.wav` or `.mp3`
* 💬 **Offline System Voices** – Uses `pyttsx3` for Windows/macOS/Linux voices
* ☁️ **Online Google TTS (gTTS)** – Optional cloud voice generation
* 🧾 **PDF Extraction** – Read and convert text directly from PDF files
* 🤖 **Simulated Voices**

  * Robot Voice — repeats words with echo-like spacing
  * Hacker Voice — converts text to l33t “hacker” code
* 👂 **Voice Preview** – Hear your selected voice before saving
* ⚙️ **Adjustable Speed** – Choose *slow*, *normal*, or *fast*
* 📝 **Text Export** – Save extracted or transformed text as `.txt` or `.docx`

---

## 🧩 Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/kcee01/Text-to-Speech-Tool.git
   cd Text-to-Speech-Tool
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   If you don’t have a `requirements.txt` yet, create one with:

   ```txt
   pyttsx3
   gTTS
   PyPDF2
   python-docx
   tkinter
   ```

   *(Tkinter is built-in on most Python installations.)*

---

## 🚀 Usage

You can run the script interactively or from the command line.

### 🧭 Interactive Mode

```bash
python text_to_speech.py
```

Then follow the prompts:

1. Select a **voice** (system or simulated)
2. Choose your **input source** (PDF or typed text)
3. Optionally **preview** the selected voice
4. Pick your **output format** (`wav` or `mp3`)
5. Adjust the **speed** and optionally save the text

---

### 🧠 Command-Line Examples

#### Convert a PDF directly:

```bash
python text_to_speech.py --pdf "my_document.pdf"
```

#### Convert text directly:

```bash
python text_to_speech.py --text "Hello, this is my AI voice speaking!"
```

---

## 🎛️ Voice Options

When prompted, you’ll see a list like:

```
0: Microsoft Zira Desktop (Female, en_US)
1: Microsoft David Desktop (Male, en_US)
2: 🤖 Robot Voice (simulated)
3: 💻 Hacker Voice (simulated)
```

Just enter the number to select your voice.

---

## 🔊 Output Formats

| Format  | Engine    | Voice Source                            |
| :------ | :-------- | :-------------------------------------- |
| **WAV** | `pyttsx3` | Uses your chosen system voice (offline) |
| **MP3** | `gTTS`    | Uses Google’s online TTS voice          |

> 💡 **Tip:** WAV gives you full control over the chosen system voice.
> MP3 (via gTTS) uses Google’s voice — it may sound different from the preview.

---

## 📂 Output Files

| File Type        | Description                              |
| :--------------- | :--------------------------------------- |
| `.wav` / `.mp3`  | The generated speech                     |
| `.txt` / `.docx` | (Optional) Extracted or transformed text |

---

## ⚙️ Example Workflow

1. Launch the script
2. Select **Microsoft Zira (Female)**
3. Choose **PDF file**
4. Preview the voice 👂
5. Save as `output.wav`
6. Get your audio in seconds 🎧

---

## 🧠 Fun Modes

### 🤖 Robot Mode

Repeats words with pauses for a “mechanical” tone.
Example:

> “Hello there” → “Hello...Hello there...there”

### 💻 Hacker Mode

Converts letters to **leet-speak** and adds pauses.
Example:

> “System activated” → “5.y.5.t.3.m 4.c.t.1.v.4.t.3.d”

> Voice choice only saves to the chosen voice when saved as wav not mp3
---

## 🧰 Dependencies

| Package       | Purpose                        |
| :------------ | :----------------------------- |
| `pyttsx3`     | Offline text-to-speech engine  |
| `gTTS`        | Google Text-to-Speech for MP3  |
| `PyPDF2`      | PDF text extraction            |
| `python-docx` | Save text as Word files        |
| `tkinter`     | File dialogs for PDF selection |

---

## 🧑‍💻 Author

**Kcee01**
🔗 [GitHub Profile](https://github.com/kcee01)

---

## 📜 License

MIT License — free to use and modify.

---

