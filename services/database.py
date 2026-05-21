from peewee import ForeignKeyField, IntegerField, Model, SqliteDatabase, TextField

db = SqliteDatabase("scraper_project")


class BaseModel(Model):
    class Meta:
        database = db


class JobHistory(BaseModel):
    id = IntegerField(primary_key=True)
    title = TextField()
    description = TextField()
    tags = TextField()
    parameters = TextField()
    status = TextField()


class Artifactory(BaseModel):
    id = IntegerField(primary_key=True)
    file_path = TextField()
    job = ForeignKeyField(JobHistory, backref="artifactory")


def init_database():
    db.connect()
    db.create_tables([JobHistory])
