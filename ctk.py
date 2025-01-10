import customtkinter as ctk
from joblib import Parallel, delayed
from tqdm import tqdm
import time
import os

# Dummy match_name_parallel function
def match_name_parallel(chunk, matcher):
    time.sleep(1)  # Simulate processing time
    return chunk

# Your function to process chunks in parallel
def process_chunks(chunks, matcher, n_jobs, progress_bar, root):
    # Define a tqdm wrapper to update the progress bar
    def update_progress(t):
        progress_bar.set(t)
        root.update_idletasks()

    # Wrap the tqdm with the update_progress function
    with open(os.devnull, 'w') as fnull:
        results = Parallel(n_jobs=n_jobs, verbose=0)(
            delayed(match_name_parallel)(chunk, matcher) for chunk in tqdm(chunks, 
                                                                           desc="Processing", 
                                                                           ncols=100, 
                                                                           position=0, 
                                                                           leave=True, 
                                                                           file=fnull,  # Suppress output in terminal
                                                                           dynamic_ncols=True, 
                                                                           update_interval=0.1)
        )

    # Once the process is done, stop the progress bar
    progress_bar.set(100)
    root.update_idletasks()

# Create the customtkinter window
root = ctk.CTk()
root.title("Parallel Processing with Progress")

# Create a customtkinter progress bar
progress_bar = ctk.CTkProgressBar(root, width=300, height=20)
progress_bar.pack(pady=20)

# Dummy data for chunks
chunks = ["chunk1", "chunk2", "chunk3", "chunk4", "chunk5"]
matcher = None  # Replace with actual matcher if needed
n_jobs = 2  # Number of parallel jobs

# Start processing on button click
start_button = ctk.CTkButton(root, text="Start Processing", 
                             command=lambda: process_chunks(chunks, matcher, n_jobs, progress_bar, root))
start_button.pack(pady=10)

root.mainloop()
