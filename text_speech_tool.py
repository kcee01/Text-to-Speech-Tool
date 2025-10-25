import argparse
import pyttsx3
from gtts import gTTS
import os
from PyPDF2 import PdfReader
from docx import Document
from tkinter import Tk, filedialog
import random

# -----------------------------
# 🗣️ Voice Management
# -----------------------------
def get_voice_by_gender(engine, gender="female"):
    """Return the first voice that matches the gender (male/female)."""
    voices = engine.getProperty('voices')
    for voice in voices:
        if gender.lower() in voice.name.lower() or gender.lower() in getattr(voice, 'gender', '').lower():
            return voice.id
    return voices[0].id  # fallback

def list_voice_options():
    print("\n🗣️ Voice options:")
    print("1: Female Voice")
    print("2: Male Voice")
    print("3: 🤖 Robot Voice")
    print("4: 💻 Hacker Voice")

# -----------------------------
# 💾 Audio Generation
# -----------------------------
def save_wav(text, filename, voice_option=1, rate=150, volume=1.0):
    """Generate WAV file with selected voice option."""
    try:
        engine = pyttsx3.init()
    except Exception as e:
        print(f"❌ pyttsx3 init failed: {e}")
        return

    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)

    # Choose voice
    if voice_option == 1:  # Female
        engine.setProperty("voice", get_voice_by_gender(engine, "female"))
    elif voice_option == 2:  # Male
        engine.setProperty("voice", get_voice_by_gender(engine, "male"))
    elif voice_option == 3:  # Robot
        engine.setProperty("voice", engine.getProperty('voices')[0].id)
        text = " ".join([word + "..." + word for word in text.split()])
        engine.setProperty("rate", 120)
    elif voice_option == 4:  # Hacker
        engine.setProperty("voice", engine.getProperty('voices')[0].id)
        # Randomly insert pauses and leetspeak
        text = hacker_transform(text)
        engine.setProperty("rate", 140)

    engine.save_to_file(text, filename)
    engine.runAndWait()
    print(f"✅ Saved WAV file: {filename}")

def hacker_transform(text):
    """Transform text into 'hacker style' by adding leetspeak and pauses."""
    leet_dict = {'a':'4', 'e':'3', 'i':'1', 'o':'0', 's':'5', 't':'7'}
    words = text.split()
    transformed = []
    for word in words:
        w = ''.join(leet_dict.get(c.lower(), c) for c in word)
        w = '.'.join(list(w))  # insert dots between letters for effect
        transformed.append(w)
    return ' '.join(transformed)

def save_mp3(text, filename, lang="en"):
    """Generate MP3 file using gTTS."""
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        print(f"✅ Saved MP3 file: {filename}")
    except Exception as e:
        print(f"❌ Error generating MP3: {e}")

# -----------------------------
# 📘 PDF Text Extraction
# -----------------------------
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for i, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            text += page_text + "\n\n"
            print(f"📄 Extracted page {i}/{len(reader.pages)}")
        return text.strip()
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return ""

# -----------------------------
# ✍️ Save Text
# -----------------------------
def save_text_to_file(text, filename):
    if not text.strip():
        print("⚠️ No text to save.")
        return
    ext = os.path.splitext(filename)[1].lower()
    try:
        if ext == ".txt":
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"✅ Saved text to TXT: {filename}")
        elif ext == ".docx":
            doc = Document()
            for paragraph in text.split("\n\n"):
                doc.add_paragraph(paragraph)
            doc.save(filename)
            print(f"✅ Saved text to DOCX: {filename}")
        else:
            print("⚠️ Unsupported format. Use .txt or .docx.")
    except Exception as e:
        print(f"❌ Error saving text: {e}")

# -----------------------------
# 🚀 Main Logic
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="📖 Text-to-Speech Tool with voice options")
    parser.add_argument("--pdf", help="Path to PDF file")
    parser.add_argument("--text", "-t", help="Text to convert")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
    text_content = ""
    base_name = "output"

    # Input
    if not args.pdf and not args.text:
        print("\n📂 Choose input:")
        print("1: PDF file")
        print("2: Typed/pasted text")
        choice = input("👉 Enter 1 or 2: ").strip()
        if choice == "1":
            root = Tk(); root.withdraw()
            pdf_path = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF Files","*.pdf")])
            root.destroy()
            if not pdf_path: print("❌ No PDF selected."); return
            text_content = extract_text_from_pdf(pdf_path)
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        elif choice == "2":
            text_content = input("📝 Enter text:\n> ").strip()
            base_name = "text_input"
        else: print("⚠️ Invalid choice"); return
    elif args.pdf:
        if not os.path.exists(args.pdf): print("❌ PDF not found"); return
        text_content = extract_text_from_pdf(args.pdf)
        base_name = os.path.splitext(os.path.basename(args.pdf))[0]
    else:
        text_content = args.text.strip()
        base_name = "text_input"

    if not text_content: print("⚠️ No text to convert"); return

    # Output format
    output_choice = input("\n🎧 Output format (wav/mp3): ").strip().lower()
    if output_choice not in ["wav","mp3"]: output_choice="mp3"

    save_text_file = input("💾 Save text too? (y/n): ").strip().lower()=="y"

    # Speed
    rate = 150
    speed_choice = input("⚙️ Speaking speed (slow/normal/fast): ").strip().lower()
    if speed_choice=="slow": rate=120
    elif speed_choice=="fast": rate=200

    # Voice selection
    voice_option = 1
    if output_choice=="wav":
        list_voice_options()
        while True:
            choice = input("🎙️ Choose voice (1-4): ").strip()
            try:
                voice_option = int(choice)
                if 1 <= voice_option <=4: break
                else: print("⚠️ Invalid number")
            except ValueError: print("⚠️ Enter a number")

    # Generate
    audio_path = os.path.join(base_dir, f"{base_name}.{output_choice}")
    text_path = os.path.join(base_dir, f"{base_name}.txt")

    print("\n🚀 Generating audio...")
    if output_choice=="wav":
        save_wav(text_content, audio_path, voice_option=voice_option, rate=rate)
    else:
        save_mp3(text_content, audio_path)

    if save_text_file:
        save_text_to_file(text_content, text_path)

    print("\n✅ Done!")
    print(f"📂 Audio: {audio_path}")
    if save_text_file: print(f"📂 Text: {text_path}")

if __name__=="__main__":
    main()
