import os
import sys
import re
import ast
from sklearn.metrics import r2_score

def parse_file(file_path):
    """
    Parse a file containing dictionaries and extract values from each dictionary.

    Args:
        file_path (str): Path to the file to be parsed.

    Returns:
        tuple: A tuple containing a list of merged values from all dictionaries and a list of end indices of each dictionary.
    """
    merged_values = []
    ends=[]
    with open(file_path, 'r') as file:
        for line in file:
            # Extract the dictionary from each line using regular expression
            dict = ast.literal_eval(line[line.find("{"):-1])
            values = dict.values()
            keys = list(dict.keys())
            ends.append(keys[-1])
            merged_values.extend(values)
    
    return merged_values,ends

def main():

    # Check if the right number of command line arguments are provided
    if len(sys.argv) != 3:
        sys.stderr.write("Arguments error. Usage:\n")
        sys.stderr.write("\tpython evaluate.py gt-file computed-file\n")
        sys.exit(1)

    gt_path = sys.argv[1]
    computed_path = sys.argv[2]

    gt_arr,gt_ends = parse_file(gt_path)
    comp_arr,_ = parse_file(computed_path)
    
    # Preprocess the computed array if the length isn't the same as the GT array (to ensure they are equal in length)
    if(len(gt_ends)==2):
        comp_arr = comp_arr[:gt_ends[0]] + comp_arr[12:12+gt_ends[1]]
    elif(len(gt_ends)==1):
        comp_arr = comp_arr[:gt_ends[0]]
    else:
        comp_arr = []
        for i in range(len(gt_ends)):
            comp_arr = comp_arr+comp_arr[12*i:12*i+gt_ends[i]]

    r2 = r2_score(gt_arr,comp_arr)

    # Create the evaluated folder if it doesn't exist
    if not os.path.exists("/Users/nikhilanand/CS5830_DVC/data/evaluated"):
        os.makedirs("/Users/nikhilanand/CS5830_DVC/data/evaluated")

    # Write R2 score to evaluation.txt
    with open("/Users/nikhilanand/CS5830_DVC/data/evaluated/evaluation.txt",'w') as file:
        pass
    with open("/Users/nikhilanand/CS5830_DVC/data/evaluated/evaluation.txt",'a') as file:
        file.write("Measure of Consistence, R2 Score is: "+str(r2)+"\n")
    
    # Write consistency message to evaluation.txt based on R2 score
    with open("/Users/nikhilanand/CS5830_DVC/data/evaluated/evaluation.txt",'a') as file:
        if(r2>0.9):
            file.write("Consistent data")
        else:
            file.write("Inconsistent data")

if __name__=="__main__":
    main()