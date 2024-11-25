import pandas as pd
import matplotlib.pyplot as plt

def visualize_jobs():
    try:
        input_path = '/opt/airflow/datasets/skills_analysis.csv'
        output_path = '/opt/airflow/datasets/trends.png'

        # Load the analyzed data
        print(f"Loading data from {input_path}...")
        df = pd.read_csv(input_path)

        # Log the contents for debugging
        print("Preview of the data:")
        print(df.head())

        # Check for required columns
        required_columns = {'title', 'count'}
        if not required_columns.issubset(df.columns):
            raise KeyError(f"The file does not contain the required columns: {required_columns}")

        # Ensure non-empty data
        if df.empty:
            raise ValueError("The input data is empty. Cannot create visualization.")

        # Sort the data for better visualization (optional)
        df = df.sort_values(by='count', ascending=False)

        # Create a bar chart
        print("Creating a bar chart...")
        df.plot(kind='bar', x='title', y='count', figsize=(12, 8), legend=False)
        plt.title("Job Listings by Title")
        plt.xlabel("Job Title")
        plt.ylabel("Number of Listings")
        plt.xticks(rotation=45, ha='right')  # Rotate labels for better readability
        plt.tight_layout()

        # Save the visualization
        plt.savefig(output_path)
        print(f"Visualization saved successfully at {output_path}")

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}. Please ensure the file exists at {input_path}.")
    except KeyError as key_error:
        print(f"Error in visualize_jobs: {key_error}")
    except ValueError as value_error:
        print(f"Error in visualize_jobs: {value_error}")
    except Exception as e:
        print(f"An unexpected error occurred in visualize_jobs: {e}")
