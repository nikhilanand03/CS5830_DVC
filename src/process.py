import sys
import os
import ast
import pandas as pd

def process_csv(input_path, output_file):
    """
    Process a CSV file, calculate the monthly average of a specific column,
    and save the results to an output file.

    Args:
        input_path (str): Path to the input CSV file.
        output_file (str): Path to the output file where processed data will be saved.
    """

    df = pd.read_csv(input_path)
    
    # Computations to get the mean over all days of a given month
    df2=df.loc[:,('DATE','DailyDepartureFromNormalAverageTemperature')]
    df2['MONTH']=df2.loc[:,'DATE'].map(lambda x: x[5:7])
    monthly_avg_dict = df2.groupby('MONTH')['DailyDepartureFromNormalAverageTemperature'].mean().to_dict()
    month_value_dict_new = {int(key): value for key, value in monthly_avg_dict.items()}
    
    # Create the output folder if it doesn't exist
    directory = os.path.dirname(output_file)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Check if the file exists, if not create it
    if not os.path.exists(output_file):
        with open(output_file, 'w'):
            pass  # This creates an empty file
    
    with open(output_file,'a') as file:
        file.write(str(input_path)+": "+str(month_value_dict_new)+"\n")
    
    print(f"Filtered data saved to: {output_file}")

def main():
    # params = yaml.safe_load(open("params.yaml"))["prepare"]

    # Check if the number of command-line arguments is correct
    if len(sys.argv) != 2:
        sys.stderr.write("Arguments error. Usage:\n")
        sys.stderr.write("\tpython prepare.py data-file\n")
        sys.exit(1)

    input = sys.argv[1] # Pass the data directory path here

    files = os.listdir(input)
    
    # Iterate over each file in the directory
    for file in files:
        # Check if the file has a .csv extension
        if file.endswith('.csv'):
            file_path = os.path.join(input, file) # Get the full path of the CSV file
            process_csv(file_path,"/Users/nikhilanand/CS5830_DVC/data/processed/computed_monthly_averages.txt")

if __name__=="__main__":
    main()