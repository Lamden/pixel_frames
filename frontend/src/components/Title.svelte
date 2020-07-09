<script>
    import { onMount } from 'svelte'
	import { letter_to_color, color_to_letter } from '../js/utils'

    export let fontSize = 8;

	$: framesColor = undefined;
    onMount(() => {
    	framesColor = letter_to_color['G'];
		const colorTimer = setInterval(changeColor, 1000)
		return () => {
			clearInterval(colorTimer)
		}
	})

    const changeColor = () => {
    	let currIndex = Object.keys(color_to_letter).indexOf(framesColor)
		let nextIndex = currIndex + 1
		let nextColor = Object.keys(color_to_letter)[nextIndex]
		if (!nextColor) framesColor = letter_to_color['G']
		else framesColor = nextColor
	}

</script>

<style>
	div{
		min-width: -moz-fit-content;
		min-width: max-content;
		text-align: center;
	}
	div > strong {
		transition: color, 0.5s;
	}
</style>

<div style={`font-size: ${fontSize}em`}>Pixel
    <strong style={`color: ${framesColor};`}>Frames</strong>
</div>