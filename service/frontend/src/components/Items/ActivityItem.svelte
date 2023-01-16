<script>
	import LikeOrDislike from "../Buttons/LikeOrDislike.svelte";
	import GpsIcon from "../svg/GpsIcon.svelte";
	import { getActivity, getRestaurant } from "../../lib/api.js";

	export let title = "Déjeuner";
	export let description = "Brunch luxe gucci tier";
	export let location = "114 rue de la briquetterie";

	let googleMapsSearchLink = function (location) {
		return "https://www.google.com/maps/search/?api=1&query=" + location;
	};
</script>

<div
	class="flex flex-col gap-8 text-center py-4 px-3 border-2 border-soft-pink shadow-lg rounded-3xl w-full h-full"
>
	<div class="flex flex-col gap-3">
		<div class="flex flex-col gap-1">
			<p1>{title}</p1>
			<p2>{description}</p2>
		</div>
		<div class="flex flex-row items-center text-center justify-center">
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
	</div>
	<div class="flex flex-row justify-around">
		<LikeOrDislike like={true} />
		<LikeOrDislike like={false} />
	</div>
</div>
