<script>
    export let activity = {
        title:"",
        description:"",
        time:""
    }
</script>

<div class="border-blue-200 border-2 bg-red-200 rounded-lg text-sm justify-center">
    <h2 class="font-semibold">{activity.title}</h2>
    <p class="">{activity.description}</p>
    <p class="">{activity.time}</p>
    <div class="flex self-center justify-center items-center gap-1">
        <img src="./icon.png" class="custom_png h-3" alt="gps icon">
        <p class="text-gray-700">{activity.address}</p>
    </div>
</div>

<style>
    .custom_png {
        filter: invert(27%) sepia(8%) saturate(1097%) hue-rotate(188deg) brightness(98%) contrast(87%);
    }
</style>