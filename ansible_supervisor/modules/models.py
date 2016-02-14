from django.db import models
from ..inventory.models import Host, Group, Facts
import os
import json
import re


# Create your models here.

ANSIBLE_ADMIN = 'ansible'
ANSIBLE_SERVER = 'localhost'
ANSIBLE_DYNAMIC_INVENTORY = 'personalAnsibleTools/ai.py'
ANSIBLE_HOME = '/home/ansible/ansible'
ANSIBLE_VIR_ENV = '/home/ansible/ansiblevirenv'
ANSIBLE_COMMAND_PREFIX = 'ssh ' + ANSIBLE_ADMIN + '@' + ANSIBLE_SERVER + " '. "\
    + ANSIBLE_VIR_ENV + '/bin/activate;' + '. ' + ANSIBLE_HOME \
    + '/hacking/env-setup -q;' + 'ansible -i ' + ANSIBLE_DYNAMIC_INVENTORY + ' '
ANSIBLE_COMMAND_SUFFIX = " -m setup;exit'"


class SetupModule(models.Model):
    command = models.CharField(default='', max_length=200, unique=True, blank=True)
    hosts = models.ManyToManyField(Host)
    groups = models.ManyToManyField(Group)

    def save(self, using='default', *args, **kwargs):
        if self.pk is not None:
            hosts = self.hosts.get_queryset().all()
            groups = self.groups.get_queryset().all()
            targets = []
            targets += [host.ansible_alias for host in hosts]
            targets += [group.ansible_group for group in groups]
            target = ','.join(targets)
            self.command = ANSIBLE_COMMAND_PREFIX + target + ANSIBLE_COMMAND_SUFFIX
            print(self.command)
            p = os.popen(self.command)
            raw_data = p.read()
            p = re.compile(r'(?<=})\n(?=\S+\s+\|\s+[A-Z]+\s+=>\s+{)', re.M)
            data = raw_data
            datas = p.split(data)
            for xdata in datas:
                p = re.compile(r'\s+\|\s+(?=[A-Z]+\s+=>\s+{)|\s+=>\s+(?=\{)', re.M)
                xdatas = p.split(xdata)
                hostinstance = Host.objects.filter(ansible_alias=xdatas[0])
                hostinstance = hostinstance[0]
                jd = json.loads(xdatas[2])
                jd = jd['ansible_facts']
                if xdatas[1] == 'SUCCESS':
                    try:
                        facts = hostinstance.facts
                        facts.ansible_memtotal_mb = int(jd['ansible_memtotal_mb'])
                        facts.ansible_disktotal_size = int(jd['ansible_mounts'][0]['size_total'])/1024/1024
                        facts.ansible_ipv4_address = jd['ansible_all_ipv4_addresses'][0]
                        facts.ansible_processor_cores = int(jd['ansible_processor_cores'][0])
                    except Exception as e:
                        facts = Facts.objects.create(host=hostinstance,
                                                    ansible_memtotal_mb=int(jd['ansible_memtotal_mb']),
                                                    ansible_disktotal_size=int(jd['ansible_mounts'][0]['size_total'])/1024/1024,
                                                    ansible_ipv4_address=jd['ansible_all_ipv4_addresses'][0],
                                                    ansible_processor_cores=int(jd['ansible_processor_cores']))

                    facts.save()
                hostinstance.save()
                # result = {}
                # result['ansible_alias'] = xdatas[0]
                # result['ansible_setup_status'] = xdatas[1]
                # result['ansible_setup_result'] = json.loads(xdatas[2])
        super(SetupModule, self).save(using='default', *args, **kwargs)
