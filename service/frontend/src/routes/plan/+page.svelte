<script>
	import Geolocation from "svelte-geolocation";
	// Date handling
	import { onMount } from "svelte";
	import Anchor from "../../components/Buttons/Anchor.svelte";

	let getPosition = false;
	let coord = [];
	let rayon = 10;

	let now = new Date(),
		month,
		day,
		year;
	let dateString;

	onMount(() => {
		(month = "" + (now.getMonth() + 1)),
			(day = "" + now.getDate()),
			(year = now.getFullYear());

		if (month.length < 2) month = "0" + month;
		if (day.length < 2) day = "0" + day;

		dateString = [year, month, day].join("-");
	});

	// Process handling
	$: validCoord = coord.length === 2;
	$: validDate = dateString !== "";
	$: validInformations = validCoord && validDate;
</script>

<div
	class="flex flex-col text-center xl:w-3/5 md:text-left md:p-10 md:border-soft-yellow md:border-dashed md:border-13 md:rounded-3xl"
>
	<h2 class="my-5">When ?</h2>

	<h3 class="text-white mt-5">
		<input
			bind:value={dateString}
			class="bg-soft-blue px-3 md:px-10 py-8 rounded-3xl dark:text-white dark:[color-scheme:dark]"
			id="date"
			name="date"
			type="date"
		/>
	</h3>
	<div class="my-1 text-left">
		<h4 class={validDate ? "text-green-200" : "text-red-200"}>
			{validDate ? "" : "Date incorrecte"}
		</h4>
	</div>

	<h2 class="my-5">Where ?</h2>

	<button
		class="bg-soft-pink px-10 py-8 mb-0 mt-5 rounded-3xl lg:w-10/12 xl:w-11/12"
		on:click={() => (getPosition = true)}
	>
		<h3 class="text-white">Partager ma position</h3>
	</button>

	<Geolocation
		{getPosition}
		on:position={(e) => {
			coord = [e.detail.coords.latitude, e.detail.coords.longitude];
		}}
	/>
	<div class="text-left">
		<h4 class={validCoord ? "text-green-200" : "text-red-200"}>
			{validCoord ? "Coordonnées reçue" : "Veuillez partager votre position"}
		</h4>
	</div>
	<div class="flex content-center justify-center mt-5">
		<label class="text-lg" for="myRange">Rayon: </label>
		<input
			bind:value={rayon}
			class="mx-3 rounded-lg overflow-hidden appearance-none bg-soft-pink h-3 my-auto w-128"
			id="myRange"
			max="50"
			min="0"
			type="range"
		/>
		<p class="text-lg">{rayon} km</p>
	</div>

	<Anchor
		bind:condition={validInformations}
		class="bg-soft-purple my-10 px-2 py-4 rounded-3xl lg:w-10/12 xl:w-11/12"
		href="/results?date={dateString}&rayon={rayon}&latit={coord[0]}&long={coord[1]}"
		>Voir mon programme
	</Anchor>
</div>
