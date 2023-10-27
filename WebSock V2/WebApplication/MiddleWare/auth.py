from importlib.machinery import SourceFileLoader
import pathlib, os
Cryptography = SourceFileLoader("Cryptography", os.path.join(pathlib.Path(__file__).parent, 'Cryptography.py')).load_module()
import sqlite3 as sql
import base64, time

Hash = Cryptography.Hash

# Custom cookies-based authentication system
class MiddleWare_Default_Models:
    class User():
        def create_user(self, request, username, password, email=None, first_name=None, last_name=None):
            ApplicationDB = sql.connect(os.path.join(pathlib.Path(__file__).parent, "Database\\sqlite3.db"))
            cur = ApplicationDB.cursor()
            cur.execute("UPDATE auth_websock_default_user_table SET authentication=? WHERE authentication=?", (
                None, request.remote_ip
            )); ApplicationDB.commit()
            hashed_password = Hash.Sha384(password)
            try:
                authentication = base64.b64encode(f'{request.remote_ip}|{time.ctime()}'.encode('utf-8')).decode('utf-8')
                cur.execute("INSERT INTO auth_websock_default_user_table (username, password, email, first_name, last_name, authentication)\nVALUES(?, ?, ?, ?, ?, ?)", (
                    username, hashed_password, email, first_name, last_name, authentication
                ))
                ApplicationDB.commit()
                user_id = cur.lastrowid
                cur.close()
                ApplicationDB.close()
                request.cookies['session'] = authentication
                request.session = authentication
                request.user_creditentials = {
                    'username': username,
                    'password': hashed_password,
                    'email': email,
                    'first_name': first_name,
                    'last_name': first_name,
                    'authentication': authentication
                }
                request.authenticated_user = True
                return user_id
            except sql.IntegrityError:
                cur.close()
                ApplicationDB.close()
                return False
        def login_user(self, request, password, email=None, username=None):
            ApplicationDB = sql.connect(os.path.join(pathlib.Path(__file__).parent, "Database\\sqlite3.db"))
            cur = ApplicationDB.cursor()
            hashed_password = Hash.Sha384(password)
            if email:
                cur.execute("SELECT * FROM auth_websock_default_user_table WHERE email=? AND password=?", (
                    email, hashed_password
                ))
            elif username:
                cur.execute("SELECT * FROM auth_websock_default_user_table WHERE username=? AND password=?", (
                    username, hashed_password
                ))
            else: return None
            query = cur.fetchone()
            if query:
                cur.execute("UPDATE auth_websock_default_user_table SET authentication=? WHERE authentication=?", (
                    None, request.remote_ip
                )); ApplicationDB.commit()
                authentication = base64.b64encode(f'{request.remote_ip}|{time.ctime()}'.encode('utf-8')).decode('utf-8')
                cur.execute("UPDATE auth_websock_default_user_table SET authentication=? WHERE UserID=?", (
                    authentication, query[0]
                )); ApplicationDB.commit()
                cur.close()
                ApplicationDB.close()
                request.cookies['session'] = authentication
                request.session = authentication
                rows = ['username', 'password', 'email', 'first_name', 'last_name', 'authentication']
                request.user_creditentials = {rows[num]: query[num+1] for num in range(len(rows))}
                request.authenticated_user = True
                return True
            else:
                cur.close()
                return False
        def logout_user(self, request, password, username=None, email=None):
            ApplicationDB = sql.connect(os.path.join(pathlib.Path(__file__).parent, "Database\\sqlite3.db"))
            cur = ApplicationDB.cursor()
            hashed_password = Hash.Sha384(password)
            if email:
                cur.execute("UPDATE auth_websock_default_user_table SET authentication=? WHERE email=? AND password=?", (
                    None, email, hashed_password
                ))
            elif username:
                cur.execute("UPDATE auth_websock_default_user_table SET authentication=? WHERE username=? AND password=?", (
                    None, username, hashed_password
                ))
            else: return None
            if cur.rowcount == 1:
                request.session = ''
                request.cookies['session'] = ''
                request.authenticated_user = False
                request.user_creditentials = None
                return True
            else: return False
        def set_username(self, request, username):
            ApplicationDB = sql.connect(os.path.join(pathlib.Path(__file__).parent, "Database\\sqlite3.db"))
            cur = ApplicationDB.cursor()
            cur.execute("UPDATE auth_websock_default_user_table SET username=? WHERE authentication=?", (
                username, request.remote_ip
            ))
            request.user_creditentials['username'] = username
            ApplicationDB.commit()
            cur.close()
            ApplicationDB.close()
        def set_password(self, request, password):
            ApplicationDB = sql.connect(os.path.join(pathlib.Path(__file__).parent, "Database\\sqlite3.db"))
            cur = ApplicationDB.cursor()
            hashed_password = Hash.Sha384(password)
            cur.execute("UPDATE auth_websock_default_user_table SET password=? WHERE authentication=?", (
               hashed_password , request.remote_ip
            ))
            request.user_creditentials['password'] = hashed_password
            ApplicationDB.commit()
            cur.close()
            ApplicationDB.close()
        def set_email(self, request, email):
            ApplicationDB = sql.connect(os.path.join(pathlib.Path(__file__).parent, "Database\\sqlite3.db"))
            cur = ApplicationDB.cursor()
            cur.execute("UPDATE auth_websock_default_user_table SET email=? WHERE authentication=?", (
                email, request.remote_ip
            ))
            request.user_creditentials['email'] = email
            ApplicationDB.commit()
            ApplicationDB.close()
            cur.close()
        def set_first_name(self, request, first_name):
            ApplicationDB = sql.connect(os.path.join(pathlib.Path(__file__).parent, "Database\\sqlite3.db"))
            cur = ApplicationDB.cursor()
            cur.execute("UPDATE auth_websock_default_user_table SET first_name=? WHERE authentication=?", (
                first_name, request.remote_ip
            ))
            request.user_creditentials['first_name'] = first_name
            ApplicationDB.commit()
            cur.close()
            ApplicationDB.close()
        def set_last_name(self, request, last_name):
            ApplicationDB = sql.connect(os.path.join(pathlib.Path(__file__).parent, "Database\\sqlite3.db"))
            cur = ApplicationDB.cursor()
            cur.execute("UPDATE auth_websock_default_user_table SET last_name=? WHERE authentication=?", (
                last_name, request.remote_ip
            ))
            request.user_creditentials['last_name'] = last_name
            ApplicationDB.commit()
            cur.close()
            ApplicationDB.close()
def __load_user_to_database():
    try:
        ApplicationDB = sql.connect(os.path.join(pathlib.Path(__file__).parent, "Database\\sqlite3.db"))
        cur = ApplicationDB.cursor()
        cur.execute("""CREATE TABLE auth_websock_default_user_table(
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(250) NOT NULL UNIQUE,
    password VARCHAR(300) NOT NULL,
    email VARCHAR(250) UNIQUE,
    first_name VARCHAR(250),
    last_name VARCHAR(250),
    authentication VARCHAR(700)
);""")
        ApplicationDB.commit()
        cur.close()
        ApplicationDB.close()
    except sql.Error: pass

__load_user_to_database()

def login_needed(func):
    def __call__(arg):
        func(arg)
    return __call__
