import { writable, get, derived } from 'svelte/store';
import { config } from './config.js'
import { newPixelFrame } from './defaults'

export const released = writable(false);
export const timeToRelease = writable(Date.UTC(2021, 3, 19, 22) - new Date());

export const totalPixels = writable(256)
export const currentColor = writable(['A','B'])
// export const frames = writable([Array.from(Array(config.totalPixels)).map((v)=> v = "B")])
export const currentFrame = writable(0)
//export const frameSpeed = writable(1000)

export const walletInstalled = writable('checking');
export const walletInfo = writable({});
export const userAccount = writable("");
export const autoTx = writable(false);
export const stampRatio = writable();

export const snackbars = writable([]);
export const currency = writable(0);
export const approvalAmount = writable(0);
export const showModal = writable({data: {}, show: false});
export const tabHidden = writable();

export const tauPrice = (() => {
    let store = writable([])
    let lastCheck

    if (typeof window !== 'undefined') {
        let lsValue = localStorage.getItem('tau_price')
        if (!lsValue) store.set(0)
        else store.set(parseFloat(lsValue))

        store.subscribe(current => localStorage.setItem('tau_price', JSON.stringify(current)))

        refreshPrice()
    }

    async function refreshPrice(){
        lastCheck = new Date()
        let priceData = await fetch('./tauPrice.json').then(res => res.json())
        store.set(priceData.currentPrice)
    }

    const setStore = (value) => store.set(value)


    return {
        subscribe: store.subscribe,
        get: () => get(store),
        refreshPrice,
        lastCheck
    }
})()

export const frameStore = (() => {
    let store = writable([])
    if (typeof window !== 'undefined') {
        let lsFrames = localStorage.getItem('saved_frames')
        if (!lsFrames) store.set([newPixelFrame()])
        else store.set(JSON.parse(lsFrames))

        store.subscribe(current => {
            let currentLsValue = localStorage.getItem('saved_frames')
            if (!currentLsValue) currentLsValue = []
            else currentLsValue = JSON.parse(currentLsValue)

            if (JSON.stringify(current) !== JSON.stringify(currentLsValue)) {
                if (current.length === 0) {
                    store.set([newPixelFrame()])
                    return
                }
                localStorage.setItem('saved_frames', JSON.stringify(current))
            }
        })
    }

    const setStore = (value) => store.set(value)

    return {
        subscribe: store.subscribe,
        get: () => get(store),
        update: store.update,
        set: setStore,
    }
})()

export const activeFrame = (() => {
    let store = writable(0)
    if (typeof window !== 'undefined') {
        let activeFrame = localStorage.getItem('active_frame')
        try{
            activeFrame = JSON.parse(activeFrame)
            if (!activeFrame) activeFrame = 0
        }catch (e) {
            activeFrame = 0
        }
        store.set(activeFrame)

        store.subscribe(current => {
            let currentLsValue = localStorage.getItem('active_frame')
            if (!currentLsValue) currentLsValue = null
            else currentLsValue = JSON.parse(currentLsValue)

            if (current !== currentLsValue) {
                localStorage.setItem('active_frame',current)
            }
        })
    }

    const setStore = (value) => store.set(value)

    return {
        subscribe: store.subscribe,
        get: () => get(store),
        set: setStore,
    }
})()

export const currentTool = (() => {
    let store = writable('fill')
    if (typeof window !== 'undefined') {
        let lsToolValue = localStorage.getItem('current_tool')
        if (lsToolValue) store.set(lsToolValue)

        store.subscribe(current => {
            let currentLsValue = localStorage.getItem('current_tool')
            if (!currentLsValue) currentLsValue = null

            if (current !== currentLsValue) {
                localStorage.setItem('current_tool', current)
            }
        })
    }

    const setStore = (value) => store.set(value)

    return {
        subscribe: store.subscribe,
        get: () => get(store),
        set: setStore,
    }
})()

export const brushSize = (() => {
    let store = writable('fill')
    if (typeof window !== 'undefined') {
        let lsValue = localStorage.getItem('brush_size')
        if (!lsValue) lsValue = 1
        if (lsValue) store.set(parseInt(lsValue))

        store.subscribe(current => {
            let currentLsValue = localStorage.getItem('brush_size')
            if (!currentLsValue) currentLsValue = null

            if (current !== currentLsValue) {
                localStorage.setItem('brush_size', current)
            }
        })
    }

    const setStore = (value) => store.set(value)

    return {
        subscribe: store.subscribe,
        get: () => get(store),
        set: setStore,
    }
})()

export const frames = derived(
    ([frameStore, activeFrame]), ([$frameStore, $activeFrame]) => {
        let framesValue = $frameStore[$activeFrame]
        if (!framesValue) return newPixelFrame().frames
        return $frameStore[$activeFrame].frames
    }
);
export const frameSpeed = derived(
    ([frameStore, activeFrame]), ([$frameStore, $activeFrame]) => {
        let framesValue = $frameStore[$activeFrame]
        if (!framesValue) return newPixelFrame().speed
        return $frameStore[$activeFrame].speed
    }
);