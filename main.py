import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, Button, Label, filedialog, Toplevel


# Step 1: Load Data
def load_data(filepath):
    try:
        data = pd.read_csv(filepath)
        print("Data loaded successfully!")
        return data
    except FileNotFoundError:
        print("File not found. Please check the filepath.")
        return None


# Step 2: Clean Data
def clean_data(data):
    # Drop rows with all missing values
    data = data.dropna(how='all')

    # Drop columns with all missing values
    data = data.dropna(axis=1, how='all')

    print("Data cleaned dynamically based on available rows and columns!")
    return data


# Visualization helper functions
def draw_correlation_heatmap(data, window):
    numerical_columns = data.select_dtypes(include=['number']).columns
    if len(numerical_columns) > 1:
        correlation_matrix = data[numerical_columns].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
        plt.title("Correlation Heatmap (Numerical Columns)")
        plt.show()
    else:
        display_message(window, "Not enough numerical columns for a heatmap.")


def draw_histograms(data, window):
    numerical_columns = data.select_dtypes(include=['number']).columns
    if len(numerical_columns) >= 1:
        for col in numerical_columns:
            plt.figure(figsize=(8, 4))
            sns.histplot(data[col], kde=True, bins=30)
            plt.title(f"Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            plt.show()
    else:
        display_message(window, "No numerical columns available for histograms.")


def draw_pairwise_scatter(data, window):
    numerical_columns = data.select_dtypes(include=['number']).columns
    if len(numerical_columns) > 1:
        sns.pairplot(data[numerical_columns])
        plt.suptitle("Pairwise Scatter Plots", y=1.02)
        plt.show()
    else:
        display_message(window, "Not enough numerical columns for scatter plots.")


def draw_categorical_barcharts(data, window):
    categorical_columns = data.select_dtypes(include=['object', 'category']).columns
    if len(categorical_columns) >= 1:
        for col in categorical_columns:
            plt.figure(figsize=(8, 4))
            data[col].value_counts().plot(kind='bar', color='skyblue')
            plt.title(f"Bar Plot for {col}")
            plt.xlabel(col)
            plt.ylabel("Count")
            plt.show()
    else:
        display_message(window, "No categorical columns available for bar plots.")


def display_message(window, message):
    """Displays a message if a visualization is not possible."""
    error_window = Toplevel(window)
    error_window.title("Error")
    error_label = Label(error_window, text=message, font=("Arial", 12), fg="red")
    error_label.pack(pady=10)


# Main Window GUI
def main_gui():
    loaded_data = {"data": None}  # Shared data storage for `loaded_data`
    open_chart_window = {"window": None}  # Keep track of opened chart window

    def load_and_clean_data():
        # Open file dialog to select a CSV file
        filepath = filedialog.askopenfilename(
            title="Select a CSV File",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        if filepath:
            # Update label to show selected file
            label_file.config(text=f"Selected File: {filepath}")

            # Load and clean the dataset
            data = load_data(filepath)
            if data is not None:
                data = clean_data(data)
                loaded_data["data"] = data  # Pass the cleaned data for use in visualizations

    def show_chart(chart_function):
        if loaded_data["data"] is not None:
            # Close any existing chart window (if present)
            if open_chart_window["window"] is not None:
                open_chart_window["window"].destroy()
                open_chart_window["window"] = None

            # Create a new chart window
            new_window = Toplevel(root)
            new_window.title("Chart Display")
            open_chart_window["window"] = new_window  # Keep track of this window

            # Call the selected chart function in the new window
            chart_function(loaded_data["data"], new_window)
        else:
            print("No dataset loaded. Please load a dataset first.")

    # Create the main Tkinter window
    root = Tk()
    root.title("CSV Data Analysis")
    root.geometry("500x300")

    # Add a label for instructions
    label_instruction = Label(root, text="Load a CSV file and select a chart type to display.", font=("Arial", 12))
    label_instruction.pack(pady=10)

    # Add a button to load a CSV file
    button_load = Button(root, text="Load CSV", command=load_and_clean_data, font=("Arial", 12), bg="lightblue")
    button_load.pack(pady=10)

    # Label to show which file is loaded
    label_file = Label(root, text="No file selected", font=("Arial", 10), fg="grey")
    label_file.pack(pady=5)

    # Buttons for chart types
    button_heatmap = Button(
        root, text="Correlation Heatmap", font=("Arial", 12),
        command=lambda: show_chart(draw_correlation_heatmap), bg="lightgreen"
    )
    button_heatmap.pack(pady=5)

    button_histogram = Button(
        root, text="Histograms", font=("Arial", 12),
        command=lambda: show_chart(draw_histograms), bg="lightgreen"
    )
    button_histogram.pack(pady=5)

    button_scatter = Button(
        root, text="Pairwise Scatter", font=("Arial", 12),
        command=lambda: show_chart(draw_pairwise_scatter), bg="lightgreen"
    )
    button_scatter.pack(pady=5)

    button_bar = Button(
        root, text="Categorical Bar Charts", font=("Arial", 12),
        command=lambda: show_chart(draw_categorical_barcharts), bg="lightgreen"
    )
    button_bar.pack(pady=5)

    # Start the Tkinter event loop
    root.mainloop()


# Run the GUI
if __name__ == "__main__":
    main_gui()
