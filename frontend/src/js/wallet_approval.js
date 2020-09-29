/* /frontend/src/wallet_approval.js   */
import { config } from './config.js'

const approvalRequest = {
    appName: 'Lamden Demo App',
    version: '1.1.0',
    contractName: config.masterContract,
    networkType: 'testnet'
}

approvalRequest.logo = 'logo-192.png'
approvalRequest.background = 'wallet/background.png'

export { approvalRequest };
