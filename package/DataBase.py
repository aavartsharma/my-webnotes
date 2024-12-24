import sqlite3
import package as pk

# class Notes(pk.db.Model):
#     serialNumber = pk.db.Column(pk.db.Integer, primary_key = True)
#     name = pk.db.Column(pk.db.String(200), nullable= False)
#     typeOf = pk.db.Column(pk.db.String(200), nullable = False)
#     timeCreated = pk.db.Column(pk.db.String(20), nullable = False)
#     jsonFile = pk.db.Column(pk.db.JSON, nullable=False) 

#     def __repr__(self):
#         return f"{self.name} is in {self.typeof} also {self.nu}"

class DataBaseEntry():
    def __init__(self,entry: tuple):
        self.number = entry[0]
        self.serialNumber = entry[1]
        self.name = entry[2]
        self.typeOf = entry[3]
        self.timeCreated = entry[4]
        self.jsonString = entry[5]
        self.values = entry

    def __iter__(self):
        # Allow the object to be converted into an iterable
        return iter(self.values)

def ReadFromDataBase(database,tableName):
    with sqlite3.connect(database) as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM {tableName}')
        rows = cur.fetchall()
    return rows

def AddDatabaseEntry(dataBase,tableName,newNote: tuple):
    # insert table statement
    sql = f''' INSERT INTO {tableName}(serialNumber,name,typeOf,timeCreated,jsonString)
              VALUES(?,?,?,?,?) '''
    with sqlite3.connect(dataBase) as conn:
        # Create  a cursor
        cur = conn.cursor()

        # execute the INSERT statement
        cur.execute(sql, newNote)

        # commit the changes
        conn.commit()
    #print(ReadFromDataBase(dataBase,tableName))
    # get the id of the last inserted row
    return cur.lastrowid

def InzliteDataBase():
    try:
        sql_statements = [ 
            f"""CREATE TABLE IF NOT EXISTS {pk.noteTableName} (
                    id INTEGER PRIMARY KEY, 
                    serialNumber TEXT NOT NULL,
                    name TEXT NOT NULL,
                    typeOf TEXT NOT NULL,
                    timeCreated TEXT NOT NULL,
                    jsonString TEXT NOT NULL
                );"""
        ]
        with sqlite3.connect(pk.databaseName) as conn:
            # create a cursor
            cursor = conn.cursor()
            # execute statements
            for statement in sql_statements:
                cursor.execute(statement)
            # commit the changes
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Failed to create tables:", e)