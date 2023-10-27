import sqlite3 as sql
import datetime, os
import traceback

# Super {[("`CREATIVE`")]} databse handling.

class __WHERE_STATEMENT:
    def __getitem__(self, params):
        if type(params) != 'str':
            params = params.data
        return params

class __WHERE_FRAGMENT:
    def __and__(self, data_):
        self.data = f"({self.data} AND  {data_.data})"
        return self

    def __or__(self, data_):
        self.data = f"({self.data} OR  {data_.data})"
        return self

    def __init__(self, data):
        self.data = data

_FIELD__WHERE_FRAGMENT = __WHERE_FRAGMENT

class __FIELD:
    where_fragment = __WHERE_FRAGMENT
    def __hash__(self):
        return id(self)
    def __eq__(self, param):
        if isinstance(param, int) or isinstance(param, float): data = param
        else: data = f'''"{param}"'''
        result = self.where_fragment(f'({self.__fieldname__} = {data})')
        return result

    def __ne__(self, param):
        if isinstance(param, int) or isinstance(param, float): data = param
        else: data = f'''"{param}"'''
        result = self.where_fragment(f'({self.__fieldname__} != {data})')
        return result

    def __lt__(self, param):
        if isinstance(param, int) or isinstance(param, float): data = param
        else: data = f'''"{param}"'''
        result =  self.where_fragment(f'({self.__fieldname__} < {data})')
        return result

    def __le__(self, param):
        if isinstance(param, int) or isinstance(param, float): data = param
        else: data = f'''"{param}"'''
        result = self.where_fragment(f'({self.__fieldname__} <= {data})')
        return result

    def __ne__(self, param):
        if isinstance(param, int) or isinstance(param, float): data = param
        else: data = f'''"{param}"'''
        result = self.where_fragment(f'({self.__fieldname__} != {data})')
        return result
    
    def __ge__(self, param):
        if isinstance(param, int) or isinstance(param, float): data = param
        else: data = f'''"{param}"'''
        result = self.where_fragment(f'({self.__fieldname__} >= {data})')
        return result
    
    def __gt__(self, param):
        if isinstance(param, int) or isinstance(param, float): data = param
        else: data = f'''"{param}"'''
        result = self.where_fragment(f'({self.__fieldname__} > {data})')
        return result

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

Where = __WHERE_STATEMENT()
DATABASE_PATH = os.path.join(os.getcwd(), 'WebApplication\\MiddleWare\\Database')

class CharField(__FIELD):
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

class IntegerField(__FIELD):
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

class AutoField(__FIELD):
    def __init__(self, primary_key:bool=False, unique:bool=False):
        if primary_key in [True, 1]:
            self.primary_key = True
        else:
            self.primary_key = False
        if unique in [True, 1]:
            self.unique = True
        else:
            self.unique = False

class BooleanField(__FIELD):
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

class DateField(__FIELD):
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

class DateTimeField(__FIELD):
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

class TimeField(__FIELD):
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

class DecimalField(__FIELD):
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

class ForeignKey(__FIELD):
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
    initiated = False
    padding_name = lambda _, num: ("0"*(4-len(num.__str__())))+str(num)
    def Initiate_database(self):
        if not self.initiated:
            self.db = sql.connect(os.path.join(DATABASE_PATH, 'sqlite3.db'))
            self.initiated = True
    def drop_db(self):
        f = open(os.path.join(DATABASE_PATH, 'sqlite3.db'), 'wb')
        f.write(b''); f.close()
    def load_queries(self):
        dirs = os.listdir(os.path.join(DATABASE_PATH, 'schemas'))
        schema_count = 0
        for dir_ in dirs:
            try:
                num = int(dir_.split('_')[-1].split('.')[0])
                if num > schema_count: schema_count = num
            except:pass
        f = open(os.path.join(DATABASE_PATH, f'schemas\\schema_{self.padding_name(schema_count)}.sql'), 'r')
        data = f.read()
        f.close()
        # Slice:
        data = '["""' + data
        data = data.replace("\n\n", '""","""')
        data += '"""]'
        return eval(data)

    def loading_tbls(self):
        try:
            db = sql.connect(os.path.join(DATABASE_PATH, 'sqlite3.db'))
            cur = db.cursor()
            failures = []; count = 1
            for query in self.load_queries():
                try:
                    cur.execute(query)
                    db.commit()
                except Exception as e: failures.append([query, e, count])
                count += 1

            for i in failures:
                print(f"""\n({i[2]}) [{i[1]}]{i[0]}\n""")
            cur.execute("""CREATE TABLE auth_websock_default_user_table(
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(250) NOT NULL UNIQUE,
    password VARCHAR(300) NOT NULL,
    email VARCHAR(250) UNIQUE,
    first_name VARCHAR(250),
    last_name VARCHAR(250),
    authentication VARCHAR(700)
);""")
            db.commit()
            cur.close()
            db.close()
        except:
            traceback.print_exc()
            print("[Server][SQL_Database] loading tables error!")

