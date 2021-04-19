import { config } from './config.js'
import { blockexplorer_api } from './blockexplorer_api.js'
import { snackbars, currency, userAccount, approvalAmount, showModal } from "./stores";
import { get } from 'svelte/store'
import Lamden from 'lamden-js'
import { validateTypes } from 'types-validate-assert'

let API = new Lamden.Masternode_API({hosts: [config.masternode]})

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

export const formatThings = (things) => {
    if (!things) return
    things.forEach(thing => {
        thing.frames = decodeFrames(thing.thing)
    })
    return things
}

export const drawFrame = (canvas, pixels, pixelSize, watermark) => {
    if (!pixels || !canvas) return
    let pixelSizeRatio = 10
    let ctx = canvas.getContext('2d')
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    pixels.forEach((letter, index) => {
        ctx.fillStyle = letter_to_color[letter];
        let rowBefore = Math.floor(index / config.frameWidth)
        let rowAdj = (pixelSize * rowBefore)
        let y = Math.floor(index / config.frameWidth)
        let x = (index - ( y * config.frameWidth)) * pixelSize
        ctx.fillRect(x, rowAdj, pixelSize, pixelSize);
    })

    if (watermark) {
        ctx.font = `${pixelSize / pixelSizeRatio}em Roboto`;

        ctx.textBaseline = 'middle';
        ctx.textAlign = 'center';
        ctx.strokeStyle = watermark.strokeColor;
        ctx.lineWidth = 1;
        ctx.miterLimit=2;
        ctx.strokeText(watermark.text, canvas.width / 2, canvas.height - (canvas.height / 4));
        ctx.fillStyle = watermark.fillColor;
        ctx.fillText(watermark.text, canvas.width / 2, canvas.height - (canvas.height / 4));
    }
}

export const emptyFrame = () => Array.from(Array(config.totalPixels)).map((v)=> v = "B")

export const isEmptyFrame = (frame) => {return JSON.stringify(frame) === JSON.stringify(emptyFrame())}

export const framesEmpty = (frames) => {
    return frames.map(frame => isEmptyFrame(frame)).filter(f => !f).length == 0
}

export const createSnack = (snackInfo) => {
    const { type, title, body, delay } = snackInfo;
    snackbars.update(curr => {
        let snack = { type, time: new Date().getTime(), title, body, delay: delay || 5000 }
        return [...curr, snack]
    })
}

export const processTxResults = (results) => {
    if (results.data) {
        if (results.data.errors) return results.data.errors
        if (results.data.resultInfo) {
            createSnack({
                title: results.data.resultInfo.title,
                body: results.data.resultInfo.subtitle,
                type: results.data.resultInfo.type
            })
            refreshTAUBalance()
        }
    }
    return []
}

export const refreshTAUBalance = async () => {
    if (!get(userAccount)) return
    let keyList = [
		{
			"contractName": "currency",
			"variableName": "balances",
			"key": get(userAccount)
		}
	]
    const res = await blockexplorer_api.getKeys(keyList)
    let data = valuesToBigNumber(res)
    let balance = data[`currency.balances:${keyList[0].key}`]
    if (balance) currency.set(balance)
}

export const checkForApproval = async () => {
    if (!get(userAccount)) return
    let keyList = [
        {
            "contractName": "currency",
            "variableName": "balances",
            "key": `${get(userAccount)}:${config.masterContract}`
        }
    ]
    const res = await blockexplorer_api.getKeys(keyList)
    let approval = res[`currency.balances:${keyList[0].key}`]

    if (approval === null ) approval = toBigNumber(0)
    else approval = toBigNumber(approval)
    approvalAmount.set(approval)

    return approval
}

export const needsApproval = async () => {
    let approval = await checkForApproval()
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
    let name_uid = await sha256(name.toLowerCase().replace(" ", ""))
    const res = await fetch(`./name_taken.json?name_uid=${name_uid}`)
    const taken = await res.json();
    return taken
}

export const alreadyLiked = async (uid) => {
    let account = get(userAccount)
    //console.log({account, uid})
    if (account === '' || typeof window === 'undefined') return false;

    let lsValue = localStorage.getItem(`${uid}:${account}:liked`)
    //console.log({lsValue})
    if (lsValue !== null) return true;

    const liked = await fetch(`./${uid}.json?account=${account}`).then(res => res.json())
    //console.log(liked)

    if (liked === true) localStorage.setItem(`${uid}:${account}:liked`, true)

    return liked
}

export const formatAccountAddress = (account, lsize = 8, rsize = 4) => {
    return account.substring(0,lsize) + '...' + account.substring(account.length - rsize)
}

export const createWatermark = (thingInfo, account) => {
    if (account === thingInfo.owner) return
    return {
        text: config.watermark,
        fillColor: "#21d6ab"
    }
}

