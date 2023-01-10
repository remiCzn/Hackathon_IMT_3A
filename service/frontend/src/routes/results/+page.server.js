/** @type {import('./$types').PageServerLoad} */
export async function load() {
    // Fetch data on api.chillpaper.fr
    const response = await fetch('https://api.chillpaper.fr/activity');
    const data = await response.json();

    
    return data;
};