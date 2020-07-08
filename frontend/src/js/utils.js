export const color_to_number = {
    '#ffffff00': '00',
    'black': '01',
    'white': '02',
    'gray': '03',
    'red': '04',
    'maroon': '05',
    'pink': '06',
    'greenyellow':'07',
    'green':'08',
    'forestgreen':'09',
    'blue':'10',
    'darkblue':'11',
    'aqua':'12',
    'purple':'13',
    'orange':'14',
    'yellow': '15'
}

export const number_to_color = {
    '00': '#ffffff00',
    '01': 'black',
    '02': 'white',
    '03':'gray',
    '04':'red',
    '05':'maroon',
    '06':'pink',
    '07':'greenyellow',
    '08':'green',
    '09':'forestgreen',
    '10':'blue',
    '11':'darkblue',
    '12':'aqua',
    '13':'purple',
    '14':'orange',
    '15':'yellow'
}

export const padNumber = (num) => {
    var s = "000000000" + num;
    return s.substr(s.length-2);
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
           frames[i][s] = number_to_color[n]
       })
   })
    return frames
}