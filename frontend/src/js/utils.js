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


export const serializeFrame = (pixelData) => {
    let data = ''
    pixelData.forEach(pixel => {
        if (Number.isInteger(pixel)) data += '00'
        else data += color_to_number[pixel]
    })
    return data
}

export const serializeFrames = (pixelArrays) => {
    let data = ''
    pixelArrays.forEach(pixelArray => {
        data += serializeFrame(pixelArray)
    })
    return data;
}

export const stringToArrays = (str, size) => {
    var chunks = [];
    const arrayLen = str.length / size;
    for (var i = 0; i <= arrayLen - 1; i += 1) {
        chunks.push(str.slice(size * i, size * (i + 1)));
    }
    return chunks
}

export const decodeFrames = (data) => {
   let frames = stringToArrays(data, 512)
   frames.forEach((c, i) => {
       frames[i] = stringToArrays(c, 2)
       frames[i].forEach((n, s) => {
           frames[i][s] = letter_to_color[n]
       })
   })
    return frames
}

export const emptyFrame = (totalPixels) => Array.from(Array(totalPixels)).map((v)=> v = "B")