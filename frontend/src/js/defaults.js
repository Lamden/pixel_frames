import {config} from "./config";

export const newPixelFrame = () => new Object({frames: [newPixelBoard()], speed: 500, created: new Date()})

export const newPixelBoard = () => Array.from(Array(config.totalPixels)).map((v)=> v = "B")

export const brushSizeMap = {
    "1": [0, 0],
    "2": [1, 2],
    "3": [2, 4]
}