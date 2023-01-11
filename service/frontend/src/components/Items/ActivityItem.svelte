<script>
	import LikeOrDislike from "../Buttons/LikeOrDislike.svelte";
	import GpsIcon from "../svg/GpsIcon.svelte";

	export let title = "Déjeuner";
    export let description = "Brunch luxe gucci tier";
    export let location = "114 rue de la briquetterie";
</script>

<div
        class="flex flex-col gap-8 text-center py-4 px-3 border-2 border-soft-pink shadow-lg rounded-3xl max-w-fit"
>
    <div class="flex flex-col gap-3">
        <div class="flex flex-col gap-1">
            <p1>{title}</p1>
            <p2>{description}</p2>
        </div>
        <div class="flex flex-row items-center">
            <div class="mb-1">
                <GpsIcon/>
            </div>
            <p2 class="text-metal">{location}</p2>
        </div>
    </div>
    <div class="flex flex-row justify-around">
        <LikeOrDislike like={true}/>
        <LikeOrDislike like={false}/>
    </div>
</div>
