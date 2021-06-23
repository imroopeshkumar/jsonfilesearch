import json
import pandas as pd

df = pd.read_json('organizations.json')
print(df.columns.values)