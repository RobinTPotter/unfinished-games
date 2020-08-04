var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

function ping() {
    socket.emit('ping', {'hello': 'there' });
}


function ready(g) {
    socket.emit('ready', {'game': g});
}
