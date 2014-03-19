django-admin-chat

========================================

About : Admin user can chat with one another . 

Todo : admin can chat with any user .

Dependencies : 

    #http://redis.io/download
    sudo apt-get install redis-server
     
    #https://github.com/andymccurdy/redis-py
    sudo pip install redis 

    sudo apt-get install nodejs

Add 'chat' to INSTALLED_APPS directory . 

Add this urls in your root urls.py file : 

    url(r'^chathome/?$','chat.views.chat_home',name='chat_home'),
    url(r'^chatwithuser/(?P<user_id>\d+)/?$','chat.views.chat_with_user',name='chat_with_user'),
    url(r'^node_api/(?P<chat_id>\d+)/?$', 'chat.views.node_api', name='node_api'),
    
Add template path of chat application : 
    
    os.path.join(os.path.dirname(__file__), '..', 'chat', 'templates')   ## django 1.6 specific. modify according to your django version.

perform `syncdb` :
    
    python manage.py syncdb

Go to chat application folder :    
    #go to nodejs directory 
    
    cd nodejs
    
    #Run following commands . make sure 'npm' is installed.
    
    #https://github.com/LearnBoost/socket.io
    npm install socket.io
     
    #https://github.com/shtylman/node-cookie
    npm install cookie
    
    #run : chat.js server js.
    node chat.js

Start development server at default port (8000)  :

    python manage.py runserver
