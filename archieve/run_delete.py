import cv2
import os
import numpy as np
import face_recognition
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.simpledialog as simpledialog
import tkinter.filedialog as filedialog

class VideoStreamApp:
    def __init__(self, window, window_title, video_source=0):
        
        #---------------------------------------------------------------
        # load database
        self.load_database()
        
        #---------------------------------------------------------------
        # windows
        self.window = window
        self.window.title(window_title)
        
        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Set window to full screen
        self.window.attributes("-fullscreen", True)
        self.window.bind("<Escape>", self.quit_fullscreen)  # Exit full screen on pressing Escape
        
        # Create a frame for buttons
        self.button_frame = tk.Frame(window)
        self.button_frame.pack(side=tk.TOP, padx=10, pady=10)
        
        # Create the Register button
        self.register_button = tk.Button(self.button_frame, text="Register", width=10, command=self.register)
        self.register_button.pack(side=tk.LEFT, padx=5)
        
        # Create the Cancel button
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", width=10, command=self.cancel_register)
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Create the Reorganize button
        self.reorganize_button = tk.Button(self.button_frame, text="Reorganize", width=10, command=self.reorganize)
        self.reorganize_button.pack(side=tk.LEFT, padx=5)
        
        # Create the Quit button
        self.quit_button = tk.Button(self.button_frame, text="Quit", width=10, command=self.quit)
        self.quit_button.pack(side=tk.LEFT, padx=5)
        
        # Get the screen width and height
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        
        # Create canvas for video stream
        self.canvas = tk.Canvas(window, width=self.screen_width, height=self.screen_height)
        self.canvas.pack()
        
        # count frame passed
        self.frame_count = 0
        self.skip_interval = 5
        
        # get total count in database
        self.idx = len(os.listdir('database'))
        
        self.process_this_frame = True
        self.registered = False
        self.update()
    
    def load_database(self):
        self.known_face_encodings = []
        self.known_face_names = []
        
        image_paths = os.listdir('database')
        image_paths = [os.path.join('database', path) for path in image_paths]
        for path in image_paths:
            # load the image and encodings
            query_image = face_recognition.load_image_file(path)
            row, col, _ = query_image.shape
            face_locations = [(0, col, row, 0)]
            query_face_encoding = face_recognition.face_encodings(query_image, face_locations)[0]
            
            # get name
            name = os.path.basename(path).split('_')[1].split('.')[0]  
        
            # register to arrays
            self.known_face_encodings.append(query_face_encoding)
            self.known_face_names.append(name)        

    def update(self):
        is_in_ROI = False
        ret, frame = self.vid.read()        
        
        if ret:
            # make a copy of original frame
            ori_frame = frame.copy()
            
            # Only process every other frame of video to save time
            if self.process_this_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]

                    face_names.append(name)
                    
                # Display the results
                if not self.registered:
                    for (top, right, bottom, left), name in zip(face_locations, face_names):
                        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                        top *= 4
                        right *= 4
                        bottom *= 4
                        left *= 4

                        # Draw a box around the face
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                        # Draw a label with a name below the face
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                else:                          
                    # Draw a red box in the center of the frame
                    height, width = small_frame.shape[:2]
                    center_x, center_y = width // 2, height // 2
                    
                    # Calculate the box height (50% of the frame height)
                    box_height = int(0.5 * height) 
    
                    # Calculate the box width (75% of the box height)
                    box_width = int(0.75 * box_height)
                    
                    # box corner
                    x1 = center_x - box_width // 2
                    y1 = center_y - box_height // 2
                    x2 = center_x + box_width // 2
                    y2 = center_y + box_height // 2
                    
                    # check if face locations inside box                    
                    if len(face_locations) != 0:
                        for face_location in face_locations:
                            # unpack
                            top, right, bottom, left = face_location
                            # reorganize
                            f_x1, f_y1, f_x2, f_y2 = left, top, right, bottom
                            # convert to the four corners
                            face_corners = [(f_x1, f_y1), (f_x1, f_y2), (f_x2, f_y1), (f_x2, f_y2)]
                            # check if any of the corner inside the ROI box
                            is_in_ROI = False
                            for (x, y) in face_corners:
                                #print(self.frame_count, 1, x1, y1, x2, y2)
                                #print(self.frame_count, 2, x, y)
                                if x1 <= x <= x2 and y1 <= y <= y2:
                                    is_in_ROI = True
                                    break
                            if is_in_ROI:
                                break                                  

                    # prompt text
                    text = "Stay inside box to register face"
                    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    
                    # draw ROI box
                    cv2.rectangle(frame, (x1*4,y1*4), (x2*4,y2*4), (0, 0, 255), 2)   
                    
                    # draw the detected face overlapped with ROI
                    if is_in_ROI:
                        cv2.rectangle(frame, (f_x1*4,f_y1*4), (f_x2*4,f_y2*4), (0, 0, 255), 2) 
                    
                    
                    
                    
                    
                # resize to fit full screen
                frame = cv2.resize(frame, (self.screen_width, self.screen_height))
                
                # Convert frame to RGB format and display it on the canvas
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                
                # if is in ROI
                if is_in_ROI:
                    # stop the ROI box
                    self.unregister()
                    
                    # crop and resize the face from earlier
                    cropped_image = ori_frame[f_y1*4:f_y2*4, f_x1*4:f_x2*4]
                    
                    # save image
                    cv2.imwrite("query.png", cropped_image)                                        
                    
                    # promtp user for name
                    name = simpledialog.askstring("Enter name", "Enter name:")
                    if name:
                        print("Entered text:", name)
                        
                        new_file_path = os.path.join('database', f"{self.idx:04d}_{name}" + '.png')
                        cv2.imwrite(new_file_path, cropped_image)
                        self.idx += 1
                        
                        # load the image and encodings
                        query_image = face_recognition.load_image_file(new_file_path)
                        row, col, _ = query_image.shape
                        face_locations = [(0, col, row, 0)]
                        query_face_encoding = face_recognition.face_encodings(query_image, face_locations)[0]                        
                        
                        # get name
                        new_file_path = os.path.basename(new_file_path).split('_')[1].split('.')[0]  
                    
                        # register to arrays
                        self.known_face_encodings.append(query_face_encoding)
                        self.known_face_names.append(name)                        

            
            
            # update self.frame_count and see if want to skip
            self.frame_count += 1
            if self.frame_count % self.skip_interval == 0:
                self.process_this_frame = True
            else:
                self.process_this_frame = False   
            
        self.window.after(30, self.update)
                    
    def register(self):
        self.registered = True
    
    def unregister(self):
        self.registered = False

    def cancel_register(self):
        self.registered = False
    
    def reorganize(self):
        # Create a new window for image selection
        self.reorganize_window = tk.Toplevel(self.window)
        self.reorganize_window.title("Reorganize Database")

        # Get all image paths in the database
        image_paths = sorted(os.listdir('database'))
        image_paths = [os.path.join('database', path) for path in image_paths]

        # Create a frame for the images
        self.image_frame = tk.Frame(self.reorganize_window)
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas and a scrollbar for the images
        self.image_canvas = tk.Canvas(self.image_frame)
        self.scrollbar = tk.Scrollbar(self.image_frame, orient=tk.VERTICAL, command=self.image_canvas.yview)
        self.scrollable_frame = tk.Frame(self.image_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.image_canvas.configure(
                scrollregion=self.image_canvas.bbox("all")
            )
        )

        self.image_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.image_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.image_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Display images with checkboxes for deletion
        self.image_vars = []
        self.image_labels = []
        for path in image_paths:
            img = Image.open(path)
            img.thumbnail((100, 100))
            photo = ImageTk.PhotoImage(img)
            
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.scrollable_frame, image=photo, variable=var)
            chk.image = photo  # keep a reference to avoid garbage collection
            chk.pack(side=tk.TOP, padx=5, pady=5)

            self.image_vars.append(var)
            self.image_labels.append(path)

        # Create a button to delete selected images
        self.delete_button = tk.Button(self.reorganize_window, text="Delete Selected", command=self.delete_selected)
        self.delete_button.pack(side=tk.BOTTOM, pady=10)

    def delete_selected(self):
        for var, path in zip(self.image_vars, self.image_labels):
            if var.get():
                os.remove(path)
                print(f"Deleted: {path}")
        
        # Reload database after deletion
        self.load_database()
        self.reorganize_window.destroy()
    
    def quit(self):
        self.vid.release()
        self.window.destroy()

    def quit_fullscreen(self, event=None):
        self.window.attributes("-fullscreen", False)
        self.window.destroy()

# Create a window and pass it to the VideoStreamApp class
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = VideoStreamApp(root, "OpenCV Video Stream with Register, Cancel, Reorganize, and Quit Buttons")
        root.mainloop()
    except Exception as e:
        print('Error occurred, quit!', e)

