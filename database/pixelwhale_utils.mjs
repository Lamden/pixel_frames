const totalPixels = 625

export const color_to_letter = {
    //BTW
    '#ffffff00': 'A',
    '#ffffff': 'B',
    //Greys
    '#F5F5F5':'C',
    '#D4D4D4': 'D',
    '#A3A3A3': 'E',
    '#525252': 'F',
    '#000000': 'G',
    //Reds
    '#FEE2E2':'H',
    '#FCA5A5':'I',
    '#EF4444':'J',
    '#B91C1C':'K',
    '#7F1D1D':'L',
    //Orange
    '#FFEDD5':'M',
    '#FDBA74':'N',
    '#F97316':'O',
    '#EA580C':'P',
    '#C2410C':'Q',
    //Brown
    '#FEF3C7':'R',
    '#FCD34D':'S',
    '#F59E0B':'T',
    '#B45309':'U',
    '#78350F':'V',
    //Yellow
    '#ffffd5':'W',
    '#ffff8c':'X',
    '#ffff00':'Y',
    '#e2e200':'Z',
    '#a5a500':'[',
    //Lime
    '#ECFCCB':']',
    '#BEF264':'^',
    '#84CC16':'_',
    '#4D7C0F':'`',
    '#3F6212':'a',
    //Green
    '#D1FAE5': 'b',
    '#6EE7B7': 'c',
    '#10B981': 'd',
    '#047857': 'e',
    '#064E3B': 'f',
    //Blue
    '#DBEAFE': 'g',
    '#93C5FD': 'h',
    '#3B82F6': 'i',
    '#1D4ED8': 'j',
    '#1E3A8A': 'k',
    //Cyan
    '#CFFAFE':'l',
    '#67E8F9':'m',
    '#06B6D4':'n',
    '#0E7490':'o',
    '#164E63':'p',
    //Purple
    '#EDE9FE': 'q',
    '#C4B5FD': 'r',
    '#8B5CF6': 's',
    '#6D28D9': 't',
    '#4C1D95': 'u',
    //Pink
    '#FCE7F3': 'v',
    '#F9A8D4': 'w',
    '#EC4899': 'x',
    '#BE185D': 'y',
    '#831843': 'z'
}

export const letter_to_color = {
    //BTW
    'A':'#ffffff00',
    'B':'#ffffff',
    //Greys
    'C':'#F5F5F5',
    'D':'#D4D4D4',
    'E' :'#A3A3A3',
    'F' :'#525252',
    'G' :'#000000',
    //Reds
    'H' :'#FEE2E2',
    'I' :'#FCA5A5',
    'J' :'#EF4444',
    'K' :'#B91C1C',
    'L' :'#7F1D1D',
    //Orange
    'M' :'#FFEDD5',
    'N' :'#FDBA74',
    'O' :'#F97316',
    'P' :'#EA580C',
    'Q' :'#C2410C',
    //Brown
    'R' :'#FEF3C7',
    'S' :'#FCD34D',
    'T' :'#F59E0B',
    'U' :'#B45309',
    'V' :'#78350F',
    //Yellow
    'W' :'#ffffd5',
    "X" :'#ffff8c',
    'Y' :'#ffff00',
    'Z' :'#e2e200',
    '[' :'#a5a500',
    //Lime
    ']' :'#ECFCCB',
    '^' :'#BEF264',
    '_' :'#84CC16',
    '`' :'#4D7C0F',
    'a' :'#3F6212',
    //Green
    'b' :'#D1FAE5',
    'c' :'#6EE7B7',
    'd' :'#10B981',
    'e' :'#047857',
    'f' :'#064E3B',
    //Blue
    'g' :'#DBEAFE',
    'h' :'#93C5FD',
    'i' :'#3B82F6',
    'j' :'#1D4ED8',
    'k' :'#1E3A8A',
    //Cyan
    'l' :'#CFFAFE',
    'm' :'#67E8F9',
    'n' :'#06B6D4',
    'o' :'#0E7490',
    'p' :'#164E63',
    //Purple
    'q' :'#EDE9FE',
    'r' :'#C4B5FD',
    's' :'#8B5CF6',
    't' :'#6D28D9',
    'u' :'#4C1D95',
    //Pink
    'v':'#FCE7F3',
    'w' :'#F9A8D4',
    'x' :'#EC4899',
    'y' :'#BE185D',
    'z' :'#831843'
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
    let frames = stringToArrays(data, totalPixels)
    frames.forEach((c, i) => {
        frames[i] = stringToArrays(c, 1)
    })
    return frames
}

export const formatThings = (things) => {
    if (!things) return
    things.forEach(thing => {
        thing.frames = decodeFrames(thing.thing)
    })
    return things
}