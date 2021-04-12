<script>
	import {onMount} from 'svelte'
	import {letter_to_color, color_to_letter} from '../js/utils'
	import CreatedWithLove from "./CreatedWithLove.svelte";

	export let fontSize = 8;
	export let subtitle = true;

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
		color: var(--primary);
	}
	div > strong {
		transition: color 1s ease-in-out ;
	}
	p{
		margin: -2rem 0 0;
	}

</style>

<div style={`font-size: ${fontSize}em`}>Pixel
    <strong style={`color: ${framesColor};`}>Whale</strong>
</div>
{#if subtitle}
	<p class="text-color-primary-dark weight-600">
		On-chain NFT Pixel Animations created by YOU!
	</p>
{/if}