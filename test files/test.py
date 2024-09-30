import tkinter as tk
from tkinter import ttk
import pandas as pd

root = tk.Tk()

sample = {"File Name":[f"file_{i}" for i in range(10)],
          'Sheet Name': [f"sheet_{i}" for i in range(10)],
          'Number Of Rows': [f"row_{i}" for i in range(10)],
          'Number Of Columns': [f"col_{i}" for i in range(10)]
          }
df = pd.DataFrame(sample)
print(df)
cols = list(df.columns)

tree = ttk.Treeview(root)
tree.pack()
tree["columns"] = cols
for i in cols:
    tree.column(i, anchor="w")
    tree.heading(i, text=i, anchor='w')

for index, row in df.iterrows():
    tree.insert("",tk.END,text=index,values=list(row))
print(df)
root.mainloop()