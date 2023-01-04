<script>
    import Blob from "../components/svg/Blob.svelte";
</script>

<div>
    <div class="w-6/12 my-12">
        <h2>Découvrez des activités uniques en <span class="text-soft-purple">Loire-Atlantique</span></h2>
        <br>
        <h3> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc vulputate libero et velit interdum, ac aliquet odio mattis.</h3>
    </div>

    <a href="/">
        <div class="ml-auto max-w-max relative">
            <div class="border-dashed border-soft-yellow border-13 rounded-2xl
                        absolute w-96 h-28 right-3">
            </div>
            <div class="bg-soft-blue rounded-3xl py-8 px-10 text-center">
                <h2 class="text-bold text-white">Plan my Day!</h2>
            </div>
        </div>
    </a>

    <div class="py-12">
        <div class="flex items-center pl-5">
            <h3>Creators</h3>
            <img src="./img/creators.png" alt="creators"/>
        </div>

        <div class="relative -top-20">
            <Blob></Blob>
            <img src="./img/logo_imta.png" alt="logo" class="absolute bottom-3 left-12">
        </div>
    </div>
</div>