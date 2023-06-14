from tkinter import *

# Set font for the whole application
font_style = ("Segoe UI Semibold", 11)

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
    content_label.config(text="Survey Questions")

    # Create the survey questions and radio buttons
    question1_label = Label(content_frame, text="1. Was the service fast and friendly?", font=font_style, bg="white")
    question1_label.pack(anchor="w", pady=(20, 10))
    question1_label.configure(pady=5)  # Add letter spacing of 2 pixels
    survey_widgets.append(question1_label)
    
    satisfied1 = IntVar()
    satisfied1_radiobutton = Radiobutton(content_frame, text="Satisfied", bg="white", variable=satisfied1, value=1, font=font_style, command=lambda: unsatisfied1.set(0))
    satisfied1_radiobutton.pack(anchor="w")
    survey_widgets.append(satisfied1_radiobutton)

    unsatisfied1 = IntVar()
    unsatisfied1_radiobutton = Radiobutton(content_frame, text="Unsatisfied", bg="white", variable=unsatisfied1, value=1, font=font_style, command=lambda: satisfied1.set(0))
    unsatisfied1_radiobutton.pack(anchor="w", pady=(0, 20))
    survey_widgets.append(unsatisfied1_radiobutton)

    question2_label = Label(content_frame, text="2. Was your food fresh and tasty?", font=font_style, bg="white")
    question2_label.pack(anchor="w", pady=(20, 10))
    question2_label.configure(pady=5)  # Add letter spacing of 2 pixels
    survey_widgets.append(question2_label)
    
    satisfied2 = IntVar()
    satisfied2_radiobutton = Radiobutton(content_frame, text="Satisfied", bg="white", variable=satisfied2, value=1, font=font_style, command=lambda: unsatisfied2.set(0))
    satisfied2_radiobutton.pack(anchor="w")
    survey_widgets.append(satisfied2_radiobutton)

    unsatisfied2 = IntVar()
    unsatisfied2_radiobutton = Radiobutton(content_frame, text="Unsatisfied", bg="white", variable=unsatisfied2, value=1, font=font_style, command=lambda: satisfied2.set(0))
    unsatisfied2_radiobutton.pack(anchor="w", pady=(0, 20))
    survey_widgets.append(unsatisfied2_radiobutton)

    question3_label = Label(content_frame, text="3. Are you pleased with the quality of the meal?", font=font_style, bg="white")
    question3_label.pack(anchor="w", pady=(20, 10))
    question3_label.configure(pady=5)  # Add letter spacing of 2 pixels
    survey_widgets.append(question3_label)

    satisfied3 = IntVar()
    satisfied3_radiobutton = Radiobutton(content_frame, text="Satisfied", bg="white", variable=satisfied3, value=1, font=font_style, command=lambda: unsatisfied3.set(0))
    satisfied3_radiobutton.pack(anchor="w")
    survey_widgets.append(satisfied3_radiobutton)

    unsatisfied3 = IntVar()
    unsatisfied3_radiobutton = Radiobutton(content_frame, text="Unsatisfied", bg="white", variable=unsatisfied3, value=1, font=font_style, command=lambda: satisfied3.set(0))
    unsatisfied3_radiobutton.pack(anchor="w", pady=(0, 20))
    survey_widgets.append(unsatisfied3_radiobutton)

    question4_label = Label(content_frame, text="4. Rate your overall satisfaction?", font=font_style, bg="white")
    question4_label.pack(anchor="w", pady=(20, 10))
    question4_label.configure(pady=5)  # Add letter spacing of 2 pixels
    survey_widgets.append(question4_label)

    satisfied4 = IntVar()
    satisfied4_radiobutton = Radiobutton(content_frame, text="Satisfied", bg="white", variable=satisfied4, value=1, font=font_style, command=lambda: unsatisfied4.set(0))
    satisfied4_radiobutton.pack(anchor="w")
    survey_widgets.append(satisfied4_radiobutton)

    unsatisfied4 = IntVar()
    unsatisfied4_radiobutton = Radiobutton(content_frame, text="Unsatisfied", bg="white", variable=unsatisfied4, value=1, font=font_style, command=lambda: satisfied4.set(0))
    unsatisfied4_radiobutton.pack(anchor="w", pady=(0, 20))
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

# Configure the button_frame row to expand vertically
button_frame.grid_rowconfigure(0, weight=1)

# Create left-side navigation buttons
feedback_btn = Button(button_frame, text="Feedback", command=show_feedback, relief="flat", cursor="hand2", font=font_style)
feedback_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
feedback_btn.pack(padx=(25, 10), pady=(40, 20), fill="x")

analytics_btn = Button(button_frame, text="Analytics", command=show_analytics, relief="flat", cursor="hand2", font=font_style)
analytics_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
analytics_btn.pack(padx=(25, 10), pady=20, fill="x")

data_btn = Button(button_frame, text="Data", command=show_data, relief="flat", cursor="hand2", font=font_style)
data_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
data_btn.pack(padx=(25, 10), pady=20, fill="x")

start_btn = Button(button_frame, text="Start", command=show_start, relief="flat", cursor="hand2", font=font_style)
start_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
start_btn.pack(padx=(25, 10), pady=20, fill="x")

satisfaction_analytics_btn = Button(button_frame, text="Satisfaction Analytics", command=show_satisfaction_analytics, relief="flat", cursor="hand2", font=font_style)
satisfaction_analytics_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
satisfaction_analytics_btn.pack(padx=(25, 20), pady=20, fill="x")

satisfaction_data_btn = Button(button_frame, text="Satisfaction Data", command=show_satisfaction_data, relief="flat", cursor="hand2", font=font_style)
satisfaction_data_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
satisfaction_data_btn.pack(padx=(25, 20), pady=(20, 40), fill="x")

# Create a frame to hold the content
content_frame = Frame(main, bg="white")
content_frame.grid(row=0, column=1, padx=(50, 0), pady=(20, 0), sticky="nsew")

# Create a label inside the content frame
content_label = Label(content_frame, text="Start Page", font=font_style)
content_label.configure(bg="white")  # Remove this line to have no background color
content_label.pack()

# Show the initial content (Start Page)
show_start()

# Configure grid weights to allow expansion
main.grid_columnconfigure(0, weight=0)
main.grid_columnconfigure(1, weight=1)
main.grid_rowconfigure(0, weight=1)

# Run the application
main.mainloop()
