from django.db import models

# Create your models here.


class Host(models.Model):
    ansible_alias = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.ansible_alias


class Group(models.Model):
    ansible_group = models.CharField(default='', max_length=200)
    ansible_hosts = models.ManyToManyField(Host)
    ansible_children = models.TextField(default='')


class Var(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    var_name = models.CharField(max_length=200)
    var_value = models.CharField(max_length=200)

    def __str__(self):
        return self.var_name
