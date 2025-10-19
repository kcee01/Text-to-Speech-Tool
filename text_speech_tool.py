import argparse
import pyttsx3
from gtts import gTTS

def list_voices(engine):
    """List available voices for pyttsx3."""
    voices = engine.getProperty('voices')
    print("\n🗣️ Available voices:")
    for i, voice in enumerate(voices):
        print(f"{i}: {voice.name} ({voice.id})")
    print(f"{len(voices)}: 🤖 Robot Voice (simulated)")
    print(f"{len(voices) + 1}: 🕶️ Deep Voice (simulated)")
    return voices

def save_wav(text, filename, voice_id=None, rate=150):
    """Generate WAV file using pyttsx3 (offline)"""
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    voices = engine.getProperty('voices')

    # Handle robot and deep voice
    if voice_id is not None:
        if voice_id == len(voices):  # Robot voice
            print("🤖 Applying robot effect...")
            engine.setProperty('rate', 120)
            engine.setProperty('volume', 1.0)
            engine.setProperty('voice', voices[0].id)
            text = ' '.join([word + "..." + word for word in text.split()])

        elif voice_id == len(voices) + 1:  # Deep voice
            print("🕶️ Applying deep voice effect...")
            engine.setProperty('rate', 110)
            engine.setProperty('voice', voices[0].id)
            # Trick: Add a deep-tone simulation (stretch text slightly)
            text = ' '.join([word + '...' for word in text.split()])

        else:  # Normal voice
            try:
                engine.setProperty('voice', voices[voice_id].id)
            except Exception:
                print("⚠️ Invalid voice index, using default.")
    engine.save_to_file(text, filename)
    engine.runAndWait()
    print(f"✅ Saved WAV file: {filename}")

def save_mp3(text, filename, lang='en'):
    """Generate MP3 file using gTTS (online, requires internet)"""
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    print(f"✅ Saved MP3 file: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Text-to-Speech Tool with Voice Options (Robot, Deep, etc.)")
    parser.add_argument("--text", "-t", help="Text to convert to speech")
    parser.add_argument("--wav", help="Output WAV file (offline, uses pyttsx3)")
    parser.add_argument("--mp3", help="Output MP3 file (online, uses gTTS)")
    args = parser.parse_args()

    if not args.text:
        args.text = input("📝 Enter the text you want to convert to speech:\n> ")

    if not args.wav and not args.mp3:
        choice = input("🎧 Do you want WAV or MP3 output? (type 'wav' or 'mp3'): ").strip().lower()
        filename = input("💾 Enter output filename (without extension): ").strip()
        if choice == "wav":
            args.wav = f"{filename}.wav"
        elif choice == "mp3":
            args.mp3 = f"{filename}.mp3"
        else:
            print("⚠️ Invalid choice. Please restart.")
            return

    try:
        speed_choice = input("⚙️ Choose speaking speed (slow / normal / fast): ").strip().lower()
        if speed_choice == "slow":
            rate = 120
        elif speed_choice == "fast":
            rate = 200
        else:
            rate = 150
    except Exception:
        rate = 150

    if args.wav:
        engine = pyttsx3.init()
        voices = list_voices(engine)
        try:
            voice_choice = int(input("\n🎙️ Choose a voice number from the list above: "))
        except ValueError:
            voice_choice = None
        save_wav(args.text, args.wav, voice_id=voice_choice, rate=rate)

    if args.mp3:
        save_mp3(args.text, args.mp3)

if __name__ == "__main__":
    main()
