import { page } from '$app/stores'

/** @type {import('./$types').PageServerLoad} */

export async function load({ params, url}) {
    const email = url.searchParams.get("email");
    const uuid = params.slug;
    return {uuid: uuid, email: email};
}