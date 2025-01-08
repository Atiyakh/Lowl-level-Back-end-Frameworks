import sqlite3 as sql
import datetime, os

class __NULL: val = None
NULL = __NULL()
class __CASCADE: val = "CASCADE"
CASCADE = __CASCADE()
class __NO_ACTION: val = "NO ACTION"
NO_ACTION = __NO_ACTION()
class __STRICT: val = "STRICT"
STRICT = __STRICT()
class __DEFAULT_VALUE: val = "DEFAULT"
DEFAULT_VALUE = __DEFAULT_VALUE()
class SET:
    def __init__(self, value):
        self.val = f"SET {value}"
 
database_path = dirs = os.path.join(os.getcwd(), 'WebApplication\\MiddleWare\\Database')

class CharField:
    def __init__(self, max_length:int=250, choices:list=None, allow_null:bool=False, primary_key:bool=False, default=None, unique:bool=False):
        if(not isinstance(max_length,int))or(50_000_000<max_length)or(max_length<1):
            raise ValueError(
                "[WebSock] max_length should be an integer between (1-50,000,000)."
            )
        else: self.max_length = max_length
        if choices:
            if isinstance(choices, dict):
                if len(choices) < 2:
                    raise ValueError(
                        "[WebSock] The dictionary of choices the choices should contain at least two values."
                    )
                else:
                    for val in choices:
                        if not isinstance(val, str):
                            raise ValueError(
                                "[WebSock] The keys of the choices dictionary should be string values."
                            )
                        self.choices = choices
            else: raise ValueError(
                "[WebSock] The choices argument should be a dictionary"
            )
        else:
            self.choices = None
        if allow_null in [True, 1]:
            self.allow_null = True
        else:
            self.allow_null = False
        if primary_key in [True, 1]:
            self.primary_key = True
        else:
            self.primary_key = False
        if unique in [True, 1]:
            self.unique = True
        else:
            self.unique = False
        if default != None:
            self.default = default.__str__()
        else:
            self.default = None

class IntegerField:
    def __init__(self, allow_null:bool=False, primary_key:bool=False, default=None, unique:bool=False):
        if allow_null in [True, 1]:
            self.allow_null = True
        else:
            self.allow_null = False
        if primary_key in [True, 1]:
            self.primary_key = True
        else:
            self.primary_key = False
        if unique in [True, 1]:
            self.unique = True
        else:
            self.unique = False
        if default != None:
            if isinstance(default, int):
                self.default = default
            else:
                raise ValueError(
                    "[WebSock] The default value should be integer."
                )
        else: self.default = None

class AutoField:
    def __init__(self, primary_key:bool=False, unique:bool=False):
        if primary_key in [True, 1]:
            self.primary_key = True
        else:
            self.primary_key = False
        if unique in [True, 1]:
            self.unique = True
        else:
            self.unique = False

class BooleanField:
    def __init__(self, allow_null:bool=False, default=None):
        if allow_null in [True, 1]:
            self.allow_null = True
        else:
            self.allow_null = False
        if default:
            if isinstance(default, bool):
                if default == True: self.default = True
                else: self.default = False
            else: raise ValueError(
                "[WebSock] The default value should be bool."
            )
        else:
            self.default = None

class DateField:
    def __self__(self, auto_now_created:bool=False, auto_now_modified:bool=False, allow_null:bool=False, default:datetime.date=None):
        if auto_now_created in [True, 1]:
            self.auto_now_created = True
        else: self.auto_now_created = False
        if auto_now_modified in [True, 1]:
            self.auto_now_modified = True
        else: self.auto_now_modified = False
        if auto_now_created and auto_now_modified:
            raise AssertionError(
                "[WebSock] You could choose either auto_now_create or auto_now_modified but not both."
            )
        if default != None:
            if type(default) == "<class 'datetime.date'>":
                self.default = default
            else: raise ValueError(
                "[WebSock] The default value should be datetime.date object."
            )
        else:
            self.default = None
        if allow_null in [True, 1]:
            if auto_now_created or auto_now_modified:
                raise ValueError(
                    "[WebSock] cannot set allow_null to True with auto_now_created or auto_now_modified." # FIXME Message
                )
            else: self.allow_null = True
        else: self.allow_null = False

