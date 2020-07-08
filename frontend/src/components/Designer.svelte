<script>
	import PixelBoard from './PixelBoard.svelte'
	import Pallet from './Pallet.svelte'
	import Frames from './Frames.svelte'
	import Preview from './Preview.svelte'
	import ClearButton from './ClearButton.svelte'
	import UploadButton from './UploadButton.svelte'

	import { frames } from '../js/stores'

	export let account;
</script>

<style>
	.info{
		padding: 0 50px;
	}
	.buttons{
		flex-grow: 1;
		justify-content: flex-end;
	}
	.pallet-board{
		align-items: center;
	}
</style>

<svelte:head>
	<title>Pixel Board</title>
</svelte:head>

<div class="flex-row">
	<div class="flex-col info">
		<Preview frames={$frames} title={false}/>
		<Frames />
		<div class="flex-col buttons">
			<ClearButton />
			<UploadButton />
		</div>
	</div>
	<div class="flex-row pallet-board">
		<Pallet />
		<PixelBoard />
	</div>
</div>
