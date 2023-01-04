/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ["./src/**/*.{html,js,svelte,ts}"],
	theme: {
		extend: {
			colors: {
				"soft-pink": "#EDB5A3",
				"soft-purple": "#98A8EE",
				"soft-yellow": "#FFF280",
				"soft-blue": "#B8DFEF",
				metal: "#4E4E4E",
			},
		},
	},
	plugins: [],
};
