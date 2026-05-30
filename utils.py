import csv
import os

def save_to_csv(data):
    file_exists = os.path.isfile("data.csv")

    with open("data.csv", "a", newline="", encoding="utf-8") as file:
        fieldnames = ["name", "email", "phone", "role", "score", "decision"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)