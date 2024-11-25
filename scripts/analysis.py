import pandas as pd
import os

def analyze_jobs():
    try:
        # Check if the input CSV exists
        csv_path = '/opt/airflow/datasets/jobs.csv'
        if not os.path.exists(csv_path):
            print(f"Input CSV file not found: {csv_path}")
            return

        # Read the jobs.csv file
        df = pd.read_csv(csv_path)

        # Ensure the necessary columns are present
        # Ensure both 'title' and 'company' are available
        # if 'title' in df.columns and 'company' in df.columns:
        #     skill_counts = df.groupby('company').size().reset_index(name='count')
        #     skill_counts.to_csv('/opt/airflow/datasets/skills_analysis.csv', index=False)
        #     print("Job analysis complete!")
        # else:
        #     print("Error: Required columns 'title' and 'company' are missing in the input file.")

        # Perform analysis and save results
        skill_counts = df['title'].value_counts()
        output_path = '/opt/airflow/datasets/skills_analysis.csv'
        skill_counts.to_csv(output_path, header=True)
        print(f"Job analysis complete! Results saved to {output_path}")

    except Exception as e:
        print(f"Error occurred during analysis: {e}")
