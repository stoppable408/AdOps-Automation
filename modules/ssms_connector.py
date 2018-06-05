#!/usr/bin/python
import pyodbc
import pandas as pd

class SSMSConnector(object):

    def __init__(self):
        self.connection = "Driver={SQL SERVER};SERVER=EMDC2SQM102\DB102;DATABASE=GM;UID=gmapp_user;PWD=woodward01"
        self.connect_to_database(self.connection)

    def connect_to_database(self,connection):
        # print the connection string we will use to connect
        print ("Connecting to database: GM")
        for x in connection.split(';'):
            print ('\n   {0}  ->  {1}'.format(x.split('=')[0],x.split('=')[1]))

    	# get a connection, if a connect cannot be made an exception will be raised here
        self.conn = pyodbc.connect(connection)

    	# conn.cursor will return a cursor object, you can use this cursor to perform queries
        self.cursor = self.conn.cursor()
        print ("\nConnected!\n")

    def to_df(self,query):
        return pd.read_sql(query,self.conn)

    def runQuery(self, query):
        self.cursor.execute(query)
        self.conn.commit()

if __name__ == "__main__":
    ssms = SSMSConnector()
    query = "SELECT * FROM [vendors].[Chevy_LMA_New_Placements_Distribution_Table]"
    df = ssms.query_to_df(query)
