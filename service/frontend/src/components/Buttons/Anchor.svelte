<script>
	export let href;
	export let condition = true;
</script>

<a
	class="text-center {$$props.class} {condition
		? ''
		: 'opacity-50 cursor-not-allowed pointer-events-none'}"
	{href}
>
	<h3 class="text-white">
		<slot />
	</h3>
</a>
