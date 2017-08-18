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
    WHERE exit_time > 0 and transfer_newservice_provider= 4 and
    last_trip_id not in ('', '0') and 
    transfer_boarding_stop_id not in ('-1', 'ERR') and 
    transfer_route_taken not in ('sounder', 'slut','link','ERR','de','cde','cd','','-1','0')
    '''  # ignore the ones fail to process the exit time and only the kcm 
    print("reading query.....")
    df = pd.read_sql(query, engine)

    print("reading completes.....cleanning now")
    ############### Combine time and date into one variable ########################
    df['transfer_boarding_date'] = pd.to_datetime(df.transfer_boarding_date)
    df['transfer_boarding_combine'] = df.transfer_boarding_date + df.transfer_boarding_time
    df['exit_time_timedelta'] = pd.to_timedelta(df.exit_time)
    df['exit_combine'] = df.transfer_boarding_date + df.exit_time_timedelta

    df.ix[df['transfer_boarding_combine']-df['transfer_duration'] != df['exit_combine'], 'exit_combine'] -=datetime.timedelta(days=1)
    df.ix[np.logical_or(df['transfer_duration']> datetime.timedelta(seconds=7200), df['transfer_duration']<= datetime.timedelta(seconds= -300)),'transfer_duration'] = np.nan 
    
    # df.loc[np.logical_and(df['transfer_boarding_combine']-df['transfer_duration'] != df['exit_combine'],\
    # df['transfer_boarding_time'] < datetime.timedelta(hours=2))]
    

    ############ Drop the invalid rows and excess columns ###########################
    df = df.drop(df[df['transfer_duration'].isnull()].index)
    df.drop(['exit_time','transfer_boarding_date','exit_time_timedelta','transfer_boarding_time'],inplace=True,axis=1,errors='ignore')
    print("table is clean now")
    return df


transfer = get_transfer_duration_table()
##  Converting data type for analysis #########
'''
print("getting rid of weird data")
transfer = transfer.loc[np.logical_not(transfer['last_trip_id'].isin(['0','']))]
transfer = transfer.loc[np.logical_not(transfer['transfer_boarding_stop_id'].isin(['-1','','ERR']))]
transfer = transfer.loc[np.logical_not(transfer['transfer_route_taken'].isin(['sounder', 'slut','link','ERR','de','cde','cd','','-1','0']))]
''' 
transfer['last_trip_id']= transfer['last_trip_id'].astype(str).astype(int)
transfer['transfer_boarding_stop_id']=transfer['transfer_boarding_stop_id'].astype(str).astype(int)
transfer['transfer_route_taken']= transfer['transfer_route_taken'].astype(str).astype(int)

transfer['bus_missed'] = '' #initialize an empty column '''
sorted_transfer = transfer.sort_values('transfer_route_taken')
print('ready to compute now')


def compute_bus_missed(sorted_transfer):
    # sorted_transfer is sorted by route 
    db_info = {
        'host': '',
        'user': '',
        'password': '',
        'port': ,
        'dbname': ''
    }
    sql_str = 'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}'.format
    engine = create_engine(sql_str(**db_info))

    rte_so_far = -1   # initialize the for loop

    for index in sorted_transfer.index[0:100]:
        # print( str(index) + ' is computing.. ')
        if sorted_transfer['transfer_route_taken'].loc[index] != rte_so_far :
            rte_so_far = sorted_transfer['transfer_route_taken'].loc[index]
            query = "SELECT RTE, STOP_ID, stop_datetime from `kcm-avl`where RTE = " + str(rte_so_far)
            print('rte swtiched to '+ str(rte_so_far))
            print('reloading temp table')
            temp  = pd.read_sql(query, engine)
            
        if sorted_transfer['transfer_duration'].loc[index]>= datetime.timedelta(seconds=0):
            count = temp.loc[ temp['STOP_ID'] == sorted_transfer['transfer_boarding_stop_id'].loc[index]].loc[np.logical_and(sorted_transfer['exit_combine'].loc[index] <= temp['stop_datetime'], temp['stop_datetime'] <= sorted_transfer['transfer_boarding_combine'].loc[index])].shape[0]
            sorted_transfer.set_value(index,'bus_missed', count) 
        else:
            sorted_transfer.set_value(index,'bus_missed', -1)  # negative sorted_transfer     

    return sorted_transfer

sorted_transfer = compute_bus_missed(sorted_transfer)
sorted_transfer.to_csv('~/Desktop/kcm_transfer.csv') 