ApplicationDatabase = __Application_Database()

def UpdateSchema():
    ApplicationDatabase.drop_db()
    ApplicationDatabase.loading_tbls()
    print('[WebSock] Database Schema updated.')

MODEL_ACTIONS_LOOKUP_TABLE = dict()
FIELDS_NAMES_LIST = [
    'ForeignKey', 'DecimalField','TimeField', 
    'DateTimeField','DateField', 'BoolanField',
    'AutoField', 'IntegerField','CharField',
]

def analize_dictionaries(dict_:dict):
    result = dict()
    for key, val in dict_.items():
        if type(key).__name__ in FIELDS_NAMES_LIST:
            result[key.__fieldname__] = val
        elif type(key).__name__ == 'str': result[key] = val
        else: raise ValueError(
            f"[WebSock] Invalid value: {key}"
        )
    return result

class Model:
    def __init__(self):
        self.fields = dict()
        if not ApplicationDatabase.initiated:
            ApplicationDatabase.Initiate_database()
        self.ExtractFields()

    def ExtractFields(self):
        self.__modelname__ = type(self).__name__
        for obj_name in dir(self):
            obj_value = self.__getattribute__(obj_name)
            if type(obj_value).__name__ in FIELDS_NAMES_LIST:
                self.fields[obj_name] = obj_value
                obj_value.__fieldname__ = obj_name

    def Update(self, data, where=None):
        data = analize_dictionaries(data)
        table = self.__modelname__
        S = 'SET'; W = ''; params = []
        for key in data:
            val = data[key]; params.append(val)
            S+=f" {key} = ?,"
        if where:
            W = f'WHERE {where}'
        query = f"""UPDATE {table}\n{S[:-1]}\n{W};"""
        cur = ApplicationDatabase.db.cursor()
        cur.execute(query, tuple(params))
        ApplicationDatabase.db.commit(); cur.close()

    def Insert(self, data):
        data = analize_dictionaries(data)
        table = self.__modelname__
        key = (str(list(data.keys())).replace('"', '')).replace("'", '')
        val = list(data.values())
        cur = ApplicationDatabase.db.cursor()
        cur.execute(f'''INSERT INTO {table} ({key[1:-1]})\nVALUES ({("?,"*len(val))[:-1]});''', tuple(val))
        ApplicationDatabase.db.commit()
        id_ = cur.lastrowid
        cur.close()
        return id_

    def Delete(self, where=None):
        table = self.__modelname__
        if where:
            query = f'''DELETE FROM {table} WHERE {where};'''
        else:
            query = f'TRUNCATE TABLE {table};'
        cur = ApplicationDatabase.db.cursor()
        cur.execute(query)
        ApplicationDatabase.db.commit()
        cur.close()

    def Check(self, where=None, fetch=None, columns=['*']):
        table = self.__modelname__
        W = ''
        if where: W = f'WHERE {where}'
        if isinstance(fetch, int): L = f'LIMIT {fetch}'
        else: L = ''
        cur = ApplicationDatabase.db.cursor()
        cur.execute(f"""SELECT {str(columns)[1:-1].replace('"', '').replace("'", '')} FROM {table}\n{W}\n{L};""")
        ApplicationDatabase.db.commit()
        if fetch: response = cur.fetchall(); cur.close(); return response
        else: response = bool(cur.fetchone()); cur.fetchall(); cur.close(); return response
