from tkinter import *
import json
import datetime
import calendar
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
from collections import Counter
import threading
import numpy as np
import cv2
import os
from keras.models import load_model
from tkinter import messagebox

canvas = None 
survey_done = False
start_btn_clicked = False

# Set font for the whole application
font_style = ("Segoe UI Semibold", 11)

# Create the main window
main = Tk()
main.title("satisFACEtion")

# Set the path to your icon file (should be a .ico file on Windows)
icon_path = "./images/favicon.ico"

# Set the window icon
main.iconbitmap(icon_path)

# Set window size
main.geometry("1360x768")

# Configure main window background color
main.configure(background="white", padx=0, pady=0)

content_frame = None  # Declare content_frame as a global variable
survey_widgets = []  # List to store survey question widgets

# Create a frame to hold the content
content_frame = Frame(main, bg="white")
content_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

# Configure grid weights to allow expansion
main.grid_columnconfigure(0, weight=0)
main.grid_columnconfigure(1, weight=1)
main.grid_rowconfigure(0, weight=1)

def welcome_page():
    global content_frame, survey_widgets, canvas  # Declare content_frame and survey_widgets as global variables
    remove_survey_widgets()  # Remove any existing survey widgets
    
    if canvas is not None:
        canvas.get_tk_widget().destroy()
    
    # Load the image
    image = Image.open("./images/welcome_bg.png")  # Replace "path_to_your_image_file.jpg" with the actual image file path
    
    # Create a Label widget to display the image
    image_label = Label(content_frame)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)  # Position the image label with absolute coordinates
    
    # Resize the image to fit the label
    width = content_frame.winfo_width()
    height = content_frame.winfo_height()
    resized_image = image.resize((width, height), Image.LANCZOS)
    
    # Create a PhotoImage object from the resized image
    photo = ImageTk.PhotoImage(resized_image)
    
    # Configure the image label to display the resized image
    image_label.config(image=photo)
    image_label.image = photo  # Store a reference to the image to prevent garbage collection

    # Create a Button widget with absolute positioning
    button = Button(content_frame, command=show_feedback,text="GIVE FEEDBACK", font=("Segoe UI Semibold", 13), bg="white", fg="orange", relief="flat", borderwidth=0, padx=10, pady=5, cursor="hand2")
    button.place(x=50, y=300)  # Adjust the coordinates as needed

    survey_widgets.extend([image_label, button])  # Add the widgets to the survey_widgets list
    
    # Update the image label size when the content frame size changes
    def resize_image(event):
        width = event.width
        height = event.height
        resized_image = image.resize((width, height), Image.LANCZOS)
        new_photo = ImageTk.PhotoImage(resized_image)
        image_label.config(image=new_photo)
        image_label.image = new_photo
    
    content_frame.bind("<Configure>", resize_image)

def get_next_survey_id():
    survey_data = []
    try:
        with open("survey_answer.json", "r") as file:
            survey_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Handle the case when the file is not found or contains invalid JSON data
        # messagebox.showerror("Error", "Failed to load survey data.")
        return 1

    if not survey_data:
        # If the survey_data list is empty, return 1 as the initial ID
        return 1

    # Find the last survey ID in the survey_data list
    last_survey = survey_data[-1]
    last_survey_id = last_survey.get("id", 0)

    # Return the next survey ID by incrementing the last survey ID
    return last_survey_id + 1

def remove_survey_widgets():
    feedback_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
    feedback_btn.pack(padx=(17, 10), pady=20, fill="x")
    for widget in survey_widgets:
        widget.destroy()

