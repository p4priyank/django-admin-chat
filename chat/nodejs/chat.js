var http = require('http');
var server = http.createServer().listen(4000);
var io = require('socket.io').listen(server);
var cookie_reader = require('cookie');
var querystring = require('querystring');
 
var redis = require('socket.io/node_modules/redis');
var sub = redis.createClient();
 
//Subscribe to the Redis chat channel
sub.subscribe('chat');
var pub = redis.createClient(); //publish cli
 
//Configure socket.io to store cookie set by Django
io.configure(function(){
    io.set('authorization', function(data, accept){
        if(data.headers.cookie){
            data.cookie = cookie_reader.parse(data.headers.cookie);
            return accept(null, true);
        }
        return accept('error', false);
    });
    io.set('log level', 1);
});

//Grab message from Redis and send to client
sub.on('message', function(channel, message){
    //console.log('channel ==',channel);
    //console.log('message ==',message);
    io.sockets.emit(channel, message);
});

io.sockets.on('connection', function (socket) {
    var target_chat_id;
    //Client is sending message through socket.io
    socket.on('send_message', function (message) {

        target_chat_id = JSON.parse(message)['chat_id'];
        target_user_id = JSON.parse(message)['user_id'];
        var message =   JSON.parse(message)['msg'];
        
        // subscribe to created channel
        sub.subscribe('message'+target_chat_id);
        sub.subscribe('userchannel'+target_user_id);
        
        values = querystring.stringify({
            comment: message,
            sessionid: socket.handshake.cookie['sessionid'],
        });
        var options = {
            host: 'localhost',
            port: 8000,
            path: '/node_api/' + target_chat_id,
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': values.length
            }
        };
        //Send message to Django server
        var req = http.get(options, function(res){
            res.setEncoding('utf8');
            //Print out error message
            res.on('data', function(message){
                if(message != 'Everything worked :)'){
                    console.log('Message: ' + message);
                }
            });
        });
        
        req.write(values);
        req.end();
    });
});