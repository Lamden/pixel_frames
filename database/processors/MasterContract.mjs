import util from "util";

export const masterContractProcessor = (database, socket_server) =>{
    const processorName = 'Master Contract'
    let db = database

    function processUpdate(update, loader=false){
        console.log(util.inspect({processorName, update}, false, null, true))
    }

    return {
        setDb: (database) => db = database,
        processUpdate
    }
}