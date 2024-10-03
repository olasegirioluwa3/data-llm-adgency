import csv
import functions as fc

def filter_us_states(csv_file_path, output_file_path):
    us_territory_codes = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC', 'PR', 'GU', 'VI', 'AS', 'MP']

    with open(csv_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', newline='', encoding='utf-8') as output_file, open("output/raw.csv", 'w', newline='', encoding='utf-8') as output_file2:
        reader = csv.DictReader(input_file)
        fieldnames2 = reader.fieldnames
        print(fieldnames2)

        # Define the columns for the output file
        output_fieldnames = [
            'Client Customer ID', 'First Name', 'Last Name', 'Business Email', 'Phone Number'
        ]

        # Write header to the output file
        writer = csv.DictWriter(output_file, fieldnames=output_fieldnames)
        writer.writeheader()

        writer2 = csv.DictWriter(output_file2, fieldnames=fieldnames2)
        writer2.writeheader()

        # Autoincrement for "Client Customer ID"
        client_customer_id_counter = 1

        # Track the number of rows before processing
        num_rows_before = sum(1 for _ in reader)
        print(f'Number of rows before processing: {num_rows_before}')

        # Reset the file pointer to the beginning of the file
        input_file.seek(0)

        # Skip the header row
        next(reader)

        # Filter rows and write to the output file
        for row in reader:
            state_column = row.get('PERSONAL_STATE', '')  # Assuming the column name is 'PERSONAL_STATE'
            
            # Validate addresses
            valid_address1 = fc.validate_address(row.get('PERSONAL_ADDRESS', ''), row.get('PERSONAL_ADDRESS_2', ''))
            valid_address2 = fc.validate_address(row.get('PROFESSIONAL_ADDRESS', ''), row.get('PROFESSIONAL_ADDRESS2', ''))
            valid_address3 = fc.validate_address(row.get('COMPANY_ADDRESS', ''), row.get('COMPANY_ADDRESS2', ''))

            # Check conditions before adding the row to the output file
            if state_column in us_territory_codes and (valid_address1 or valid_address2 or valid_address3) and fc.validate_email(row.get('BUSINESS_EMAIL_VALIDATION_STATUS', '')):
            # if fc.validate_email(row.get('BUSINESS_EMAIL_VALIDATION_STATUS', '')):
                # Prepare the row for the output file
                output_row = {
                    'Client Customer ID': client_customer_id_counter,
                    'First Name': row.get('FIRST_NAME', ''),
                    'Last Name': row.get('LAST_NAME', ''),
                    'Business Email': row.get('BUSINESS_EMAIL', '') or row.get('PERSONAL_EMAIL', '') or row.get('PROGRAMMATIC_BUSINESS_EMAILS', ''),
                    'Phone Number': row.get('MOBILE_PHONE', '')
                }

                # Write the row to the output file
                writer.writerow(output_row)
                writer2.writerow(row)

                # Increment the "Client Customer ID" counter
                client_customer_id_counter += 1

        # Track the number of rows after processing
        num_rows_after = client_customer_id_counter - 1  # Exclude the header row
        print(f'Number of rows after processing: {num_rows_after}')

# Replace 'your_input_file.csv' and 'output_filtered_states.csv' with the actual paths
input_file_path = 'docs/Adpromoter_FirstPriority.csv'
output_file_path = 'output/output_email_filtered_states.csv'

filter_us_states(input_file_path, output_file_path)
