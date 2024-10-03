import pandas as pd
import numpy as np

# Step 1: Read the CSV file
file_path = 'other/raw.csv'
df = pd.read_csv(file_path)

# Identify rows where 'BUSINESS_EMAIL' is empty or '-'
mask = (df['BUSINESS_EMAIL'].isna()) | (df['BUSINESS_EMAIL'] == '-')
# Replace 'BUSINESS_EMAIL' with corresponding values from 'PERSONAL_EMAIL' for identified rows
df.loc[mask, 'BUSINESS_EMAIL'] = df.loc[mask, 'PERSONAL_EMAIL']
# Remove rows where 'BUSINESS_EMAIL' is still empty or '-'
df = df[df['BUSINESS_EMAIL'].notna() & (df['BUSINESS_EMAIL'] != '-')]


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

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Assuming df is your DataFrame with the industry_scores, seniority_level_scores, and company_revenue_scores columns

# Combine the scores based on provided dictionaries
df['EMAIL_SCORE'] = (
    df['INDUSTRY_SCORE'] +
    df['JOB_TITLE_SCORE'] +
    df['SENIORITY_SCORE'] +
    df['COMPANY_REVENUE_SCORE']
) / 4  # You might want to adjust this based on the importance of each score

# Drop the intermediate scores if needed
df.drop(['INDUSTRY_SCORE', 'JOB_TITLE_SCORE', 'SENIORITY_SCORE', 'COMPANY_REVENUE_SCORE'], axis=1, inplace=True)

# Standardize the features for k-means
features = df[['EMAIL_SCORE']]
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(features), columns=features.columns)

# Apply k-means clustering
kmeans = KMeans(n_clusters=5, random_state=42)
df['CLUSTER'] = kmeans.fit_predict(df_scaled)

# Save the DataFrame with 'EMAIL_SCORE' and 'CLUSTER' to a CSV file
output_file_path = 'email_predict_kmeans.csv'
df.to_csv(output_file_path, index=False)

print(f"DataFrame with 'EMAIL_SCORE' and 'CLUSTER' columns saved to {output_file_path}")

# Separate into DataFrames based on cluster
cluster_dataframes = [df[df['CLUSTER'] == i] for i in range(5)]

# Save each cluster's DataFrame to a separate CSV file
for i, cluster_df in enumerate(cluster_dataframes):
    cluster_output_file = f'cluster_{i}_emails.csv'
    cluster_df.to_csv(cluster_output_file, index=False)
    print(f"Cluster {i} saved to {cluster_output_file}")

# Separate into lists based on cluster
cluster_lists = [df[df['CLUSTER'] == i]['BUSINESS_EMAIL'].tolist() for i in range(5)]

# Display the separate lists
for i, email_list in enumerate(cluster_lists):
    print(f"Cluster {i} Emails:", email_list)