def show_feedback():
    global content_frame, survey_widgets, survey_done, canvas, start_btn_clicked  # Declare content_frame and survey_widgets as global variables
    if start_btn_clicked == False:
        messagebox.showerror("Press Start", "Press Start Button First.")
    else:
        remove_survey_widgets()  # Remove any existing survey widgets
        if canvas is not None:
            canvas.get_tk_widget().destroy()

        feedback_btn.configure(bg="white", fg="black", highlightbackground="white", borderwidth=0, anchor="w")
        feedback_btn.pack(padx=(25, 10), pady=20, fill="x")
        
        # Create the survey questions and radio buttons
        survey_question1_label = Label(content_frame, text="Survey Questions", font=("Segoe UI Bold", 15), bg="white")
        survey_question1_label.pack(anchor="w", pady=(20, 10), padx=(70, 0))
        survey_question1_label.configure(pady=5)  # Add letter spacing of 2 pixels
        survey_widgets.append(survey_question1_label)

        # Create the survey questions and radio buttons
        question1_label = Label(content_frame, text="1. Was the service fast and friendly?", font=font_style, bg="white")
        question1_label.pack(anchor="w", pady=(20, 10), padx=(70, 0))
        question1_label.configure(pady=5)  # Add letter spacing of 2 pixels
        survey_widgets.append(question1_label)

        satisfied1 = IntVar()
        satisfied1_radiobutton = Radiobutton(content_frame, text="Satisfied", bg="white", variable=satisfied1, value=1, font=font_style, command=lambda: unsatisfied1.set(0))
        satisfied1_radiobutton.pack(anchor="w", padx=(70, 0))
        survey_widgets.append(satisfied1_radiobutton)

        unsatisfied1 = IntVar()
        unsatisfied1_radiobutton = Radiobutton(content_frame, text="Unsatisfied", bg="white", variable=unsatisfied1, value=1, font=font_style, command=lambda: satisfied1.set(0))
        unsatisfied1_radiobutton.pack(anchor="w", pady=(0, 20), padx=(70, 0))
        survey_widgets.append(unsatisfied1_radiobutton)

        question2_label = Label(content_frame, text="2. Was your food fresh and tasty?", font=font_style, bg="white")
        question2_label.pack(anchor="w", pady=(20, 10), padx=(70, 0))
        question2_label.configure(pady=5)  # Add letter spacing of 2 pixels
        survey_widgets.append(question2_label)

        satisfied2 = IntVar()
        satisfied2_radiobutton = Radiobutton(content_frame, text="Satisfied", bg="white", variable=satisfied2, value=1, font=font_style, command=lambda: unsatisfied2.set(0))
        satisfied2_radiobutton.pack(anchor="w", padx=(70, 0))
        survey_widgets.append(satisfied2_radiobutton)

        unsatisfied2 = IntVar()
        unsatisfied2_radiobutton = Radiobutton(content_frame, text="Unsatisfied", bg="white", variable=unsatisfied2, value=1, font=font_style, command=lambda: satisfied2.set(0))
        unsatisfied2_radiobutton.pack(anchor="w", pady=(0, 20), padx=(70, 0))
        survey_widgets.append(unsatisfied2_radiobutton)

        question3_label = Label(content_frame, text="3. Are you pleased with the quality of the meal?", font=font_style, bg="white")
        question3_label.pack(anchor="w", pady=(20, 10), padx=(70, 0))
        question3_label.configure(pady=5)  # Add letter spacing of 2 pixels
        survey_widgets.append(question3_label)

        satisfied3 = IntVar()
        satisfied3_radiobutton = Radiobutton(content_frame, text="Satisfied", bg="white", variable=satisfied3, value=1, font=font_style, command=lambda: unsatisfied3.set(0))
        satisfied3_radiobutton.pack(anchor="w", padx=(70, 0))
        survey_widgets.append(satisfied3_radiobutton)

        unsatisfied3 = IntVar()
        unsatisfied3_radiobutton = Radiobutton(content_frame, text="Unsatisfied", bg="white", variable=unsatisfied3, value=1, font=font_style, command=lambda: satisfied3.set(0))
        unsatisfied3_radiobutton.pack(anchor="w", pady=(0, 20), padx=(70, 0))
        survey_widgets.append(unsatisfied3_radiobutton)

        question4_label = Label(content_frame, text="4. Rate your overall satisfaction?", font=font_style, bg="white")
        question4_label.pack(anchor="w", pady=(20, 10), padx=(70, 0))
        question4_label.configure(pady=5)  # Add letter spacing of 2 pixels
        survey_widgets.append(question4_label)

        satisfied4 = IntVar()
        satisfied4_radiobutton = Radiobutton(content_frame, text="Satisfied", bg="white", variable=satisfied4, value=1, font=font_style, command=lambda: unsatisfied4.set(0))
        satisfied4_radiobutton.pack(anchor="w", padx=(70, 0))
        survey_widgets.append(satisfied4_radiobutton)

        unsatisfied4 = IntVar()
        unsatisfied4_radiobutton = Radiobutton(content_frame, text="Unsatisfied", bg="white", variable=unsatisfied4, value=1, font=font_style, command=lambda: satisfied4.set(0))
        unsatisfied4_radiobutton.pack(anchor="w", pady=(0, 20), padx=(70, 0))
        survey_widgets.append(unsatisfied4_radiobutton)

        # Function to validate the survey choices
        def validate_survey():
            if satisfied1.get() == 0 and unsatisfied1.get() == 0:
                return False
            if satisfied2.get() == 0 and unsatisfied2.get() == 0:
                return False
            if satisfied3.get() == 0 and unsatisfied3.get() == 0:
                return False
            if satisfied4.get() == 0 and unsatisfied4.get() == 0:
                return False
            return True

        def submit_survey():
            global survey_done
            if validate_survey():
                # Prepare the survey data
                feedback_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
                feedback_btn.pack(padx=(17, 10), pady=20, fill="x")
                survey_done = True
                survey_data = {
                    "date": str(datetime.date.today()),
                    "id": get_next_survey_id(),
                    "answers": {
                        "Question 1": "Satisfied" if satisfied1.get() == 1 else "Unsatisfied",
                        "Question 2": "Satisfied" if satisfied2.get() == 1 else "Unsatisfied",
                        "Question 3": "Satisfied" if satisfied3.get() == 1 else "Unsatisfied",
                        "Question 4": "Satisfied" if satisfied4.get() == 1 else "Unsatisfied"
                    }
                }

                # Load existing survey data from the JSON file
                existing_data = []
                try:
                    with open("survey_answer.json", "r") as file:
                        existing_data = json.load(file)
                except FileNotFoundError:
                    pass

                # Append the new survey data to the existing data
                existing_data.append(survey_data)

                # Save the updated survey data to the JSON file
                with open("survey_answer.json", "w") as file:
                    json.dump(existing_data, file, indent=4)

                # Create a new window for displaying the completion message and image
                complete_window = Toplevel(content_frame)
                complete_window.title("")
                complete_window.overrideredirect(True)  # Remove the title bar

                # Load the completion image
                completion_image = Image.open("./images/prompt_bg.png")
                window_width = 811  # Set the desired window width
                window_height = 458  # Set the desired window height
                resized_image = completion_image.resize((window_width, window_height), Image.LANCZOS)
                completion_photo = ImageTk.PhotoImage(resized_image)

                # Create a Label widget to display the completion image
                image_label = Label(complete_window, image=completion_photo)
                image_label.pack(fill='both', expand=True)

                # Store the image as an attribute of the label widget
                image_label.image = completion_photo

                # Define the close_window function
                def close_window():
                    feedback_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
                    feedback_btn.pack(padx=(17, 10), pady=20, fill="x")
                    complete_window.destroy()
                    welcome_page()

                # Create a Button widget for closing the window
                close_button = Button(complete_window, text="Okay", command=close_window, font=("Segoe UI Semibold", 12),
                                    bg="white", fg="orange", relief="flat", borderwidth=0, pady=5, padx=15, cursor="hand2")
                close_button.place(relx=0.5, rely=0.9, anchor="center")

                # Center the window on the screen
                complete_window.update_idletasks()
                screen_width = complete_window.winfo_screenwidth()
                screen_height = complete_window.winfo_screenheight()
                x = (screen_width - window_width) // 2
                y = (screen_height - window_height) // 2
                complete_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

            else:
                messagebox.showwarning("Incomplete Survey", "Please answer all the survey questions!")
                
        # Create a button to submit the survey
        submit_button = Button(content_frame, text="Submit", command=submit_survey, relief="flat", cursor="hand2", bg="green", fg="white", borderwidth=0, padx=20, pady=5, font=font_style)
        submit_button.pack(pady=(20, 0))
        survey_widgets.append(submit_button)

