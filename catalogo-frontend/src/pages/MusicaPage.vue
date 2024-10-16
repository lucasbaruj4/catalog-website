<template>
  <q-page padding>
    <!-- Grilla -->
    <section v-if="view === 'list'">
      <q-table
        title="Música"
        :rows="filteredRows"
        :columns="columns"
        :loading="loading"
      >
        <template v-slot:top-right>
          <q-input
            outlined
            dense
            filled
            label="Buscar música..."
            debounce="300"
            color="amber"
            v-model="filter"
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
          <q-btn
            outline
            icon="add"
            color="positive"
            :disable="loading"
            :loading="loading"
            label="Agregar"
            class="q-ml-sm"
            @click.prevent="onAdd"
          />
          <q-space />
        </template>

        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td v-for="col in props.cols" :key="col.name" :props="props">
              <div
                v-if="col.name === 'acciones'"
                class="row justify-center items-center"
              >
                <q-btn
                  round
                  flat
                  color="green-7"
                  @click.prevent="onEdit(props.row)"
                >
                  <q-icon name="edit" color="white" />
                  <q-tooltip>Editar</q-tooltip>
                </q-btn>
                <q-btn
                  round
                  flat
                  color="green-7"
                  @click.prevent="onDelete(props.row.id)"
                >
                  <q-icon name="delete" color="black" />
                  <q-tooltip>Eliminar</q-tooltip>
                </q-btn>
              </div>
              <div v-else>{{ col.value }}</div>
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </section>

    <!-- Formulario -->
    <section v-if="view === 'add' || view === 'edit'">
      <q-form @submit="onSubmit">
        <q-card>
          <q-card-section>
            <div class="text-h6">
              {{ view === "add" ? "Agregar Música" : "Editar Música" }}
            </div>
            <div class="text-subtitle2">Complete los datos del formulario</div>
          </q-card-section>

          <q-card-section>
            <q-input v-model="form.nombre" label="Nombre de la Música" />
            <q-input v-model="form.descripcion" label="Descripción" />

            <!-- Dropdowns -->
            <q-select
              v-model="form.album_id"
              :options="albums"
              option-label="nombre"
              option-value="id"
              label="Álbum"
              emit-value
              map-options
            />

            <q-select
              v-model="form.proveedor_id"
              :options="proveedores"
              option-label="nombre"
              option-value="id"
              label="Proveedor"
              emit-value
              map-options
            />

            <q-select
              v-model="form.categoria_id"
              :options="categorias"
              option-label="nombre"
              option-value="id"
              label="Categoría"
              emit-value
              map-options
            />

            <q-select
              v-model="form.artista_id"
              :options="artistas"
              option-label="nombre"
              option-value="id"
              label="Artista"
              emit-value
              map-options
            />
          </q-card-section>

          <q-separator dark />

          <q-card-actions align="around">
            <q-btn flat @click.prevent="view = 'list'">Volver</q-btn>
            <q-btn flat type="submit">{{
              view === "add" ? "Grabar" : "Actualizar"
            }}</q-btn>
          </q-card-actions>
        </q-card>
      </q-form>
    </section>
  </q-page>
</template>

<script>
import { onMounted, ref, computed } from "vue";
import axios from "axios";

