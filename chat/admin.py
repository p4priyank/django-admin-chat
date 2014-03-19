from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import ChatUser
from django.core.urlresolvers import reverse, reverse_lazy

class ChatUserInline(admin.TabularInline):
    model = ChatUser
    extra = 0
    max_num = 15

class UserChatAdmin(admin.ModelAdmin):
    list_display = ('username','chat_url')
    inlines = [ChatUserInline,]

    def chat_url(self, obj):
        return '<a href="#" onclick="window.open(\'%s\',name=\'Chat Window\',\'height=500,width=800,resizable=yes,scrollbars=yes\');">%s</a>' % (reverse_lazy('chat_with_user',kwargs={'user_id':obj.id}), "Chat")
    chat_url.allow_tags = True
    chat_url.short_description = 'Chat with user'

admin.site.register(ChatUser,UserChatAdmin)

