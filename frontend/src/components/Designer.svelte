<script>
	import PixelBoard from './PixelBoard.svelte'
	import Pallet from './Pallet.svelte'
	import Frames from './Frames.svelte'
	import Preview from './Preview.svelte'
	import ClearButton from './ClearButton.svelte'
	import DeleteButton from './DeleteButton.svelte'
	import UploadButton from './UploadButton.svelte'
	import NewFrame from './NewFrame.svelte'

	import { frames } from '../js/stores'

</script>

<style>
	.designer {
		display: flex;
		flex-direction: column;
	}
	.info{
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: end;
		margin-bottom: 2rem;
		padding: 0 20px;
	}
	.frames{
		justify-content: center;
		align-items: center;
	}
	.buttons{
		background: white;
		width: unset;

	}
	.pallet-board{
		align-items: flex-start;
	}
	.shadowbox{
		background: white;
		padding: 10px 25px 1rem;
		margin: 0;
		height: unset;
	}

	@media (min-width: 980px) {
		.designer {
			flex-direction: row;
		}
		.info{
			flex-direction: column;
			align-items: center;
			padding-right: 3rem;
			margin-bottom: 0;
		}
		.frames{
			flex-grow: 1;
		}
		.shadowbox{
		    height: 150px;
			justify-content: space-evenly;
		}
	}
</style>

<svelte:head>
	<title>Pixel Board</title>
</svelte:head>

<div class="designer">
	<div class="info flex-col" on:drap|preventDefault>
		<Preview frames={$frames}/>
		<div class="flex-col frames">
			<Frames />
		</div>
		<div class="flex-col buttons shadowbox">
			<ClearButton />
			<DeleteButton />
			<NewFrame />
			<UploadButton />
		</div>
	</div>
	<div class="flex-row pallet-board">
		<PixelBoard />
		<Pallet />
	</div>
</div>
