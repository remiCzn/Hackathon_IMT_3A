/** @type {import('./$types').PageServerLoad} */
import {getAgenda} from "$lib/api.js";
import {historyStore} from "$lib/historyStore.js";
import {get} from "svelte/store"

export async function load({url}) {
    const date = new Date(url.searchParams.get("date"));
    const lat = parseFloat(url.searchParams.get("latit"));
    const long = parseFloat(url.searchParams.get("long"));
    const range = parseInt(url.searchParams.get("rayon"));
    // Fetch data on chillpaper.fr/api
    const agenda = await getAgenda(date, get(historyStore), lat, long, range);
    return {
        agenda: agenda
    }
}