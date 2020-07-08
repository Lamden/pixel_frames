import { writable, get } from 'svelte/store';

export const totalPixels = writable(256)
export const currentColor = writable('black')
export const frames = writable([Array.from(Array(get(totalPixels)).keys())])
export const currentFrame = writable(0)

export const walletInstalled = writable('checking');
export const walletInfo = writable({});
export const txResults = writable({});
export const userAccount = writable("");