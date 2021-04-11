export async function get(req, res) {
    let releaseDate = Date.UTC(2021, 4, 19, 22)
    let serverDate = new Date()

    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(serverDate > releaseDate));
}