<script>
    let result = {
        activities:[],
        date:""
    }

    import { onMount } from 'svelte';
	
	let now = new Date(), month, day, year;
	let dateString;
	
	onMount(()=> {
        month = '' + (now.getMonth() + 1),
        day = '' + now.getDate(),
        year = now.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    dateString = [year, month, day].join('-');
	})

    async function getActivities() {
        const response = await fetch("http://localhost:3000/activities");
        const data = await response.json();
        result = data;
    }

    function getActivitiesTemp(){
        result = {
            activities:[
                {title:"Déjeuner", description:"Déjeuner au restaurant", time:"12:00", address:"1 rue de la paix"},
                {title:"Conférence", description:"Conférence sur le thème de la blockchain", time:"14:00", address:"10 boulevard de la paix"},
                {title:"Dîner", description:"Dîner au restaurant", time:"19:00", address:"40 avenue de la paix"}
            ],
            date:dateString
        }
    }

    import "../app.css"
    import ResultsItem from "../components/ResultsItem.svelte";
</script>


<h1 class="title">Hackathon</h1>
<input class="input text-lg p-0.5" type="date" id="start" bind:value={dateString}>
<button on:click={getActivitiesTemp} class="input text-xl p-2">Plannifie ma journée</button>

<br>

<ResultsItem data={result} />

<style>

</style>