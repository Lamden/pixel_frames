<script>
    import { onMount } from 'svelte'

    // Misc
    import { getTimeDelta } from '../js/utils'

    export let auctionInfo

    let timer = null

    $: endTime = new Date(auctionInfo.scheduled_end_date)
    $: ended = auctionInfo.ended
    $: currentTime = new Date()
    $: deltaTime = getTimeDelta(currentTime, endTime)
    $: hasEnded = ended ? true : currentTime > endTime


    onMount(() => {
        timer = setInterval(updateTime, 1000)
        return () => {
            clearInterval(updateTime)
            timer = null
        }
    })

    const updateTime = () => currentTime = new Date();

</script>

<style>
    p{
        padding: 5px 0;
        margin: 0;
        width: 100%;
        background: var(--primary-dark);
        color: var(--color-white-primary-tint);
        border-radius: 0 0 10px 10px;
    }
</style>

<p class="text-center"
    class:hasEnded={hasEnded}
    class:hasStarted={!hasEnded}>
    {#if hasEnded}
        Auction has ended
    {:else}
        {#if deltaTime.days === 0}
            Ends in {deltaTime.hours} Hrs {deltaTime.minutes} Mins {deltaTime.seconds} Secs
        {:else}
            Ends in {deltaTime.days} Days {deltaTime.hours} Hrs {deltaTime.minutes} Mins
        {/if}
    {/if}
</p>
