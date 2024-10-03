#make sure you import all the needed functions from adlist.py as below
from Adfunctions import *

def liveramp_adlist(file_path: str, target_industries: list, adlist_name: str, **kwargs):
    """
    Processes an input data file to generate a formatted advertising list following specific criteria. 
    The data is filtered by target industries and USA states, validated for addresses and phone numbers, 
    and formatted in the Liveramp specified format.

    Args:
        file_path (str): Path to the input data file.
        target_industries (list): List of target industries for filtering.
        adlist_name (str): Name for the output advertising list file.
        **kwargs: Additional arguments to pass to filtering and formatting functions.

    Returns:
        str: A message indicating the status of the file saving process.

    Raises:
        Exception: If any errors occur during the data processing steps.
    """

    try:
        # Load data from the file
        df = get_data(file_path)
        
        # Filter by target industries
        df_industries = filter_by_target_industries(df, target_industries)

        # Filter for USA states only
        state_df = filter_usa_states(df_industries)
    
        # Filter for valid addresses
        valid_address_df = filter_and_label_valid_addresses(state_df.copy())
    
        # Get valid phone numbers
        valid_numbers = enrich_phone_numbers(valid_address_df.copy())
   
        # Filter for valid business and personal emails
        valid_number_email_df = filter_by_valid_business_personal_email(
            valid_numbers,
            validation_column="BUSINESS_EMAIL_VALIDATION_STATUS",
            business_email_column="BUSINESS_EMAIL",
            personal_email_column="PERSONAL_EMAIL"
        )
    
        # Split programmatic business emails into separate columns
        df_program_emails = split_columns_by_separator(
            valid_number_email_df, 
            'PROGRAMMATIC_BUSINESS_EMAILS', 
            separator=',', 
            keep_non_missing_only=True, 
            drop_duplicates=True
        )
    
        # Format data in Liveramp format
        formatted_df = liveramp_formatter(df_program_emails)
    
        # Save to file
        output_message = save_df_to_csv(formatted_df, adlist_name)

        return output_message

    except Exception as e:
        # Handle any exceptions that occur during the process
        return f"An error occurred: {str(e)}"

#Apply function to generate adlis data in liverampt format 
primary_industries=['Advertising Services', 'Marketing','Book And Periodical Publishing', 'Entertainment Providers', 'Events Services','Broadcast Media Production And Distribution','Public Relations And Communications Services', 'Online Audio And Video Media', 'Printing Services','Newspaper Publishing', 'Newspapers']
liveramp_adlist(file_path='./raw_data/Adpromoter_FirstPriority.csv', target_industries=primary_industries, adlist_name='final_list')