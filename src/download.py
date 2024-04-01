import os
import random
import re
import sys
import xml.etree.ElementTree

import yaml
import wget
import pandas as pd

import requests

from pathlib import Path

def download_2023(n_locs,output):
    # Just to speed it up specifically for the case of year=2023
    url = "www.ncei.noaa.gov/data/local-climatological-data/access/2023/"
    # arr contains only those files that are less than 1MB in size
    arr = ["99999994290.csv","99999953186.csv","99999923272.csv","99999923271.csv","99999913782.csv",\
           "99999913724.csv","99999904134.csv","99999900447.csv","99844199999.csv","99820599999.csv",\
            "99800399999.csv","99734499999.csv","99421099999.csv","99090099999.csv","99020099999.csv",\
                "98747099999.csv","98644099999.csv","98630099999.csv","98550099999.csv"]
    num_csvs=0
    
    for file in arr:
        # print(size)
        saved = download_and_save_csv(url+file,"MonthlyDepartureFromNormalAverageTemperature",output)
        if(saved):
            num_csvs+=1
        if(num_csvs>n_locs):
            break
    if(num_csvs!=n_locs):
        return False
    else:
        return True

def get_file_size(url):
    response = requests.head(url)  # Only get headers, not content
    file_size = int(response.headers.get('content-length', -1))  # Get file size from headers

    if file_size == -1:
        return 'Could not get the file size.'
    else:
        return file_size

def download_and_save_csv(url, column_to_check, output_folder):
    print("Downloading ",url,"Checking ",column_to_check,"Outputting to ",output_folder)
    filename = wget.download("https://"+url)
    print("wget done")
    df = pd.read_csv(filename)
    
    if not df[column_to_check].isnull().all():
        output_file = os.path.join(output_folder, os.path.basename(url))
        df.to_csv(output_file, index=False)
        print(f"Saved CSV file with non-empty '{column_to_check}' column to {output_file}")
        os.remove(filename)
        return True
    else:
        print(f"Skipping '{url}' as '{column_to_check}' column is full of NaNs")
        os.remove(filename)
        return False

def download_csvs(n_locs,year,output):
    """
    Download the given number of csvs from the given year in the climatological data site.

    Args:
        n_locs (int): Number of csvs to be downloaded
        year (int): Year of the data that must be downloaded
    """

    url = "www.ncei.noaa.gov/data/local-climatological-data/access/"+str(year)+"/"

    path = Path('/Users/nikhilanand/CS5830_DVC/data/list.txt')
    if(path.is_file()):
        print("list.txt already exists")
    else:
        result = os.popen("curl --silent https://"+ url +" | grep -o 'href=\".*\">' | sed 's/href=\"//;s/\/\">//'").read()

        with open("data/list_of_file.txt",'w') as file:
            file.write(result)
        with open("data/list_of_file.txt",'r') as file:
            with open("data/list.txt",'w') as file2:
                pass
            with open("data/list.txt",'a') as file2:
                lines = file.readlines()
                for line in lines:
                    if(line[:15].find("csv")!=-1):
                        file2.write(line[:15]+"\n")
        
        print("Wrote list.txt")
        os.remove("/Users/nikhilanand/CS5830_DVC/data/list_of_file.txt")

    with open("data/list.txt",'r') as file:
        list_of_files = file.readlines()[-1::-1]
    
    num_csvs=0

    for file in list_of_files:
        # print(".")
        # print("https://"+url+file[:-1])
        size=get_file_size("https://"+url+file[:-1])
        # print(size)
        if(size<1000000): # Size < 1MB
            saved = download_and_save_csv(url+file,"MonthlyDepartureFromNormalAverageTemperature",output)
            if(saved):
                num_csvs+=1
            if(num_csvs>n_locs):
                break
        else:
            print(file[:-1],": Too big.")
    
def main():
    params = yaml.safe_load(open("params.yaml"))["download"]

    if len(sys.argv) != 1:
        print(sys.argv)
        sys.stderr.write("Arguments error. Usage:\n")
        sys.stderr.write("\tpython src/download.py\n")
        sys.exit(1)

    year = params["year"]
    n_locs = params["n_locs"]

    output = "/Users/nikhilanand/CS5830_DVC/data"
    if(year==2023):
        saved = download_2023(n_locs,output)
    else:
        download_csvs(n_locs,year,output)
    
    if not saved:
        download_csvs(n_locs,year,output)

if __name__ == "__main__":
    main()