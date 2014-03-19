from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.template import RequestContext, loader
from django.db import transaction
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
import redis

def chat_home(request):
    return HttpResponse('chat home')
    
@login_required
def chat_with_user(request, user_id = None):
    extra_context	=	{}
    sender_recipient    =   ChatSenderRecipient.objects.filter(user_1__in = [request.user.id, user_id], user_2__in = [request.user.id, user_id])
    if sender_recipient:
        chat_id = sender_recipient[0]
    else:   
        user_id = User.objects.get(pk = user_id)
        chat_id = ChatSenderRecipient.objects.create(user_1 = request.user, user_2 = user_id)

    extra_context['chat_id']    =   chat_id.id
    return render_to_response('chat_with_user.html', extra_context, context_instance=RequestContext(request))
    
@csrf_exempt
def node_api(request, chat_id = None):
    try:
        #Get User from sessionid
        session = Session.objects.get(session_key=request.POST.get('sessionid'))
        user_id = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(id=user_id)
        #Create comment
        # Comments.objects.create(user=user, text=request.POST.get('comment'))
        #Once comment has been created post it to the chat channel
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.publish('message' + chat_id, user.username + ': ' + request.POST.get('comment'))
        return HttpResponse("Everything worked :)")
    except Exception, e:
        return HttpResponseServerError(str(e))