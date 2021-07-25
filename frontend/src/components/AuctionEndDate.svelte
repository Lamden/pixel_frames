<script>
    import { onMount } from 'svelte'

    // Misc
    import { getTimeDelta } from '../js/utils'

    export let auctionInfo

    let timer = null

    $: endTime = new Date(auctionInfo.scheduled_end_date)
    $: startTime = new Date(auctionInfo.start_date)
    $: ended = auctionInfo.ended
    $: ended_early = auctionInfo.ended_early
    $: ended_earlyTime = new Date(auctionInfo.ended_early_date)
    $: currentTime = new Date()
    $: started = currentTime >= new Date(auctionInfo.start_date)
    $: hasEnded = ended ? true : currentTime > endTime
    $: deltaTime = determineTimeDelta(started, hasEnded, endTime, startTime, ended_early, ended_earlyTime)


    onMount(() => {
        timer = setInterval(updateTime, 1000)

        console.log({
            endTime, ended, ended_early, ended_earlyTime, currentTime, deltaTime, hasEnded, started, startTime
        })
        return () => {
            clearInterval(updateTime)
            timer = null
        }
    })

    const updateTime = () => currentTime = new Date();

    function determineTimeDelta(started, hasEnded, endTime, startTime, ended_early, ended_earlyTime){
        console.log({started, hasEnded, endTime, startTime, ended_early, ended_earlyTime})
        if (!started){
            return getTimeDelta(currentTime, startTime)
        }else{ß
            if (ended_early){
                return getTimeDelta(ended_earlyTime, currentTime)
            }
            return getTimeDelta(endTime, currentTime)
        }

    }

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
    {#if !started}
        {#if deltaTime.days === 0}
            Starts in {deltaTime.hours} Hrs {deltaTime.minutes} Mins {deltaTime.seconds} Secs
        {:else}
            Starts in {deltaTime.days} Days {deltaTime.hours} Hrs {deltaTime.minutes} Mins
        {/if}
    {:else}
        {#if hasEnded}
            Ended {deltaTime.hours} Hrs {deltaTime.minutes} Mins {deltaTime.seconds} Secs ago
        {:else}
            {#if deltaTime.days === 0}
                Ends in {deltaTime.hours} Hrs {deltaTime.minutes} Mins {deltaTime.seconds} Secs
            {:else}
                Ends in {deltaTime.days} Days {deltaTime.hours} Hrs {deltaTime.minutes} Mins
            {/if}
        {/if}
    {/if}

</p>
