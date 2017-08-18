
# get frequency and the distribution time between offboard and onboard 
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy.types as types
import numpy as np
import datetime

def get_transfer_duration_table():

    db_info = {
        'host': '',
        'user': '',
        'password': '',
        'port': ,
        'dbname': ''
    }
    
    sql_str = 'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}'.format 
    engine = create_engine(sql_str(**db_info))
    ## enter you sql query in the multi-line command #####
    ## For this code runs, please at least select the variables below from od-transfer
    ## transfer_boarding_time, transfer_boarding_date, exit_time, transfer_duration 
    query = '''SELECT id, transfer_boarding_time, transfer_boarding_date, exit_time, transfer_duration, last_trip_id, transfer_boarding_stop_id, transfer_route_taken
    FROM `od-transfer`
    WHERE exit_time > 0 and
    exit_stop_id  not in ('N/A', '') and 
    transfer_boarding_stop_id not in ('-1', 'ERR', '') and 
    transfer_route_taken not in ('ERR','de','cde','cd','','-1','0')
    '''  # ignore the ones fail to process the exit time and only the kcm 
    print("reading query.....")
    df = pd.read_sql(query, engine)

    print("reading completes.....cleanning now")
    ############### Combine time and date into one variable ########################
    df['transfer_boarding_date'] = pd.to_datetime(df.transfer_boarding_date)
    df['transfer_boarding_combine'] = df.transfer_boarding_date + df.transfer_boarding_time
    df['exit_time_timedelta'] = pd.to_timedelta(df.exit_time)
    df['exit_combine'] = df.transfer_boarding_date + df.exit_time_timedelta

    df.ix[df['transfer_boarding_combine']-df['transfer_duration'] != df['exit_combine'], 'exit_combine'] -= datetime.timedelta(days=1)
    df.ix[np.logical_or(df['transfer_duration']> datetime.timedelta(seconds=7200), df['transfer_duration']<= datetime.timedelta(seconds= -300)),'transfer_duration'] = np.nan 
    
    # df.loc[np.logical_and(df['transfer_boarding_combine']-df['transfer_duration'] != df['exit_combine'],\
    # df['transfer_boarding_time'] < datetime.timedelta(hours=2))]
    

    ############ Drop the invalid rows and excess columns ###########################
    df = df.drop(df[df['transfer_duration'].isnull()].index)
    df.drop(['exit_time','transfer_boarding_date','exit_time_timedelta','transfer_boarding_time'],inplace=True,axis=1,errors='ignore')
    print("table is clean now")
    return df

transfer = get_transfer_duration_table()





# debugging: 
# transfer.loc[ transfer['exit_combine'].dt.date != transfer['transfer_boarding_combine'].dt.date]

''''
print("fixing the data types")

transfer['last_trip_id']= transfer['last_trip_id'].astype(str)
transfer['transfer_boarding_stop_id']=transfer['transfer_boarding_stop_id'].astype(str)
transfer['transfer_route_taken']= transfer['transfer_route_taken'].astype(str)
'''