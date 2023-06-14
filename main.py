from tkinter import *

# Set font for the whole application
font_style = ("Segoe UI", 11)

# Create the main window
main = Tk()
main.title("satisFACEtion")

# Set window size
main.geometry("1360x768")

# Configure main window background color
main.configure(background="white")

content_frame = None  # Declare content_frame as a global variable
survey_widgets = []  # List to store survey question widgets

def remove_survey_widgets():
    for widget in survey_widgets:
        widget.destroy()

def show_feedback():
    global content_frame, survey_widgets  # Declare content_frame and survey_widgets as global variables
    remove_survey_widgets()  # Remove any existing survey widgets
    
    # Create a new label inside the content frame
    content_label.config(text="Survey Questions Here")

    # Create the survey questions and radio buttons
    question1_label = Label(content_frame, text="1. Was the service fast and friendly?", font=font_style)
    question1_label.pack(anchor="w")
    survey_widgets.append(question1_label)

    satisfied1 = IntVar()
    satisfied1_radiobutton = Radiobutton(content_frame, text="Satisfied", variable=satisfied1, value=1, font=font_style, command=lambda: unsatisfied1.set(0))
    satisfied1_radiobutton.pack(anchor="w")
    survey_widgets.append(satisfied1_radiobutton)

    unsatisfied1 = IntVar()
    unsatisfied1_radiobutton = Radiobutton(content_frame, text="Unsatisfied", variable=unsatisfied1, value=1, font=font_style, command=lambda: satisfied1.set(0))
    unsatisfied1_radiobutton.pack(anchor="w")
    survey_widgets.append(unsatisfied1_radiobutton)

    question2_label = Label(content_frame, text="2. Was your food fresh and tasty?", font=font_style)
    question2_label.pack(anchor="w")
    survey_widgets.append(question2_label)

    satisfied2 = IntVar()
    satisfied2_radiobutton = Radiobutton(content_frame, text="Satisfied", variable=satisfied2, value=1, font=font_style, command=lambda: unsatisfied2.set(0))
    satisfied2_radiobutton.pack(anchor="w")
    survey_widgets.append(satisfied2_radiobutton)

    unsatisfied2 = IntVar()
    unsatisfied2_radiobutton = Radiobutton(content_frame, text="Unsatisfied", variable=unsatisfied2, value=1, font=font_style, command=lambda: satisfied2.set(0))
    unsatisfied2_radiobutton.pack(anchor="w")
    survey_widgets.append(unsatisfied2_radiobutton)

    question3_label = Label(content_frame, text="3. Are you pleased with the quality of the meal?", font=font_style)
    question3_label.pack(anchor="w")
    survey_widgets.append(question3_label)

    satisfied3 = IntVar()
    satisfied3_radiobutton = Radiobutton(content_frame, text="Satisfied", variable=satisfied3, value=1, font=font_style, command=lambda: unsatisfied3.set(0))
    satisfied3_radiobutton.pack(anchor="w")
    survey_widgets.append(satisfied3_radiobutton)

    unsatisfied3 = IntVar()
    unsatisfied3_radiobutton = Radiobutton(content_frame, text="Unsatisfied", variable=unsatisfied3, value=1, font=font_style, command=lambda: satisfied3.set(0))
    unsatisfied3_radiobutton.pack(anchor="w")
    survey_widgets.append(unsatisfied3_radiobutton)

    question4_label = Label(content_frame, text="4. Rate your overall satisfaction?", font=font_style)
    question4_label.pack(anchor="w")
    survey_widgets.append(question4_label)

    satisfied4 = IntVar()
    satisfied4_radiobutton = Radiobutton(content_frame, text="Satisfied", variable=satisfied4, value=1, font=font_style, command=lambda: unsatisfied4.set(0))
    satisfied4_radiobutton.pack(anchor="w")
    survey_widgets.append(satisfied4_radiobutton)

    unsatisfied4 = IntVar()
    unsatisfied4_radiobutton = Radiobutton(content_frame, text="Unsatisfied", variable=unsatisfied4, value=1, font=font_style, command=lambda: satisfied4.set(0))
    unsatisfied4_radiobutton.pack(anchor="w")
    survey_widgets.append(unsatisfied4_radiobutton)

    # Function to submit the survey and print the answers
    def submit_survey():
        print("Survey Answers:")
        print("Question 1:", "Satisfied" if satisfied1.get() == 1 else "Unsatisfied")
        print("Question 2:", "Satisfied" if satisfied2.get() == 1 else "Unsatisfied")
        print("Question 3:", "Satisfied" if satisfied3.get() == 1 else "Unsatisfied")
        print("Question 4:", "Satisfied" if satisfied4.get() == 1 else "Unsatisfied")

    # Create a button to submit the survey
    submit_button = Button(content_frame, text="Submit", command=submit_survey, font=font_style)
    submit_button.pack(pady=(20, 0))
    survey_widgets.append(submit_button)

