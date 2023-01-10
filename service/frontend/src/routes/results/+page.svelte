<script>
	import ActivityItem from "../../components/Items/ActivityItem.svelte";

	/** @type {import('./$types').PageData} */
	export let data;
</script>

<ActivityItem />
<p1>Sample data fetched</p1>
<p>{JSON.stringify(data)}</p>
