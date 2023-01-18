<script>
	import { slide } from "svelte/transition";

	import LikeOrDislike from "../Buttons/LikeOrDislike.svelte";
	import GpsIcon from "../svg/GpsIcon.svelte";

	export let activityType = "restaurant";
	export let title = "Déjeuner";
	export let description = "Brunch luxe gucci tier";
	export let location = "114 rue de la briquetterie";

	let googleMapsSearchLink = function (location) {
		return "https://www.google.com/maps/search/?api=1&query=" + location;
	};

	let actualiseCard = (adress, name) => {
		description = name;
		location = adress;
	};

	// Callback on dislike
	import { getActivity, getRestaurant } from "../../lib/api.client.js";

	let dislikeCallback = async () => {
		let data;
		if (activityType === "restaurant") {
			data = await getRestaurant(2);
		} else {
			data = await getActivity(2);
		}
		console.log(data);
		actualiseCard(data.activity.adress, data.activity.name);
	};
</script>

<div
	class="flex flex-col gap-8 text-center py-4 px-3 border-2 border-soft-pink shadow-lg rounded-3xl w-full h-full"
>
	<div class="flex flex-col gap-3">
		<div class="flex flex-col gap-1">
			<p1>{title}</p1>
			{#key description}
				<p2 transition:slide={{ duration: 1000 }}>{description}</p2>
			{/key}
		</div>
		{#key location}
			<div
				transition:slide={{ duration: 1000 }}
				class="flex flex-row items-center text-center justify-center"
			>
				<div class="mb-1">
					<GpsIcon />
				</div>
				<p2 class="text-metal"
					><a
						href={location.includes("NA") && location.length < 4
							? ""
							: googleMapsSearchLink(location)}>{location}</a
					></p2
				>
			</div>
		{/key}
	</div>

	<div class="flex flex-row justify-around">
		<LikeOrDislike like={true} />
		<LikeOrDislike like={false} callback={dislikeCallback} />
	</div>
</div>
