import json
import pandas as pd

df = pd.read_json('organizations.json')
# print(df.columns.values)
# print(df.head)


x =(df[df._id == 101].values.tolist())
print(x)