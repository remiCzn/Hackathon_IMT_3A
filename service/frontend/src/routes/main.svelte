<script>
    import axios from "axios";

    let data = "";

    axios.get("http://localhost:3001").then((res) => {
        data = JSON.stringify(res.data);
    });
</script>

<h1>Welcome to SvelteKit</h1>
<p>This is data from backend:</p>
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