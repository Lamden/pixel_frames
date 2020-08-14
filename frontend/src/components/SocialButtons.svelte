<script>
    import { Email, HackerNews, Reddit, LinkedIn, Pinterest, Telegram, Tumblr, Vk, WhatsApp, Xing, Facebook, Twitter } from 'svelte-share-buttons-component';

    export let thingInfo

    let tunnel = "https://sweet-goose-47.serverless.social"
    let ngrok = "https://f2106a2c41eb.ngrok.io"

    let twitter_url = `${ngrok}/frames/${thingInfo.uid}`
    let facebook_url = `${tunnel}/frames/${thingInfo.uid}`
    let telegram_url = `${tunnel}/dynamic/${thingInfo.uid}.gif`
    let whatsapp_url = `${tunnel}/frames/${thingInfo.uid}`
    let reddit_url = `${tunnel}/dynamic/${thingInfo.uid}.gif`
    let description = thingInfo.description
    let title = thingInfo.name

</script>
<p>Share it on social media </p>
<div >
    <Twitter class="share-button" text={title} url={twitter_url} />
    <Facebook class="share-button" url={facebook_url} />
    <Telegram class="share-button" text={title} url={telegram_url} />
    <Reddit class="share-button" {title} url={reddit_url} />
<!--
    <Email subject="{title}" body="{desc} {url}" />
    <HackerNews class="share-button" {title} {url} />
    <Reddit class="share-button" {title} {url} />
    <LinkedIn class="share-button" {url} />
    <Tumblr class="share-button" {title} {url} caption="{title}" />
    <Pinterest class="share-button" description={title} />
    <Vk class="share-button" {title} {url} />
    <Xing class="share-button" {title} {url} />
   -->
</div>

