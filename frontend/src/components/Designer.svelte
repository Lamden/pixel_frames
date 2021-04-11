<script>
	// Components
	import PixelBoard from './PixelBoard.svelte'
	import Pallet from './Pallet.svelte'
	import Frames from './Frames.svelte'
	import Preview from './Preview.svelte'
	import ClearButton from './ClearButton.svelte'
	import DeleteButton from './DeleteButton.svelte'
	import CreateButton from "./CreateButton.svelte";
	import RangeSlider from './RangeSlider.svelte'
	import NewFrame from './NewFrame.svelte'
	import SavedFrames from './SavedFrames.svelte'
	import NewButton from './NewButton.svelte'
	import Tools from './Tools.svelte'

	// Misc
	import { frames, frameStore, activeFrame } from '../js/stores'

	let itemCreated = false;

	const handleCreated = () => {
		itemCreated = true
		setTimeout(() => itemCreated = false, 2100)
	}

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
	hr{
		color: var(--gray-5);
		width: 100%;
	}

	@media (min-width: 980px) {
		.designer {
			flex-direction: column;
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
			justify-content: space-evenly;
			border: 1px solid #afafaf;
		}
	}
</style>

<svelte:head>
	<title>Pixel Whale Art Designer!</title>
</svelte:head>

<div class="designer">
	<div class="flex-row">
		<div class="info flex-col" on:drap|preventDefault>
			<div class="flex-col">
				<Preview frames={$frames} showWatermark={false}/>
				<RangeSlider />
			</div>

			<div class="flex-col buttons shadowbox">
				<NewButton />
				<hr>
				<ClearButton />
				<DeleteButton />
				<NewFrame />
				<CreateButton on:created={handleCreated}/>
			</div>
		</div>
		<div class="flex-row pallet-board">
			<div class="flex-col">
				<Frames />
				<PixelBoard {itemCreated}/>
			</div>
			<div class="flex-col">
				<Pallet />
				<Tools />
			</div>
		</div>
	</div>
	<div>
		<SavedFrames />
	</div>
</div>