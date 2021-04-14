<script>
    // Misc
    import { copyToClipboard } from '../js/utils'

    export let width = "20px"
    export let color = "var(--primary)"
    export let textToCopy = ""

    const handleClick = () => {
        copyToClipboard(textToCopy, () => {
            color = "var(--color-success)"
            setTimeout(() => color = "var(--primary)", 3000)
        })
    }
</script>

<style>
    div{
        cursor: pointer;
        align-self: center;
    }
</style>
<div on:click={handleClick} style={`height: ${width};`}>
    <svg {width} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" data-reactroot="">
        <path fill={color} d="M8 6V3C8 2.45 8.45 2 9 2H20C20.55 2 21 2.45 21 3V17C21 17.55 20.55 18 20 18H16V7C16 6.45 15.55 6 15 6H8Z" clip-rule="evenodd" fill-rule="evenodd" undefined="1"></path>
        <path stroke-linejoin="round" stroke-width="1" stroke="white" d="M8 6H15C15.55 6 16 6.45 16 7V18"></path>
        <path fill={color} d="M15 22H4C3.45 22 3 21.55 3 21V7C3 6.45 3.45 6 4 6H15C15.55 6 16 6.45 16 7V21C16 21.55 15.55 22 15 22Z" clip-rule="evenodd" fill-rule="evenodd" undefined="1"></path>
    </svg>
</div>
