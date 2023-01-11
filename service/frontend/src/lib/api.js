import axios from "axios";

const client = axios.create({
    baseURL: "http://api.chillpaper.fr"
});


export function dateToHalfday(day) {
    let dayOfWeek = dateToDay(day);
    let partOfDay = day.getHours() >= 12;
    return 2 * dayOfWeek + partOfDay;
}

export function dateToDay(day) {
    return (((day.getDay() - 1) % 7) + 7) % 7;
}

export function getActivity(day, historyToken) {
    return client.get("/activity", {
        params: {
            time: dateToHalfday(day)
        },
        headers: {
            hist: historyToken
        }
    }).then((res) => {
        res.data
    });
}

export function getRestaurant(day, historyToken) {
    return client.get("/restaurant", {
        params: {
            time: dateToHalfday(day),
        },
        headers: {
            hist: historyToken
        }
    }).then((res) => res.data);
}

export function getAgenda(day, historyToken) {
    return client.get("/agenda", {
        params: {
            time: dateToDay(day)
        },
        headers: {
            hist: historyToken
        }
    }).then((res) => {
        return res.data.agenda;
    }).catch((_) => {
        return undefined;
    });
}
