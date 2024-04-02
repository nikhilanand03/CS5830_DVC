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
    """
    Download CSV files specifically for the year 2023.

    Args:
        n_locs (int): Number of CSV files to download.
        output (str): Output folder path to save downloaded files.
    
    Returns:
        bool: True if download is successful, False otherwise.
    """
    print("2023",n_locs)
    # Just to speed it up specifically for the case of year=2023
    url = "www.ncei.noaa.gov/data/local-climatological-data/access/2023/"
    # arr contains only those files that are less than 1MB in size
    arr = ["99999994290.csv","99999913724.csv"]
    num_csvs=0
    
    for file in arr[:n_locs]:
        # print(size)
        saved = download_and_save_csv(url+file,"MonthlyDepartureFromNormalAverageTemperature",output)
    return True

def get_file_size(url):
    """
    Get the size of a file from a given URL.

    Args:
        url (str): URL of the file.

    Returns:
        int: Size of the file in bytes, or -1 if size retrieval fails.
    """
    response = requests.head(url)  # Only get headers, not content
    file_size = int(response.headers.get('content-length', -1))  # Get file size from headers

    if file_size == -1:
        return 'Could not get the file size.'
    else:
        return file_size

def download_and_save_csv(url, column_to_check, output_folder):
    """
    Download a CSV file from a given URL, check a specific column for NaNs, and if not fully NaN, save it to an output folder.

    Args:
        url (str): URL of the CSV file.
        column_to_check (str): Name of the column to check for NaN values.
        output_folder (str): Folder path to save the downloaded CSV file.

    Returns:
        bool: True if the CSV is saved successfully, False otherwise.
    """

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
        output (str): Output folder path to save downloaded files.
    """

    url = "www.ncei.noaa.gov/data/local-climatological-data/access/"+str(year)+"/"

    path = Path('/Users/nikhilanand/CS5830_DVC/data/list.txt') # list.txt contains all csv filenames from the given year
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

    # Now it goes over each filename url and if it's smaller than 1MB, it checks that the columns aren't NaN and saves it in that case
    for file in list_of_files:
        size=get_file_size("https://"+url+file[:-1])
        if(size<1000000): # Size < 1MB
            saved = download_and_save_csv(url+file,"MonthlyDepartureFromNormalAverageTemperature",output)
            if(saved):
                num_csvs+=1
            if(num_csvs>=n_locs):
                break
        else:
            print(file[:-1],": Too big.")
    
def main():
    # Load parameters from the YAML configuration file
    params = yaml.safe_load(open("params.yaml"))["download"]

    # Check if any command line arguments are provided
    if len(sys.argv) != 1:
        print(sys.argv)
        sys.stderr.write("Arguments error. Usage:\n")
        sys.stderr.write("\tpython src/download.py\n")
        sys.exit(1)

    # Extract parameters from the configuration
    year = params["year"]
    n_locs = params["n_locs"]

    # Set the output folder path where downloaded files will be saved
    output = "/Users/nikhilanand/CS5830_DVC/data/downloaded"
    if not os.path.exists(output):
        os.makedirs(output)

    print(n_locs)

    # Check if the requested year is 2023 and the number of locations is either 1 or 2
    if(year==2023 and (n_locs==2 or n_locs==1)):
        saved = download_2023(n_locs,output)
    else:
        download_csvs(n_locs,year,output)
        
    # If files were not saved during the initial 2023-specific download, attempt regular download
    if not saved:
        download_csvs(n_locs,year,output)

if __name__ == "__main__":
    main()