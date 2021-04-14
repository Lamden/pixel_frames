import fs from 'fs'
export async function get(req, res) {
    let { artist } = req.query;

    var whitelist = JSON.parse(fs.readFileSync('./src/js/whitelist.json', 'utf8'));

    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(whitelist.artists.includes(artist)));
}