export const updateInfo = (thingInfo, updates) => {
    Object.keys(updates).forEach(update => {
        //console.log({update, thingInfoValue: thingInfo[update], updateValue: updates[update]})
        if (typeof thingInfo[update] !== 'undefined') thingInfo[update] = updates[update]
    })
    return thingInfo
    //console.log(thingInfo)
}

export const closeModel = () => {
    const modal = get(showModal)
    if (modal.show) showModal.set({modalData:{}, show: false})
}

export const dedupArray = (arr) => {
    const seen = new Set();
    return arr.filter(el => {
         const duplicate = seen.has(el._id);
         seen.add(el._id);
         return !duplicate;
    });
}

export const stringToFixed = (value, precision) => {
	if (isBigNumber(value) && precision ) value = value.toFixed(precision)
	if (!value) return "0.0"
		try {
			var values = value.split('.')
		} catch {
			var values = value.toString().split('.')
		}
		if (!values[1]) return value
		else {
			if (values[1].length < precision) precision = values[1].length
				let decValue = parseInt(values[1].substring(0, precision))
			if (decValue === 0) return `${values[0]}`
			else {
				let decimals = values[1].substring(0, precision)
				for (let i = precision - 1; i >= 0; i--) {
					if (decimals[i] === '0') precision -= 1
					else i = -1
			}
			return `${values[0]}.${values[1].substring(0, precision)}`
		}
	}
}

export const toBigNumber = (value) => {
  if (Lamden.Encoder.BigNumber.isBigNumber(value)) return value
  return Lamden.Encoder.BigNumber(value)
}

export const isBigNumber = (value) => Lamden.Encoder.BigNumber.isBigNumber(value)

export const toBigNumberPrecision = (value = null, precision) => {
	if (value === null) return toBigNumber("0")
	try{
		return toBigNumber(stringToFixed(toBigNumber(value).toFixed(precision), precision))
	}catch(e){
		return toBigNumber("0")
	}
}
export const displayBalanceToPrecision = (value, precision) => {
	if (!value) return "0"
	return toBigNumberPrecision(value, precision).toFormat({  decimalSeparator: '.', groupSeparator: ',', groupSize: 3})
}
export function valuesToBigNumber(obj) {
    if (typeof obj === 'object') {
        for (let property in obj) {
            if (!isBigNumber(obj[property])){
                if (	property === 'thing' ) {
                    // ignore these values
                } else if (typeof obj[property] === 'string') {
                    // Check if item is a string
                    if (!isNaN(parseFloat(obj[property]))) {
                        obj[property] = toBigNumberPrecision(obj[property], 8)
                    }
                } else if (typeof obj[property] === 'number') {
                    obj[property] = toBigNumberPrecision(obj[property], 8)
                } else if (typeof obj[property] === 'object') {
                    valuesToBigNumber(obj[property])
                }
            }
        }
    }
    return obj
}

export const isLamdenKey = ( key ) => {
    if (validateTypes.isStringHex(key) && key.length === 64) return true;
    return false;
}

export const timeDelta = (timestamp) => {
    timestamp = new Date(timestamp)
    let seconds = Math.floor((Date.now() - timestamp) / 1000);
    let unit = "second";
    let direction = "ago";
    if (seconds < 0) {
        seconds = -seconds;
        direction = "from now";
    }
    let value = seconds;
    if (seconds >= 31536000) {
        value = Math.floor(seconds / 31536000);
        unit = "year";
    } else if (seconds >= 86400) {
        value = Math.floor(seconds / 86400);
        unit = "day";
    } else if (seconds >= 3600) {
        value = Math.floor(seconds / 3600);
        unit = "hour";
    } else if (seconds >= 60) {
        value = Math.floor(seconds / 60);
        unit = "minute";
    }
    if (value != 1)
        unit = unit + "s";
    return value + " " + unit + " " + direction;
}

export const copyToClipboard = ( textTOcopy='', callback=undefined ) => {
    if (validateTypes.isString(textTOcopy)){
        try{
            var dummy = document.createElement("input");
            document.body.appendChild(dummy);
            dummy.setAttribute("id", "copyhelper");
            document.getElementById("copyhelper").value=textTOcopy;
            dummy.select();
            document.execCommand("copy");
            document.body.removeChild(dummy);

        } catch (e) {
            throw new Error('unable to copy')
        }
        if (callback){callback()}
    }
};

export const indexToPos = (index) => {
    return {
        y: parseInt(index / config.frameWidth),
        x: index - (parseInt(index / config.frameWidth) * config.frameWidth)
    }
}

export const hasNulls = (array) => {
    let hasNulls = false
    array.forEach((frame) => {
        if (frame.includes(null)){
            hasNulls = true
        }
    })
    return hasNulls
}