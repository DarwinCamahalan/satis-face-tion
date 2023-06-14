from tkinter import *
import json
import datetime
import calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import numpy as np
from tkinter import messagebox

canvas = None 

# Set font for the whole application
font_style = ("Segoe UI Semibold", 11)

# Create the main window
main = Tk()
main.title("satisFACEtion")

# Set window size
main.geometry("1360x768")
# main.eval('tk::PlaceWindow . center')

# Configure main window background color
main.configure(background="white")

content_frame = None  # Declare content_frame as a global variable
survey_widgets = []  # List to store survey question widgets

# Create a frame to hold the content
content_frame = Frame(main, bg="white")
content_frame.grid(row=0, column=1, padx=(50, 0), pady=(20, 0), sticky="nsew")

# Create a label inside the content frame
content_label = Label(content_frame, text="Start Page", font=font_style)
content_label.configure(bg="white")  # Remove this line to have no background color
content_label.pack()


# Configure grid weights to allow expansion
main.grid_columnconfigure(0, weight=0)
main.grid_columnconfigure(1, weight=1)
main.grid_rowconfigure(0, weight=1)


# Function to get the next survey ID
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
    for widget in survey_widgets:
        widget.destroy()

def show_feedback():
    global content_frame, survey_widgets, removeGraph, canvas  # Declare content_frame and survey_widgets as global variables
    remove_survey_widgets()  # Remove any existing survey widgets
    if canvas is not None:
        canvas.get_tk_widget().destroy()
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

    # Function to submit the survey and store the answers in a JSON file
    def submit_survey():
        if validate_survey():
            # Prepare the survey data
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

            messagebox.showinfo("Survey Complete", "Thank you for answering the survey!")
            feedback_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
            show_start()
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
    content_label.config(text="Analytics Page")
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
        axes[row_index, col_index].set_ylabel("Count")
        if(i == 3):
            question = f"Overall Satisfaction"
        axes[row_index, col_index].set_title(question)

        # Set y-axis label to total number of surveys
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
    content_label.config(text="Data Page")

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
        elif view == 'week':
            month = data[0]
            selected_week = data[1]
            plot_data_by_day(month, selected_week)
            current_view = 'day'

    
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
        # Extract months and counts for plotting
        months = list(month_counts.keys())
        month_names = [calendar.month_name[month] for month in months]
        satisfied_counts = [month_counts[month]['Satisfied'] for month in months]
        unsatisfied_counts = [month_counts[month]['Unsatisfied'] for month in months]

        # Plot the bar graph by month
        plt.figure(figsize=(8, 6))
        x_pos = np.arange(len(months))
        plt.bar(x_pos - 0.2, satisfied_counts, 0.4, label='Satisfied', color='#00b7ff')
        plt.bar(x_pos + 0.2, unsatisfied_counts, 0.4, label='Unsatisfied', color='#ff2929')
        plt.xticks(x_pos, month_names)

        plt.xlabel('Month')
        plt.ylabel('Number of Surveys')
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
        plt.ylabel('Number of Surveys')
        plt.title('Customer Satisfaction by Week - {}'.format(calendar.month_name[month]))
        plt.legend()

        # Create a Tkinter canvas to display the plot
        canvas = FigureCanvasTkAgg(plt.gcf(), master=content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        plt.close()



    def plot_data_by_day(month, week):
        global canvas
        if canvas is not None:
            canvas.get_tk_widget().destroy()

        week_data = week_counts[month][week]

        # Extract days and counts for plotting
        days = list(week_data.keys())
        day_names = ['Day {}'.format(day) for day in days]
        satisfied_counts = [week_data[day]['Satisfied'] for day in days]
        unsatisfied_counts = [week_data[day]['Unsatisfied'] for day in days]

        # Plot the bar graph by day
        plt.figure(figsize=(8, 6))
        x_pos = np.arange(len(days))
        plt.bar(x_pos - 0.2, satisfied_counts, 0.4, label='Satisfied', color='#00b7ff')
        plt.bar(x_pos + 0.2, unsatisfied_counts, 0.4, label='Unsatisfied', color='#ff2929')
        plt.xticks(x_pos, day_names)

        plt.xlabel('Day')
        plt.ylabel('Number of Surveys')
        plt.title('Customer Satisfaction by Day - Week {}'.format(week))
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


def show_start():
    global content_frame, survey_widgets, canvas  # Declare content_frame and survey_widgets as global variables
    remove_survey_widgets()  # Remove any existing survey widgets
    if canvas is not None:
        canvas.get_tk_widget().destroy()
    content_label.config(text="Start Page")

    # subprocess.Popen(["python", "cam.py"])
    # feedback_btn.configure(bg="white", fg="black", highlightbackground="white", borderwidth=0, anchor="w")
    # show_feedback()
    

def show_satisfaction_analytics():
    global content_frame, survey_widgets, canvas  # Declare content_frame and survey_widgets as global variables
    remove_survey_widgets()  # Remove any existing survey widgets
    if canvas is not None:
        canvas.get_tk_widget().destroy()
    content_label.config(text="Satisfaction Analytics Page")

def show_satisfaction_data():
    global content_frame, survey_widgets, canvas   # Declare content_frame and survey_widgets as global variables
    remove_survey_widgets()  # Remove any existing survey widgets
    if canvas is not None:
        canvas.get_tk_widget().destroy()
    content_label.config(text="Satisfaction Data Page")
    

# Create a frame for the stacked buttons
button_frame = Frame(main, bg="#302d2d")
button_frame.grid(row=0, column=0, padx=0, pady=0, sticky="ns")

# Configure the button_frame row to expand vertically
button_frame.grid_rowconfigure(0, weight=1)

# Create left-side navigation buttons
start_btn = Button(button_frame, text="Start", command=show_start, relief="flat", cursor="hand2", font=font_style)
start_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
start_btn.pack(padx=(25, 10),pady=(40, 20), fill="x")

feedback_btn = Button(button_frame, text="Feedback", command=show_feedback, relief="flat", cursor="hand2", font=font_style)
feedback_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
feedback_btn.pack(padx=(25, 10), pady=20 , fill="x")

analytics_btn = Button(button_frame, text="Analytics", command=show_analytics, relief="flat", cursor="hand2", font=font_style)
analytics_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
analytics_btn.pack(padx=(25, 10), pady=20, fill="x")

data_btn = Button(button_frame, text="Data", command=show_data, relief="flat", cursor="hand2", font=font_style)
data_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
data_btn.pack(padx=(25, 10), pady=20, fill="x")


satisfaction_analytics_btn = Button(button_frame, text="Satisfaction Analytics", command=show_satisfaction_analytics, relief="flat", cursor="hand2", font=font_style)
satisfaction_analytics_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
satisfaction_analytics_btn.pack(padx=(25, 25), pady=20, fill="x")

satisfaction_data_btn = Button(button_frame, text="Satisfaction Data", command=show_satisfaction_data, relief="flat", cursor="hand2", font=font_style)
satisfaction_data_btn.configure(bg="#302d2d", fg="white", highlightbackground="white", borderwidth=0, anchor="w")
satisfaction_data_btn.pack(padx=(25, 25), pady=(20, 40), fill="x")

# Show the initial content (Start Page)
show_start()

# Run the application
main.mainloop()
