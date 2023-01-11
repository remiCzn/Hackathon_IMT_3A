/** @type {import('./$types').PageServerLoad} */
import {getAgenda} from "$lib/api.js";
import {historyStore} from "$lib/historyStore.js";
import {get} from "svelte/store"

export async function load({url}) {
    const date = new Date(url.searchParams.get("date"));
    const lat = url.searchParams.get("latit");
    const long = url.searchParams.get("long");
    const range = url.searchParams.get("rayon");
    console.log(lat, long, range);
    // Fetch data on chillpaper.fr/api
    const agenda = await getAgenda(date, get(historyStore).history);
    return {
        agenda: agenda
    }
}