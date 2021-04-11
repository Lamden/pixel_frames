import fs from 'fs'
export async function get(req, res) {
    let { artist } = req.query;
    console.log(artist)

    console.log(__dirname)
    var whitelist = JSON.parse(fs.readFileSync('./src/js/whitelist.json', 'utf8'));
    console.log(whitelist)

    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(whitelist.artists.includes(artist)));
}