#Import necessary libraries
from flask import Flask, render_template, Response
import cv2
import json
import sqlite3
from data.TEST import TestCase
#Initialize the Flask app
app = Flask(__name__)



camera = cv2.VideoCapture('Val.mp4')


@app.route("/")
def hello_world():
    a = TestCase(camera)
    Data_Base(a.output_data())
    z = GetCoordinates(d=1)
    return render_template('index.html',result = z)

def Data_Base(traffic):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute('Create Table if not exists Coordinates (point Integer, x Integer, y Integer)')
    for row in traffic:
        # print(traffic[row])
        keys= (row,traffic[row][0],traffic[row][1])
        # print(keys)
        cursor.execute('insert into Coordinates values(?,?,?)',keys)
        print(f'{traffic[row]} data inserted Succefully')
    connection.commit()
    connection.close()

def GetCoordinates(d=0):
    conn = sqlite3.connect('data.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Retrieving data
    cursor.execute('''SELECT * from Coordinates''')

    result = cursor.fetchall()
    # print(result)
    if d !=0:
        cursor.execute('''DROP TABLE Coordinates''')
    #Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()
    return result





if __name__ == "__main__":
    app.run(debug=True)