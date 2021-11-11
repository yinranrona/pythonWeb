from django.db import models
from datetime import date
from django.utils import timezone

# Create your models here.
class Project(models.Model):
    taskID = models.IntegerField(primary_key=True, default=0)
    taskName = models.TextField(null=True, blank=True)
    # labelID = models.ManyToManyField(null=True, blank=True, default='')
    personID = models.ForeignKey('Person', on_delete=models.CASCADE, default=0)
    planStartTime = models.DateTimeField(null=True, blank=True, default=timezone.now)
    planFinishTime = models.DateTimeField(null=True, blank=True, default=timezone.now)
    actualStartTime = models.DateTimeField(null=True, blank=True)
    actualFinishTime = models.DateTimeField(null=True, blank=True)
    dtcreate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    dtupdate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    def __str__(self):
        return 'タスクID：' + str(self.taskID) + ',タスク名：' + self.taskName

# class LabelManage(models.Model):
#     class Meta:
#         unique_together = (('labelIDFst', 'labelIDScd', 'labelIDThd'),)
#
#     labelID = models.IntegerField(primary_key=True, default=0)
#     # labelName = models.CharField(max_length= 10, default= ' ')
#     labelIDFst = models.ForeignKey('LabelFst', on_delete=models.CASCADE, default=0)
#     labelIDScd = models.ForeignKey('LabelScd', on_delete=models.CASCADE, default=0)
#     labelIDThd = models.ForeignKey('LabelThd', on_delete=models.CASCADE, default=0)
#     taskID = models.ManyToManyField('Project')
#
#     dtcreate = models.DateTimeField(null=True, blank=True, default=timezone.now)
#     dtupdate = models.DateTimeField(null=True, blank=True, default=timezone.now)
#     # taskID = models.ForeignKey(to=Project, unique=True, related_name='under_labels', null=True, blank=True, on_delete=models.CASCADE)
#     def __str__(self):
#         return 'ラベルID：' + str(self.labelID) + ',ラベル名：' + self.labelName

class LabelManage(models.Model):
    labelID = models.IntegerField(primary_key=True, default=0)
    labelName = models.CharField(max_length= 20, null=True, blank=True, default= '')
    labelChildID = models.ManyToManyField('Label1st',blank=True, default= '')
    taskID = models.ManyToManyField('Project',blank=True, default= '')
    dtcreate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    dtupdate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    def __str__(self):
        return 'ラベルID：' + str(self.labelID) +  ',ラベル名：' + self.labelName

class Label1st(models.Model):
    labelID = models.IntegerField(primary_key=True, default=0)
    labelName = models.CharField(max_length= 20, null=True, blank=True, default= '')
    labelChildID = models.ManyToManyField('Label2nd',blank=True, default= '')
    taskID = models.ManyToManyField('Project',blank=True, default= '')
    dtcreate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    dtupdate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    def __str__(self):
        return 'ラベルID：' + str(self.labelID) +  ',ラベル名：' + self.labelName

class Label2nd(models.Model):
    labelID = models.IntegerField(primary_key=True, default=0)
    labelName = models.CharField(max_length= 20, null=True, blank=True, default= '')
    labelChildID = models.ManyToManyField('Label3rd',blank=True, default= '')
    taskID = models.ManyToManyField('Project',blank=True, default= '')
    dtcreate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    dtupdate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    def __str__(self):
        return 'ラベルID：' + str(self.labelID) +  ',ラベル名：' + self.labelName

class Label3rd(models.Model):
    labelID = models.IntegerField(primary_key=True, default=0)
    labelName = models.CharField(max_length= 20, null=True, blank=True, default= '')
    labelChildID = models.ManyToManyField('Label4th',blank=True, default= '')
    taskID = models.ManyToManyField('Project',blank=True, default= '')
    dtcreate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    dtupdate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    def __str__(self):
        return 'ラベルID：' + str(self.labelID) +  ',ラベル名：' + self.labelName

class Label4th(models.Model):
    labelID = models.IntegerField(primary_key=True, default=0)
    labelName = models.CharField(max_length= 20, null=True, blank=True, default= '')
    taskID = models.ManyToManyField('Project',blank=True, default= '')
    dtcreate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    dtupdate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    def __str__(self):
        return 'ラベルID：' + str(self.labelID) +  ',ラベル名：' + self.labelName

class Person(models.Model):
    personID = models.IntegerField(primary_key=True, default=0)
    personName = models.CharField(max_length= 20, default= ' ')
    password = models.CharField(max_length= 2000, default= ' ')
    personImage = models.FileField(upload_to='profile_image')
    dtcreate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    dtupdate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    # taskID = models.ForeignKey(to=Project, unique=True, related_name='under_persons', null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return '社員ID：' + str(self.personID) + ',社員名：' + self.personName

# class ProjectLabelManage(models.Model):
#     # labelID = models.IntegerField(null=True, blank=True, default=0)
#     taskID = models.ForeignKey(to=Project, related_name='under_projectlabels', on_delete=models.CASCADE)
#     labelID = models.ForeignKey(to=LabelManage, related_name='under_labels', on_delete=models.CASCADE)
#     dtcreate = models.DateField(default=date.today)
#     dtupdate = models.DateField(default=date.today)
#     def __str__(self):
#         return str(self.taskID.taskID) + ',  ' + str(self.labelID.labelID)
        # return 'タスクID：' + str(self.taskID) + ',ラベルID：' + str(self.labelID)

class Comment(models.Model):
    # name = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(null=True, blank=True, max_length=50)
    comment = models.TextField()
    taskID = models.ForeignKey(to=Project, related_name='under_comments', null=True, blank=True, on_delete=models.CASCADE)
    dtcreate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    dtupdate = models.DateTimeField(null=True, blank=True, default=timezone.now)
    def __str__(self):
        return '社員名：' + self.name + ',コメント：' + self.comment
