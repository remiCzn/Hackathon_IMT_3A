<script>
    import {sendInvite} from "$lib/api.js";

    let submited = false;
    let _email = '';

    function onSubmit(e) {
        const formData = new FormData(e.target);
        let email = formData.get("emailField");
        if(!new RegExp('^[\\w\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$').test(email)) {
            alert("Wrong email address")
        } else {
            _email = email.toLowerCase();
            console.log(sendInvite(email));
            submited = true;

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
                {#if submited === false}

                    <form name="registrationForm" on:submit|preventDefault={onSubmit}
                    >

                        <!-- Email input -->
                        <div class="mb-6">
                            <input
                                    type="text"
                                    class="form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                                    name="emailField"
                                    placeholder="Email address"
                            />
                        </div>

                        <div class="text-center lg:text-left">
                            <button
                                    type="submit"
                                    class="inline-block px-7 py-3 bg-blue-600 text-white font-medium text-sm leading-snug uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"

                            >Register</button>

                            <p class="text-sm font-semibold mt-2 pt-1 mb-0">
                                Already have an account?
                                <a
                                        href="/login"
                                        class="text-red-600 hover:text-red-700 focus:text-red-700 transition duration-200 ease-in-out"
                                >Login</a
                                >
                            </p>
                        </div>
                    </form>
                {:else}
                    <h1>Une invitation a été envoyée à <b class="text-blue-400">{_email}</b></h1>
                {/if}
            </div>
        </div>
    </div>
</section>