from django.db import models
from db.base_model import BaseModel
from utils.get_hash import get_hash


class PassportManager(models.Manager):
    def add_one_passport(self,username,password,email):
        passport = self.create(username = username,password = get_hash(password),email = email)
        return passport
    def get_one_passport(self,username,password):
        try:
            passport = self.get(username=username,password=get_hash(password))
        except self.model.DoesNotExist:
            passport = None
        return passport
        

class Passport(BaseModel):
    username = models.CharField(max_length=20,unique=True,verbose_name='用户名称')
    password = models.CharField(max_length=40,verbose_name='用户密码')
    email = models.EmailField(verbose_name='用户邮箱')
    is_active = models.BooleanField(default=False,verbose_name='是否激活')

    objects = PassportManager()

    class Meta:
        db_table = 's_user_account' 
