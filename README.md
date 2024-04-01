# CS5830_DVC
This is my assignment related to Data Version Control (DVC) of the course CS5830 (Big Data Lab).

# Usage

Running `dvc repro` will reproduce the pipeline below:

<img width="1030" alt="image" src="https://github.com/nikhilanand03/CS5830_DVC/assets/75153414/d9a19c53-2c26-44a4-9ea3-0f81232244bb">

This thus downloads required number of files from the server, prepares the list of monthly averages, processes (or computes) the monthly averages from the daily averages, and evaluates (or compares) the two averages to get an R2 score.

If you get an error saying no changes were made, make minor changes (like a variable name) to the download.py file, and then run `dvc repro`. This should do the trick and all your files will be populated. 

The data/evaluated directory contains a txt file with our evaluation output.

The directory structure should look like this after running:

<img width="252" alt="image" src="https://github.com/nikhilanand03/CS5830_DVC/assets/75153414/37f1be7b-afd5-4aea-ad6c-bfce124d6cf4">
</br>

Running `dvc dag` on the commnd line should reveal this:

<img width="507" alt="image" src="https://github.com/nikhilanand03/CS5830_DVC/assets/75153414/9da8409b-4885-4d88-92e3-ef7b1e2f636f">
</br>

Running `dvc exp show` on the commnd line should reveal this:

<img width="755" alt="image" src="https://github.com/nikhilanand03/CS5830_DVC/assets/75153414/5dd9b0fc-c1e2-4910-8a51-1ffeb15aaf2d">

Next, we can change the `n_locs` parameter in `params.yaml` from 2 to 1 and re-run `dvc repro`. Then we see `dvc exp show`:

<img width="756" alt="image" src="https://github.com/nikhilanand03/CS5830_DVC/assets/75153414/313f14fd-7cd5-4e35-9055-ac6287a9358c">
</br>

A `dvc params diff` reveals exactly which params were changed between experiments.

<img width="628" alt="image" src="https://github.com/nikhilanand03/CS5830_DVC/assets/75153414/6d019fd9-d74a-4470-b36a-583a6a9dee1c">
