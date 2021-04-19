<script>
	import {onMount} from 'svelte'
	import {letter_to_color, color_to_letter} from '../js/utils'
	import CreatedWithLove from "./CreatedWithLove.svelte";

	export let fontSize = 8;
	export let subtitle = true;
	export let showFullLogo = false;

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
		justify-content: center;

	}
	.top-margin{
		margin-top: 3rem;
	}
	span{
		position: relative;
		transition: color 1s ease-in-out ;
		z-index: 1;
	}
	strong {
		position: relative;
		color: var(--primary);
		z-index: 1;
	}
	.right-margin{
		margin-right: 10px;
	}
	p{
		margin: -4rem 0 0;
		position: relative;
		right: -42px;
	}
	img{
		position: relative;
		width: 13%;
	}


</style>

<div class="flex-row" style={`font-size: ${fontSize}em`} class:top-margin={showFullLogo}>
	{#if showFullLogo}<img src="./img/logo_full-512.png" alt="pixel whale full logo"/>{/if}
	<strong class:right-margin={showFullLogo}>Pixel</strong>
    <span style={`color: ${framesColor};`}>Whale</span>
</div>

{#if subtitle}
	<p class="text-color-primary-dark weight-600">
		On-chain NFT Pixel Animations created by YOU!
	</p>
{/if}