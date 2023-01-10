<script>
	import ActivityItem from "../../components/Items/ActivityItem.svelte";
    import {onMount} from "svelte";

	/** @type {import('./$types').PageData} */
	export let data;
    onMount(() => {
        data = JSON.parse(data);
    })
</script>

<div>{data}</div>

{#if data === {}}
    <h1>Aucun résultat</h1>
{:else}
    <ActivityItem />
{/if}
<p>{JSON.stringify(data)}</p>
