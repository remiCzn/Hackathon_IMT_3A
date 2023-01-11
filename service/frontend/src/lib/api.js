import axios from "axios";
import jwt from "jsonwebtoken"

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

function history() {
    cookies
    let a = jwt.sign({
        history: []
    }, "secret");
    console.log(a);
    return a;
}

export function getActivity(day) {
    return client.get("/activity", {
        params: {
            time: dateToHalfday(day)
        },
        headers: {
            hist: history()
        }
    }).then((res) => res.data);
}

export function getRestaurant(day) {
    return client.get("/restaurant", {
        params: {
            time: dateToHalfday(day),
        },
        headers: {
            hist: history()
        }
    }).then((res) => res.data);
}

export function getAgenda(day) {
    return client.get("/agenda", {
        params: {
            time: dateToHalfday(day)
        },
        headers: {
            hist: history()
        }
    }).then((res) => res.data).catch((_) => {
        return undefined;
    });
}
