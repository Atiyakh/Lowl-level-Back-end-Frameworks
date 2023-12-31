import sqlite3 as sql

class CharField:
    def __init__(self, max_length:int, choices:list=None, allow_null:bool=False, primary_key:bool=False):
        if(not isinstance(max_length,int))or(not(50_000_000<max_length<0)):
            raise ValueError(
                "[WebSock] max_length should be an integer between (1-50,000,000).+"
            )
        else: self.max_length = max_length
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
            "[WebSock] the choices argument should be a dictionary"
        )
        if allow_null in [True, 1]:
            self.allow_null = True
        if primary_key in [True, 1]:
            self.primary_key = True

class IntegerField:
    def __init__(self, allow_null:bool=False, primary_key:bool=False):
        if allow_null in [True, 1]:
            self.allow_null = True
        if primary_key in [True, 1]:
            self.primary_key = True

class AutoField:
    def __init__(self, primary_key:bool=False):
        if primary_key in [True, 1]:
            self.primary_key = True

class BooleanField:
    def __init__(self, allow_null:bool=False):
        if allow_null in [True, 1]:
            self.allow_null = True

class DateField:
    def __self__(self, auto_now_created:bool=False, auto_now_modified:bool=False):
        if auto_now_created in [True, 1]:
            self.auto_now_created = True
        if auto_now_modified in [True, 1]:
            self.auto_now_modified = True
        if auto_now_created and auto_now_modified:
            raise AssertionError(
                "[WebSock] you could choose either auto_now_create or auto_now_modified but not both."
            )

class DateTimeField:
    def __init__(self, auto_now_created:bool=False, auto_now_modified:bool=False):
        if auto_now_created in [True, 1]:
            self.auto_now_created = True
        if auto_now_modified in [True, 1]:
            self.auto_now_modified = True
        if auto_now_created and auto_now_modified:
            raise AssertionError(
                "[WebSock] you could choose either auto_now_create or auto_now_modified but not both."
            )

class Application_Database:
    def __init__(self):
        self.models_list = []
    def drop_db(host, user, passwd, database):
        try:
            db = sql.connect(
                host = host,
                user = user,
                passwd = passwd
            )
            cur = db.cursor(); cur.execute(f'DROP DATABASE {database}')
            db.commit(); db.close()
        except:
            print(f'[Server][SQL_Database] Cannot delete the previous schema from "{database}"')

    def LoadQueries(path):
        # Fitch:
        f = open(path, 'r')
        data = f.read()
        data = data[data.find('/*START*/'):]
        f.close()
        # Slice:
        data = data.replace("/*START*/", '["""')
        data = data.replace("/*END*/", '"""]')
        data = data.replace("/**/", '""","""')
        # Loading & Creating & Returning a list to Encompass the whole thing:
        return eval(data)

    def loading_tbls(host, user, passwd, database):
        try:
            db = sql.connect(
                host = host,
                user = user,
                passwd = passwd,
                database = database
            )
            cur = db.cursor()
            failures = []; count = 1
            for query in LoadQueries(R"C:\Users\lenovo\Desktop\server_root\ServerSide\Server\DB_Configurations\structure.sql"):
                try:
                    cur.execute(query)
                    db.commit()
                except Exception as e: failures.append([query, e, count])
                count += 1

            for i in failures:
                print(f"""\n({i[2]}) [{i[1]}]{i[0]}\n""")
        except:
            print("[Server][SQL_Database] loading tables error!")

    def create_db(host, user, passwd, database): ######
        try:
            db = sql.connect(
                host = host,
                user = user,
                passwd = passwd
            )
            cur = db.cursor(); cur.execute(f"CREATE DATABASE {database}")
            db.commit(); db.close()
        except:
            print(f'[Server][SQL_Database] Cannot create the database "{database}"!')

class Model:
    def update_conn(self, conn):
        for table in self.conn_tables:
            self.Update(table, data={"_connection_": None}, where=self.where[table._connection_ == conn])
    def UpdateSchema(self):
        self.db.close()
        drop_db(self.host, self.user, self.passwd , self.db_)
        create_db(self.host, self.user, self.passwd , self.db_)
        loading_tbls(self.host, self.user, self.passwd , self.db_)
        self.InitiateDatabase()
        print(f"[SERVER][SQL-DATABASE] Database schema has been updated...")

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
            self.db = sql.connect(
                host = self.host,
                user = self.user,
                passwd = self.passwd,
                database = self.db_
            )
            cur = self.db.cursor()
            cur.execute("SHOW TABLES")
            self.tablesNames = [i[0] for i in cur.fetchall()]
            for i in self.tablesNames:
                exec(f'self.{i} = self.Table(self, "{i}")', locals())
            cur.close()
        except sql.errors.ProgrammingError as e:
            if e.errno == 1049:
                create_db(host=self.host, user=self.user, passwd=self.passwd, database=self.db_)
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

    def __init__(self, database, host, password, user):
        self.where = self.Where()
        self.all_tables = []
        self.conn_tables = []
        self.db_ = database
        self.host = host
        self.passwd = password
        self.user = user
        self.InitiateDatabase()
        self.Connections()