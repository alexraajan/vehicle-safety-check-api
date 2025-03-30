import pyodbc

class DatabaseContext:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def get_connection(self):
        return pyodbc.connect(self.connection_string)