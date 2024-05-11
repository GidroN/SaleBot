import os
import secrets
from tortoise import models, fields


class User(models.Model):
    tg_id = fields.CharField(max_length=10, unique=True)
    username = fields.CharField(max_length=32, null=True)
    name = fields.CharField(max_length=129)  # 128 max chars + spacebar


class Product(models.Model):
    title = fields.CharField(max_length=100)
    description = fields.TextField(null=True)
    price = fields.FloatField()
    img = fields.CharField(max_length=255)
    img_file_id = fields.CharField(max_length=100)

    async def delete(self, *args, **kwargs):
        os.remove(self.img)
        await super().delete(*args, **kwargs)


class Subscription(models.Model):
    img = fields.CharField(max_length=255)
    img_file_id = fields.CharField(max_length=100)
    product_type = fields.ForeignKeyField('models.Product', on_delete=fields.CASCADE)

    async def delete(self, *args, **kwargs):
        os.remove(self.img)
        await super().delete(*args, **kwargs)


class Queue(models.Model):
    user = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE, related_name='queue')
    product_type = fields.ForeignKeyField('models.Product', on_delete=fields.CASCADE, related_name='queue')
    date = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=True)
    req_id = fields.CharField(max_length=8)

    async def save(self, *args, **kwargs):
        if not self.req_id:
            self.req_id = ''.join(secrets.choice('0123456789') for _ in range(8))
        await super().save(*args, **kwargs)