import warnings
import logging
import pymysql

from .base import AbstractStorage

logger = logging.getLogger(__name__)


def create_table_if_not_exists(conn, table):
    """
    Creates MySQL table if not exists according to the product model attributes
    Args:
        cursor (MySQLdb.cursors.Cursor): MySQL cursor
        conn (MySQLdb.connections.Connection): MySQL connection
        table (str): Table name
    Return:
        None
    """
    query = 'CREATE TABLE IF NOT EXISTS {}  (\
		id int(10) NOT NULL AUTO_INCREMENT,\
		articlecode varchar(255) CHARACTER SET utf8 DEFAULT NULL ,\
		title varchar(255) CHARACTER SET utf8 DEFAULT NULL ,\
		producturl text CHARACTER SET utf8,\
		price varchar(12) DEFAULT NULL,\
		status int(1) DEFAULT NULL,\
		description text CHARACTER SET utf8,\
		imageurl varchar(1000) CHARACTER SET utf8,\
		thumburl varchar(1000) CHARACTER SET utf8,\
		parent_id varchar(45) CHARACTER SET utf8 DEFAULT "PARENT",\
		brand varchar(255) CHARACTER SET utf8 DEFAULT NULL ,\
		category varchar(255) CHARACTER SET utf8 DEFAULT NULL,\
		subcategory2 text CHARACTER SET utf8,\
		subcategory1 text CHARACTER SET utf8,\
		uzip_id varchar(8) CHARACTER SET utf8 DEFAULT "NA",\
		delivery varchar(255) CHARACTER SET utf8 DEFAULT NULL ,\
		client varchar(255) CHARACTER SET utf8 DEFAULT NULL ,\
	PRIMARY KEY (id),\
	KEY articlecode (articlecode),\
	KEY status (status)\
	)'.format(table)


    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()

            cursor.execute("truncate table {}".format(table))
            conn.commit()
    logger.info("MySQL table ready")


class MySQLStorage(AbstractStorage):

    def __init__(self, config=None):
        self.conn = pymysql.connect(host=config['host'],
                             user=config['user'],
                             password=config['passwd'],
                             db=config['db'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        self.table = config['table']

    def clear(self):
        create_table_if_not_exists(self.conn, self.table)

    def save_product(self, product):
        """
        Saves product to MySQL table
        Args:
            product (models.Product): Product object to be saved in MySQL table
        Return:
            None
        """
        with self.conn.cursor() as cursor:
            cursor.execute("INSERT INTO {} (status,description,title,price,imageurl,thumburl,producturl,\
                articlecode,brand,category,subcategory1,subcategory2, uzip_id, delivery, client)\
                VALUES (%(status)s,%(description)s,%(title)s,%(price)s,%(imageurl)s,%(thumburl)s,%(producturl)s,\
                %(articlecode)s,%(brand)s,%(category)s,%(subcategory1)s,%(subcategory2)s,%(uzip_id)s,\
                %(delivery)s,%(client)s)".format(self.table), product.to_dict())

            self.conn.commit()
