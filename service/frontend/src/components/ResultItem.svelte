<script>
    export let data = {
        activities:[],
        date:""
    }
</script>

{#if data.activities.length === 0}
    {#if data.date === ""}
        <br>
    {:else}
        <h1 class="text-lg">Aucune activité n'est prévue pour le {data.date}</h1>
    {/if}
{:else}
    <h1 class="text-lg font-semibold">{data.date}</h1>
    <div class="gap-14 flex-column items-center text-center">
    {#each data.activities as activity}
        <div class="border-blue-200 border-2 bg-red-200 rounded-lg text-sm">
            <h2 class="font-semibold">{activity.title}</h2>
            <p class="">{activity.description}</p>
            <p class="">{activity.time}</p>
        </div>
    {/each}
    </div>
{/if}

