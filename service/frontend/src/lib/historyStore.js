import {writable} from "svelte/store";

const storedHistory = localStorage.getItem("history");
export const history = writable(storedHistory || JSON.stringify([]));
history.subscribe(value => {
    localStorage.setItem("history", value);
})