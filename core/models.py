from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=128)
    def __str__(self):
        return self.name


class Error(models.Model):
    content_id = models.IntegerField()
    line = models.IntegerField()
    correct = models.CharField(max_length=100)
    wrong = models.CharField(max_length=100)
    request_id = models.CharField(max_length=64)
    datetime = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        get_latest_by = 'datetime'

    def __str__(self):
        return self.content_id + ' ' + self.line + ' ' + self.datetime + ' ' + self.correct

    def __repr__ (self):
        return self.content_id + ' ' + self.line + ' ' + self.datetime + ' ' + self.correct


class Setting(models.Model):
    setting_name = models.CharField(max_length=255, unique=True)
    default_value = models.CharField(max_length=500)
    def __str__(self):
        return self.setting_name


class UserSetting(models.Model):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    value = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class UserLastLine(models.Model):
    content_id = models.IntegerField()
    line = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    datetime = models.DateTimeField()


class Word(models.Model):
    difficulty = models.IntegerField()
    word = models.CharField(max_length=100)


class Definitions(models.Model):
    id = models.IntegerField(primary_key=True)
    word = models.CharField(max_length=100)
    wordtype = models.CharField(max_length=100)
    definition = models.TextField()

    class Meta:
        managed = False
        db_table = 'definitions'


class Content(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'content'


class Line(models.Model):
    id = models.IntegerField(primary_key=True)
    content_id = models.IntegerField()
    line_id = models.IntegerField()
    text = models.TextField()
    difficulty = models.IntegerField()

    class Meta:
        db_table = 'line'


class LineWord(models.Model):
    id = models.IntegerField(primary_key=True)
    content_id = models.IntegerField()
    line_id = models.IntegerField()
    order = models.IntegerField()
    original = models.CharField(max_length=200)
    difficulty = models.IntegerField()
    definition = models.TextField()
    pos = models.CharField(max_length=100)

    class Meta:
        db_table = 'line_word'
        index_together = [
            ('content_id', 'line_id'),
        ]
