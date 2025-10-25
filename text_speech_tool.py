import argparse
import pyttsx3
from gtts import gTTS
import os
from PyPDF2 import PdfReader
from docx import Document
from tkinter import Tk, filedialog

# -----------------------------
# 🗣️ Voice Management
# -----------------------------
def list_system_voices(engine):
    """List all system voices and return them."""
    voices = engine.getProperty('voices')
    if not voices:
        print("⚠️ No system voices detected! Only simulated voices available.")
    else:
        print("\n🎙️ Available system voices:")
        for i, voice in enumerate(voices):
            lang = voice.languages[0] if voice.languages else 'Unknown'
            gender = getattr(voice, 'gender', 'Unknown')
            print(f"{i}: {voice.name} ({gender}, {lang})")
    # Add simulated voices
    print(f"{len(voices)}: 🤖 Robot Voice (simulated)")
    print(f"{len(voices)+1}: 💻 Hacker Voice (simulated)")
    return voices

def hacker_transform(text):
    """Transform text into hacker-style leetspeak."""
    leet_dict = {'a':'4','e':'3','i':'1','o':'0','s':'5','t':'7'}
    words = text.split()
    transformed = []
    for word in words:
        w = ''.join(leet_dict.get(c.lower(), c) for c in word)
        w = '.'.join(list(w))
        transformed.append(w)
    return ' '.join(transformed)

# -----------------------------
# 💾 Audio Generation
# -----------------------------
def save_wav(text, filename, voice_id=None, rate=150, volume=1.0):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    if voice_id:
        engine.setProperty('voice', voice_id)
    engine.save_to_file(text, filename)
    engine.runAndWait()
    print(f"✅ Saved WAV: {filename}")

def save_mp3(text, filename, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        print(f"✅ Saved MP3: {filename}")
    except Exception as e:
        print(f"❌ gTTS error: {e}")

# -----------------------------
# 🔊 Voice Preview
# -----------------------------
def preview_voice(text, voice_id, rate=150):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    if voice_id:
        engine.setProperty('voice', voice_id)
    print("🔊 Playing preview...")
    engine.say(text)
    engine.runAndWait()

# -----------------------------
# 📘 PDF Extraction
# -----------------------------
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for i, page in enumerate(reader.pages, start=1):
            text += (page.extract_text() or "") + "\n\n"
            print(f"📄 Extracted page {i}/{len(reader.pages)}")
        return text.strip()
    except Exception as e:
        print(f"❌ PDF error: {e}")
        return ""

# -----------------------------
# ✍️ Save Text
# -----------------------------
def save_text_to_file(text, filename):
    ext = os.path.splitext(filename)[1].lower()
    try:
        if ext == '.txt':
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"✅ Saved TXT: {filename}")
        elif ext == '.docx':
            doc = Document()
            for p in text.split('\n\n'):
                doc.add_paragraph(p)
            doc.save(filename)
            print(f"✅ Saved DOCX: {filename}")
        else:
            print("⚠️ Unsupported format")
    except Exception as e:
        print(f"❌ Error saving text: {e}")

# -----------------------------
# 🚀 Main
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Text-to-Speech Tool with system voice selection")
    parser.add_argument("--pdf", help="PDF file path")
    parser.add_argument("--text", "-t", help="Text to convert")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    text_content = ""
    base_name = "output"

    # -----------------------------
    # Voice selection first
    # -----------------------------
    engine = pyttsx3.init()
    voices = list_system_voices(engine)

    while True:
        choice = input("Choose voice number (system voices + simulated): ").strip()
        try:
            voice_index = int(choice)
            if 0 <= voice_index <= len(voices) + 1:
                break
            else:
                print("⚠️ Invalid number")
        except ValueError:
            print("⚠️ Enter a number")

    # Map voice selection
    if voice_index < len(voices):
        selected_voice_id = voices[voice_index].id
        text_transform = lambda t: t
    elif voice_index == len(voices):  # Robot
        selected_voice_id = voices[0].id if voices else None
        text_transform = lambda t: " ".join([word + "..." + word for word in t.split()])
    elif voice_index == len(voices) + 1:  # Hacker
        selected_voice_id = voices[0].id if voices else None
        text_transform = hacker_transform

    # -----------------------------
    # Input selection
    # -----------------------------
    if not args.pdf and not args.text:
        choice = input("1: PDF file\n2: Typed text\n👉 Choose: ").strip()
        if choice == "1":
            root = Tk(); root.withdraw()
            pdf_path = filedialog.askopenfilename(filetypes=[("PDF","*.pdf")])
            root.destroy()
            if not pdf_path:
                print("❌ No PDF selected")
                return
            text_content = extract_text_from_pdf(pdf_path)
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        elif choice == "2":
            text_content = input("📝 Enter text:\n> ").strip()
            base_name = "text_input"
        else:
            print("⚠️ Invalid choice")
            return
    elif args.pdf:
        if not os.path.exists(args.pdf):
            print("❌ PDF not found")
            return
        text_content = extract_text_from_pdf(args.pdf)
        base_name = os.path.splitext(os.path.basename(args.pdf))[0]
    else:
        text_content = args.text.strip()
        base_name = "text_input"

    if not text_content:
        print("⚠️ No text")
        return

    # Apply text transform if needed (Robot/Hacker)
    text_content = text_transform(text_content)

    # -----------------------------
    # Voice preview
    # -----------------------------
    preview_choice = input("👂 Preview this voice? (y/n): ").strip().lower()
    if preview_choice == 'y':
        sample_text = ' '.join(text_content.split()[:30])
        preview_voice(sample_text, selected_voice_id, rate=150)

    # -----------------------------
    # Output format
    # -----------------------------
    output_choice = input("🎧 Output format (wav/mp3): ").strip().lower()
    if output_choice not in ['wav', 'mp3']:
        output_choice = 'mp3'
    save_text_file = input("💾 Save text? (y/n): ").strip().lower() == 'y'

    # Speed
    rate = 150
    speed_choice = input("⚙️ Speed (slow/normal/fast): ").strip().lower()
    if speed_choice == 'slow':
        rate = 120
    elif speed_choice == 'fast':
        rate = 200

    # -----------------------------
    # Generate files
    # -----------------------------
    audio_path = os.path.join(base_dir, f"{base_name}.{output_choice}")
    text_path = os.path.join(base_dir, f"{base_name}.txt")

    print("🚀 Generating audio...")
    if output_choice == 'wav':
        save_wav(text_content, audio_path, voice_id=selected_voice_id, rate=rate)
    else:
        save_mp3(text_content, audio_path)

    if save_text_file:
        save_text_to_file(text_content, text_path)

    print("\n✅ Done!")
    print(f"📂 Audio: {audio_path}")
    if save_text_file:
        print(f"📂 Text: {text_path}")

if __name__ == "__main__":
    main()
