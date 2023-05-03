#helper script to merge the output of mutiple batch processing chunks

import os
import pandas as pd

csv1_path = os.path.join(os.path.dirname(__file__), "data_v8.csv")
csv1_data_df = pd.read_csv(csv1_path)

csv2_path = os.path.join(os.path.dirname(__file__), "merged5.csv")
csv2_data_df = pd.read_csv(csv2_path)

df_merged = pd.concat([ csv1_data_df, csv2_data_df ])

del df_merged[df_merged.columns[0]]

df_merged.to_csv("merged6.csv", index=False)