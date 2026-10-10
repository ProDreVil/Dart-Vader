import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from collector.importer import run_importer

# MSG TO MICHAEL:
# Kel open ka ng Shopee, 'ctrl + a' mo tas 'ctrl + c' mo lahat automatic na yan
# Pagtapos mo ma-copy yung page, lipat ka ng iba tas 'ctrl + c' mo lang
# Di mo na kailangan mag 'ctrl + v' kasi eto na bahala
# Pinutin mo 'S' kung gusto mo i-stop yung program, 10 minutes mag-aauto stop siya

def import_duty():
    run_importer()

if __name__ == "__main__":
    import_duty()