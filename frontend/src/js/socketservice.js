import io from 'socket.io-client'
import { socket_config } from './config'

export const start = () => {
    let socket = io(`${socket_config.host}:${socket_config.port}`)

    let joinedRooms = {}

    socket.on('connect', () => {
        console.log("connected to pixel whale server")
    })

    function joinRoom(room){
        if (joinedRooms[room]) return

        joinedRooms[room] = true
        socket.emit('join', room)
    }

    function leaveRoom(room){
        delete joinedRooms[room]
        socket.emit('leave', room)
    }

    return{
        joinRoom,
        leaveRoom,
        on: (event, callback) => socket.on(event, callback)
    }
}