class DateTimeField:
    def __init__(self, auto_now_created:bool=False, auto_now_modified:bool=False, allow_null:bool=False, default:datetime.datetime=None):
        if auto_now_created in [True, 1]:
            self.auto_now_created = True
        else: self.auto_now_created = False
        if auto_now_modified in [True, 1]:
            self.auto_now_modified = True
        else: self.auto_now_modified = False
        if auto_now_created and auto_now_modified:
            raise AssertionError(
                "[WebSock] You could choose either auto_now_create or auto_now_modified but not both."
            )
        if allow_null in [True, 1]:
            if auto_now_created or auto_now_modified:
                raise ValueError(
                    "[WebSock] cannot set allow_null to True with auto_now_created or auto_now_modified."
                )
            else:
                self.allow_null = True
        else:
            self.allow_null = False
        if default != None:
            if type(default) == "<class 'datetime.datetime'>":
                self.default = default
            else: raise ValueError(
                "[WebSock] The default value should be datetime.datetime object."
            )
        else:
            self.default = None

class TimeField:
    def __init__(self, auto_now_created:bool=False, auto_now_modified:bool=False, allow_null:bool=False, default:datetime.time=None):
        if auto_now_created in [True, 1]:
            self.auto_now_created = True
        else: self.auto_now_created = False
        if auto_now_modified in [True, 1]:
            self.auto_now_modified = True
        else: self.auto_now_modified = False
        if auto_now_created and auto_now_modified:
            raise AssertionError(
                "[WebSock] You could choose either auto_now_create or auto_now_modified but not both."
            )
        if allow_null in [True, 1]:
            if auto_now_created or auto_now_modified:
                raise ValueError(
                    "[WebSock] cannot set allow_null to True with auto_now_created or auto_now_modified."
                )
            else:
                self.allow_null = True
        else: self.allow_null = False
        if default != None:
            if type(default) == "<class 'datetime.time'>":
                self.default = default
            else: raise ValueError(
                "[WebSock] The default value should be datetime.time object."
            )
        else:
            self.default = None

class DecimalField:
    def __init__(self, max_digits:int=None, decimal_places:int=None, allow_null:bool=False, unique:bool=False, default:float=None):
        if (not isinstance(max_digits, int))or(not isinstance(decimal_places, int)):
            if ((max_digits == None)and(decimal_places != None))or((max_digits != None)and(decimal_places == None)):
                raise ValueError(
                    "[WebSock] max_digits and decimal_places should be assigned together"
                )
            raise ValueError(
                "[WebSock] max_digits and decimal_places should be integer values."
            )
        else:
            if isinstance(max_digits, int) and isinstance(decimal_places, int):
                self.max_digits = max_digits
                self.decimal_places = decimal_places
            else:
                raise ValueError(
                    "[WebSock] Error assigning DecimalField."
                )
        if default != None:
            if type(default) == "<class 'float'>":
                self.default = default
            else: raise ValueError(
                "[WebSock] The default value should be float."
            )
        else:
            self.default = None
        if allow_null in [True, 1]:
            self.allow_null = True
        else:
            self.allow_null = False
        if unique in [True, 1]:
            self.unique = True
        else:
            self.unique = False

class ForeignKey:
    def __init__(self, to_table, on_delete=CASCADE, allow_null:bool=True, unique:bool=False):
        self.to_table = to_table
        if allow_null in [False, 0]:
            self.allow_null = False
        else:
            self.allow_null = True
        if unique in [False, 0]:
            self.unique = False
        else:
            self.unique = True
        if type(on_delete).__name__[2:] in ['SET', 'STRICT', 'NO_ACTION', 'CASCADE']:
            self.on_delete = on_delete
        else:
            raise ValueError(
            "[WebSock] Invalid on_delete value."
        )