export default {
  name: "MusicaPage",
  setup() {
    const view = ref("list");
    const columns = [
      {
        name: "nombre",
        required: true,
        label: "Nombre de la Música",
        align: "left",
        field: "nombre",
        format: (val) => `${val}`,
        sortable: true,
      },
      {
        name: "descripcion",
        label: "Descripción",
        align: "left",
        field: "descripcion",
        sortable: true,
      },
      {
        name: "album",
        label: "Álbum",
        align: "left",
        field: "album",
        sortable: true,
      },
      {
        name: "proveedor",
        label: "Proveedor",
        align: "left",
        field: "proveedor",
        sortable: true,
      },
      {
        name: "categoria",
        label: "Categoría",
        align: "left",
        field: "categoria",
        sortable: true,
      },
      {
        name: "artista",
        label: "Artista",
        align: "left",
        field: "artista",
        sortable: true,
      },
      {
        name: "acciones",
        label: "Acciones",
        align: "center",
        field: "acciones",
        style: "text-align: center;",
      },
    ];

    const rows = ref([]);
    const loading = ref(false);
    const filter = ref("");
    const form = ref({
      id: null,
      nombre: "",
      descripcion: "",
      album_id: null,
      proveedor_id: null,
      categoria_id: null,
      artista_id: null,
    });

    const albums = ref([]);
    const proveedores = ref([]);
    const categorias = ref([]);
    const artistas = ref([]);

    const filteredRows = computed(() => {
      if (filter.value) {
        return rows.value.filter(
          (row) =>
            row.nombre.toLowerCase().includes(filter.value.toLowerCase()) ||
            row.descripcion?.toLowerCase().includes(filter.value.toLowerCase())
        );
      }
      return rows.value;
    });

    const onAdd = () => {
      form.value = {
        id: null,
        nombre: "",
        descripcion: "",
        album_id: null,
        proveedor_id: null,
        categoria_id: null,
        artista_id: null,
      };
      view.value = "add";
    };

    const onEdit = (row) => {
      form.value = {
        id: row.id,
        nombre: row.nombre,
        descripcion: row.descripcion || "",
        album_id: row.album_id || row.album?.id || null,
        proveedor_id: row.proveedor_id || row.proveedor?.id || null,
        categoria_id: row.categoria_id || row.categoria?.id || null,
        artista_id: row.artista_id || row.artista?.id || null,
      };
      view.value = "edit";
    };

    const onSubmit = () => {
      const method = form.value.id ? "put" : "post";
      const url = form.value.id
        ? `http://127.0.0.1:5000/api/musicas/${form.value.id}`
        : "http://127.0.0.1:5000/api/musicas";

      axios[method](url, form.value)
        .then(() => {
          onRequest();
          view.value = "list";
        })
        .catch((error) => console.error(error));
    };

    const onDelete = (id) => {
      if (confirm("¿Estás seguro de que deseas eliminar esta música?")) {
        axios
          .delete(`http://127.0.0.1:5000/api/musicas/${id}`)
          .then(() => {
            onRequest();
          })
          .catch((error) => console.error(error));
      }
    };

    const onRequest = () => {
      loading.value = true;
      axios
        .get("http://127.0.0.1:5000/api/musicas")
        .then((response) => {
          rows.value = response.data.musicas || [];
        })
        .catch((error) => console.error(error))
        .finally(() => {
          loading.value = false;
        });

      // Cargar albums, proveedores, categorías, y artistas para los dropdowns
      axios.get("http://127.0.0.1:5000/api/albums").then((response) => {
        albums.value = response.data.albums || [];
      });

      axios.get("http://127.0.0.1:5000/api/proveedores").then((response) => {
        proveedores.value = response.data.proveedores || [];
      });

      axios.get("http://127.0.0.1:5000/api/categorias").then((response) => {
        categorias.value = response.data.categorias || [];
      });

      axios.get("http://127.0.0.1:5000/api/artistas").then((response) => {
        artistas.value = response.data.artistas || [];
      });
    };

    onMounted(() => {
      onRequest();
    });

    return {
      view,
      rows,
      columns,
      loading,
      filter,
      filteredRows,
      form,
      albums,
      proveedores,
      categorias,
      artistas,
      onAdd,
      onEdit,
      onDelete,
      onRequest,
      onSubmit,
    };
  },
};
</script>

<style scoped>
.q-btn {
  padding: 0 !important;
  background-color: #388e3c; /* Verde green-7 */
}

.q-btn .q-icon {
  border-radius: 50%;
  padding: 8px;
}

.q-btn[color="primary"] .q-icon {
  color: white; /* Blanco para editar */
}

.q-btn[color="negative"] .q-icon {
  color: black; /* Negro para eliminar */
}

.q-tooltip {
  font-size: 12px;
}
</style>
