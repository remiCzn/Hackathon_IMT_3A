import axios from "axios";
import {historyStore} from "$lib/historyStore.js";

const client = axios.create({
    baseURL: "http://backend:3001"
});

const auth = axios.create({
    //TODO: change to http://auth:3069
    baseURL: "http://localhost:8080/api"
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
        historyStore.set(res.data.hist);
        return res.data.activity;
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
    }).then((res) => {
        historyStore.set(res.data.hist);
        return res.data.restaurant;
    });
}

export function getAgenda(day, historyToken, lat, long, r) {
    return client.get("/agenda_distance", {
        params: {
            time: dateToDay(day),
            lat: lat,
            long: long,
            r: r
        },
        headers: {
            hist: historyToken
        }
    }).then((res) => {
        historyStore.set(res.data.hist);
        return res.data.agenda;
    }).catch((_) => {
        return undefined;
    });
}

export function register(id, email) {
    return auth.post("/register/" + id, {email: email, password: password},   {headers: {
        'Content-Type': 'application/json'
    }}).then((res) => {
        return res.data;
    });
}

export function sendInvite(email) {
    return auth.post("/invitation", {email: email},   {headers: {
            'Content-Type': 'application/json'
        }}).then((res) => {
        return res.data;
    });
}

export function login(email, password) {
    return auth.get("/activity", {
        params: {
            time: dateToHalfday(day)
        },
        headers: {
            hist: historyToken
        }
    }).then((res) => {
        historyStore.set(res.data.hist);
        return res.data.activity;
    });
}
