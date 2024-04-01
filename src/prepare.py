import os
import random
import re
import sys
import xml.etree.ElementTree
import pandas as pd

import yaml

def process_csv(input_path, output_file, column_name):
    df = pd.read_csv(input_path)
    
    # Extract rows where the specified column is not NaN
    df = df.dropna(subset=[column_name])
    df2=df.loc[:,('DATE','MonthlyDepartureFromNormalAverageTemperature')]
    df2['MONTH']=df2.loc[:,'DATE'].map(lambda x: x[5:7])
    month_value_dict = df2.set_index('MONTH')['MonthlyDepartureFromNormalAverageTemperature'].to_dict()
    month_value_dict_new = {int(key): value for key, value in month_value_dict.items()}
    
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

    if len(sys.argv) != 2:
        sys.stderr.write("Arguments error. Usage:\n")
        sys.stderr.write("\tpython prepare.py data-file\n")
        sys.exit(1)

    input = sys.argv[1] # Pass the data directory path here

    files = os.listdir(input)
    
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(input, file)
            process_csv(file_path,"/Users/nikhilanand/CS5830_DVC/data/prepared/ground_truth.txt","MonthlyDepartureFromNormalAverageTemperature")

if __name__ == "__main__":
    main()
