<script>
	import Geolocation from "svelte-geolocation";
	let getPosition = false;
	let coord;

	// Date handling
	import { onMount } from "svelte";

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
		let:coords
		let:loading
		let:success
		let:error
		let:notSupported
	/>

	<a href="/result"><h2 class="text-center">- Voir mon planning -</h2></a>
</div>
