<script>
    let result = {
        activities:[],
        date:""
    }

    async function getActivities(date) {
        const response = await fetch("http://localhost:3000/activities");
        const data = await response.json();
        return data;
    }

    function getActivitiesTemp(date){
        result = {
            activities:[
                {title:"Déjeuner", description:"Déjeuner au restaurant", time:"12:00"},
                {title:"Conférence", description:"Conférence sur le thème de la blockchain", time:"14:00"},
            ],
            date:"Jeudi 04 Février 2023"
        }
    }

    import "../app.css"
    import ResultItem from "../components/ResultItem.svelte";
</script>


<h1 class="title">Hackathon</h1>
<input class="input text-lg p-0.5" type="date" id="start" value="2022-01-15">
<button on:click={getActivitiesTemp} class="input text-xl p-2">Plannifie ma journée</button>

<br>

<ResultItem data={result} />

<style>

</style>