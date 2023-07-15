<template>
  <div class="zone-editable"  :class="{'more-than-four': distributions_count >= 5 }"  >
    <div
      v-if="display"
      class="zone-display"
    >
      <div>
        Zone Name: <strong>{{ name }}</strong> - Distributions: {{ distributionDisplay }}
        <br>
        <span class="text-muted"> Updated at: {{ updatedAt }}</span>
      </div>

      <button
        class="btn btn-primary"
        @click="setDisplay(false)"
        :disabled="saving"
      >
        Edit
      </button>
    </div>
    <div
      v-else
      class="zone-edit"
    >
      <label class="control-label">
        Zone Name
      </label>

      <input
        v-model="form.name"
        placeholder="Zone name"
        class="form-control"
        :disabled="saving"
      >

      <div class="zone-edit-distributions">
        <div v-for="(distribution, index) in form.distributions" :key="index">
          <label class="control-label">
            Distribution
          </label>

          <input
            v-model="distribution.percentage"
            placeholder="Percentage"
            class="form-control"
            type="number"
          >

          <button
            class="btn btn-danger mt-2"
            v-if="index === form.distributions.length - 1"
            @click.prevent="removeDistribution(index)"
            :disabled="saving"
          >
            Remove Last Distribution
          </button>

        </div>
      </div>

      <div class="zone-edit-actions">
        <button
          class="btn btn-warning"
          @click="addDistribution"
          :disabled="saving"
        >
          Add Distribution
        </button>

        <button
          class="btn btn-secondary"
          @click="setDisplay(true)" 
          :disabled="saving"
        >
         Cancel
        </button>

        <button
          class="btn btn-success"
          @click="save"
          :disabled="saving"
        >
        Save
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2'

export default {
  name: 'ZoneEditable',
  props: {
    name: String,
    id: Number,
    updatedAt: String, // Aquí agregamos la nueva propiedad updatedAt
    distributions: Array,
    distributions_count: Number,
  },
  data() {
    return {
      error: null,
      display: true,
      form: {
        name: '',
        distributions: [],
      },
      saving: false,
      showError: false,  // Variable para controlar el error
    };
  },
  watch: {
    'form.distributions': {
      handler() {
        this.showError = false;
      },
      deep: true,
    },
  },
  computed: {
    distributionDisplay() {
      return this.distributions.map(distribution => `${distribution.percentage}%`).join('-');
    },
    totalDistribution() {
      return this.form.distributions.reduce((sum, distribution) => sum + Number(distribution.percentage), 0);
    }
  },
  mounted() {
    this.getValuesFromProps();
  },
  methods: {
    addDistribution() {
      this.form.distributions.push({
        percentage: 0
      });
    },
    removeDistribution(index) {
      this.form.distributions.splice(index, 1);
    },
    getValuesFromProps() {
      this.form.name = this.name;
      this.form.distributions = this.distributions.map(distribution => {
        return {
          id: distribution.id,
          percentage: distribution.percentage
        };
      });
    },
    setDisplay(value) {
      this.display = value;

      if(!this.display) {
        this.getValuesFromProps();
      }
    },
    async save() {

      this.saving = true;
      this.error = null;

      const params = {
        id: this.id,
        name: this.form.name,
      };

// Mostrar un alerta de carga antes de iniciar la solicitud
      Swal.fire({
        title: 'Guardando...',
        text: 'Por favor espera',
        allowEscapeKey: false,
        allowOutsideClick: false,
        onBeforeOpen: () => {
            Swal.showLoading()
        }
      });

      try {
        if (this.totalDistribution !== 100) {
          console.log(this.totalDistribution);
          throw new Error('The sum of all distributions must be 100%');
        }

        if (!this.form.name) {
          this.$emit('validationError', 'The zone name cannot be empty');
          return;
        }

        if (/\s{2,}/.test(this.form.name)) {
          this.$emit('validationError', 'The zone name cannot have more than one space between each word');
          this.saving = false;
          return;
        }

        if (/^\s|\s$/.test(this.form.name)) {
          this.$emit('validationError', 'The zone name cannot have spaces at the start or the end');
          this.saving = false;
          return;
        }

        await axios.post('/api/zones/edit', params);

        // Si la solicitud es exitosa, cerrar el alerta de carga y mostrar uno de éxito
        Swal.close();
        Swal.fire('Guardado', 'Los cambios han sido guardados exitosamente', 'success');

        this.$emit('edit', {name: params.name});

        this.display = true;

      }catch (error) {
        Swal.close();
        Swal.fire('Error', 'Ha ocurrido un error al guardar los cambios', 'error');

        let errorMessage = error.message;
        
        if (error.response) {
          // Si la API devuelve un mensaje de error, úsalo
          errorMessage = error.response.data;
        }
        console.log(errorMessage);
        this.$emit('validationError', errorMessage);
      } finally {
        this.saving = false;
      }
    }
  }
}
</script>

<style lang="scss">
@import 'resources/scss/variables.scss';

.zone-editable {
  border: 1px solid $gray-color;
  padding: $qmb;
  border-radius: $border-radius;
  

  .zone-display {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .zone-edit {
    display: flex;
    flex-direction: column;
    gap: $small-action-space;

    .zone-edit-actions {
      display: flex;
      gap: $small-action-space;
      justify-content: end;
    }

    .zone-edit-distributions {
      display: grid;
      grid-template-columns: repeat(1, 1fr);
      gap: $small-action-space;
    }
  }
}

.more-than-four {
  background-color: aqua;
}
</style>
