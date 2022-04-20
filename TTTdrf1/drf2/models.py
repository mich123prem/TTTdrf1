from django.db import models

# Create your models here.
# **TODO: Change models so that. Zones are project dependent (they are repeated for each project
# **TODO: Change models to acommodate for relation properties (sammenhengattributter)
# ** TODO: Check THE Many-to-many constraints (CASCADE / DELETE)
class Activity(models.Model):
    code = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default = "", blank=True)
    activities = models.ManyToManyField( Activity, blank="True" )
    #zones = models.ManyToOneRel('Zone')
    def __str__(self):
        return self.name

class Counting(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    observerName=models.CharField(max_length=50, default = "", blank=True)
    startTime = models.DateTimeField(auto_now=False, blank=True)
    class Meta:
        unique_together= ['project','startTime']
        # TODO: ** a counting at a project at a library needs to be unique
        #    For simplicity projects can be unique across domain (all libraries)

class Zone(models.Model):
    lettername = models.CharField(max_length=50) # MUST ADD LIBRARY NAME TO MAKE UNIQUE ?
    sequencenumber = models.IntegerField()
    description = models.CharField(max_length=255)
    observerName=models.CharField(max_length=255, default = "", blank=True)
    comment = models.CharField(max_length=255, default = "", blank=True)
    activities = models.ManyToManyField(Activity, through='ActivityZone')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='zones')


    class Meta:
        unique_together= ['lettername', 'sequencenumber', 'project']

    def __str__(self):
        return self.lettername


class  ActivityZone(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    #startTime = models.DateTimeField(auto_now=False, blank=True) # App registers time True for establish time
    countingUser = models.IntegerField(default=0) # **TODO: foreign key to a user
    numberOfVisitors = models.IntegerField(default=-1) # THE COUNT ITSELF
    counting = models.ForeignKey(Counting, default=1, on_delete=models.CASCADE) # ** TODO: counting 1 must be a dummy

    class Meta:
        unique_together = ['activity', 'zone']

    def __str__(self):
        return  str(self.zone.description) + " " +  str(self.activity.code) + " " +  str(self.numberOfVisitors)
# ** TODO: how to enforce uniqueness constraints:

# ** TODO: if an activity is repeated the same day? overwrite?
#          if an activity is releated for a zone within
#          the hour, maybe it is not a new activity but overwrites the earlier one?
#          What is implemented in the model, and what ini the view?


