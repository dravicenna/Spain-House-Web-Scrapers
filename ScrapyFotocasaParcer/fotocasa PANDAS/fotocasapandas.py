import pandas as pd

df = pd.read_csv('Fotocasa.csv', delimiter=',')#, parse_dates=[6], nrows = nRowsRead)
print(df.head())
