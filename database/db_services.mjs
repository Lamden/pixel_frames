import { getBlockService } from '../blockserviceAPI/blockservice.mjs'

export const getServices = () => {
    return {
        blockservice: getBlockService()
    }
}