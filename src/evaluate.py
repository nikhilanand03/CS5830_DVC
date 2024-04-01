import os
import sys
import re
import ast
from sklearn.metrics import r2_score

def parse_file(file_path):
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
    if len(sys.argv) != 3:
        sys.stderr.write("Arguments error. Usage:\n")
        sys.stderr.write("\tpython evaluate.py gt-file computed-file\n")
        sys.exit(1)

    gt_path = sys.argv[1]
    computed_path = sys.argv[2]

    gt_arr,gt_ends = parse_file(gt_path)
    comp_arr,_ = parse_file(computed_path)
    
    comp_arr = comp_arr[:gt_ends[0]] + comp_arr[12:12+gt_ends[1]]

    # print(gt_arr,comp_arr)

    r2 = r2_score(gt_arr,comp_arr)

    if not os.path.exists("/Users/nikhilanand/CS5830_DVC/data/evaluated"):
        os.makedirs("/Users/nikhilanand/CS5830_DVC/data/evaluated")

    with open("/Users/nikhilanand/CS5830_DVC/data/evaluated/evaluation.txt",'w') as file:
        pass
    
    with open("/Users/nikhilanand/CS5830_DVC/data/evaluated/evaluation.txt",'a') as file:
        file.write("Measure of Consistence, R2 Score is: "+str(r2)+"\n")
    
    with open("/Users/nikhilanand/CS5830_DVC/data/evaluated/evaluation.txt",'a') as file:
        if(r2>0.9):
            file.write("Consistent data")
        else:
            file.write("Inconsistent data")

if __name__=="__main__":
    main()