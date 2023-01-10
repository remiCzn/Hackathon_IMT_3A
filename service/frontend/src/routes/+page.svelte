<script>
    import Blob from "../components/svg/Blob.svelte";
</script>

<div>
    <div class="w-auto lg:w-6/12 my-12">
        <h2>Découvrez des activités uniques en <span class="text-soft-purple">Loire-Atlantique</span></h2>
        <br>
        <h3> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc vulputate libero et velit interdum, ac aliquet odio mattis.</h3>
    </div>

    <a href="/planning">
        <div class="m-auto md:m-0 md:block md:ml-auto max-w-max relative">
            <div class="invisible lg:visible
                        border-dashed border-soft-yellow border-13 rounded-2xl
                        absolute w-96 h-28 right-3">
            </div>
            <div class="bg-soft-blue rounded-3xl py-4 px-8 md:py-8 md:px-10 text-center">
                <h2 class="text-bold text-white">Plan my Day!</h2>
            </div>
        </div>
    </a>

    <div class="py-12">
        <div class="flex justify-center md:justify-start items-center  md:pl-5">
            <h3>Creators</h3>
            <img src="./img/creators.png" alt="creators"/>
        </div>

        <div class="hidden md:inline
                    relative -top-20">
            <Blob></Blob>
            <img src="./img/logo_imta.png" alt="logo" class="absolute bottom-3 left-12">
        </div>
    </div>
</div>