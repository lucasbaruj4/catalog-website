<template>
  <q-page padding>
    <!-- Grilla -->
    <section v-if="view === 'list'">
      <q-table
        title="Álbumes"
        :rows="filteredRows"
        :columns="columns"
        :loading="loading"
      >
        <template v-slot:top-right>
          <q-input
            outlined
            dense
            filled
            label="Buscar álbumes..."
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
            <q-td :props="props" v-for="col in props.cols" :key="col.name">
              <div>
                {{ formatValue(col.field, props.row[col.field]) }}
              </div>
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </section>

    <!-- Formulario -->
    <section v-if="view === 'add'">
      <q-form @submit="onSubmit">
        <q-card>
          <q-card-section>
            <div class="text-h6">Agregar Álbum</div>
            <div class="text-subtitle2">Complete los datos del formulario</div>
          </q-card-section>

          <q-card-section>
            <q-input v-model="form.nombre" label="Nombre del álbum" />
            <q-input v-model="form.descripcion" label="Descripción" />

            <!-- Dropdowns -->
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

            <q-input v-model="form.precio" label="Precio" type="number" />
            <q-toggle v-model="form.estado" label="Disponible" />
          </q-card-section>

          <q-separator dark />

          <q-card-actions align="around">
            <q-btn flat @click.prevent="view = 'list'">Volver</q-btn>
            <q-btn flat type="submit">Grabar</q-btn>
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
  name: "AlbumPage",
  components: [],
  props: {},
  emits: [],
  setup() {
    const view = ref("list");
    const columns = [
      {
        name: "nombre",
        required: true,
        label: "Nombre del Álbum",
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
        name: "precio",
        label: "Precio",
        align: "right",
        field: "precio",
        format: (val) => `$${parseFloat(val).toFixed(2)}`,
        sortable: true,
      },
      {
        name: "estado",
        label: "Estado",
        align: "left",
        field: "estado",
        sortable: true,
      },
    ];

    const rows = ref([]);
    const loading = ref(false);
    const filter = ref("");
    const form = ref({
      id: null,
      nombre: "",
      descripcion: "",
      proveedor_id: null,
      categoria_id: null,
      artista_id: null,
      precio: "0.00",
      estado: true,
    });

    const proveedores = ref([]);
    const categorias = ref([]);
    const artistas = ref([]);

    const filteredRows = computed(() => {
      if (filter.value) {
        return rows.value.filter(
          (row) =>
            row.nombre.toLowerCase().includes(filter.value.toLowerCase()) ||
            row.descripcion.toLowerCase().includes(filter.value.toLowerCase())
        );
      }
      return rows.value;
    });

    const formatValue = (field, value) => {
      if (field === "estado") {
        return value === true ? "Disponible" : "No disponible";
      }
      return value;
    };

    const onAdd = () => {
      form.value = {
        id: null,
        nombre: "",
        descripcion: "",
        proveedor_id: null,
        categoria_id: null,
        artista_id: null,
        precio: "0.00",
        estado: true,
      };
      view.value = "add";
    };

    const onSubmit = () => {
      const method = form.value.id ? "put" : "post";
      const url = form.value.id
        ? `http://127.0.0.1:5000/api/albums/${form.value.id}`
        : "http://127.0.0.1:5000/api/albums";

      axios({
        method: method,
        url: url,
        data: form.value,
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then(() => {
          onRequest();
          view.value = "list";
        })
        .catch((error) => {
          console.error("Error al hacer la solicitud:", error);
        });
    };

    const onRequest = () => {
      loading.value = true;
      axios
        .get("http://127.0.0.1:5000/api/albums")
        .then((response) => {
          rows.value = response.data.albums || [];
        })
        .catch((error) => {
          console.error("Error al cargar los álbumes:", error);
        })
        .finally(() => {
          loading.value = false;
        });

      // Cargar proveedores, categorías y artistas para los dropdowns
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
      proveedores,
      categorias,
      artistas,
      onAdd,
      onRequest,
      onSubmit,
      formatValue,
    };
  },
};
</script>

<style scoped>
.q-btn {
  padding: 0 !important;
  background-color: #388e3c;
}

.q-btn .q-icon {
  border-radius: 50%;
  padding: 8px;
}

.q-btn[color="primary"] .q-icon {
  color: white;
}

.q-btn[color="negative"] .q-icon {
  color: black;
}

.q-tooltip {
  font-size: 12px;
}
</style>
