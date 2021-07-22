import { getAuctionQueries } from "./queries/auctions.mjs";
import { getPixelWhaleQueries } from "./queries/pixelwhale.mjs";
import { getProcessedQueries } from "./queries/processed.mjs";
import { getMiscQueries } from "./queries/misc.mjs";

export const getQueries = (db) => {
    return {
        ...getAuctionQueries(db),
        ...getPixelWhaleQueries(db),
        ...getProcessedQueries(db),
        ...getMiscQueries(db)
    }
}