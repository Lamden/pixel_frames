import fs from 'fs'
export async function get(req, res) {
    let { event } = req.query;
    let eventData = {endDate: new Date(0)}

    try {
        eventData = JSON.parse(fs.readFileSync(`./events/${event}.json`, 'utf8'));
        eventData.artThingList = await Promise.all(eventData.artList.map(uid => global.db.models.PixelFrame.findOne({uid})))
    } catch (err) {
        console.log(err)
    }

    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(eventData));
}