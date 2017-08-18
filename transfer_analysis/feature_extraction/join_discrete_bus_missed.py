import csv
import pandas as pd
import numpy as np

def get_dict():
    with open('/Users/Wenonah/Desktop/DSSG/data/clean_bus_missed_result.csv', mode='r') as infile:
        reader = csv.reader(infile, delimiter = ',')
        mydict = {rows[1]:rows[2] for rows in reader} 
        with open( '/Users/Wenonah/Desktop/DSSG/data/ct_result.csv', mode='r') as infile:
            reader = csv.reader(infile, delimiter = ',')
            mydict.update(mydict = {rows[1]:rows[9] for rows in reader}) 
            with open( '/Users/Wenonah/Desktop/DSSG/data/pt_result.csv', mode='r') as infile:
                reader = csv.reader(infile, delimiter = ',')
                mydict.update(mydict = {rows[1]:rows[9] for rows in reader}) 
                
                return mydict

print("reading dictionary" )
    
bus_misseed_dict = {}

try:
    bus_misseed_dict = get_dict()
except:
    print("fail to read dictionary" )

# len(bus_misseed_dict) # 2477776

df = pd.read_csv('/Users/Wenonah/Desktop/od_transfer_updated_walk.csv', delimiter = ',')
df['bus_missed'] = -2

# df.dtypes

for index, row in df.iterrows():
        value = bus_misseed_dict.get(str(int(df.at[index, 'ID'])))
        if value != None:
            df.set_value(index, 'bus_missed', int(value))



# 523762 
df['bus_missed'].head(20)
df.loc[df['bus_missed'].notnull()]['bus_missed'].count()
df.loc[df['bus_missed'].notnull()]['bus_missed'.max()
df.loc[df['bus_missed'] == -2 ]['bus_missed'].count()
df.loc[df['bus_missed'] != -2 ]['bus_missed'].count()
df.loc[df['bus_missed'].map(np.isnan)]['bus_missed'].count()



df.to_csv('result.csv', index=True)
