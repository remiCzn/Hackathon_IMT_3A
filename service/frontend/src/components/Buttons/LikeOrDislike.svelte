<script>
	import Heart from "../svg/Heart.svelte";
	import Cross from "../svg/Cross.svelte";

	export let like = true;
	export let callback = () => {};
</script>

<button
	class="circleBase custom-shadow flex items-center justify-center"
	on:click={callback}
>
	{#if like}
		<Heart />
	{:else}
		<Cross />
	{/if}
</button>

<style>
	.circleBase {
		height: 80px;
		width: 80px;
		background-color: #fff;
		border-radius: 50%;
		background-repeat: no-repeat;
		background-position: center;
		background-size: 70% auto;
		transition: all 0.3s ease;
		cursor: pointer;
	}
	.custom-shadow {
		box-shadow: 2px 4px 4px rgba(0, 0, 0, 0.25);
	}

	.custom-shadow:hover {
		box-shadow: 2px 4px 4px rgba(0, 0, 0, 0.25), 0 0 0 2px #edb5a3;
	}

	.custom-shadow:active {
		box-shadow: 2px 4px 4px rgba(0, 0, 0, 0.25), 0 0 0 2px #edb5a3 inset;
	}
</style>
