<script>
	export let href;
	export let condition = true;
</script>

<a
	{href}
	class="text-center {$$props.class} {condition
		? ''
		: 'opacity-50 cursor-not-allowed'}"
>
	<h2 class="text-white"><slot /></h2>
</a>
