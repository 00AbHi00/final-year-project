#Cleaning the dataset:
import pandas as pd
#----------------------------#
#                            #
#                            #
#   Data cleaning stage 1    #
#                            #
#                            #
#----------------------------#


# Cleaning stage 1:
# Read the original csv data_nepse_csv
# Remove duplicated rows based on PK (PK= date+ symbol) 
# Drop the sector (since there are no values present)
# Remove empty cell if any
# Use pandas.Dataframe.to_csv for writing the cleaned data after stage 1 
# Overall description of data after cleaning stage 1:



df = pd.read_csv('data\\data_nepse_csv2.csv')
# print(df.head(5)["PK"])
# Lambda to get duplicated rows based on 'PK' column
duplicated_values = lambda x: x[x['PK'].duplicated(keep=False)]
# Get duplicated rows
result = duplicated_values(df)
# print("Duplicated rows:\n", result)
# Drop them from the DataFrame
clean_data = df.drop(result.index)
# Check again for duplicates after dropping, testing
result = duplicated_values(clean_data)
print("Remaining duplicates:\n", result)

clean_data=clean_data.drop(columns='Sector')

clean_data.to_csv("data\\clean_data_v1.csv")
print(clean_data.tail(3))



# Final DataFrame
# print(clean_data.describe())
print(len(clean_data['Symbol'].unique()))
df['Date'] = pd.to_datetime(df['Date'])
print(df['Date'].min())
print(df['Date'].max())


