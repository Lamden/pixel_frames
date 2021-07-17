import http from 'http'
import { Server } from 'socket.io'

export const start = (port, db) => {
    const server = http.createServer();
    const io = new Server(server);

    io.on('connection', (socket) => {
        socket.on('join', (room) => {
            socket.join(room)
        });
    });

    /*
    setInterval(() => {
        io.to('auction-updates').emit("auction-update", "testing")
    }, 5000)
    */

    server.listen(port, () => {
        console.log(`listening on *:${port}`);
    });

    return io
}