export async function get(req, res) {

    let priceData = await global.db.models.Prices.findOne({symbol: 'TAU'})
    if (!priceData) priceData = { currentPrice: 0}

    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(priceData));
}