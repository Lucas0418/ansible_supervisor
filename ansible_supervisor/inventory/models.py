from django.db import models


# Create your models here.


class Host(models.Model):
    ansible_alias = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.ansible_alias


class HostVar(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    var_name = models.CharField(max_length=200)
    var_value = models.CharField(max_length=200)

    def __str__(self):
        return self.var_name


class Group(models.Model):
    ansible_group = models.CharField(default='', max_length=200, unique=True)
    ansible_hosts = models.ManyToManyField(Host, blank=False)
    ansible_children = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return self.ansible_group


class GroupVar(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    var_name = models.CharField(max_length=200)
    var_value = models.CharField(max_length=200)

    def __str__(self):
        return self.var_name


class Facts(models.Model):
    host = models.OneToOneField(Host, on_delete=models.CASCADE)
    ansible_lsb = models.CharField(max_length=200)
    ansible_memtotal_mb = models.PositiveIntegerField(default=None)
    ansible_disktotal_size = models.PositiveIntegerField(default=None)
    ansible_ipv4_address = models.GenericIPAddressField(default=None)
    ansible_arch = models.CharField(max_length=200)
    ansible_processor_cores = models.PositiveSmallIntegerField(default=None)

    def __str__(self):
        return self.host.ansible_alias

    class Meta:
        verbose_name = 'Facts'
        verbose_name_plural = 'Facts'
