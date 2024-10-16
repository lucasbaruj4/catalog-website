<template>
  <q-page padding>
    <!-- Grilla -->
    <section v-if="view === 'list'">
      <q-table
        title="Artistas"
        :rows="filteredRows"
        :columns="columns"
        :loading="loading"
      >
        <template v-slot:top-right>
          <q-input
            outlined
            dense
            filled
            label="Buscar artistas..."
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
              <div
                v-if="col.name === 'acciones'"
                class="row justify-center items-center"
              >
                <q-btn
                  round
                  flat
                  color="green-7"
                  :disable="loading"
                  :loading="loading"
                  @click.prevent="onEdit(props.row)"
                  class="q-ml-xs q-mr-xs"
                >
                  <q-icon name="edit" color="white" />
                  <q-tooltip>Editar</q-tooltip>
                </q-btn>
                <q-btn
                  round
                  flat
                  color="green-7"
                  :disable="loading"
                  :loading="loading"
                  @click.prevent="onDelete(props.row.id)"
                  class="q-ml-xs"
                >
                  <q-icon name="delete" color="black" />
                  <q-tooltip>Eliminar</q-tooltip>
                </q-btn>
              </div>
              <div v-else>{{ props.row[col.field] }}</div>
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
              {{ view === "add" ? "Agregar Artista" : "Editar Artista" }}
            </div>
            <div class="text-subtitle2">Complete los datos del formulario</div>
          </q-card-section>

          <q-card-section>
            <q-input v-model="form.nombre" label="Nombre del Artista" />
            <q-input v-model="form.descripcion" label="Descripción" />
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
  name: "ArtistaPage",
  components: [],
  props: {},
  emits: [],
  setup() {
    axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
    axios.defaults.headers.common["Access-Control-Allow-Methods"] =
      "GET, POST, PUT, DELETE, OPTIONS";
    axios.defaults.headers.common["Access-Control-Allow-Headers"] =
      "Content-Type, Authorization";

    const view = ref("list");
    const columns = [
      {
        name: "nombre",
        required: true,
        label: "Nombre",
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
    });

    const filteredRows = computed(() => {
      if (filter.value) {
        return rows.value.filter(
          (row) =>
            row.nombre.toLowerCase().includes(filter.value.toLowerCase()) ||
            (row.descripcion &&
              row.descripcion
                .toLowerCase()
                .includes(filter.value.toLowerCase()))
        );
      }
      return rows.value;
    });

    const onAdd = () => {
      form.value = { id: null, nombre: "", descripcion: "" };
      view.value = "add";
    };

    const onEdit = (row) => {
      form.value = { ...row };
      view.value = "edit";
    };

    const onSubmit = () => {
      if (view.value === "add") {
        axios
          .post("http://127.0.0.1:5000/api/artistas", form.value)
          .then(() => {
            onRequest();
            view.value = "list";
          })
          .catch((error) => console.error(error));
      } else if (view.value === "edit") {
        axios
          .put(
            `http://127.0.0.1:5000/api/artistas/${form.value.id}`,
            form.value
          )
          .then(() => {
            onRequest();
            view.value = "list";
          })
          .catch((error) => console.error(error));
      }
    };

    const onDelete = (id) => {
      if (confirm("¿Estás seguro de que deseas eliminar este artista?")) {
        axios
          .delete(`http://127.0.0.1:5000/api/artistas/${id}`)
          .then(() => {
            onRequest();
          })
          .catch((error) => console.error(error));
      }
    };

    const onRequest = () => {
      loading.value = true;
      axios
        .get("http://127.0.0.1:5000/api/artistas")
        .then((response) => {
          console.log(response.data);
          rows.value = response.data.artistas || [];
        })
        .catch((error) => {
          console.log(error);
        })
        .finally(() => {
          loading.value = false;
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
