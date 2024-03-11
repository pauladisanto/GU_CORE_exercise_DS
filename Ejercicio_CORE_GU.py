#python3 Ejercicio_CORE_GU.py


'''Task: Write a script that can be run automatically each time such a quality file is generated, and look
at how many samples from each origin fail the set quality cut-off (< 95 % covered bases of the
reference genome or ‘FALSE’ in column 6).'''

import pandas as pd

# Read the CSV file into a DataFrame and store it as df
df = pd.read_csv('samples.txt')

# Display the DataFrame  (looks OK)
#print(df)

# Function to extract the origin from the sample name (this is the second letter of the samples in the column name)
def extract_origin(sample_name):
    return sample_name[1]

# Apply the function to create a new column called origin 
df['origin'] = df['sample'].apply(extract_origin)

#print the new column (looks OK)
#print(df['origin'])

# Filter the DataFrame based on the criteria and count samples from each origin that fail

failed_samples = df[(df['pct_covered_bases'] < 95) | (df['qc_pass'] == False)]
failed_counts = failed_samples['origin'].value_counts()

# Display the counts of failed samples from each origin
print("Failed samples counts by origin:")
print(failed_counts)

'''The first part is finished '''


'''As this script should run automatically once a week, the script should also serve as a warning system,
sending warnings if there are certain origins producing more than 10% failed samples. Therefore, you
need to implement a system that notifies its user in some way, telling them the latest results.'''

# Calculate total samples for each origin (all the samples)
total_samples = df['origin'].value_counts()

#print(total_samples) #it is OK since the sum is the same number as the original Dataframe

# Calculate the percentage of failed samples for each origin
failed_percentage = (failed_counts / total_samples) * 100

# Display the percentage of failed samples for each origin
print("Percentage of failed samples by origin:")
print(failed_percentage)

# Check if any origin exceeds the 10% threshold and trigger a notification when the value is higher than 10 (threshold)
threshold = 10
high_failure_origins = failed_percentage[failed_percentage > threshold]
if not high_failure_origins.empty:
    print("\nWarning: The following origins have more than 10% failed samples:")
    for origin, percentage in high_failure_origins.items():
        print(f"Origin {origin}: {percentage:.2f}% failed samples")
    # Trigger notification 
else:
    print("\nNo origins have more than 10% failed samples.")

    