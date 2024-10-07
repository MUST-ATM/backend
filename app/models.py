from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    user_id = fields.CharField(max_length=10, unique=True)

class Balance(Model):
    user = fields.ForeignKeyField("models.User", related_name="balances")
    foreign_account = fields.FloatField()
    hkd_account = fields.FloatField()
    mop_account = fields.FloatField()


