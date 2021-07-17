//import blockserviceAPI from '../../blockserviceAPI/blockservice.mjs'
import io_client from 'socket.io-client'
import { config } from "./js/config";

export const start = (io_server, database_service_url='http://localhost', database_service_port=3536) => {
    let databaseSocket = io_client(`${database_service_url}:${database_service_port}`);

    databaseSocket.on('connect', () => {
        console.log("CONNECTED TO DATABASE SERVICE")
        databaseSocket.emit('join', 'auction-updates')
        databaseSocket.emit('join', 'market-updates')
        databaseSocket.emit('join', 'thing-events')
    })

    databaseSocket.on('auction-update', (data) => {
        //data = JSON.parse(data)
        //console.log(data)
        io_server.to('auction-updates').emit(data.type, data)
    })

    databaseSocket.on('market-update', (data) => {
        //data = JSON.parse(data)
        //console.log(data)
        io_server.to('market-updates').emit(data.type, data)
    })

    databaseSocket.on('main-events', (data) => {
        //data = JSON.parse(data)
        //console.log(data)
        io_server.to('thing-events').emit(data.type, data)
    })

    io_server.on('connection', socket => {
        socket.on('join', (room) => {
            socket.join(room)
        })
        socket.on('leave', (room) => {
            socket.leave(room)
        })
    })
}
