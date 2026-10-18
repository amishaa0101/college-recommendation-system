import pandas as pd
# Load current year's and previous year's data
current_data = pd.read_csv('newcolleges2.csv')
previous_data = pd.read_csv('cleaned_acpc.csv')

# Merge the data on College Name and Program Name
merged_data = pd.merge(current_data, previous_data, on=['College Name', 'Program Name'], suffixes=('_current', '_previous'))

# Calculate change in Open Rank
merged_data['Open Rank_change'] = merged_data['Open Rank_current'] - merged_data['Open Rank_previous']

# Calculate percentage change
merged_data['Percentage_change'] = (merged_data['Open Rank_change'] / merged_data['Open Rank_previous']) * 100
