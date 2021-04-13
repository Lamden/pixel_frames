import CoinGecko from 'coingecko-api';
const CoinGeckoClient = new CoinGecko();



export const update_tau_price = (models) => {
    let coinName = "lamden"

    const updatePrice = async  () => {
        await CoinGeckoClient.coins.fetchTickers(coinName)
            .then(async res => {
                if (!res || !res.data){
                    checkAgain()
                    return
                }
                let txBitData = res.data.tickers.find(f => f.market.name === "Txbit")
                if (!txBitData) checkAgain()
                let prices = await models.Prices.findOne({symbol: 'TAU'})

                if (!prices){
                    prices = await new models.Prices({
                        symbol: 'TAU',
                    })
                }

                prices.currentPrice = txBitData.converted_last.usd
                prices.lastUpdated = new Date()

                await prices.save()
                checkAgain()
            })
            .catch(() => checkAgain());


    }

    const checkAgain = () => setTimeout(updatePrice, 120000)

    return { updatePrice }
}

