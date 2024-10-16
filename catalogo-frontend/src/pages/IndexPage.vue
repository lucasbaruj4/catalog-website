<template>
  <q-page class="q-pa-md bg-primary text-white">
    <div class="row justify-center items-center">
      <div class="col-12 col-md-6 text-center">
        <div class="circle-mask">
          <img
            alt="LucasFy logo"
            src="~assets/lucasfy-logo.jpg"
            class="circle-image"
          />
        </div>
        <h1 class="q-mt-md text-h4 text-center">LucasFy</h1>
        <h2 class="q-mt-md text-h4 text-center">
          Música que vacía tu billetera
        </h2>
        <q-btn
          label="Empieza a escuchar"
          class="q-mt-lg btn-spotify"
          @click="goToMusic"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { useRouter } from "vue-router";

defineOptions({
  name: "IndexPage",
});

const router = useRouter();

const goToMusic = () => {
  router.push("/musica");
};
</script>

<style scoped>
.bg-primary {
  background-color: #191414;
}

.text-white {
  color: #fff;
}

.text-center {
  text-align: center;
}

.q-btn.btn-spotify {
  background-color: #1db954;
  color: #fff;
  padding: 10px 20px;
  font-size: 1.2rem;
  border-radius: 25px;
}

.q-btn.btn-spotify:hover {
  background-color: #1ed760;
}

.circle-mask {
  width: 300px;
  height: 300px;
  position: relative;
  display: inline-block;
  overflow: hidden;
  border-radius: 50%;
}

.circle-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
