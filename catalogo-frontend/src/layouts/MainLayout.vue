<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-toolbar>
        <q-btn
          class="bg-green-6 text-black"
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title> LucasFy </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <!-- Cambiando el color de fondo del Drawer a verde y el texto a blanco -->
    <q-drawer
      class="bg-green-7 text-black"
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label class="text-black" header> Menú </q-item-label>

        <!-- Nuevo enlace para la página principal -->
        <q-item to="/" exact clickable v-ripple class="text-black">
          <q-item-section avatar>
            <q-icon name="home" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Casa</q-item-label>
            <q-item-label caption>Back Home</q-item-label>
          </q-item-section>
        </q-item>

        <!-- Enlaces para las otras categorías -->
        <q-item
          v-for="link in linksList"
          :key="link.title"
          :to="`/${link.link}`"
          exact
          clickable
          v-ripple
          class="text-black"
        >
          <q-item-section avatar>
            <q-icon :name="link.icon" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ link.title }}</q-item-label>
            <q-item-label caption>{{ link.caption }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from "vue";

defineOptions({
  name: "MainLayout",
});

const linksList = [
  {
    title: "Categorías",
    caption: "Explora géneros",
    icon: "category",
    link: "categoria",
  },
  {
    title: "Álbumes",
    caption: "Top 100",
    icon: "album",
    link: "album",
  },
  {
    title: "Artistas",
    caption: "Tus favoritos",
    icon: "person",
    link: "artista",
  },
  {
    title: "Proveedores",
    caption: "Distribuidores",
    icon: "money",
    link: "proveedor",
  },
  {
    title: "Música",
    caption: "Lo mejor ahora",
    icon: "favorite",
    link: "musica",
  },
];

const leftDrawerOpen = ref(false);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
</script>

<style scoped>
.bg-secondary {
  background-color: #1db954;
}

.text-white {
  color: #fff;
}
</style>
