import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy.types as types
import numpy as np
import datetime
import csv


def get_transfer_duration_table():
    # getting data from dssg schemma

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
    query = '''SELECT id, Transfer_boarding_datetime, exit_dateime, transfer_duration_seconds, last_trip_id, transfer_boarding_stop_id, transfer_route_taken, transfer_direction
    FROM orca2016.`od-transfer-clean`
    WHERE exit_dateime > 0 and transfer_newservice_provider= 2 and transfer_duration_seconds <= 7200 and transfer_duration_seconds > -300 and 
    last_trip_id not in ('', '0') and 
    transfer_boarding_stop_id not in ('-1', 'ERR') and 
    transfer_route_taken not in ('sounder', 'slut','link','ERR','de','cde','cd','','-1','0')
    '''  # ignore the ones fail to process the exit time and only the kcm 
    print("reading query.....")
    df = pd.read_sql(query, engine)

    print("reading completes.....cleanning now")

    ############### Combine time and date into one variable ########################
    # df.loc[np.logical_and(df['transfer_boarding_combine']-df['transfer_duration'] != df['exit_combine'],\
    # df['transfer_boarding_time'] < datetime.timedelta(hours=2))]
    

    ############ Drop the invalid rows and excess columns ###########################
    df = df.drop(df[df['transfer_duration_seconds'].isnull()].index)
    print("table is clean now")
    return df


def compute_bus_missed(df):
    # df is sorted by route 
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

    for index in df.index:
        # print( str(index) + ' is computing.. ')
        if df['transfer_route_taken'].loc[index] != rte_so_far :
            rte_so_far = df['transfer_route_taken'].loc[index]
            query = "select Route, STOPID, Direction, stop_datetime from orca2016.`ct-avl`where Route = " + str(rte_so_far)
            print('rte swtiched to '+ str(rte_so_far))
            print('reloading temp table')
            temp  = pd.read_sql(query, engine)
        if df['transfer_direction'].loc[index] != "Outbound" and df['transfer_direction'].loc[index] !=  "Inbound":
            if df['transfer_duration_seconds'].loc[index]>= 0:
                count = temp.loc[ temp['STOPID'] == df['transfer_boarding_stop_id'].loc[index]].loc[temp['Direction'] == df['transfer_direction'].loc[index]].loc[np.logical_and(df['exit_dateime'].loc[index] <= temp['stop_datetime'], temp['stop_datetime'] <= df['Transfer_boarding_datetime'].loc[index])].shape[0]
                df.set_value(index,'bus_missed', count) 
            else:
                df.set_value(index,'bus_missed', -1)  # negative df 
        else:
            df.set_value(index,'bus_missed', np.nan)


    return df



def main():
    transfer = get_transfer_duration_table()

    #initialize empty columns 
    transfer['bus_missed'] = '' 

    ##  Converting data type for analysis #########
    transfer['last_trip_id']= transfer['last_trip_id'].astype(str).astype(int)
    transfer['transfer_boarding_stop_id']=transfer['transfer_boarding_stop_id'].astype(str).astype(int)
    transfer['transfer_route_taken']= transfer['transfer_route_taken'].astype(str).astype(int)

    sorted_transfer = transfer.sort_values('transfer_route_taken')

    # mark the one row needs fixing 
   
    print('ready to compute now')
   
    result = compute_bus_missed(sorted_transfer)
    result.to_csv('ct_bus_missed.csv') 

if __name__ == "__main__":
    main()   

