export const config = {
    frameWidth: 25,
    totalPixels: 625,
    totalFrames: 8,
    infoContract: "con_pixel_whale_info_v1",
    masterContract: "con_pixel_whale_master_v1",
    networkType: "mainnet",
    currencySymbol: "TAU",
    domainName: "https://www.pixelwhale.com",
    blockExplorer: "https://mainnet.lamden.io",
    masternode: "https://masternode-01.lamden.io/"
}


export const stampLimits = (()=>{
    let stampValues = {}
    stampValues[config.masterContract] = {
        sell_thing: 90,
        like_thing: 90,
        transfer: 105,
        prove_ownership: 95
    }
    stampValues.currency = {
        approve: 25
    }
    return stampValues
})()