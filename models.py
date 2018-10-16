from peewee import MySQLDatabase, Model, CharField, IntegerField

MYSQL_DB = 'cinema'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASS = ''

db = MySQLDatabase(MYSQL_DB, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASS)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Tickets(BaseModel):
    name = CharField(50)
    ticket_type = CharField(10)
    cnp = CharField(15)
    details = CharField(15)
    row = IntegerField()
    col = IntegerField()
    order_id = IntegerField()