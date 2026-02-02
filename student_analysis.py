import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df=pd.read_csv(r'C:\Users\LAKSHAN S\OneDrive\Desktop\studentdata2.csv')
pd.set_option('display.max_columns', None)
#whatpd.set_option('display.max_rows', None)
print(df.head())
print(df.columns)
df.loc[[5,10,25,40],"G2"]=np.nan
df.loc[[12,60,5],"absences"]=np.nan
df.loc[20,"studytime"]=np.nan
print(df.isnull().sum())
print(df.isnull().sum().sum())
df['G2']=df['G2'].fillna(df["G2"].mean())
df['absences']=df['absences'].fillna(df['absences'].median())
df['studytime']=df['studytime'].fillna(df['studytime'].mean())
print(df.isnull().sum())
print(df.isnull().sum().sum())
def performance_level(score):
    if score>=15:
        return 'High'
    elif score>=10:
        return 'Average'
    else:
        return 'Low'
df['performance_level']=df['G3'].apply(performance_level)

def improvement_progress(g1,g3):
    if g3>g1:
        return "Improved"
    elif g3==g1:
        return "Same"
    else:
        return "Declined"
#df['Improvement_level']=df.apply(lambda row: improvement_progress(row['G1'],row['G3']),axis=1)
df['Improvement_level']=[improvement_progress(g1,g3) for g1,g3 in zip(df['G1'],df['G3'])]

def attendance(value):
    if value>15:
        return "High Risk"
    elif value>10:
        return "Medium Risk"
    else:
        return "Low Risk"
df["Attendance_Risk"]=df['absences'].apply(attendance)

def study_time(value):
    if value>=3:
        return 'Good'
    elif value>=2:
        return 'Moderate'
    else:
        return 'Bad'

df['study_time_check']=df['studytime'].apply(study_time)


average_class=df['G3'].mean()
print("The overall average of the class is ",average_class)

count_of_students=df['performance_level'].value_counts()
print("Number of performance in each category : ",count_of_students)

good_grad_low_abs=df[(df['absences']<=10)&(df['G3']>=15)].shape[0]
low_grad_high_abs=df[(df['absences']>10)&(df['G3']<10)].shape[0]
print(
    f"Students with low absences and high grades (G3 ≥ 15): {good_grad_low_abs}\n"
    f"Students with high absences and low grades (G3 < 10): {low_grad_high_abs}\n"
    f"This indicates that regular attendance is associated with better academic performance."
)

print("Improvement trend of students:")
print(df['Improvement_level'].value_counts())


high_perf_pct = (
    df[df["performance_level"] == "High"]
    .groupby("Attendance_Risk")
    .size()
    / df.groupby("Attendance_Risk").size()
) * 100

print("Percentage of High Performers by Attendance Risk:")
print(high_perf_pct)

high_perf_pct.plot(kind="bar")
plt.xlabel("Attendance Risk Level")
plt.ylabel("Percentage of High Performers (%)")
plt.title("Impact of Attendance on High Academic Performance")
plt.tight_layout()
plt.show()
