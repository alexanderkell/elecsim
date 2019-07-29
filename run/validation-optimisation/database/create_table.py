"""
File name: create_table
Date created: 29/07/2019
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

import mysql.connector
from mysql.connector import errorcode

# Obtain connection string information from the portal
config = {
  'host':'elecsimresults.mysql.database.azure.com',
  'user':'alexkell@elecsimresults',
  'password':'b3rz0s4m4dr1dth3h01113s!',
  'database':'elecsim',
  'ssl_ca':'/Users/b1017579/Downloads/BaltimoreCyberTrustRoot.crt.pem'
}


try:
    conn = mysql.connector.connect(**config)
    print("Connection established")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = conn.cursor()


    # Insert some data into table
    cursor.execute("INSERT INTO validoptimresults (run_number, reward, individual_m, individual_c) VALUES ({},{},{},{})".format(1, 1.1, 1.2, 1.3))
    print("Inserted", cursor.rowcount, "row(s) of data.")
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")
