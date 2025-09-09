import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import time
from moviepy.editor import VideoFileClip


class TempoTweakApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TempoTweak")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        # Variables
        self.input_video_path = tk.StringVar()
        self.output_folder_path = tk.StringVar()
        self.target_fps = tk.StringVar(value="30")
        self.progress_var = tk.DoubleVar()
        self.is_processing = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="TempoTweak - Video FPS Modifier", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input video selection
        ttk.Label(main_frame, text="Select Input Video:").grid(row=1, column=0, 
                                                              sticky=tk.W, pady=5)
        
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_video_path, 
                                   width=60, state="readonly")
        self.input_entry.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(input_frame, text="Browse", 
                  command=self.browse_input_video).grid(row=0, column=1)
        
        # Output folder selection
        ttk.Label(main_frame, text="Select Output Folder:").grid(row=3, column=0, 
                                                                sticky=tk.W, pady=5)
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_folder_path, 
                                    width=60, state="readonly")
        self.output_entry.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(output_frame, text="Browse", 
                  command=self.browse_output_folder).grid(row=0, column=1)
        
        # FPS selection
        fps_frame = ttk.Frame(main_frame)
        fps_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(fps_frame, text="Target FPS:").grid(row=0, column=0, sticky=tk.W)
        
        # FPS entry with validation
        vcmd = (self.root.register(self.validate_fps), '%P')
        self.fps_entry = ttk.Entry(fps_frame, textvariable=self.target_fps, 
                                 width=10, validate='key', validatecommand=vcmd)
        self.fps_entry.grid(row=0, column=1, padx=(10, 20))
        
        # Common FPS buttons
        common_fps = [4, 24, 30, 60, 120]
        for i, fps in enumerate(common_fps):
            ttk.Button(fps_frame, text=f"{fps}", width=5,
                      command=lambda f=fps: self.set_fps(f)).grid(row=0, column=i+2, padx=2)
        
        # Current video info
        self.info_frame = ttk.LabelFrame(main_frame, text="Video Information", padding="10")
        self.info_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                           pady=10, padx=5)
        
        self.info_label = ttk.Label(self.info_frame, text="No video selected", 
                                  foreground="gray")
        self.info_label.grid(row=0, column=0, sticky=tk.W)
        
        # Progress bar
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                               pady=10)
        
        ttk.Label(self.progress_frame, text="Progress:").grid(row=0, column=0, sticky=tk.W)
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.status_label = ttk.Label(self.progress_frame, text="Ready", 
                                    foreground="green")
        self.status_label.grid(row=2, column=0, sticky=tk.W)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=3, pady=20)
        
        self.start_button = ttk.Button(button_frame, text="Start Processing", 
                                     command=self.start_processing)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.cancel_button = ttk.Button(button_frame, text="Cancel", 
                                      command=self.cancel_processing, state="disabled")
        self.cancel_button.grid(row=0, column=1)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(0, weight=1)
        output_frame.columnconfigure(0, weight=1)
        self.progress_frame.columnconfigure(0, weight=1)
        
    def validate_fps(self, value):
        """Validate FPS input - only allow numbers and decimal points"""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def set_fps(self, fps):
        """Set FPS from button click"""
        self.target_fps.set(str(fps))
    
    def browse_input_video(self):
        """Browse for input video file"""
        file_types = [
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v"),
            ("MP4 files", "*.mp4"),
            ("AVI files", "*.avi"),
            ("MOV files", "*.mov"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=file_types
        )
        
        if filename:
            self.input_video_path.set(filename)
            self.load_video_info()
    
    def browse_output_folder(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder_path.set(folder)
    
    def load_video_info(self):
        """Load and display video information"""
        try:
            if self.input_video_path.get():
                clip = VideoFileClip(self.input_video_path.get())
                duration = clip.duration
                fps = clip.fps
                resolution = clip.size
                
                info_text = f"Duration: {duration:.2f}s | Current FPS: {fps:.2f} | Resolution: {resolution[0]}x{resolution[1]}"
                self.info_label.config(text=info_text, foreground="black")
                clip.close()
        except Exception as e:
            self.info_label.config(text=f"Error loading video: {str(e)}", foreground="red")
    
    def validate_inputs(self):
        """Validate all inputs before processing"""
        if not self.input_video_path.get():
            messagebox.showerror("Error", "Please select an input video file.")
            return False
        
        if not os.path.exists(self.input_video_path.get()):
            messagebox.showerror("Error", "Input video file does not exist.")
            return False
        
        if not self.output_folder_path.get():
            messagebox.showerror("Error", "Please select an output folder.")
            return False
        
        if not os.path.exists(self.output_folder_path.get()):
            messagebox.showerror("Error", "Output folder does not exist.")
            return False
        
        try:
            fps = float(self.target_fps.get())
            if fps <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid FPS value (greater than 0).")
            return False
        
        return True
    
    def get_output_filename(self):
        """Generate output filename"""
        input_path = self.input_video_path.get()
        output_folder = self.output_folder_path.get()
        target_fps = self.target_fps.get()
        
        # Get filename without extension
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        extension = os.path.splitext(input_path)[1]
        
        # Create new filename
        new_name = f"{base_name}_{target_fps}fps{extension}"
        return os.path.join(output_folder, new_name)
    
    def start_processing(self):
        """Start video processing in a separate thread"""
        if not self.validate_inputs():
            return
        
        if self.is_processing:
            return
        
        # Check if output file already exists
        output_path = self.get_output_filename()
        if os.path.exists(output_path):
            result = messagebox.askyesno(
                "File Exists", 
                f"Output file already exists:\n{output_path}\n\nDo you want to overwrite it?"
            )
            if not result:
                return
        
        self.is_processing = True
        self.start_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.progress_var.set(0)
        self.status_label.config(text="Processing...", foreground="orange")
        
        # Start processing in a separate thread
        self.processing_thread = threading.Thread(target=self.process_video)
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def process_video(self):
        """Process the video with new FPS"""
        try:
            input_path = self.input_video_path.get()
            output_path = self.get_output_filename()
            target_fps = float(self.target_fps.get())
            
            # Load video
            self.root.after(0, lambda: self.status_label.config(text="Loading video..."))
            self.root.after(0, lambda: self.progress_var.set(5))
            clip = VideoFileClip(input_path)
            
            # Get video info for progress calculation
            total_duration = clip.duration
            
            # Change FPS
            self.root.after(0, lambda: self.status_label.config(text="Changing FPS..."))
            self.root.after(0, lambda: self.progress_var.set(15))
            new_clip = clip.set_fps(target_fps)
            
            # Write video file with progress tracking
            self.root.after(0, lambda: self.status_label.config(text="Processing video..."))
            
            # Simple progress simulation during processing
            def simulate_progress():
                progress = 15
                while self.is_processing and progress < 90:
                    self.root.after(0, lambda p=progress: self.progress_var.set(p))
                    progress += 1
                    time.sleep(0.5)  # Update every 0.5 seconds
            
            # Start progress simulation in a separate thread
            progress_thread = threading.Thread(target=simulate_progress)
            progress_thread.daemon = True
            progress_thread.start()
            
            # Write the video file
            new_clip.write_videofile(
                output_path,
                fps=target_fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            # Final progress updates
            if self.is_processing:
                self.root.after(0, lambda: self.progress_var.set(95))
                self.root.after(0, lambda: self.status_label.config(text="Finalizing..."))
                time.sleep(0.5)
            
            # Clean up
            new_clip.close()
            clip.close()
            
            if self.is_processing:  # Only show success if not cancelled
                self.root.after(0, lambda: self.processing_complete(output_path))
            
        except Exception as e:
            if self.is_processing:  # Only show error if not cancelled
                error_message = str(e)
                self.root.after(0, lambda: self.processing_error(error_message))
    
    def processing_complete(self, output_path):
        """Handle successful processing completion"""
        self.is_processing = False
        self.start_button.config(state="normal")
        self.cancel_button.config(state="disabled")
        self.progress_var.set(100)
        self.status_label.config(text="Processing complete!", foreground="green")
        
        messagebox.showinfo(
            "Success", 
            f"Video processing completed successfully!\n\nOutput saved to:\n{output_path}"
        )
    
    def processing_error(self, error_message):
        """Handle processing error"""
        self.is_processing = False
        self.start_button.config(state="normal")
        self.cancel_button.config(state="disabled")
        self.progress_var.set(0)
        self.status_label.config(text="Processing failed", foreground="red")
        
        messagebox.showerror("Error", f"An error occurred during processing:\n\n{error_message}")
    
    def cancel_processing(self):
        """Cancel video processing"""
        if self.is_processing:
            result = messagebox.askyesno("Cancel", "Are you sure you want to cancel processing?")
            if result:
                self.is_processing = False
                self.start_button.config(state="normal")
                self.cancel_button.config(state="disabled")
                self.progress_var.set(0)
                self.status_label.config(text="Processing cancelled", foreground="red")


def main():
    root = tk.Tk()
    app = TempoTweakApp(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
