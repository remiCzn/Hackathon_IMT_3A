<script>
    import {login} from "$lib/api.js";
    import { redirect } from '@sveltejs/kit';
    import {goto} from "$app/navigation";

    /** @type {import('./$types').PageData} */

    export let data;

     async function onSubmit(e) {
         const formData = new FormData(e.target);
         let email = formData.get("email");
         let password = formData.get("password");
         let l = await login(email, password)
         console.log(l);
         // console.log(cookies.get('auth'))
         return goto("/");


     }
</script>


<section class="h-screen">
    <div class="px-6 h-full text-gray-800">
        <div
                class="flex xl:justify-center lg:justify-between justify-center items-center flex-wrap h-full g-6"
        >
            <div
                    class="grow-0 shrink-1 md:shrink-0 basis-auto xl:w-6/12 lg:w-6/12 md:w-9/12 mb-12 md:mb-0"
            >
                <img
                        src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.webp"
                        class="w-full"
                        alt="Sample image"
                />
            </div>
            <div class="xl:ml-20 xl:w-5/12 lg:w-5/12 md:w-8/12 mb-12 md:mb-0">
                <form name="loginForm" on:submit|preventDefault={onSubmit}>

                    <!-- Email input -->
                    <div class="mb-6">
                        <input
                                type="text"
                                class="form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                                name="email"
                                placeholder="Email address"
                        />
                    </div>

                    <!-- Password input -->
                    <div class="mb-6">
                        <input
                                type="password"
                                class="form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                                name="password"
                                placeholder="Password"
                        />
                    </div>


                    <div class="text-center lg:text-left">
                        <button
                                type="submit"
                                class="inline-block px-7 py-3 bg-blue-600 text-white font-medium text-sm leading-snug uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
                        >
                            Login
                        </button>
                        <p class="text-sm font-semibold mt-2 pt-1 mb-0">
                            Don't have an account?
                            <a
                                    href="/register"
                                    class="text-red-600 hover:text-red-700 focus:text-red-700 transition duration-200 ease-in-out"
                            >Register</a
                            >
                        </p>
                    </div>
                </form>
            </div>
        </div>
    </div>
</section>