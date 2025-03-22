# scripts/validate_data.py

from generated_validation_code import validate_data  # Ensure this import is correct

import pandas as pd

def validate_dataset(data_file):
    data = pd.read_csv(data_file)
    errors = []

    for index, row in data.iterrows():
        validation_errors = validate_data(row)  # Calls the validate_data function
        if validation_errors:
            errors.append((index, validation_errors))

    return errors

if __name__ == "__main__":
    validation_errors = validate_dataset('C://Users//jahna//IdeaProjects//DataProfiling//src//data//example_data.csv')
    if validation_errors:
        for error in validation_errors:
            print(f"Row {error[0]}: {error[1]}")
    else:
        print("No validation errors found!")
