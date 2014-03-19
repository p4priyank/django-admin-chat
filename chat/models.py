from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class ChatUser(models.Model):
    email   =   models.CharField(blank=False,null=False, max_length = 255)
    username   =   models.CharField(blank=False,null=False, max_length = 255)
    
    def __unicode__(self):
        return self.username
    
    class Meta:
        app_label = 'user_chat'
        managed     =   False
        db_table    =   'auth_user'
        
class ChatSenderRecipient(models.Model):
    user_1  =   models.ForeignKey(User, related_name =   'user_1')
    user_2  =   models.ForeignKey(User, related_name =   'user_2')
    
    def __unicode__(self):
        return self.user_1.username + " - " + self.user_2.username