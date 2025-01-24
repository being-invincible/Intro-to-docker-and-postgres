import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table = params.table
    url = params.url
    
    # download the csv
    csv_name = url.split("/")[-1]
    os.system(f"wget {url} -O {csv_name}")
    
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    # create an iterator using pandas
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    # handling date & time with pandas
    df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
    df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])

    df.head(n=0).to_sql(name=table, con=engine, if_exists='replace')

    df.to_sql(name=table, con=engine, if_exists='append')

    while True:
        try:
            t_start = time()
            df = next(df_iter)
            
            # handling date & time with pandas
            df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
            df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
            
            df.to_sql(name=table, con=engine, if_exists='append')
            t_end = time()
            print('Inserted chunk in...', t_end-t_start)
        except StopIteration:
            print("Finished ingesting data into the database")
            break
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingesting CSV data into a PostgreSQL database')

    # user, password, host, port, db name, table name
    parser.add_argument('--user', help='User name for PostgreSQL')
    parser.add_argument('--password', help='Password for PostgreSQL')
    parser.add_argument('--host', help='Host for PostgreSQL')
    parser.add_argument('--port', help='Port for PostgreSQL')
    parser.add_argument('--db', help='Database name for PostgreSQL')
    parser.add_argument('--table', help='Table name for ingesting data')
    # csv url
    parser.add_argument('--url', help='URL of the csv file')

    args = parser.parse_args()
    #print(args.accumulate(args.integers))