def show_analytics():
    global content_frame, survey_widgets  # Declare content_frame and survey_widgets as global variables
    remove_survey_widgets()  # Remove any existing survey widgets
    content_label.config(text="Analytics Page")

def show_data():
    global content_frame, survey_widgets  # Declare content_frame and survey_widgets as global variables
    remove_survey_widgets()  # Remove any existing survey widgets
    content_label.config(text="Data Page")

def show_start():
    global content_frame, survey_widgets  # Declare content_frame and survey_widgets as global variables
    remove_survey_widgets()  # Remove any existing survey widgets
    content_label.config(text="Start Page")

def show_satisfaction_analytics():
    global content_frame, survey_widgets  # Declare content_frame and survey_widgets as global variables
    remove_survey_widgets()  # Remove any existing survey widgets
    content_label.config(text="Satisfaction Analytics Page")

def show_satisfaction_data():
    global content_frame, survey_widgets  # Declare content_frame and survey_widgets as global variables
    remove_survey_widgets()  # Remove any existing survey widgets
    content_label.config(text="Satisfaction Data Page")

# Create a frame for the stacked buttons
button_frame = Frame(main, bg="#302d2d")
button_frame.grid(row=0, column=0, padx=0, pady=0, sticky="ns")

# Configure the grid to expand the sidebar to full length
main.grid_columnconfigure(0, weight=0)

# Create left-side navigation buttons
feedback_btn = Button(button_frame, text="Feedback", command=show_feedback, relief="flat", cursor="hand2", font=font_style)
feedback_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0)
feedback_btn.grid(row=0, padx=10, pady=(20, 20), sticky="ew")

analytics_btn = Button(button_frame, text="Analytics", command=show_analytics, relief="flat", cursor="hand2", font=font_style)
analytics_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0)
analytics_btn.grid(row=1, padx=10, pady=20, sticky="ew")

data_btn = Button(button_frame, text="Data", command=show_data, relief="flat", cursor="hand2", font=font_style)
data_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0)
data_btn.grid(row=2, padx=10, pady=20, sticky="ew")

# Create right-side navigation buttons
start_btn = Button(button_frame, text="Start", command=show_start, relief="flat", cursor="hand2", font=font_style)
start_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0)
start_btn.grid(row=3, padx=10, pady=20, sticky="ew")

satisfaction_analytics_btn = Button(button_frame, text="Satisfaction Analytics", command=show_satisfaction_analytics, relief="flat", cursor="hand2", font=font_style)
satisfaction_analytics_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0)
satisfaction_analytics_btn.grid(row=4, padx=10, pady=20, sticky="ew")

satisfaction_data_btn = Button(button_frame, text="Satisfaction Data", command=show_satisfaction_data, relief="flat", cursor="hand2", font=font_style)
satisfaction_data_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0)
satisfaction_data_btn.grid(row=5, padx=10, pady=(20, 40), sticky="ew")

# Create a frame to hold the content
content_frame = Frame(main, bg="white")
content_frame.grid(row=0, column=1, padx=(50, 0), pady=(20, 0), sticky="nsew")

# Configure the grid to expand the content frame
main.grid_columnconfigure(1, weight=1)

# Create a label inside the content frame
content_label = Label(content_frame, text="Start Page", font=font_style)
content_label.pack()

# Show the initial content (Start Page)
show_start()

# Run the application
main.mainloop()
