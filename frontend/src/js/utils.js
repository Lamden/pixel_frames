import { config } from './config.js'
import { snackbars, dTau, userAccount } from "./stores";
import { get } from 'svelte/store'

export const color_to_letter = {
    //BTW
    'black': 'A',
    '#ffffff00': 'B',
    'white': 'C',
    //Greys
    'lightgray': 'D',
    'darkgray': 'E',
    'dimgray': 'F',
    //Reds
    'lightcoral': 'G',
    'red':'H',
    'darkred':'I',
    //Yellow
    'khaki':'J',
    'yellow':'K',
    'darkkhaki':'L',
    //Blue
    'lightblue':'M',
    'blue':'N',
    'darkblue':'O',
    //Green
    'lightgreen': 'P',
    'green': 'Q',
    'darkgreen': 'R',
    //Orange
    'sandybrown': 'S',
    'orange': 'T',
    'darkorange': 'U',
    //Purple
    'violet': 'V',
    'purple': 'W',
    'indigo': 'X',
    //Brown
    'burlywood':'Y',
    'saddlebrown':'Z'
}

export const letter_to_color = {
    //BTW
    'A' : 'black',
    'B' : '#ffffff00',
    'C' : 'white',
    //Greys
    'D' : 'lightgray',
    'E' : 'darkgray',
    'F' : 'dimgray',
    //Reds
    'G' : 'lightcoral',
    'H' : 'red',
    'I' : 'darkred',
    //Yellow
    'J' : 'khaki',
    'K' : 'yellow',
    'L' : 'darkkhaki',
    //Blue
    'M' : 'lightblue',
    'N' : 'blue',
    'O' : 'darkblue',
    //Green
    'P' : 'lightgreen',
    'Q' : 'green',
    'R' : 'darkgreen',
    //Orange
    'S' : 'sandybrown',
    'T' : 'orange',
    'U' : 'darkorange',
    //Purple
    'V' : 'violet',
    'W' : 'purple',
    'X' : 'indigo',
    //Brown
    'Y' : 'burlywood',
    'Z' : 'saddlebrown',
}


export const replaceAll = (string, char, replace) => {
  return string.split(char).join(replace);
}

export const loadEmptyFrames = (pixelArrays) => {
    for (let i = 0; i < 4; i += 1){
        if (!pixelArrays[i]) pixelArrays[i] = emptyFrame()
    }
}

export const serializeFrame = (pixelArray) => {
    return replaceAll(pixelArray.toString(), ",","");
}

export const serializeFrames = (pixelArrays) => {
    let arrayCopy = JSON.parse(JSON.stringify(pixelArrays))
    let data = ''
    arrayCopy.forEach(pixelArray => {
        data += serializeFrame(pixelArray);
    })
    return data;
}

export const stringToArrays = (str, size) => {
    let chunks = [];
    const arrayLen = str.length / size;
    for (let i = 0; i <= arrayLen - 1; i += 1) {
        chunks.push(str.slice(size * i, size * (i + 1)));
    }
    return chunks
}

export const decodeFrames = (data) => {
    let frames = stringToArrays(data, config.totalPixels)
    frames.forEach((c, i) => {
        frames[i] = stringToArrays(c, 1)
    })
    return frames
}

export const emptyFrame = () => Array.from(Array(config.totalPixels)).map((v)=> v = "B")

export const isEmptyFrame = (frame) => {return JSON.stringify(frame) === JSON.stringify(emptyFrame())}

export const framesEmpty = (frames) => {
    return frames.map(frame => isEmptyFrame(frame)).filter(f => !f).length == 0
}

export const createSnack = (title, body, type) => {
    snackbars.update(curr => {
        let snack = { type, time: new Date().getTime(), title, body }
        return [...curr, snack]
    })
}

export const processTxResults = (results) => {
    console.log(results)
    if (results.data) {
        if (results.data.errors) return results.data.errors
        if (results.data.resultInfo) {
            createSnack(
                results.data.resultInfo.title,
                results.data.resultInfo.subtitle,
                results.data.resultInfo.type
            )
            refreshTAUBalance(get(userAccount))
        }
    }
    return []
}

export const refreshTAUBalance = async (account) => {
    const res = await fetch(`${config.masternode}/contracts/currency/balances?key=${account}`)
    const data = await res.json();
    if (!data.value) dTau.set(0)
    else dTau.set(data.value);
}

export const sha256 = async (message) => {
    // encode as UTF-8
    const msgBuffer = new TextEncoder('utf-8').encode(message);

    // hash the message
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);

    // convert ArrayBuffer to Array
    const hashArray = Array.from(new Uint8Array(hashBuffer));

    // convert bytes to hex string
    const hashHex = hashArray.map(b => ('00' + b.toString(16)).slice(-2)).join('');
    return hashHex;
}

export const nameTaken = async (name) => {
    let hash = await sha256(name.toLowerCase().replace(" ", ""))
    const res = await fetch(`${config.masternode}/contracts/${config.infoContract}/S?key=names:${hash}`)
    const data = await res.json();
    return !!data.value
}