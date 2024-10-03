import pandas as pd
import numpy as np

# Step 1: Read the CSV file
file_path = 'other/raw.csv'
df = pd.read_csv(file_path)
print(df.head())

unique_primary_industries = df['PRIMARY_INDUSTRY'].unique()


# Convert 'JOB_TITLE' to uppercase
df['JOB_TITLE'] = df['JOB_TITLE'].str.upper()
print(df['JOB_TITLE'].value_counts())
# print(count_job_title)
unique_job_title = df['JOB_TITLE'].unique()


# Step 3: Create a DataFrame with unique job titles
unique_job_titles_df = pd.DataFrame({'JOB_TITLE': unique_job_title})


# Step 3: Create a dictionary with randomly generated scores
# job_title_scores = {job_title: np.random.randint(1, 6) for job_title in unique_job_title}
# Step 2: Create a new column 'JOB_TITLE_SCORE' and assign scores based on keywords
# Step 2: Create a new column 'JOB_TITLE_SCORE' and assign scores based on keywords
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

# Display the DataFrame with the updated 'JOB_TITLE_SCORE' column
print(df.head())


# Step 4: Save the DataFrame to a new CSV file
output_file_path_job_titles_txt = 'job_title.txt'
# with open(output_file_path_job_titles_txt, 'w') as txt_file:
#     for job_title in unique_job_title:
#         score = job_title_scores.get(job_title, 0)  # Default score is 0 if not found in the dictionary
#         txt_file.write(f"{job_title}:{score}\n")
# with open(output_file_path_job_titles_txt, 'w') as txt_file:
#     for job_title, score in job_title_scores.items():
#         txt_file.write(f'"{job_title}":{score},\n')
        # txt_file.write(f"{job_title}:{score}\n")
# output_file_path_job_titles = 'job_titles.csv'
# unique_job_titles_df.to_csv(output_file_path_job_titles, index=False)



unique_seniority_level = df['SENIORITY_LEVEL'].unique()

print(unique_job_title)

print("Unique Values in PRIMARY_INDUSTRY:")
for industry in unique_primary_industries:
    # print(industry)
    pass

print("Unique Values in JOB_TITLE:")
# print(unique_job_title.__len__())
for job_title in unique_job_title:
    # print(job_title)
    pass

print("Unique Values in SENIORITY_LEVEL:")
for seniority_level in unique_seniority_level:
    # print(seniority_level)
    pass

# Create a dictionary to store random scores for each industry
# industry_scores = {industry: np.random.randint(1, 6) for industry in unique_primary_industries}
industry_scores = {
    'Advertising Services': 4,
    'Entertainment Providers': 3,
    'Events Services': 5,
    'Broadcast Media Production And Distribution': 2,
    'Book And Periodical Publishing': 1,
    'Public Relations And Communications Services': 5,
    'Online Audio And Video Media': 3,
    'Printing Services': 4,
    'Newspaper Publishing': 2,
    'Newspapers': 5
}

# job_title_scores = {job_title: np.random.randint(1, 6) for job_title in unique_job_title}
seniority_level_scores = {seniority_level: np.random.randint(1, 6) for seniority_level in unique_seniority_level}

# Create a new column 'INDUSTRY_SCORE' and assign scores based on 'PRIMARY_INDUSTRY'
df['INDUSTRY_SCORE'] = df['PRIMARY_INDUSTRY'].map(industry_scores)
# df['JOB_SCORE'] = df['JOB_TITLE'].map(job_title_scores)
df['SENIORITY_SCORE'] = df['SENIORITY_LEVEL'].map(seniority_level_scores)
# Display the DataFrame with the new 'INDUSTRY_SCORE' column
print(df.head())
print(df.tail())

# Save the DataFrame to CSV
output_file_path = 'job_titles.csv'
df.to_csv(output_file_path, index=False)

output_file_path_job_titles = 'job_titles.csv'
print(f"DataFrame with 'INDUSTRY_SCORE','JOB_SCORE','SENIORITY_SCORE' column saved to {output_file_path}")
