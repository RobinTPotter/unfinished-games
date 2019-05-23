const express = require('express');
const app = express();
const server = require('http').Server(app);
var mustacheExpress = require('mustache-express');
app.engine('html', mustacheExpress());

const port = 3000
app.use(express.static('public'))

app.set('view engine', 'html');
app.set('views', __dirname + '/views');

app.get('/donkey', function(req, res) { res.render('donkey', { "a": "robin"}) })

var io = require('socket.io')(server) //require socket.io module and pass the http object (server)

server.listen(port, () => console.log(`Example app listening on port ${port}!`))

io.sockets.on('connection', function (socket) {// WebSocket Connection

    var lightvalue = 0; //static variable for current status
    socket.on('server_receive', function(data) { //get light switch status from client
        lightvalue = data; 
        console.log(lightvalue);     
    });
  
    setTimeout(function() { socket.emit('client_receive' , 'poo')  }, 2000)
  
});


function hashthing(thing) {
    return crypto.createHmac('sha256', secret)
                   .update(thing)
                   .digest('hex');
}

function player(name, password) {

    this.name = name;
    this.password = hashthing(password)

    console.log(this.name, this.password)

}


