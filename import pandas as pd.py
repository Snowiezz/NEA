import pandas as pd

data = {
    'Hours_Studied': [2, 5, 1, 10, 7, 3, 4, 12],
    'Attendance_%': [70, 90, 60, 100, 95, 65, 80, 100],
    'Asked_for_Help': [0, 1, 0, 1, 1, 0, 1, 1],
    'Passed': [0, 1, 0, 1, 1, 0, 1, 1]
}

df = pd.DataFrame(data)
print(df)
print(df.describe())
print(df.corr())
import matplotlib.pyplot as plt
plt.scatter(df['Hours_Studied'], df['Attendance_%'], c=df['Passed'])
plt.xlabel('Hours Studied')
plt.ylabel('Attendance %')
plt.title('Pass/Fail by Study Time & Attendance')
plt.show()