<script>
	import Geolocation from "svelte-geolocation";
	let getPosition = false;
	let coord = [];

	// Date handling
	import { onMount } from "svelte";
	import Anchor from "../../components/Buttons/Anchor.svelte";

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
	$: validCoord = coord.length == 2;
	$: validDate = dateString != "";
	$: validInformations = validCoord && validDate;
</script>

<div
	class="flex flex-col gap-10 text-center xl:w-3/5 md:text-left md:p-10 md:border-soft-yellow md:border-dashed md:border-13 md:rounded-3xl"
>
	<h2>When ?</h2>

	<h2 class="text-white">
		<input
			class="bg-soft-blue px-3 md:px-10 py-8 rounded-3xl dark:text-white dark:[color-scheme:dark]"
			type="date"
			name="date"
			id="date"
			bind:value={dateString}
		/>
	</h2>

	<h2>Where ?</h2>

	<button
		on:click={() => (getPosition = true)}
		class="bg-soft-pink px-10 py-8 rounded-3xl lg:w-10/12 xl:w-11/12"
	>
		<h2 class="text-white">Partager ma position</h2>
	</button>

	<Geolocation
		{getPosition}
		on:position={(e) => {
			coord = [e.detail.coords.latitude, e.detail.coords.longitude];
		}}
	/>

	<Anchor
		href="/results?date={dateString}&coords={coord}"
		class="bg-soft-pink px-2 py-4 rounded-3xl lg:w-10/12 xl:w-11/12"
		bind:condition={validInformations}>Voir mon programme</Anchor
	>

	<div class="text-left">
		<h3 class={validDate ? "text-green-200" : "text-red-200"}>
			{validDate ? "Date correct" : "Date non correcte"}
		</h3>
		<h3 class={validCoord ? "text-green-200" : "text-red-200"}>
			{validCoord ? "Coordonnées reçue" : "Veuillez partager votre position"}
		</h3>
	</div>
</div>
