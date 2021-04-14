<script>
    // Components
    import FormCreateShareLink from './FormCreateShareLink.svelte'
    import FormDeleteShareLink from './FormDeleteShareLink.svelte'
    import CopyButton from './CopyButton.svelte'

    // Misc
    import { userAccount, showModal } from '../js/stores'

    export let thingInfo
    export let owner

	$: owner = $userAccount === thingInfo.owner;
    $: ownerShareLink = getShareLink(thingInfo)


    const openModal = (modal) => {
        showModal.set({modalData:{thingInfo, modal: modal, updateInfo}, show:true})
    }

    const updateInfo = (update) => {
        storeLinkInLS(update.shareLink)
        ownerShareLink = getShareLink(thingInfo)
    }

    const storeLinkInLS = (link) => {
        if (typeof window === 'undefined') return
        let shareLinks = localStorage.getItem(`sharelinks`)
        try {
            shareLinks = JSON.parse(shareLinks)
            if (!shareLinks) shareLinks = {}
        }catch(e){
            shareLinks = {}
        }
        shareLinks[thingInfo.uid] = link
        localStorage.setItem(`sharelinks`, JSON.stringify(shareLinks))
    }

    const getShareLink = (thing) => {
        if (typeof window === 'undefined') return
        let shareLinks = localStorage.getItem(`sharelinks`)
        if (!shareLinks) return false
        try {
            shareLinks = JSON.parse(shareLinks)
            let shareLink = shareLinks[thing.uid]
            if (!shareLink) return  false
            else return shareLink
        }catch(e){
            return  false
        }
    }
</script>

<style>
    .container{
        margin-bottom: 1rem;
    }
    input{
        width: 100%;
        margin-right: 8px;
        height: 26px;
        padding: 0 8px;
    }
    .create-link{
        margin: auto;
    }
    .link-row{
        align-items: end;
    }
</style>

{#if owner}
    <div class="container flex-col">
        {#if !ownerShareLink}
            <button class="create-link button" on:click={() => openModal(FormCreateShareLink)}>Create A File Link</button>
        {:else}
            <h3>Share Link:</h3>
            <div class="flex-row link-row">
                <input value={`${window.location.origin}/gif/${ownerShareLink}.gif`} />
                <CopyButton width="20px" textToCopy={`${window.location.origin}/gif/${ownerShareLink}.gif`}/>
            </div>
            <div class="flex-row flex-justify-end">
                <a class="button_text small"
                   href="{`${window.location.origin}/gif/${ownerShareLink}.gif`}"
                   download="{`${thingInfo.name}.gif`}">
                    download file
                </a>
                <button class="button_text small" on:click={() => openModal(FormDeleteShareLink)}>delete link</button>
            </div>
        {/if}
    </div>
{/if}