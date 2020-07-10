import { writable, get } from 'svelte/store';
import { config } from './config.js'

export const totalPixels = writable(256)
export const currentColor = writable(['A','C'])
export const frames = writable([Array.from(Array(config.totalPixels)).map((v)=> v = "B")])
export const currentFrame = writable(0)
export const frameSpeed = writable(1000)

export const walletInstalled = writable('checking');
export const walletInfo = writable({});
export const userAccount = writable("");

export const snackbars = writable([]);
export const dTau = writable(0);