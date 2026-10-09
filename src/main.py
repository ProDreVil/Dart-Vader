from evaluation.evaluator import analyze_and_save
from utils.config import DATA_FILE, ANALYZED_DATA_FILE

def main():
    print("Started Analysis...")
    output_file = ANALYZED_DATA_FILE
    analyze_and_save(DATA_FILE, output_file)
    print(f"Analysis saved to {output_file}")

if __name__ == "__main__":
    main()