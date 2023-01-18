import {get} from "svelte/store"

/** @type {import('./$types').PageServerLoad} */
export async function load({params}) {
    const email = "dqzd"; //params.searchParams.get("email");
    const uuid = params;
    return {uuid: uuid, email: email};
}