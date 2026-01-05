import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os


class FileSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV/TXT File Splitter")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        # Title
        title_label = tk.Label(root, text="Split File into 10 Parts",
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Instructions
        instructions = tk.Label(root, text="Select a CSV or TXT file to split into 10 equal parts",
                                font=("Arial", 10))
        instructions.pack(pady=10)

        # Select file button
        self.select_button = tk.Button(root, text="Select File",
                                       command=self.select_and_split,
                                       font=("Arial", 12),
                                       bg="#4CAF50", fg="white",
                                       padx=20, pady=10)
        self.select_button.pack(pady=20)

        # Status label
        self.status_label = tk.Label(root, text="", font=("Arial", 10),
                                     fg="blue", wraplength=450)
        self.status_label.pack(pady=10)

    def select_and_split(self):
        # Open file dialog
        filename = filedialog.askopenfilename(
            title="Select a file to split",
            filetypes=(("CSV files", "*.csv"), ("Text files", "*.txt"),
                       ("All files", "*.*"))
        )

        if not filename:
            return

        try:
            self.status_label.config(text="Processing...", fg="blue")
            self.root.update()

            # Split the file
            output_dir = self.split_file(filename)

            # Show success message
            self.status_label.config(
                text=f"Success! Files saved in:\n{output_dir}",
                fg="green"
            )
            messagebox.showinfo("Success",
                                f"File split into 10 parts successfully!\n\n"
                                f"Output location:\n{output_dir}")

        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg="red")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def split_file(self, input_file):
        # Read all lines from the input file
        with open(input_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            lines = list(reader)

        total_lines = len(lines)

        if total_lines == 0:
            raise ValueError("The file is empty!")

        # Calculate lines per file
        lines_per_file = total_lines // 10

        # Create output directory in the same location as input file
        input_dir = os.path.dirname(input_file)
        input_basename = os.path.splitext(os.path.basename(input_file))[0]
        output_dir = os.path.join(input_dir, f"{input_basename}_split")

        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Split and write files
        for i in range(10):
            output_file = os.path.join(output_dir, f"output_{i + 1}.csv")

            # Calculate start and end indices
            start_idx = i * lines_per_file

            # For the last file, include all remaining lines
            if i == 9:
                end_idx = total_lines
            else:
                end_idx = (i + 1) * lines_per_file

            # Write the chunk to output file
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(lines[start_idx:end_idx])

        return output_dir


def main():
    root = tk.Tk()
    app = FileSplitterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()