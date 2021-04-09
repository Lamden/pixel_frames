<script>
    // MISC
    import { newPixelFrame } from '../js/defaults'
    import { frameStore, activeFrame } from '../js/stores'

    const handleClick = () => {
        frameStore.update(currentValue => {
            let newList = currentValue.unshift(newPixelFrame())
            console.log(newList)
            console.log({currentValue})
            activeFrame.set(0)
            return currentValue
        })
    }
</script>


<button class="button_text weight-600" on:click={handleClick}>NEW</button>