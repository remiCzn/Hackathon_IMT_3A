<script>
    import axios from "axios";

    let data = "";

    axios.get("https://pokeapi.co/api/v2/pokemon/ditto").then((res) => {
        data = JSON.stringify(res.data);
    })
</script>

<h1>Welcome to SvelteKit</h1>
<p>{data}</p>

<style>
    p {
        color: darkred;
    }
    h1 {
        font-style: italic;
        color: darkblue;
    }
</style>