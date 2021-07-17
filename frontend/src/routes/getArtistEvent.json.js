import fs from 'fs'
export async function get(req, res) {
    let { event } = req.query;
    let eventData = {endDate: new Date(0)}

    try {
        eventData = JSON.parse(fs.readFileSync(`./events/${event}.json`, 'utf8'));
        eventData.artThingList = await Promise.all(eventData.artList.map(uid => global.db.models.PixelFrame.findOne({uid})))
        if (eventData.eventType === "auction"){
            eventData.auctions = {data:[]}
            let auctions = await global.db.queries.getAuctions(eventData.artList)
            eventData.auctions.data = await global.db.queries.populateThingInfo(auctions)
        }
    } catch (err) {
        console.log(err)
    }

    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(eventData));
}