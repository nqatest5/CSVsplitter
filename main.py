import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os
import pandas as pd


class FileSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV File Splitter & Processor")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        # Title
        title_label = tk.Label(root, text="CSV File Processor",
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=20)

        # Frame for Mode Selection
        mode_frame = tk.Frame(root)
        mode_frame.pack(pady=10)

        tk.Label(mode_frame, text="Select Mode:", font=("Arial", 12, "bold")).pack()

        # Mode 1: Split file into 10 parts
        mode1_frame = tk.Frame(root, relief=tk.RIDGE, borderwidth=2, padx=20, pady=15)
        mode1_frame.pack(pady=10, padx=20, fill=tk.BOTH)

        tk.Label(mode1_frame, text="Mode 1: Split File",
                 font=("Arial", 12, "bold")).pack()
        tk.Label(mode1_frame, text="Split a CSV/TXT file into 10 equal parts",
                 font=("Arial", 9)).pack(pady=5)

        self.split_button = tk.Button(mode1_frame, text="Select File to Split",
                                      command=self.select_and_split,
                                      font=("Arial", 11),
                                      bg="#4CAF50", fg="white",
                                      padx=15, pady=8)
        self.split_button.pack(pady=5)

        # Mode 2: Process WLOCK and EVENT_COUNT files
        mode2_frame = tk.Frame(root, relief=tk.RIDGE, borderwidth=2, padx=20, pady=15)
        mode2_frame.pack(pady=10, padx=20, fill=tk.BOTH)

        tk.Label(mode2_frame, text="Mode 2: Process WLOCK & EVENT_COUNT",
                 font=("Arial", 12, "bold")).pack()
        tk.Label(mode2_frame, text="Rank and combine WLOCK_DESC.csv and EVENT_COUNT DESC.csv",
                 font=("Arial", 9)).pack(pady=5)

        self.process_button = tk.Button(mode2_frame, text="Select Files to Process",
                                        command=self.select_and_process,
                                        font=("Arial", 11),
                                        bg="#2196F3", fg="white",
                                        padx=15, pady=8)
        self.process_button.pack(pady=5)

        # Status label
        self.status_label = tk.Label(root, text="", font=("Arial", 10),
                                     fg="blue", wraplength=550)
        self.status_label.pack(pady=15)

    def select_and_split(self):
        """Original functionality: Split file into 10 parts"""
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

            output_dir = self.split_file(filename)

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
        """Split file into 10 equal parts"""
        with open(input_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            lines = list(reader)

        total_lines = len(lines)

        if total_lines == 0:
            raise ValueError("The file is empty!")

        lines_per_file = total_lines // 10

        input_dir = os.path.dirname(input_file)
        input_basename = os.path.splitext(os.path.basename(input_file))[0]
        output_dir = os.path.join(input_dir, f"{input_basename}_split")

        os.makedirs(output_dir, exist_ok=True)

        for i in range(10):
            output_file = os.path.join(output_dir, f"output_{i + 1}.csv")
            start_idx = i * lines_per_file
            end_idx = total_lines if i == 9 else (i + 1) * lines_per_file

            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(lines[start_idx:end_idx])

        return output_dir

    def select_and_process(self):
        """New functionality: Process WLOCK and EVENT_COUNT files"""
        self.status_label.config(text="Select WLOCK_DESC.csv file...", fg="blue")
        self.root.update()

        wlock_file = filedialog.askopenfilename(
            title="Select WLOCK_DESC.csv",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )

        if not wlock_file:
            return

        self.status_label.config(text="Select EVENT_COUNT DESC.csv file...", fg="blue")
        self.root.update()

        event_file = filedialog.askopenfilename(
            title="Select EVENT_COUNT DESC.csv",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )

        if not event_file:
            return

        try:
            self.status_label.config(text="Processing files...", fg="blue")
            self.root.update()

            output_dir = self.process_wlock_event_files(wlock_file, event_file)

            self.status_label.config(
                text=f"Success! Processed files saved in:\n{output_dir}",
                fg="green"
            )
            messagebox.showinfo("Success",
                                f"Files processed successfully!\n\n"
                                f"Output location:\n{output_dir}")

        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg="red")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def process_wlock_event_files(self, wlock_file, event_file):
        """Process WLOCK and EVENT_COUNT files according to specifications"""

        # Read WLOCK_DESC.csv
        wlock_df = pd.read_csv(wlock_file)

        # Clean column names (remove whitespace)
        wlock_df.columns = wlock_df.columns.str.strip()

        # Select only PACK and WLOCK columns
        wlock_cols = [col for col in wlock_df.columns if 'PACK' in col.upper()]
        wlock_metric_cols = [col for col in wlock_df.columns if 'WLOCK' in col.upper()]

        if not wlock_cols or not wlock_metric_cols:
            raise ValueError("Could not find PACK and WLOCK columns in WLOCK_DESC.csv")

        wlock_df = wlock_df[[wlock_cols[0], wlock_metric_cols[0]]]
        wlock_df.columns = ['PACK', 'WLOCK']

        # Remove duplicates and sort by WLOCK (largest to smallest)
        wlock_df = wlock_df.drop_duplicates(subset=['PACK'])
        wlock_df = wlock_df.sort_values(by='WLOCK', ascending=False).reset_index(drop=True)

        # Add rank for WLOCK (1 = highest value)
        wlock_df['WLOCK_RANK'] = range(1, len(wlock_df) + 1)

        # Read EVENT_COUNT DESC.csv
        event_df = pd.read_csv(event_file)

        # Clean column names
        event_df.columns = event_df.columns.str.strip()

        # Select only PACK and EVENT_COUNT columns
        event_pack_cols = [col for col in event_df.columns if 'PACK' in col.upper()]
        event_count_cols = [col for col in event_df.columns if 'EVENT' in col.upper() and 'COUNT' in col.upper()]

        if not event_pack_cols or not event_count_cols:
            raise ValueError("Could not find PACK and EVENT_COUNT columns in EVENT_COUNT DESC.csv")

        event_df = event_df[[event_pack_cols[0], event_count_cols[0]]]
        event_df.columns = ['PACK', 'EVENT_COUNT']

        # Remove duplicates and sort by EVENT_COUNT (largest to smallest)
        event_df = event_df.drop_duplicates(subset=['PACK'])
        event_df = event_df.sort_values(by='EVENT_COUNT', ascending=False).reset_index(drop=True)

        # Add rank for EVENT_COUNT (1 = highest value)
        event_df['EVENT_COUNT_RANK'] = range(1, len(event_df) + 1)

        # Merge the two dataframes on PACK
        merged_df = pd.merge(wlock_df, event_df[['PACK', 'EVENT_COUNT', 'EVENT_COUNT_RANK']],
                             on='PACK', how='outer')

        # Fill NaN ranks with a high number (packages that only appear in one file)
        max_rank = max(len(wlock_df), len(event_df)) + 1
        merged_df['WLOCK_RANK'] = merged_df['WLOCK_RANK'].fillna(max_rank)
        merged_df['EVENT_COUNT_RANK'] = merged_df['EVENT_COUNT_RANK'].fillna(max_rank)

        # Calculate sum of ranks
        merged_df['RANK_SUM'] = merged_df['WLOCK_RANK'] + merged_df['EVENT_COUNT_RANK']

        # Sort by rank sum (lowest sum = best rank)
        merged_df = merged_df.sort_values(by='RANK_SUM').reset_index(drop=True)

        # Add final rank
        merged_df['FINAL_RANK'] = range(1, len(merged_df) + 1)

        # Create output directory
        output_dir = os.path.join(os.path.dirname(wlock_file), "processed_rankings")
        os.makedirs(output_dir, exist_ok=True)

        # Save the full merged file for reference
        full_output = os.path.join(output_dir, "full_rankings.csv")
        merged_df.to_csv(full_output, index=False)

        # Split into Top files (up to 4000 rows, excluding header)
        total_packages = len(merged_df)

        # Determine how many files to create
        if total_packages <= 1000:
            ranges = [(1, min(1000, total_packages))]
        elif total_packages <= 2000:
            ranges = [(1, 1000), (1001, total_packages)]
        elif total_packages <= 3000:
            ranges = [(1, 1000), (1001, 2000), (2001, total_packages)]
        else:
            ranges = [(1, 1000), (1001, 2000), (2001, 3000), (3001, min(4000, total_packages))]

        # Create the Top files
        for start, end in ranges:
            filename = f"Top{start}-{end}.csv"
            output_file = os.path.join(output_dir, filename)

            # Extract the subset (accounting for 0-based indexing)
            subset_df = merged_df.iloc[start - 1:end]
            subset_df.to_csv(output_file, index=False)

        return output_dir


def main():
    root = tk.Tk()
    app = FileSplitterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()