class __Application_Database:
    def drop_db(self):
        f = open("MiddleWare/Database/sqlite3.db", 'wb')
        f.write(b''); f.close()
        print("[WebSock][Database] Database droped.")
    def LoadQueries(self):
        dirs = os.listdir(os.path.join(os.getcwd(), 'WebApplication\\MiddleWare\\Database\\schemas'))
        schema_count = 0
        for dir_ in dirs:
            try:
                num = int(dir_.split('_')[-1].split('.')[0])
                if num > schema_count: schema_count = num
            except:pass
        f = open(os.path.join(os.getcwd(), 'WebApplication\\MiddleWare\\Database\\schemas'), 'r')
        data = f.read()
        f.close()
        # Slice:
        data += '["""'
        data = data.replace("\n\n", '""","""')
        data += '"""]'
        return eval(data)

    def loading_tbls(self):
        try:
            db = sql.connect(os.path.join(os.getcwd(), 'WebApplication\\MiddleWare\\Database\\sqlite3.db'))
            cur = db.cursor()
            failures = []; count = 1
            for query in self.LoadQueries(R"C:\Users\lenovo\Desktop\server_root\ServerSide\Server\DB_Configurations\structure.sql"):
                try:
                    cur.execute(query)
                    db.commit()
                except Exception as e: failures.append([query, e, count])
                count += 1

            for i in failures:
                print(f"""\n({i[2]}) [{i[1]}]{i[0]}\n""")
        except:
            print("[Server][SQL_Database] loading tables error!")

    def create_db(database):
        try:
            db = sql.connect("MiddleWare/Database/sqlite3.db")
            cur = db.cursor(); cur.execute(f"CREATE DATABASE {database}")
            db.commit(); db.close()
        except:
            print(f'[Server][SQL_Database] Cannot create the database "{database}"!')
ApplicationDatabase = __Application_Database()












