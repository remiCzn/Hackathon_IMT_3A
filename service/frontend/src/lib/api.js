import axios from "axios";
import {historyStore} from "$lib/historyStore.js";

const client = axios.create({
    baseURL: "http://backend:3001"
});

const auth = axios.create({
    //TODO: change to http://auth:3069
    baseURL: "http://auth:3069/api"
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

export function register(uuid, email, password) {
    return auth.post("/register/" + uuid, {email: email, password: password},   {headers: {
        'Content-Type': 'application/json'
    }}).then((res) => {
        return res.json;
    });
}

export function sendInvite(email) {
    return auth.post("/invitation", {email: email},   {headers: {
            'Content-Type': 'application/json'
        }}).then((res) => {
        return res.json;
    });
}

export function login(email, password) {
    return auth.post("/auth", {email: email, password: password},   {headers: {
            'Content-Type': 'application/json',
            withCredentials: true
        }}).then((res) => {
        return res;
    });
}
