/* /frontend/src/wallet_approval.js   */
import { config } from './config.js'

const approvalRequest = {
    appName: 'Pixel Whale Testing',
    version: '3.0',
    contractName: config.masterContract,
    networkType: config.networkType
}

const charms = [
    {
        name: 'Owned',
        variableName: "balances",
        key: "<wallet vk>",
        formatAs: "number",
        iconPath: "logo-192.png"
    }
]
approvalRequest.charms = charms
approvalRequest.logo = 'wallet/logo.png'
approvalRequest.background = 'wallet/background.png'

export { approvalRequest };
