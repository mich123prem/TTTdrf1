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

class Zone(models.Model):
    lettername = models.CharField(max_length=50) # MUST ADD LIBRARY NAME TO MAKE UNIQUE ?
    sequencenumber = models.IntegerField()
    description = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    activity = models.ManyToManyField(Activity, through='ActivityZone')

    def __str__(self):
        return self.lettername


class  ActivityZone(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    startTime = models.DateTimeField(auto_now=False) # App registers time
    countingUser = models.IntegerField() # **TODO: foreign key to a user
    numberOfVisitors = models.IntegerField() # THE COUNT ITSELF
    def __str__(self):
        return str(self.startTime) + " " + str(self.countingUser) + " " + str(self.numberOfVisitors)
# ** TODO: how to enforce uniqueness constraints:
#          if an activity is repeated the same day? overwrite?
#          if an activity is releated for a zone within
#          the hour, maybe it is not a new activity but overwrites the earlier one?
#          What is implemented in the model, and what ini the view?

