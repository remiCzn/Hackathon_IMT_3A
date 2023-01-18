<script>
    import {register} from "$lib/api.js";
    import {goto} from "$app/navigation";

    /** @type {import('./$types').PageData} */

    export let data;

    let submited = false;

    async function onSubmit(e) {
        const formData = new FormData(e.target);
        let password = formData.get("passwordField");
        alert(password);
        let passwordConfirmation = formData.get("passwordConfirmationField");
        if(password != passwordConfirmation) {
            alert("Wrong email address")
        } else {
            console.log(register(data.uuid, data.email, password));
            submited = true;
            return await goto("/login");
        }


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
                <p class="mb-2">
                    Vous vous enregistrez avec l'adresse : <b>{data.email}</b>
                </p>
                {#if submited === false}

                    <form name="registrationForm" on:submit|preventDefault={onSubmit}>
                        <!-- Email input -->
                        <div class="mb-6">

                            <input
                                    type="password"
                                    class="form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                                    name="passwordField"
                                    placeholder="Password"
                            />
                            <input
                                    type="password"
                                    class="mt-4 form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                                    name="passwordConfirmationField"
                                    placeholder="Password Verification"
                            />
                        </div>

                        <div class="text-center lg:text-left">
                            <button
                                    type="submit"
                                    class="inline-block px-7 py-3 bg-blue-600 text-white font-medium text-sm leading-snug uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"

                            >Set Password</button>
                        </div>
                    </form>
                {:else}
                    <h1>An invitation as been sent on</h1>
                {/if}
            </div>
        </div>
    </div>
</section>