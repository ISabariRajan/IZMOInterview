"""
    This script is used to analyse the given input file with
    machineip, ipaddress, security-group and subnet
    And analyse the frequency count and store the analysis in csv files
        -   Subnets
        -   Security Groups
        -   Subnets abd Security Groups
"""
import sys
import pandas as pd


def identify_and_explode_multivalued_columns(df):
    """
        The identify_and_explode_multivalued_columns function takes a dataframe as input
        and identifies multivalued columns and returns the same dataframe with
        all the multivalued columns columns exploded.
        
        :param df: Pass the dataframe to the function
        :return: A dataframe

    """
    # The requirement is to identify multivalued columns and
    # Explode those columns, that is why I looped all columns
    # Or else, I should have used this on only "security-group" and "subnet"
    for column in df.columns:
        # converting multi-valued columns to list of values
        df[column] = df[column].str.split(",")
        # Explode multi-valued columns
        df = df.explode(column)
    return df

def analyze_dataframe_for_frequency_count(df, column_name):
    """
        The analyse_dataframe_for_frequency_count function takes a dataframe and
        a column name as input. It then counts the frequency of each value in that column,
        prints the results to console, and stores them in an output file.
        
        :param df: Pass the dataframe to the function
        :param column_name: Specify the column name of the dataframe that is to be analyzed
        :return: None
    """
    # Get frequency count of each security-group and subnet
    count =df[column_name].value_counts()

    # Print results
    # to_string() method ensures that all the values are displayed in the console
    print(count.to_string())

    # Storing the analysis to output file for future use
    count.to_csv("_".join(column_name) + ".csv")

# The main function responsible for
def main(input_file):
    """
        The main function is the entry point of the program.
        -   It takes in a file path as an argument and parses it to a dataframe.
        -   Then, it identifies multivalued columns and explodes them into multiple rows.
        -   Finally, it analyses the dataframe for frequency count on different combinations
        of columns and displays the count and store them to specific files.
        
        :param input_file: Pass the file path to the main function
        :return: None
    """
    try:

        # Base Assignment
        # Parse given file to dataframe using custom separator
        df = pd.read_csv(input_file, sep="|")
        # Explode multivalued columns
        # This function will not create any exception, So it is not handled
        df = identify_and_explode_multivalued_columns(df)
        # Analysis
        analyse_coulumns = [["security-group"], ["subnet"], ["subnet", "security-group"]]
        for column in analyse_coulumns:
            analyze_dataframe_for_frequency_count(df, column)

    except FileNotFoundError:
        print("File not found in location: " + input_file)
        print("Please check the file path and try again...")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide input file path...")
