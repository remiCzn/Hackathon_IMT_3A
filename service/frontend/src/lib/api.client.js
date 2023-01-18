const baseURL = "https://chillpaper.fr/api"

const defaultheader = {
    headers: {
        hist: "",
    }
}

export function dateToHalfday(day) {
    let dayOfWeek = dateToDay(day);
    let partOfDay = day.getHours() >= 12;
    return 2 * dayOfWeek + partOfDay;
}

export function dateToDay(day) {
    return (((day.getDay() - 1) % 7) + 7) % 7;
}

export async function getActivity(day) {
    console.log("suu")
    day = new Date(day)
    const data = await fetch(`${baseURL}/activity?time=${dateToHalfday(day)}`,defaultheader);
    const data_json = await data.json();
    return data_json
}

export async function getRestaurant(day) {
    const data = await fetch(`${baseURL}/restaurant?time=${dateToHalfday(day)}`,defaultheader);
    const data_json = await data.json();
    return data_json
}