/** @type {import('./$types').PageServerLoad} */
import {getAgenda} from "$lib/api.js";
import {historyStore} from "$lib/historyStore.js";
import {get} from "svelte/store"

export async function load({url}) {
    const date = new Date(url.searchParams.get("date"));
    const coords = url.searchParams.get("coords");
    // Fetch data on api.chillpaper.fr
    const agenda = await getAgenda(date, get(historyStore).history);
    return {
        agenda: agenda
    }
}