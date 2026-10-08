from evaluation.evaluator import load_reviews, analyze_reviews, save_analysis
from config import DATA_FILE

def main():
    reviews = load_reviews(DATA_FILE)
    evaluated = analyze_reviews(reviews)
    output_file = "data/manual/analyzed_reviews.csv"
    save_analysis(evaluated, output_file)
    print(f"\nAnalysis saved to {output_file}")

if __name__ == "__main__":
    main()