<script>
	import ActivityItem from "../../components/Items/ActivityItem.svelte";

	/** @type {import('./$types').PageData} */
	export let data;
</script>

{#if data.agenda === undefined }
    <h3>Aucun résultat</h3>
{:else}
    {#each data.agenda as activity, i}
        <ActivityItem description="{activity.name}" location="{activity.adress}"/>
    {/each}
{/if}
