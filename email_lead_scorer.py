# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score

# # Load your CSV file into a pandas DataFrame
# df = pd.read_csv('output_list_database/final_list.csv')

# # Assuming 'email' is the column containing email addresses
# email_column = 'email'

# # Make the email column unique
# df[email_column] = df[email_column].astype(str)
# df[email_column] = df.groupby(email_column).cumcount().astype(str) + '_' + df[email_column]

# # Create a dictionary to store scores for each unique email
# email_scores = {}

# # Assign scores based on other columns (customize this based on your requirements)
# for index, row in df.iterrows():
#     score = 0
    
#     # Example: If 'column1' has a certain value, add to the score
#     if row['column1'] == 'some_value':
#         score += 1
    
#     # You can add more conditions based on other columns
    
#     # Store the score in the dictionary
#     email_scores[row[email_column]] = score

# # Now, you can use the email_scores dictionary for predictions

# # Example: Split the data into training and testing sets
# train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)

# # Example: Train a simple RandomForestClassifier
# X_train = train_data[['column1', 'column2', 'column3']]  # Add columns you want to use for prediction
# y_train = train_data[email_column]

# X_test = test_data[['column1', 'column2', 'column3']]  # Add columns you want to use for prediction
# y_test = test_data[email_column]

# clf = RandomForestClassifier()
# clf.fit(X_train, y_train)

# # Make predictions
# predictions = clf.predict(X_test)

# # Evaluate the accuracy (you can use other metrics as well)
# accuracy = accuracy_score(y_test, predictions)
# print(f'Accuracy: {accuracy}')

import pandas as pd

# Step 1: Read the CSV file
file_path = 'other/raw.csv'
df = pd.read_csv(file_path)

# Convert column names to uppercase
df.columns = [col.upper() for col in df.columns]

# Step 2: Create dictionaries for unique values in each column
score_dict = {
    'PRIMARY_INDUSTRY': {},
    'SENIORITY_LEVEL': {},
    'JOB_TITLE': {},
    'DEPARTMENT': {},
    'COMPANY_REVENUE': {},
    'COMPANY_EMPLOYEE_COUNT': {},
    # ... (add other columns as needed)
}

# Step 3: Assign scores to each unique value in the dictionaries
for col in score_dict.keys():
    unique_values = df[col].unique()
    for i, value in enumerate(unique_values):
        score_dict[col][value] = i + 1  # You can customize the scoring logic

# Step 4: Replace original values with scores in the DataFrame
df.replace(score_dict, inplace=True)

# Now, df contains scores instead of original values for each column.

# Step 5: Use the scored DataFrame for prediction or analysis
# For example, if you want to predict using a machine learning model, you can do something like this:
# X = df.drop(columns=['TARGET_COLUMN'])
# y = df['TARGET_COLUMN']
# ... (train your model using X and y)
