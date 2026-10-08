from collector.importer import run_importer
from evaluation.evaluator import load_reviews, analyze_reviews, save_analysis
from config import DATA_FILE

# MSG TO MICHAEL:
# Kel open ka ng Shopee, 'ctrl + a' mo tas 'ctrl + c' mo lahat automatic na yan
# Pagtapos mo ma-copy yung page, lipat ka ng iba tas 'ctrl + c' mo lang
# Di mo na kailangan mag 'ctrl + p' kasi eto na bahala
# Pinutin mo 'S' kung gusto mo i-stop yung program, 10 minutes lang siya gagana

def main():
    run_importer()
    # reviews = load_reviews(DATA_FILE)
    # evaluated = analyze_reviews(reviews)
    # output_file = "data/analyzed_reviews.csv"
    # save_analysis(evaluated, output_file)
    # print(f"\nAnalysis saved to {output_file}")

if __name__ == "__main__":
    main()