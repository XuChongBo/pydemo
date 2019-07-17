import pandas as pd

frame = pd.DataFrame({
        'onething':[1,2,3,4],
        'otherthing':[0.1,0.2,1,2],
        'secondthing':['a','e','i','o']}, index=[10, 11, 12, 13], columns=['onething', 'secondthing', 'otherthing'])

print(frame)
print(frame.itertuples)
columnsTitles = ['onething', 'secondthing', 'otherthing']

frame = frame.reindex(columns=columnsTitles)
print(frame)
rows = frame.itertuples()

for r in rows:
    print(r[0], r[1], r[2])
