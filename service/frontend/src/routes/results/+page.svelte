<script>
    import ActivityItem from "../../components/Items/ActivityItem.svelte";

    /** @type {import('./$types').PageData} */
    export let data;
</script>

{#if data.agenda === undefined }
    <h3>Aucun résultat</h3>
{:else}
    <div class="grid sm:grid-cols-2 grid-cols-1 gap-5 mb-5 place-items-center auto-cols-autor">
        <ActivityItem title="Matin" description="{data.agenda[0].name}" location="{data.agenda[0].adress}"/>
        <ActivityItem title="Déjeuner" description="{data.agenda[1].name}" location="{data.agenda[1].adress}"/>
        <ActivityItem title="Après-midi" description="{data.agenda[2].name}" location="{data.agenda[2].adress}"/>
        <ActivityItem title="Diner" description="{data.agenda[3].name}" location="{data.agenda[3].adress}"/>
    </div>
{/if}
