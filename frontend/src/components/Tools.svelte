<script>
    import FillButton from './FillButton.svelte'
    import PaintButton from './PaintButton.svelte'
    import BrushSize from './BrushSize.svelte'
</script>

<style>
    div{
        margin-top: 1rem;
        padding-left: 3rem;
    }
</style>

<div class="flex-col">
    <div class="flex-row">
        <PaintButton />
        <FillButton />
    </div>
    <BrushSize />
</div>