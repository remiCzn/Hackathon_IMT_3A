<script>
    import axios from "axios";
    import "./main.css"
    let data = "";

    // axios.get("http://localhost:3001").then((res) => {
    //     data = JSON.stringify(res.data);
    // });
</script>

<div class="main">
    <h1 class="title">Hackathon</h1>
    <p>{data}</p>
    <input class="input text-lg p-0.5" type="date" id="start" value="2022-01-15">
    <button class="input text-xl p-2">Plannifie ma journée</button>
</div>