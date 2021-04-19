export async function get(req, res) {

    let stampRatio = await global.models.StampRatio.findOne({symbol: 'TAU'})
    if (!stampRatio) stampRatio = { currentRatio: 0}

    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(stampRatio));
}