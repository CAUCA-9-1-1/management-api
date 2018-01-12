from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from ..config import setup as config

SQL_ENGINE = {}
SQL_ENGINE_SESSION = {}


class Database:
    engine = None
    session = None
    metadata = None

    def __init__(self, db_name='general'):
        if config.DATABASE is None:
            raise Exception("""You need to set 'DATABASE' inside your config file
				DATABASE = {
					'general': {
						'engine': '',
						'dbname': ''
					}
				}""")

        self.engine = self.create_engine(db_name)
        self.session = self.init_session(db_name)
        self.metadata = MetaData(bind=self.engine)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.expunge_all()

    def init_session(self, db_name):
        if db_name not in SQL_ENGINE_SESSION or SQL_ENGINE_SESSION[db_name] is None:
            Session = sessionmaker(bind=self.engine)

            SQL_ENGINE_SESSION[db_name] = Session()

        return SQL_ENGINE_SESSION[db_name]

    def create_engine(self, db_name):
        if db_name not in SQL_ENGINE or SQL_ENGINE[db_name] is None:
            if 'username' in config.DATABASE[db_name]:
                SQL_ENGINE[db_name] = create_engine('%s://%s:%s@%s/%s' % (
                    config.DATABASE[db_name]['engine'],
                    config.DATABASE[db_name]['username'],
                    config.DATABASE[db_name]['password'],
                    config.DATABASE[db_name]['host'],
                    config.DATABASE[db_name]['dbname'],
                ), echo=config.IS_DEV)
            else:
                SQL_ENGINE[db_name] = self.engine = create_engine('%s:///%s' % (
                    config.DATABASE[db_name]['engine'],
                    config.DATABASE[db_name]['dbname'],
                ), echo=config.IS_DEV)

        return SQL_ENGINE[db_name]

    def execute(self, query, args=()):
        result = self.engine.execute(query, args)
        result_assoc = None

        if result is None:
            return None
        if result.returns_rows is not False:
            result_assoc = self._fetch_assoc(result.fetchall(), result.keys())

        result.close()
        return result_assoc

    def callproc(self, procedure, args=()):
        cursor = self.engine.raw_connection().cursor()

        if cursor is None:
            return None

        cursor.callproc(procedure, args)

        return self._fetch_assoc(cursor.fetchall(), self._keys_of_cursor(cursor))

    def get_row(self, query, args=()):
        result = self.engine.execute(query, args)
        result_assoc = self._fecth_row_assoc(result.fetchone(), result.keys())

        result.close()
        return result_assoc

    def get(self, query, args=()):
        result = self.engine.execute(query, args)
        value = None

        if result is None:
            return None
        if result.returns_rows is not False:
            value = self._first(result)

        result.close()
        return value

    def query(self, *args):
        return self.session.query(*args)

    def insert(self, item):
        self.session.add(item)

        return True

    def commit(self):
        self.session.commit()

        return True

    def _first(self, result):
        for row in result:
            for val in row:
                return val

        return None

    def _keys_of_cursor(self, cursor):
        keys = list()

        # If we use python3-mysqldb
        if cursor.description is not None:
            for field in cursor.description:
                keys.append(field[0])

        # If we use python3-pymysql
        if cursor._result is not None:
            fields = cursor._result.fields

            for field in fields:
                keys.append(field.name)

        return keys

    def _fetch_assoc(self, rows, keys=None):
        result = list()

        try:
            for row in rows:
                result.append(self._fecth_row_assoc(row, keys))
        except:
            pass

        return result

    def _fecth_row_assoc(self, row, keys):
        nb = 0
        my_row = {}

        for val in row:
            my_row[keys[nb]] = val
            nb = nb + 1

        return my_row
