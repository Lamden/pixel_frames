/* /frontend/src/wallet_approval.js   */
import { config } from './config.js'

const approvalRequest = {
    appName: 'Pixel Frames',
    description: 'Approve this website to start creating and owning unique pixel animations!',
    contractName: config.masterContract,
    networkType: 'testnet'
}

approvalRequest.logo = 'logo-192.png'
approvalRequest.background = 'wallet/background.png'

export { approvalRequest };
