# python code to do database queries for astronaut photos

# LRMayer 10/13/2016

import pyodbc
import sys
import logging
import re  # for using regular expressions


def getMissionRowFrame(imageName):
    # --------------------------------------------
    # get mission, roll, frame from the imageName
    # --------------------------------------------

    # Find the mission name, starting w/ ISS - will have to change this for other missions****

    # regular expression search for misssion, roll, frame
    searchObj = re.search(r'ISS(\d+)-(\w)-(\d+).jpg',imageName)
    if searchObj :
        mission = 'ISS' + searchObj.group(1)
        roll = searchObj.group(2)
        frame = searchObj.group(3)

    logging.debug("mission, roll, frame = %s %s %s", mission, roll, frame)


    # # frame is before last . and after last "-"
    # frame = imageName[imageName.rfind("-") + 1:imageName.rfind(".")]
    # get length of frame, add spaces to front, NECESSARY FOR QUERYING THE DATABASE!!!!
    frame = " " * (7 - len(frame)) + frame

    return (mission, roll, frame)





class PHOTOSDB:

    # open a connection to the Photos database and get a cursor
    def __init__(self):
        # The SQL server is EO-Web, the DSN name is Photos

        # Connection example: with a DSN
        cnxn = pyodbc.connect('DSN=Photos')  #

        # Opening a cursor
        self.cursor = cnxn.cursor()


    def getField(self, field, imageName) :

        # --------------------------------------------
        # get mission, roll, frame from the imageName
        # --------------------------------------------
        mission, roll, frame = getMissionRowFrame(imageName)

        table = "frames" # cataloged

        # All SQL statements are executed using Cursor.execute. If the statement returns rows,
        # such as a select statement, you can retrieve them using the Cursor fetch functions
        # (fetchone, fetchall, fetchmany).

        # Cursor.fetchone is used to return a single Row.
        #                                                                            '123456789'  - spaces at beginning needed
        # the sql query
        query = "SELECT " + field + " FROM " + table + " WHERE mission='" + mission + "' AND roll='" + roll + "' AND frame='" + frame + "'"

        self.cursor.execute(query)
        value = self.cursor.fetchone()

        if not value:  # was not found in frames table, check uncataloged table

            if (field == 'fclt') :
                table = "camera"  # uncataloged

            elif (field == 'elev'):
                table = "nadir"  # cataloged

        logging.debug("Getting %s from %s table", field, table)

        # Set up the database query
        query = "SELECT " + field + " FROM " + table + " WHERE mission='" + mission + "' AND roll='" + roll + "' AND frame='" + frame + "'"

        logging.debug("getField query: %s",query)

        self.cursor.execute(query)
        value = self.cursor.fetchone()

        if not value:
            return None

        logging.debug("getLength : field = %s", value)
        return value[0]


    # Get all the info about imageName
    def getAll(self, imageName):

        setLen = 7 # the length that frame needs to be

        # --------------------------------------------
        # get mission, roll, frame from the imageName
        # --------------------------------------------
        mission, roll, frame = getMissionRowFrame(imageName)
        # mission = info[0]
        # roll = info[1]
        # frame = info[2]

        logging.debug("mission, roll, frame : %s %s %s%s%s", mission, roll, "*", frame, "*")

        table = "frames" # cataloged

        # All SQL statements are executed using Cursor.execute. If the statement returns rows,
        # such as a select statement, you can retrieve them using the Cursor fetch functions
        # (fetchone, fetchall, fetchmany).

        # the sql query
        query = "SELECT * FROM " + table + " WHERE mission='" + mission + "' AND roll='" + roll + "' AND frame='" + frame + "'"


        self.cursor.execute(query)
        row = self.cursor.fetchone()

        if not row :  # was not found in frames table, check uncataloged table

            table = "camera"  # uncataloged
            logging.debug("Getting info from %s table", table)
            #query = "SELECT * FROM " + table + " WHERE mission='" + mission + "' AND roll='E' AND frame='  26493'"
            query = "SELECT * FROM " + table + " WHERE mission='" + mission + "' AND roll='" + roll + "' AND frame='" + frame + "'"
            self.cursor.execute(query)
            row = self.cursor.fetchone()

        return row


    """Get a list of photo frames since the input frame for the mission, roll, and
    with sun elevation > minElev"""
    def list_frames_since(self, table, mission, roll, lastFrame, elev):
        query = "SELECT FRAME FROM " + table + " WHERE mission='" + mission + "' AND roll='" + roll + "' AND frame>'" + lastFrame + \
                 "' AND ELEV<'" + str(elev) + "'"

        #query = "SELECT FRAME FROM " + table + " WHERE mission='" + mission + "' AND roll='" + roll + "' AND frame>'" + lastFrame + "'"

        logging.debug("query = %s", query)

        self.cursor.execute(query)
        #row = self.cursor.fetchone()  # fetches 1 row
        row = self.cursor.fetchall()   # fetches all rows

        return row


