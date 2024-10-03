import pandas as pd
import numpy as np

# Step 1: Read the CSV file
file_path = 'other/raw.csv'
df = pd.read_csv(file_path)



# Clean 'PRIMARY_INDUSTRY' by stripping leading and trailing spaces and converting to uppercase
df['PRIMARY_INDUSTRY'] = df['PRIMARY_INDUSTRY'].str.strip().str.upper()

# Create a dictionary to store random scores for each industry
industry_scores = {
    'ADVERTISING SERVICES': 4,
    'ENTERTAINMENT PROVIDERS': 3,
    'EVENTS SERVICES': 5,
    'BROADCAST MEDIA PRODUCTION AND DISTRIBUTION': 2,
    'BOOK AND PERIODICAL PUBLISHING': 1,
    'PUBLIC RELATIONS AND COMMUNICATIONS SERVICES': 5,
    'ONLINE AUDIO AND VIDEO MEDIA': 3,
    'PRINTING SERVICES': 4,
    'NEWSPAPER PUBLISHING': 2,
    'NEWSPAPERS': 5
}
# Map the cleaned 'PRIMARY_INDUSTRY' to 'INDUSTRY_SCORE'
df['INDUSTRY_SCORE'] = df['PRIMARY_INDUSTRY'].map(industry_scores).fillna(0).astype(int)




# Convert 'JOB_TITLE' to uppercase
df['JOB_TITLE'] = df['JOB_TITLE'].str.strip().str.upper()
# df['JOB_TITLE'] = df['JOB_TITLE'].str.upper()
df['JOB_TITLE_SCORE'] = 0  # Initialize the column with default value
for index, row in df.iterrows():
    job_title = row['JOB_TITLE']
    
    # Check for missing values before iterating
    if pd.notna(job_title):
        if any(keyword in job_title for keyword in ['MEDIA', 'PARTNER', 'DIRECTOR']):
            df.at[index, 'JOB_TITLE_SCORE'] = 5
        elif any(keyword in job_title for keyword in ['MANAGER', 'STRATEGY', 'BRAND']):
            df.at[index, 'JOB_TITLE_SCORE'] = 4
        elif any(keyword in job_title for keyword in ['SENIOR', 'EXECUTIVE', 'PROGRAM']):
            df.at[index, 'JOB_TITLE_SCORE'] = 3
        elif any(keyword in job_title for keyword in ['COO', 'CEO', 'CTO', 'VICE']):
            df.at[index, 'JOB_TITLE_SCORE'] = 2
        else:
            df.at[index, 'JOB_TITLE_SCORE'] = 1

                                                        



df['SENIORITY_LEVEL'] = df['SENIORITY_LEVEL'].str.strip().str.upper()

# Create a dictionary to store random scores for each seniority level
seniority_level_scores = {
    'CXO': 3,
    'DIRECTOR': 4,
    'MANAGER': 5,
    'VP': 2
}

# Map the 'SENIORITY_LEVEL' to 'SENIORITY_SCORE'
df['SENIORITY_SCORE'] = df['SENIORITY_LEVEL'].map(seniority_level_scores).fillna(0).astype(int)






# Display the unique values in the 'COMPANY_REVENUE' column
unique_company_revenue = df['COMPANY_REVENUE'].unique()
print("Unique Values in COMPANY_REVENUE:")
print(unique_company_revenue)

# Create a dictionary to store scores for each company revenue range
company_revenue_scores = {
    'Under 1 Million': 5,
    '1 Million to 5 Million': 5,
    '5 Million to 10 Million': 4,
    '10 Million to 25 Million': 4,
    '25 Million to 50 Million': 3,
    '50 Million to 100 Million': 3,
    '100 Million to 250 Million': 2,
    '250 Million to 500 Million': 2,
    '500 Million to 1 Billion': 1,
    '1 Billion and Over': 1
}

# Map the 'COMPANY_REVENUE' to 'COMPANY_REVENUE_SCORE'
df['COMPANY_REVENUE_SCORE'] = df['COMPANY_REVENUE'].map(company_revenue_scores).fillna(0).astype(int)

# Display the DataFrame with the new 'COMPANY_REVENUE_SCORE' column
print(df[['COMPANY_REVENUE', 'COMPANY_REVENUE_SCORE']])


# Save the DataFrame to CSV
output_file_path = 'job_titles.csv'
df.to_csv(output_file_path, index=False)

print(f"DataFrame with 'INDUSTRY_SCORE','JOB_TITLE_SCORE','SENIORITY_SCORE', 'COMPANY_REVENUE_SCORE' column saved to {output_file_path}")