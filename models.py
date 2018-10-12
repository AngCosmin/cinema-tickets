from peewee import Model, MySQLDatabase, CharField, DateTimeField, ForeignKeyField

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


class Movie(BaseModel):
    title = CharField()
    start_time = DateTimeField()


class Tickes(BaseModel):
    movie_id = ForeignKeyField(Movie, backref='movie')