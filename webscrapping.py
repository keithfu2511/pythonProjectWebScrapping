import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import requests
from dotenv import find_dotenv, load_dotenv

from fredapi import Fred
fred = Fred(api_key='TYPE_API_KEY_HERE')
FED_RATE = fred.get_series('DFF',observation_start='1954-07-01', observation_end='2023-05-01')

import nasdaqdatalink
#loading the env file that contains api key
_ = load_dotenv(find_dotenv())
SP500_data = nasdaqdatalink.get('MULTPL/SP500_REAL_PRICE_MONTH', start_date="1954-07-01", end_date="2023-05-01")

#Check the the information to make sure the datatypes are correct
print(FED_RATE.info(), SP500_data.info())

#Pre-processing to merge the data, then drop the repeating column
#then set date as index and rename the columns to meaningful names
df1 = FED_RATE.to_frame() #first convert the Series to a DataFrame (with a single column) and then merge
final_df = df1.merge(SP500_data, right_on='Date', left_index=True, how='inner')
final_df.columns = ['FED_RATE', 'SP500']
final_df = final_df.reset_index().rename(columns={'index': 'Date'})
final_df = final_df.set_index('Date')
final_df.head()
print(final_df.head())

# Plot the data to visualise if there are any patters
plt.plot(final_df.index, final_df['FED_RATE'], label='Fed fund', c='r')
ax = plt.gca()
ax2 = ax.twinx()
ax2.plot(final_df.index, np.log(final_df['SP500']), label='SP500', c='g')
ax.legend()
ax2.legend()
plt.show()

# Finding the correlation to analyze the relatioinship between SP500 and Fed Interest Rate
corr = final_df.corr()
sns.heatmap(corr, annot=True)
plt.show()
