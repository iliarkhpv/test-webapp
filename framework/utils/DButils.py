import pymysql
from contextlib import closing
from pymysql.cursors import DictCursor
from framework.utils.assistance import open_logfile, get_config_data


config_data = get_config_data()
HOST = config_data['db_host']
USER = config_data['db_user']
PASS = config_data['db_pass']
DB = config_data['db_name']
BROWSER = config_data['browser']


def update_test_in_database(testid, screenshot, logfile):
    with closing(pymysql.connect(
            host=HOST,
            user=USER,
            password=PASS,
            db=DB,
            charset='utf8mb4',
            cursorclass=DictCursor)) as conn:

        with conn.cursor() as cursor:
            content_type = 'image/png'
            query = f'insert into attachment (test_id, content, content_type) values (' \
                    f'{testid}, "{screenshot}", "{content_type}")'
            cursor.execute(query)
        conn.commit()

        with conn.cursor() as cursor:
            content = open_logfile(logfile)
            query = f'insert into log (test_id, content) values (' \
                    f'{testid}, "{content}")'
            cursor.execute(query)
        conn.commit()


def get_attachment_to_test(test_id):
    with closing(pymysql.connect(
            host=HOST,
            user=USER,
            password=PASS,
            db=DB,
            charset='utf8mb4',
            cursorclass=DictCursor)) as conn:
        with conn.cursor() as cursor:
            query = f'select * from attachment where test_id = {test_id};'
            cursor.execute(query)
            for row in cursor:
                return row['content'].decode('utf-8')
