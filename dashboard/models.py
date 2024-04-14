# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccessRoles(models.Model):
    name = models.CharField(primary_key=True, max_length=45)
    access_level = models.CharField(max_length=45, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'access_roles'


class ActiveUsers(models.Model):
    hosts = models.ForeignKey('Hosts', models.DO_NOTHING)
    users_name = models.OneToOneField('Users', models.DO_NOTHING, db_column='users_name', primary_key=True)
    access_roles_name = models.ForeignKey(AccessRoles, models.DO_NOTHING, db_column='access_roles_name')

    class Meta:
        managed = False
        db_table = 'active_users'
        unique_together = (('users_name', 'access_roles_name'),)


class AssignedGroups(models.Model):
    groups_name = models.OneToOneField('Groups', models.DO_NOTHING, db_column='groups_name', primary_key=True)
    hosts = models.ForeignKey('Hosts', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'assigned_groups'
        unique_together = (('groups_name', 'hosts'),)


class Groups(models.Model):
    name = models.CharField(primary_key=True, max_length=45)
    type = models.CharField(max_length=45, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'

    def __str__(self):
        return self.name


class Hosts(models.Model):
    name = models.CharField(max_length=45)
    ip = models.CharField(max_length=45, blank=True, null=True)
    os = models.ForeignKey('Os', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hosts'

    def __str__(self):
        return self.name
    

class Os(models.Model):
    family = models.CharField(max_length=45, blank=True, null=True)
    version = models.CharField(max_length=45, blank=True, null=True)
    patch = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'os'
    def __str__(self):
        return f"{self.family} {self.version} - {self.patch}"

class Results(models.Model):
    hosts = models.OneToOneField(Hosts, models.DO_NOTHING, primary_key=True)
    vulnerabilities_cve = models.ForeignKey('Vulnerabilities', models.DO_NOTHING, db_column='vulnerabilities_cve')
    proof = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    first_found = models.DateField(blank=True, null=True)
    last_update = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'results'
        unique_together = (('hosts', 'vulnerabilities_cve'),)


class Users(models.Model):
    name = models.CharField(primary_key=True, max_length=45)
    full_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Vulnerabilities(models.Model):
    cve = models.CharField(primary_key=True, max_length=45)
    software = models.CharField(max_length=45, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    severity = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    cwe = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vulnerabilities'
