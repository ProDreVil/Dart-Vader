import subprocess
import time
import msvcrt
import winsound

from config import PROJECT_NAME, DATA_FILE, RAW_DATA_DIR
from collector.parser import parse_reviews_from_text
from collector.storage import save_reviews

SFX_FILE = "resources/sfx/kaching.mp3"

def get_clipboard():
    result = subprocess.run(
        ["powershell", "-command", "Get-Clipboard"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    return result.stdout

def play_sfx():
    winsound.PlaySound(None, 0)
    winsound.PlaySound(
        "resources/sfx/kaching.wav",
        winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT
    )

# MSG TO MICHAEL:
# Kel open ka ng Shopee, 'ctrl + a' mo tas 'ctrl + c' mo lahat automatic na yan
# Pagtapos mo ma-copy yung page, lipat ka ng iba tas 'ctrl + c' mo lang
# Di mo na kailangan mag 'ctrl + p' kasi eto na bahala
# Pinutin mo 'S' kung gusto mo i-stop yung program, 10 minutes lang siya gagana

def main():
    print(f"{PROJECT_NAME} is starting...")
    print("(Press [S] to stop)")
    previous_clipboard = ""
    start_time = time.time()
    while time.time() - start_time < 600:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode("utf-8").lower()
            if key == "s":
                print("\nStopping program...")
                break
        raw_text = get_clipboard()
        if raw_text and raw_text != previous_clipboard:
            previous_clipboard = raw_text
            with open("data/raw/pasted_reviews.txt", "w", encoding="utf-8") as file:
                file.write(raw_text)
            print("----------------------------------------")
            print("New clipboard content detected.")
            play_sfx()
            reviews = parse_reviews_from_text(raw_text)
            print(f"Parsed {len(reviews)} review(s).")
            if not reviews:
                print("WARNING: No reviews were detected in the clipboard.")
            saved_count, duplicate_count = save_reviews(reviews, DATA_FILE)
            print(f"Saved {saved_count} new review(s).")
            print(f"Skipped {duplicate_count} duplicate review(s).")
        time.sleep(0.5)
    print("\nProgram stopped.")
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        total_reviews = sum(1 for line in file) - 1
    print(f"Total reviews: {total_reviews}")

if __name__ == "__main__":
    main()