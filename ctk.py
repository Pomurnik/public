import customtkinter as ctk
from joblib import Parallel, delayed
import threading
import time
import os

# Dummy match_name_parallel function
def match_name_parallel(chunk, matcher):
    time.sleep(1)  # Simulate processing time
    return chunk

# Your function to process chunks in parallel
def process_chunks(chunks, matcher, n_jobs, progress_bar, root):
    def update_progress(current_progress):
        # Update the progress bar in the GUI thread
        progress_bar.set(current_progress)
        root.update_idletasks()

    # Define the function that runs in a separate thread
    def run_parallel():
        total_chunks = len(chunks)
        
        # Suppress terminal output by redirecting to os.devnull
        with open(os.devnull, 'w') as fnull:
            for i, _ in enumerate(
                Parallel(n_jobs=n_jobs, verbose=0)(
                    delayed(match_name_parallel)(chunk, matcher) for chunk in chunks
                ), 1
            ):
                # Update progress in the GUI thread
                update_progress(i / total_chunks * 100)  # Percentage progress

        # Once the process is done, set the progress bar to 100%
        update_progress(100)
    
    # Run the parallel processing in a separate thread to keep the UI responsive
    threading.Thread(target=run_parallel, daemon=True).start()

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
