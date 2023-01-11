<script>
	import ActivityItem from "../../components/Items/ActivityItem.svelte";

	/** @type {import('./$types').PageData} */
	export let data;
</script>

{#if data.agenda === undefined}
	<h3>Aucun résultat</h3>
	<br />
	<a
		href="/plan"
		class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
	>
		Retour en arrière
	</a>
{:else}
	<div class="flex flex-col gap-6 md:gap-12">
		<div
			class="grid sm:grid-cols-2 grid-cols-1 gap-5 mb-5 place-items-center auto-cols-autor"
		>
			<ActivityItem
				title="Matin"
				description={data.agenda[0].name}
				location={data.agenda[0].adress}
			/>
			<ActivityItem
				title="Déjeuner"
				description={data.agenda[1].name}
				location={data.agenda[1].adress}
			/>
			<ActivityItem
				title="Après-midi"
				description={data.agenda[2].name}
				location={data.agenda[2].adress}
			/>
			<ActivityItem
				title="Diner"
				description={data.agenda[3].name}
				location={data.agenda[3].adress}
			/>
		</div>
		<div class="flex justify-center">
			<button
				on:click={() => {
					location.reload();
				}}
				class="bg-soft-pink rounded-3xl py-4 px-8 md:py-6 md:px-10 text-center"
			>
				<h2 class="text-white text-bold">Reroll !</h2>
			</button>
		</div>
	</div>
{/if}
