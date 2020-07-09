import { config } from './config.js'

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

export const serializeFrames = (pixelArrays, speed) => {
    console.log(pixelArrays)
    let arrayCopy = JSON.parse(JSON.stringify(pixelArrays))
    console.log(arrayCopy)
    let data = ''
    arrayCopy.forEach(pixelArray => {
        data += serializeFrame(pixelArray);
        console.log(data.length)
    })
    console.log(data.length)
    return data + ':' + speed;
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
    console.log(frames)
    frames.forEach((c, i) => {
        frames[i] = stringToArrays(c, 1)
    })
    console.log(frames)
    return frames
}

export const emptyFrame = (totalPixels) => Array.from(Array(config.totalPixels)).map((v)=> v = "B")