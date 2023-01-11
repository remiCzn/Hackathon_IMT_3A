<script>
	import Blob from "../components/svg/Blob.svelte";
	import { historyStore } from "$lib/historyStore.js";

	historyStore.set("");
</script>

<div>
	<div class="w-auto lg:w-6/12 my-6">
		<h2>
			Découvrez des activités uniques en <span class="text-soft-purple"
				>Loire-Atlantique</span
			>
		</h2>
		<br />
		<h3>
			Vous ne savez pas quoi faire de votre journée ? Laissez-vous tenter par
			notre sélécteur d'activités et vous ne serez pas déçu !
		</h3>
	</div>

	<a href="/plan">
		<div class="m-auto lg:m-0 lg:block lg:ml-auto max-w-max relative">
			<div
				class="invisible lg:visible
                        border-dashed border-soft-yellow border-13 rounded-2xl
                        absolute w-96 h-28 right-3"
			/>
			<div
				class="bg-soft-blue rounded-3xl py-4 px-8 lg:py-8 lg:px-10 text-center"
			>
				<h2 class="text-bold text-white">Plan my Day!</h2>
			</div>
		</div>
	</a>

	<div class="pt-8">
		<div class="flex justify-center lg:justify-start items-center  lg:pl-5">
			<h3>Creators</h3>
			<img alt="creators" src="./img/creators.png" />
		</div>

		<div
			class="hidden lg:inline
                    relative -top-20"
		>
			<Blob />
			<img
				alt="logo"
				class="absolute bottom-3 left-12"
				src="./img/logo_imta.png"
			/>
		</div>
	</div>
</div>
