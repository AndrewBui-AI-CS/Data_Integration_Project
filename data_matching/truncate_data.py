import pandas as pd

df = pd.read_csv(r'data/car.csv')
remove_fields = ['_id', 'fuel_consumption', 'km', 'time_update', 'image']
df_truncate = df.drop(remove_fields, 1)
df_truncate.to_csv('data/truncated_data.csv', index=False)
