import pandas as pd


clean_data=pd.read_csv("data\\clean_data_v1.csv")
clean_data['Date']=pd.to_datetime(clean_data['Date'])


# Total number of unique data
count_total_data=clean_data.value_counts('Symbol')

# Maximum Closing Value
max_close_per_symbol = clean_data.groupby('Symbol')['Close'].max().reset_index()

# Minimum Closing Value
min_close_per_symbol = clean_data.groupby('Symbol')['Close'].min().reset_index()


#Last available data in date
last_available_date = clean_data.groupby('Symbol')['Date'].min().reset_index()

# Most current date in date
current_available_date = clean_data.groupby('Symbol')['Date'].max().reset_index()


# Merging can only be done one at a time
# First merge: count with max close
merged_data = pd.merge(count_total_data, max_close_per_symbol, on='Symbol')

# Second merge: add min close
merged_data = pd.merge(merged_data, min_close_per_symbol, on='Symbol')

# Add the last available date
merged_data = pd.merge(merged_data,last_available_date, on='Symbol')

merged_data=merged_data.rename(columns={'Date':'Oldest Date'})
# Add the most current available date
merged_data = pd.merge(merged_data,current_available_date, on='Symbol')


# data_above_600=merged_data[merged_data['count']>1000]
merged_data = merged_data.rename(columns={'Close_x': 'Max Close value'
                                          ,'count':'Count',
                                          'Close_y':'Min Close value',
                                          'Date':'Recent Date'
                                          },)

print(merged_data)


checkDate=pd.Timestamp('2021-1-1')


print("Symbols Currently existing")

recent_data=merged_data[merged_data["Recent Date"]>pd.Timestamp('2025-01-01')]
print(recent_data[['Symbol','Recent Date']].sort_values(by='Recent Date',ascending=False))

recent_data.to_csv("data/recent_data_v2.csv")

# print("Symbols older than 2021")
# print(merged_data[merged_data['Date']<checkDate])

# Counting data greater than 600
# print(merged_data[merged_data['Count']<600])

