# Cross File Analyzer

Cross File Analyzer is an application that allows you to analyze files on your operating system. It works on all operating systems and provides various functionalities to analyze and search for files.

## Installation

To use the Cross File Analyzer, follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/selimcavas/cross-file-analyzer.git
   ```
   
2. Change into the project directory:

    ```
    cd cross-file-analyzer
    ```
  
3. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

## Usage

To use Cross File Analyzer, open a terminal or command prompt and navigate to the directory where the script is located. Then, run the script with the following command:

  ```
    python main.py
  ```
 
### Options ###

- Option 1: Get total count and size of files on the operating system
    
    
    ```
    This option allows you to retrieve the total count and size of files on the entire operating system. 
    It may take some time to complete depending on the size of the system.

    To choose this option, enter `1` when prompted.
    ```


- Option 2: Search for files with a specific extension on the operating system
    
    ```
    This option enables you to search for files with a specific extension on the operating system. 
    It provides the count and allocated space for the files found.

    To choose this option, enter `2` when prompted and provide the desired file extension.
    ```


- Option 3: Search for files with a specific extension on a specific directory
    
    ```
    This option allows you to search for files with a specific extension in a specific directory. 
    It provides the count and allocated space for the files found.

    To choose this option, enter `3` when prompted and provide the desired file extension and directory path.
    ```


- Option 4: Find a file with a specific name on the operating system
    
    ```
    With this option, you can search for files with a specific name on the operating system. 
    It returns the file paths for the files found.

    To choose this option, enter `4` when prompted and provide the desired file name.
    ```


- Option 5: Get the top 10 largest files in a specific directory
    
    ```
    This option allows you to retrieve the top 10 largest files in a specific directory. 
    It displays the file names and their respective sizes in a bar chart as well as listing their paths.

    To choose this option, enter `5` when prompted and provide the directory path.
    ```


- Option 6: Exit the program

    ```
    To exit the Cross File Analyzer, choose this option by entering `6` when prompted.
    ```

