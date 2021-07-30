export const getAuctionQueries = (db) => {
    async function getAllActiveAuctions(limit, offset) {
        let match = {
            $match: {ended: false}
        }
        let sort = {$sort: {"start_date": -1.0}}
        let skip = {$skip: parseInt(offset)}
        let reclimit = {$limit: limit}
        let dataPipeline = []
        let countPipeline = [match]
        if (offset) {
            dataPipeline = [match, sort, skip, reclimit]
        } else dataPipeline = [match, sort, reclimit]
        let facet = {$facet: {data: dataPipeline, "count": countPipeline}}
        let collation = {locale: "en_US", numericOrdering: true}

        return db.models.AuctionHistory
            .aggregate([facet])
            .collation(collation)
    }

    async function getActiveAuction(uid) {
        return db.models.AuctionHistory.findOne({uid, ended: false})
    }

    async function getAuctions(uidList = []) {
        console.log({uidList})
        return db.models.AuctionHistory.find({uid: {$in: uidList}, ended: false})
    }

    async function getAllAuctions() {
        return db.models.AuctionHistory.find({})
    }

    return{
        getAllActiveAuctions,
        getAuctions,
        getActiveAuction,
        getAllAuctions
    }
}