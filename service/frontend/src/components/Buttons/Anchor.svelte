<script>
	export let href;
	export let condition = true;
</script>

<a
	{href}
	class="bg-soft-pink px-10 py-8 rounded-3xl lg:w-10/12 xl:w-11/12 text-center {condition
		? ''
		: 'opacity-50 cursor-not-allowed'}"
>
	<h2 class="text-white"><slot /></h2>
</a>
