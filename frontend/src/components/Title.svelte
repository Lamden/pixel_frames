<script>
    import { onMount } from 'svelte'
	import {number_to_color, color_to_number, padNumber} from '../js/utils'

    export let fontSize = 8;

	$: framesColor = number_to_color['06'];
    onMount(() => {
		const colorTimer = setInterval(changeColor, 1000)
		return () => {
			clearInterval(colorTimer)
		}
	})

    const changeColor = () => {
		let nextNumber = padNumber(parseInt(color_to_number[framesColor]) + 1)
		if (!number_to_color[nextNumber]) framesColor = number_to_color['03']
		else framesColor = number_to_color[nextNumber]

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