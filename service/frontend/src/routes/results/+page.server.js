/** @type {import('./$types').PageServerLoad} */
import {getAgenda} from "$lib/api.js";

export async function load({ url }) {
    // Fetch data on api.chillpaper.fr
    const date = new Date(url.searchParams.get("date"));
    const coords = url.searchParams.get("coords");
    const agenda = getAgenda(date);
    if(agenda === {}) {
        return undefined
    } else {
        return {
            agenda: agenda
        };
    }
}