class Model:
    def update_conn(self, conn):
        for table in self.conn_tables:
            self.Update(table, data={"_connection_": None}, where=self.where[table._connection_ == conn])

    def Delete(self, table, where=None): # DONE
        table = table.name
        print(f"[SERVER][SQL-DATABASE] (Delete) Has been applied:[{table}]")
        if where: query = f'TRUNCATE TABLE {table};'
        else: query = f'''DELETE FROM {table} WHERE {where};'''
        cur = self.db.cursor()
        cur.execute(query)
        self.db.commit(); cur.close()
    
    def Insert(self, table, data): # DONE
        if data["_connection_"] != None:
                try:
                    data["_connection_"] = data["_connection_"].ip
                except:
                    raise ValueError(
                        "ConnectionValuseError: only `connection` or a None object could be passed in a `_connection_` column"
                    )
        table = table.name
        key = (str(list(data.keys())).replace('"', '')).replace("'", '')
        val = list(data.values())
        cur = self.db.cursor()
        print(f"[SERVER][SQL-DATABASE] (Insert) Has been applied:[{table}] [{str(val)[1:-1]}]")
        cur.execute(f'''INSERT INTO {table} ({key[1:-1]})\nVALUES ({("%s,"*len(val))[:-1]});''', tuple(val))
        self.db.commit()
        cur.close()

    def Update(self, table, data, where=None): # DONE
        if "_connection_" in data:
            if data["_connection_"] != None:
                try:
                    data["_connection_"] = data["_connection_"].ip
                except:
                    raise ValueError(
                        "ConnectionValuseError: only `connection` or a None object could be passed in a `_connection_` column"
                    )
        table = table.name
        print(f"[SERVER][SQL-DATABASE] (Update) Has been applied:[{table}]")
        S = 'SET'; W = ''; params = []
        for key in data:
            val = data[key]; params.append(val)
            S+=f" {key}=%s,"
        if where:
            W = f'WHERE {where}'
        query = f"""UPDATE {table}\n{S[:-1]}\n{W};"""
        cur = self.db.cursor()
        cur.execute(query, tuple(params))
        self.db.commit(); cur.close()
    
    def Check(self, table, where=None, fetch=None, columns=['*']): # DONE
        table = table.name
        print(f"[SERVER][SQL-DATABASE] (Check) Has been applied:[{table} :: {fetch}]")
        # Extrect:
        W = ''; params = []
        if where: W = f'WHERE {where}'
        if isinstance(fetch, int): L = f'LIMIT {fetch}'
        elif fetch == '*': L = ''
        else: L = ''
        cur = self.db.cursor(buffered=True)
        cur.execute(f"""SELECT {str(columns)[1:-1].replace('"', '').replace("'", '')} FROM {table}\n{W}\n{L};""", tuple(params))
        self.db.commit()
        if fetch: response = cur.fetchall(); cur.close(); return response 
        else: response = bool(cur.fetchone()); cur.fetchall(); cur.close(); return response

    Close = lambda self: self.close()

    class whereStatementFragment:
        def __and__(self, data_):
            self.data = self.data + ' AND ' + data_.data
            return self
        def __or__(self, data_):
            self.data = self.data + ' OR ' + data_.data
            return self
        def __init__(self, data):
            self.data = data

    class Where(list):
        def __getitem__(self, params):
            if type(params) != 'str':params = params.data
            return params

    class Column:
        def __eq__(self, param):
            if type(param).__name__ == 'AsyncStreamObject': param = param.ip
            if isinstance(param, int) or isinstance(param, float): data = param
            else: data = f'''"{param}"'''
            return self.mainclass.whereStatementFragment(f'{self.name} = {data}')

        def __ne__(self, param):
            if type(param).__name__ == 'AsyncStreamObject': param = param.ip
            if isinstance(param, int) or isinstance(param, float): data = param
            else: data = f'''"{param}"'''
            return self.mainclass.whereStatementFragment(f'{self.name} != {data}')

        def __lt__(self, param):
            if type(param).__name__ == 'AsyncStreamObject': param = param.ip
            if isinstance(param, int) or isinstance(param, float): data = param
            else: data = f'''"{param}"'''
            return self.mainclass.whereStatementFragment(f'{self.name} < {data}')

        def __le__(self, param):
            if type(param).__name__ == 'AsyncStreamObject': param = param.ip
            if isinstance(param, int) or isinstance(param, float): data = param
            else: data = f'''"{param}"'''
            return self.mainclass.whereStatementFragment(f'{self.name} <= {data}')
        
        def __ne__(self, param):
            if type(param).__name__ == 'AsyncStreamObject': param = param.ip
            if isinstance(param, int) or isinstance(param, float): data = param
            else: data = f'''"{param}"'''
            return self.mainclass.whereStatementFragment(f'{self.name} != {data}')
        
        def __ge__(self, param):
            if type(param).__name__ == 'AsyncStreamObject': param = param.ip
            if isinstance(param, int) or isinstance(param, float): data = param
            else: data = f'''"{param}"'''
            return self.mainclass.whereStatementFragment(f'{self.name} >= {data}')
        
        def __gt__(self, param):
            if type(param).__name__ == 'AsyncStreamObject': param = param.ip
            if isinstance(param, int) or isinstance(param, float): data = param
            else: data = f'''"{param}"'''
            return self.mainclass.whereStatementFragment(f'{self.name} > {data}')

        def __init__(self, name, table, mainclass):
            self.name = name
            self.table = table
            self.mainclass = mainclass

    class Table:
        def __init__(self, mainclass, name):
            self.mainclass = mainclass
            mainclass.all_tables.append((name, self))
            self.name = name
            cur = mainclass.db.cursor()
            cur.execute(f"SHOW COLUMNS FROM {name};")
            self.info = cur.fetchall()
            cur.close()
            self.columns = [i[0] for i in self.info]
            for i in self.columns:
                exec(f'self.{i} = mainclass.Column("{i}", "{name}", mainclass)', locals())
        def Insert(self, data):
            return self.mainclass.Insert(self.name, data)
        def Check(self, where=None, fetch=None, columns=['*']):
            return self.mainclass.Check(self.name, where, fetch, columns)
        def Delete(self, where=None):
            return self.mainclass.Delete(self.name, where)
        def Update(self, data, where=None):
            return self.mainclass.Update(self.name, data, where)

    def InitiateDatabase(self):
        try:
            self.db = sql.connect("MiddleWare/Database/sqlite3.db")
            cur = self.db.cursor()
            cur.execute("SHOW TABLES")
            self.tablesNames = [i[0] for i in cur.fetchall()]
            for i in self.tablesNames:
                exec(f'self.{i} = self.Table(self, "{i}")', locals())
            cur.close()
        except sql.errors.ProgrammingError as e:
            if e.errno == 1049:
                ApplicationDatabase.create_db(database=self.db_)
                print(f'[SERVER][SQL-DATABASE] Database "{self.db_}" has been generated...')
                self.InitiateDatabase()
            else: print('Error:', e)
    
    def CreateArchive(self):
        if 'archive' not in self.tablesNames:
            cur = self.db.cursor()
            cur.execute("""
CREATE TABLE archive(
    id INT AUTO_INCREMENT,
    file_name VARCHAR(150),
    t_stamp VARCHAR(30),
    data MEDIUMBLOB,
    PRIMARY KEY (id)
);"""); cur.close()

    def Connections(self):
        for _, table in self.all_tables:
            if '_connection_' in table.columns:
                self.conn_tables.append(table)

    def __init__(self):
        self.where = self.Where()
        self.all_tables = []
        self.conn_tables = []
        self.InitiateDatabase()
        self.Connections()
