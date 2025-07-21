import pandas as pd

data = {
    'Hours_Studied': [2, 5, 1, 10, 7, 3, 4, 12],
    'Attendance_%': [70, 90, 60, 100, 95, 65, 80, 100],
    'Asked_for_Help': [0, 1, 0, 1, 1, 0, 1, 1],
    'Passed': [0, 1, 0, 1, 1, 0, 1, 1]
}

df = pd.DataFrame(data)
print(df)