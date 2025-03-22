import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # Import ttk for Treeview widget
import pandas as pd
from generated_validation_code import validate_data  # Import validate_data function
import json

# Function to load the CSV file
def load_csv():
    # Open file dialog to select CSV
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            # Load CSV file into DataFrame
            data = pd.read_csv(file_path)
            global csv_data  # Store CSV data in a global variable for further processing
            csv_data = data
            # Display message to indicate the file has been successfully loaded
            status_label.config(text=f"File '{file_path.split('/')[-1]}' loaded successfully!", fg="green")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the file: {e}")

# Function to validate the CSV data and display results in the table
def submit_validation():
    if 'csv_data' not in globals():
        messagebox.showwarning("Warning", "Please upload a CSV file first!")
        return

    # Clear the existing table (if any)
    for row in treeview.get_children():
        treeview.delete(row)

    # Sample historic violations data (for demo purposes)
    historic_violations = {
        '1234567890': 3,  # Customer 1234567890 has 3 previous violations
        '0987654321': 1   # Customer 0987654321 has 1 previous violation
    }

    # Iterate over each row in the CSV data and validate
    for index, row in csv_data.iterrows():
        row_data = row.to_dict()  # Convert row to dictionary

        # Validate the data using the generated function (validate_data)
        errors, remediation_actions, risk_score = validate_data(row_data, historic_violations)

        # Retrieve Customer ID from the data and insert the result as a new row in the Treeview table
        customer_id = row_data.get('Customer_ID', f"Row {index+1}")  # Retrieve Customer ID

        # Insert row into the Treeview with Customer ID instead of Transaction ID
        treeview.insert('', 'end', values=(
            customer_id,
            ', '.join(errors) if errors else 'No Errors',
            ', '.join(remediation_actions) if remediation_actions else 'No Actions',
            risk_score
        ))

# Function to create the Tkinter UI
def create_ui():
    # Set up the root window
    root = tk.Tk()
    root.title("Data Validation UI")
    root.geometry("800x600")

    # Create and place the upload button
    upload_button = tk.Button(root, text="Upload CSV", command=load_csv, font=("Arial", 14), bg="lightblue")
    upload_button.pack(pady=10)

    # Status label to show file load status
    global status_label
    status_label = tk.Label(root, text="No file uploaded", font=("Arial", 12), fg="red")
    status_label.pack(pady=10)

    # Create and place the submit button to trigger validation
    submit_button = tk.Button(root, text="Submit for Validation", command=submit_validation, font=("Arial", 14), bg="lightgreen")
    submit_button.pack(pady=20)

    # Create the frame for the table
    table_frame = tk.Frame(root)
    table_frame.pack(pady=20, fill="both", expand=True)

    # Define columns for the table
    columns = ('Customer_ID', 'Errors', 'Remediation Actions', 'Risk Score')

    # Create Treeview widget for the table with scrollbars
    global treeview
    treeview = ttk.Treeview(table_frame, columns=columns, show='headings')

    # Define column headings
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, width=200, anchor='center')

    # Add horizontal scrollbar
    x_scroll = ttk.Scrollbar(table_frame, orient='horizontal', command=treeview.xview)
    x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    treeview.configure(xscrollcommand=x_scroll.set)

    # Add vertical scrollbar
    y_scroll = ttk.Scrollbar(table_frame, orient='vertical', command=treeview.yview)
    y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    treeview.configure(yscrollcommand=y_scroll.set)

    # Pack the Treeview into the frame
    treeview.pack(fill="both", expand=True)

    # Run the Tkinter main loop to display the UI
    root.mainloop()

if __name__ == "__main__":
    create_ui()