def show_analytics():
    global content_frame, survey_widgets, canvas
    remove_survey_widgets()
    if canvas is not None:
        canvas.get_tk_widget().destroy()
    try:
        with open("survey_answer.json", "r") as file:
            survey_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "Failed to load survey data.")
        return

    if not survey_data:
        messagebox.showinfo("No Data", "No survey data available.")
        return

    total_surveys = len(survey_data)

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
    plt.subplots_adjust(wspace=0.4, hspace=0.4)

    for i in range(4):
        question = f"Question {i+1}"            
        x_labels = ["Satisfied", "Unsatisfied"]
        satisfaction_counts = [0, 0]  # Initialize counts for both labels

        for entry in survey_data:
            answer = entry["answers"].get(question)
            if answer == "Satisfied":
                satisfaction_counts[0] += 1  # Increment count for Satisfied
            elif answer == "Unsatisfied":
                satisfaction_counts[1] += 1  # Increment count for Unsatisfied

        row_index = i // 2
        col_index = i % 2
        axes[row_index, col_index].bar(x_labels, satisfaction_counts)
        axes[row_index, col_index].set_ylabel("Number of Person")
        if(i == 3):
            question = f"Overall Satisfaction"
        axes[row_index, col_index].set_title(question)

        # Set y-axis label to total Number of Person
        axes[row_index, col_index].set_ylim([0, total_surveys])
        axes[row_index, col_index].set_yticks(range(0, total_surveys + 1, 1))

    fig.tight_layout(pad=2.0)

    canvas = FigureCanvasTkAgg(fig, master=content_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    plt.close()
    content_frame.mainloop()

def show_data():
    global content_frame, survey_widgets, canvas, current_view  # Declare content_frame, survey_widgets, and current_view as global variables
    remove_survey_widgets()  # Remove any existing survey widgets
    if canvas is not None:
        canvas.get_tk_widget().destroy()

    # Load survey data from the JSON file
    try:
        with open("survey_answer.json", "r") as file:
            survey_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "Failed to load survey data.")
        return

    if not survey_data:
        messagebox.showinfo("No Data", "No survey data available.")
        return

    # Create a global variable to keep track of the current view
    current_view = 'month'

    def update_plot(view, data):
        global current_view, canvas

        if view == 'month':
            plot_data_by_week(data)
            current_view = 'week'

    # Create a dictionary to store the counts for each month, week, and day
    month_counts = defaultdict(lambda: {'Satisfied': 0, 'Unsatisfied': 0})
    # Create a dictionary to store the counts for each month, week, and day
    week_counts = defaultdict(lambda: defaultdict(lambda: {'Satisfied': 0, 'Unsatisfied': 0}))
    day_counts = defaultdict(lambda: {'Satisfied': 0, 'Unsatisfied': 0})

    # Process survey data and count satisfied/unsatisfied customers by month, week, and day
    for entry in survey_data:
        date = entry.get('date')
        month = int(date.split('-')[1])
        week = str(datetime.datetime.strptime(date, '%Y-%m-%d').date().isocalendar()[1])  # Convert week to string key
        day = int(date.split('-')[2])
        answers = entry.get('answers')
        for question, response in answers.items():
            if response == 'Satisfied':
                month_counts[month]['Satisfied'] += 1
                week_counts[month][week]['Satisfied'] += 1
                day_counts[day]['Satisfied'] += 1
            elif response == 'Unsatisfied':
                month_counts[month]['Unsatisfied'] += 1
                week_counts[month][week]['Unsatisfied'] += 1  # Use week as a key within the month
                day_counts[day]['Unsatisfied'] += 1


    # Define the plot functions
    def plot_data_by_month():
        global canvas
        if canvas is not None:
            canvas.get_tk_widget().destroy()

        # Create a list of all months from January to December
        all_months = list(range(1, 13))
        month_names = [calendar.month_abbr[month] for month in all_months]  # Use month abbreviations

        # Extract months and counts for plotting
        month_counts = {}
        for survey in survey_data:
            date_str = survey['date']
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            month = date.month
            if month not in month_counts:
                month_counts[month] = {'Satisfied': 0, 'Unsatisfied': 0}
            answers = survey['answers']
            for answer in answers.values():
                if answer == 'Satisfied':
                    month_counts[month]['Satisfied'] += 1
                elif answer == 'Unsatisfied':
                    month_counts[month]['Unsatisfied'] += 1

        # Find the index of the selected month
        selected_month_index = datetime.datetime.now().month - 1

        # Plot the bar graph by month
        plt.figure(figsize=(8, 6))
        x_pos = np.arange(len(all_months))
        satisfied_counts = [month_counts.get(month, {'Satisfied': 0})['Satisfied'] for month in all_months]
        unsatisfied_counts = [month_counts.get(month, {'Unsatisfied': 0})['Unsatisfied'] for month in all_months]
        plt.bar(x_pos - 0.2, satisfied_counts, 0.4, label='Satisfied', color='#00b7ff')
        plt.bar(x_pos + 0.2, unsatisfied_counts, 0.4, label='Unsatisfied', color='#ff2929')
        plt.xticks(x_pos, month_names)
        plt.xlabel('Month')
        plt.ylabel('Number of People')
        plt.title('Customer Satisfaction by Month')
        plt.legend()

        # Create a Tkinter canvas to display the plot
        canvas = FigureCanvasTkAgg(plt.gcf(), master=content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        plt.close()


    def plot_data_by_week(month):
        global canvas
        if canvas is not None:
            canvas.get_tk_widget().destroy()

        month_data = week_counts[month]

        # Extract weeks and counts for plotting
        weeks = list(month_data.keys())
        week_names = ['Week {}'.format(week) for week in weeks]
        satisfied_counts = [month_data[week]['Satisfied'] for week in weeks]
        unsatisfied_counts = [month_data[week]['Unsatisfied'] for week in weeks]

        # Plot the bar graph by week
        plt.figure(figsize=(8, 6))
        x_pos = np.arange(len(weeks))
        plt.bar(x_pos - 0.2, satisfied_counts, 0.4, label='Satisfied', color='#00b7ff')
        plt.bar(x_pos + 0.2, unsatisfied_counts, 0.4, label='Unsatisfied', color='#ff2929')
        plt.xticks(x_pos, week_names)

        plt.xlabel('Week')
        plt.ylabel('Number of People')
        plt.title('Customer Satisfaction by Week - {}'.format(calendar.month_name[month]))
        plt.legend()

        # Create a Tkinter canvas to display the plot
        canvas = FigureCanvasTkAgg(plt.gcf(), master=content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        plt.close()

    def on_month_click(event):
        if event.xdata is not None:
            selected_month = int(event.xdata) + 1
            if 1 <= selected_month <= 12:
                update_plot(view=current_view, data=selected_month)

    def on_week_click(event):
        if event.xdata is not None:
            selected_week = int(event.xdata) + 1
            if 1 <= selected_week <= 53:
                update_plot(view=current_view, data=selected_week)

    # Plot the data by month by default
    plot_data_by_month()

    # Add a click event handler to the canvas to capture month/week clicks
    if current_view == 'month':
        canvas.mpl_connect('button_press_event', on_month_click)
    elif current_view == 'week':
        canvas.mpl_connect('button_press_event', on_week_click)

def camera_loop():
    global survey_done, start_btn_clicked
    # classifier = load_model(r'C:\Users\User\Desktop\satis-face-tion\ai_trained_model\model.h5')
    classifier = load_model(r'D:\CODES\satis-face-tion\ai_trained_model\model.h5')
    emotion_labels = ['Unsatisfied', 'Unsatisfied', 'Satisfied', 'Satisfied', 'Unsatisfied', 'Satisfied']

    cap = cv2.VideoCapture(0)
    start_btn.config(state=DISABLED, text="STARTED",)
    start_btn_clicked = True
    messagebox.showinfo("Camera Started", "Camera is Now Enabled!")

    json_data = []  # Initialize empty JSON data list
    max_id = 0  # Initialize the maximum ID number

    # Check if JSON file exists
    if os.path.exists('facial_recognition_result.json'):
        # Load existing data from JSON file
        with open('facial_recognition_result.json', 'r') as json_file:
            json_data = json.load(json_file)
            # Find the maximum ID value in existing data
            max_id = max([data['id'] for data in json_data]) if json_data else 0

    label = ''  # Initialize label variable outside the loop

    while True:
        ret, frame = cap.read()
        labels = []

        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except cv2.error as e:
            print("")

        # face_classifier = cv2.CascadeClassifier(r'C:\Users\User\Desktop\satis-face-tion\ai_trained_model\haarcascades\haarcascade_frontalface_default.xml')
        face_classifier = cv2.CascadeClassifier(r'D:\CODES\satis-face-tion\ai_trained_model\haarcascades\haarcascade_frontalface_default.xml')
        faces = face_classifier.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        if len(faces) > 0:
            x, y, w, h = faces[-1]  # Take the last detected face's coordinates

            cv2.rectangle(frame, (x, y), (x + w, y + h), (28, 252, 3), 3)  # Set color to yellow and thickness to 3
            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = np.expand_dims(roi, axis=0)
                prediction = classifier.predict(roi)[0]
                if 0 <= prediction.argmax() < len(emotion_labels):  # Check if the predicted value is within range
                    label = emotion_labels[prediction.argmax()]
                    label_position = (x, y - 10)
                    labels.append(label)

        if survey_done:
            current_date = datetime.date.today().strftime("%B %d, %Y")  # Format current date as "June 15, 2023"
            id_number = max_id + 1  # Increment the maximum ID value

            # Generate the new file name
            image_file_name = f"Survey #{id_number} - {current_date}.jpg"

            # Save the image to a folder with the new file name
            image_path = os.path.join(".", "user_facial_images", image_file_name)

            if labels:
                label = labels[-1]  # Take the label from the last detected face

                # Create a copy of the frame to draw the square indicator
                frame_with_square = frame.copy()

                # Draw the square indicator on the frame
                cv2.rectangle(frame_with_square, (x, y), (x + w, y + h), (0, 255, 255), 3)  # Set color to yellow and thickness to 3

                # Add label to the captured image with background
                text_width, text_height = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                margin = 10  # Set the desired margin size
                label_box_height = text_height + 2 * margin

                # Calculate the coordinates for the label background rectangle
                label_box_x1 = x
                label_box_y1 = y - label_box_height - margin
                label_box_x2 = x + text_width + 2 * margin
                label_box_y2 = y - margin

                # Draw the background rectangle for the label
                cv2.rectangle(frame_with_square, (label_box_x1, label_box_y1), (label_box_x2, label_box_y2), (0, 255, 255), cv2.FILLED)  # Set background color to yellow

                # Calculate the coordinates for the text position
                text_x = label_box_x1 + margin
                text_y = label_box_y2 - margin

                # Draw the text label
                cv2.putText(frame_with_square, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)  # Set text color to black and font family to Arial


                # Save the image with the label and square indicator
                cv2.imwrite(image_path, frame_with_square)

                date = str(datetime.date.today())
                # Create a new data entry with the incremented ID, label, and date
                data = {
                    "id": id_number,
                    "label": label,
                    "date": date
                }

                # Append the new data to the JSON data list
                json_data.append(data)

                # Update the maximum ID value
                max_id = id_number

                # Save the updated JSON data to the file
                with open('facial_recognition_result.json', 'w') as json_file:
                    json.dump(json_data, json_file)

                # Check satisfaction level and save image
                if label == 'Satisfied':
                    print("Satisfied!")
                else:
                    print("Unsatisfied!")

            survey_done = False

def show_start():
    global start_btn
    threading.Thread(target=camera_loop).start()
    # Disable the start button
    start_btn.config(state=DISABLED, text="Please Wait...",)
    
def show_satisfaction_analytics():
    global content_frame, survey_widgets, canvas
    
    # Declare content_frame and survey_widgets as global variables
    remove_survey_widgets()  # Remove any existing survey widgets
    if canvas is not None:
        canvas.get_tk_widget().destroy()

    try:
        with open("facial_recognition_result.json", "r") as file:
            survey_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "Failed to load survey data.")
        return

    if not survey_data:
        messagebox.showinfo("No Data", "No survey data available.")
        return

    labels = [entry["label"] for entry in survey_data]

    satisfaction_counts = Counter(labels)
    x_labels = list(satisfaction_counts.keys())
    counts = list(satisfaction_counts.values())

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.bar(x_labels, counts)
    ax.set_ylabel("Number of Persons")
    ax.set_xlabel("Satisfaction")
    ax.set_title("Users Facial Expression")

    canvas = FigureCanvasTkAgg(fig, master=content_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    plt.close()

    content_frame.mainloop()

def show_satisfaction_data():
    global content_frame, survey_widgets, canvas, current_view

    remove_survey_widgets()

    if canvas is not None:
        canvas.get_tk_widget().destroy()

    try:
        with open("facial_recognition_result.json", "r") as file:
            survey_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "Failed to load survey data.")
        return

    if not survey_data:
        messagebox.showinfo("No Data", "No survey data available.")
        return

    current_view = 'month'

    def update_plot(view, data):
        global current_view, canvas

        if view == 'month':
            plot_data_by_week(data)
            current_view = 'week'

    month_counts = defaultdict(lambda: {'Satisfied': 0, 'Unsatisfied': 0})
    week_counts = defaultdict(lambda: defaultdict(lambda: {'Satisfied': 0, 'Unsatisfied': 0}))
    day_counts = defaultdict(lambda: {'Satisfied': 0, 'Unsatisfied': 0})

    for entry in survey_data:
        response = entry.get('label')
        date = entry.get('date')
        month = int(date.split('-')[1])
        week = str(datetime.datetime.strptime(date, '%Y-%m-%d').date().isocalendar()[1])
        day = int(date.split('-')[2])
        if response == 'Satisfied':
            month_counts[month]['Satisfied'] += 1
            week_counts[month][week]['Satisfied'] += 1
            day_counts[day]['Satisfied'] += 1
        elif response == 'Unsatisfied':
            month_counts[month]['Unsatisfied'] += 1
            week_counts[month][week]['Unsatisfied'] += 1
            day_counts[day]['Unsatisfied'] += 1

    def plot_data_by_month():
        global canvas
        if canvas is not None:
            canvas.get_tk_widget().destroy()

        all_months = list(range(1, 13))
        month_names = [calendar.month_abbr[month] for month in all_months]

        selected_month_index = datetime.datetime.now().month - 1

        plt.figure(figsize=(8, 6))
        x_pos = list(range(len(all_months)))  # Convert x_pos to a list
        satisfied_counts = [month_counts.get(month, {'Satisfied': 0})['Satisfied'] for month in all_months]
        unsatisfied_counts = [month_counts.get(month, {'Unsatisfied': 0})['Unsatisfied'] for month in all_months]
        plt.bar([pos - 0.2 for pos in x_pos], satisfied_counts, 0.4, label='Satisfied', color='#00b7ff')  # Updated line
        plt.bar([pos + 0.2 for pos in x_pos], unsatisfied_counts, 0.4, label='Unsatisfied', color='#ff2929')  # Updated line
        plt.xticks(x_pos, month_names)
        plt.xlabel('Month')
        plt.ylabel('Number of People')
        plt.title('Customer Facial Satisfaction by Month')
        plt.legend()

        canvas = FigureCanvasTkAgg(plt.gcf(), master=content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        plt.close()


    def plot_data_by_week(month):
        global canvas
        if canvas is not None:
            canvas.get_tk_widget().destroy()

        month_data = week_counts[month]

        weeks = list(month_data.keys())
        week_names = ['Week {}'.format(week) for week in weeks]
        satisfied_counts = [month_data[week]['Satisfied'] for week in weeks]
        unsatisfied_counts = [month_data[week]['Unsatisfied'] for week in weeks]

        plt.figure(figsize=(8, 6))
        x_pos = list(range(len(weeks)))  # Convert x_pos to a list
        plt.bar([pos - 0.2 for pos in x_pos], satisfied_counts, 0.4, label='Satisfied', color='#00b7ff')  # Updated line
        plt.bar([pos + 0.2 for pos in x_pos], unsatisfied_counts, 0.4, label='Unsatisfied', color='#ff2929')  # Updated line
        plt.xticks(x_pos, week_names)

        plt.xlabel('Week')
        plt.ylabel('Number of People')
        plt.title('Customer Facial Satisfaction by Week - {}'.format(calendar.month_name[month]))
        plt.legend()

        canvas = FigureCanvasTkAgg(plt.gcf(), master=content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        plt.close()


    def on_month_click(event):
        if event.xdata is not None:
            selected_month = int(event.xdata) + 1
            if 1 <= selected_month <= 12:
                update_plot(view=current_view, data=selected_month)

    def on_week_click(event):
        if event.xdata is not None:
            selected_week = int(event.xdata) + 1
            if 1 <= selected_week <= 53:
                update_plot(view=current_view, data=selected_week)

    plot_data_by_month()

    if current_view == 'month':
        canvas.mpl_connect('button_press_event', on_month_click)
    elif current_view == 'week':
        canvas.mpl_connect('button_press_event', on_week_click)
        
def facial_images():
    global content_frame, survey_widgets, canvas, current_view

    remove_survey_widgets()

    if canvas is not None:
        canvas.get_tk_widget().destroy()

    scrollable_frame = Frame(content_frame)
    scrollable_frame.pack(fill=BOTH, expand=True)

    canvas2 = Canvas(scrollable_frame)
    canvas2.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(scrollable_frame, orient=VERTICAL, command=canvas2.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas2.configure(yscrollcommand=scrollbar.set)
    canvas2.bind('<Configure>', lambda e: canvas2.configure(scrollregion=canvas2.bbox('all')))

    inner_frame = Frame(canvas2)
    canvas2.create_window((0, 0), window=inner_frame, anchor='nw')

    folder_path = './user_facial_images'
    image_files = os.listdir(folder_path)

    image_files.sort(key=lambda x: int(re.search(r'Survey #(\d+)', x).group(1)))

    num_images = len(image_files)
    num_columns = 5
    num_rows = (num_images + num_columns - 1) // num_columns

    def delete_image(image_path):
        result = messagebox.askquestion("Delete Image", "Are you sure you want to delete this image?")
        if result == 'yes':
            os.remove(image_path)
            # Update the image display after deletion
            facial_images()

    def hover_in(event, image_label, image_path):
        event.widget.config(cursor="hand2")
        event.widget.config(borderwidth=2, relief="solid", bd=1, fg="#880808", highlightbackground="#880808")

    def hover_out(event, image_label, image_path):
        event.widget.config(cursor="")
        event.widget.config(borderwidth=0)

    for i, file_name in enumerate(image_files):
        image_path = os.path.join(folder_path, file_name)
        image = Image.open(image_path)
        image = image.resize((200, 200))  # Adjust the size as needed

        photo = ImageTk.PhotoImage(image)
        label = Label(inner_frame, image=photo)
        label.image = photo

        row = i // num_columns
        col = i % num_columns

        label.grid(row=row, column=col, padx=10, pady=(30, 2))

        file_label = Label(inner_frame, text=file_name, wraplength=180, justify=CENTER)
        file_label.grid(row=row + 1, column=col, pady=(0, 10), sticky='n')

        # Bind the delete_image function to the label click event
        label.bind("<Button-1>", lambda e, path=image_path: delete_image(path))
        label.bind("<Enter>", lambda e, label=label, path=image_path: hover_in(e, label, path))
        label.bind("<Leave>", lambda e, label=label, path=image_path: hover_out(e, label, path))

    canvas2.update_idletasks()
    canvas2.config(scrollregion=canvas2.bbox('all'))

    survey_widgets.append(scrollable_frame)


# Create a frame for the stacked buttons
button_frame = Frame(main, bg="#302d2d")
button_frame.grid(row=0, column=0, padx=0, pady=0, sticky="ns")

# Configure the button_frame row to expand vertically
button_frame.grid_rowconfigure(0, weight=1)

# Create left-side navigation buttons
start_btn = Button(button_frame, text="Start", command=show_start, relief="flat", cursor="hand2", font=font_style)
start_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
start_btn.pack(padx=(17, 10),pady=(60, 20), fill="x")

feedback_btn = Button(button_frame, text="Feedback", command=show_feedback, relief="flat", cursor="hand2", font=font_style)
feedback_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
feedback_btn.pack(padx=(17, 10), pady=20 , fill="x")

analytics_btn = Button(button_frame, text="Analytics", command=show_analytics, relief="flat", cursor="hand2", font=font_style)
analytics_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
analytics_btn.pack(padx=(17, 10), pady=20, fill="x")

data_btn = Button(button_frame, text="Data", command=show_data, relief="flat", cursor="hand2", font=font_style)
data_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
data_btn.pack(padx=(17, 10), pady=20, fill="x")

satisfaction_analytics_btn = Button(button_frame, text="Satisfaction Analytics", command=show_satisfaction_analytics, relief="flat", cursor="hand2", font=font_style)
satisfaction_analytics_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
satisfaction_analytics_btn.pack(padx=(17, 25), pady=20, fill="x")

satisfaction_data_btn = Button(button_frame, text="Satisfaction Data", command=show_satisfaction_data, relief="flat", cursor="hand2", font=font_style)
satisfaction_data_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
satisfaction_data_btn.pack(padx=(17, 25), pady=20, fill="x")

facial_images_btn = Button(button_frame, text="Facial Recognition Images", command=facial_images, relief="flat", cursor="hand2", font=font_style)
facial_images_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
facial_images_btn.pack(padx=(17, 25), pady=(20, 40), fill="x")

# Show the initial content (Welcome Page)
welcome_page()

# Run the application
main.mainloop()
