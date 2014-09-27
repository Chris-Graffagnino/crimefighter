from django.db import models
from django.utils.translation import ugettext_lazy as _
import jsonfield


class Crimes(models.Model):
    date = models.DateField()
    time = models.TimeField(blank=True)
    offense = models.CharField(max_length=180)
    surname = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50, blank=True)



class TaskHistory(models.Model):
    # Relations
    # Attributes - mandatory
    name = models.CharField(
        max_length=100,
        verbose_name=("Task name"),
        help_text=_("Select a task to record"),
        )
    # Attributes - optional
    history = jsonfield.JSONField(
        default={},
        verbose_name=_("history"),
        help_text=_("JSON containing the tasks history")
        )
    # Manageer
    # Functions

    # Meta & unicode
    class Meta:
        verbose_name = _('Task History')
        verbose_name_plural = _('Task Histories')

    def __unicode__(self):
        return _("Task History of Task: %s") % self.name

class Result(models.Model):
    """ I deleted this model...REDO!!""" 
   
    
