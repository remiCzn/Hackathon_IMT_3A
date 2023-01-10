import axios from "axios";

const client = axios.create({
    baseURL: "http://api.chillpaper.fr"
});

export function dateToTimeId(day) {
    let dayOfWeek = (((day.getDay() - 1) % 7) + 7) % 7;
    let partOfDay = day.getHours() >= 12;
    return 2 * dayOfWeek + partOfDay;
}

export function getActivity(day) {
    return client.get("/activity", {
        params: {
            time: dateToTimeId(day)
        }
    }).then((res) => res.data);
}

export function getRestaurant(day) {
    return client.get("/restaurant", {
        params: {
            time: dateToTimeId(day)
        }
    }).then((res) => res.data);
}

export function getAgenda(day) {
    return client.get("/agenda", {
        params: {
            time: dateToTimeId(day)
        }
    }).then((res) => res.data)
        .catch((_) => {
            return undefined;
        });
}

// (async () => {
//     const a = await getRestaurant(new Date());
//     console.log(a);
//     const b = await getActivity(new Date());
//     console.log(b);
//     const c = await getAgenda(new Date());
//     console.log(c);
// })();
