<template>
  <div class="home-page">

    <h1 class="display-5 fw-bold text-center mb">
      Zones and Distributions
    </h1>

    <div v-if="error" class=" col-lg-6 mx-auto p-3 alert alert-danger alert-dismissible fade show d-flex justify-content-between" role="alert">
      <span>{{ error }}</span>
      <button type="button" class="btn btn-danger" @click="error = null">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>


    <div class="col-lg-6 mx-auto zones mb p-3">
      <zone-editable
        v-for="zone in zones"
        :id="zone.id"
        :name="zone.name"
        :updatedAt="zone.updatedAt"
        :distributions="zone.distributions"
        :key="zone.uid"
        @edit="zone.name = $event.name"
        @validationError="handleValidationError"
        class="zone"
        :distributions_count="zone.distributions_count"
      />
    </div>

    <h1 class="display-5 fw-bold text-center">
      To Do List
    </h1>

    <ul class="col-lg-6 mx-auto">
      <li>Add the percentage symbol to each distribution number while is not being edited <i class="check bi bi-check-lg"></i></li>
      <li>The cancel button is not working <i class="check bi bi-check-lg"></i></li>
      <li>Without refreshing the page, be able to edit all the distributions from a zone <i class="check bi bi-check-lg"></i></li>
      <li>Be able to add more distributions <i class="check bi bi-check-lg"></i></li>
      <li>Be able to remove distributions <i class="check bi bi-check-lg"></i></li>
      <li>When the user is not able to save due to some error, the error must be showed <i class="check bi bi-check-lg"></i></li>
      <li>The sum of all distributions must be ensured to be 100% in anyway <i class="check bi bi-check-lg"></i></li>
      <li>The distributions must be integer <i class="check bi bi-check-lg"></i></li>
      <li>The zone name cannot be empty <i class="check bi bi-check-lg"></i></li>
      <li>The zone name cannot have more than one space between each word <i class="check bi bi-check-lg"></i></li>
      <li>The zone name cannot have spaces at start or the end <i class="check bi bi-check-lg"></i></li>
      <li>The zone name cannot be repeated in any way <i class="check bi bi-check-lg"></i></li>
      <li>Create a new field "updated_at" that is going to store the date when the name field change <i class="check bi bi-check-lg"></i></li>
      <li>Show the updated_at field value near each zone name <i class="check bi bi-check-lg"></i></li>
      <li>Add a way for the user to know that an element is being saved <i class="check bi bi-check-lg"></i></li>
      <li>When the number of distributions is 5 or greater, the background of that zone must change to any color while is not being edited <i class="check bi bi-check-lg"></i></li>
    </ul>
  </div>
</template>

<script>
import ZoneEditable from './ZoneEditable.vue';

export default {
  name: 'HomePage',
  components: {
    ZoneEditable
  },
  props: {
    context: {
      type: Object
    }
  },
  data() {
    return {
      error: null,
      zones: [],
      zoneUid: 0
    };
  },
  mounted() {
    this.zones = this.context.zones.map(data => {
      return {
        id: data.id,
        name: data.name,
        updatedAt: data.updated_at,
        uid: this.zoneUid++,
        distributions: data.distributions,
        distributions_count: data.distributions_count
      };
    });
  },
  methods: {
    handleValidationError(error) {
      this.error = error;
    }
  }
}
</script>

<style lang="scss">
@import 'resources/scss/variables.scss';

.home-page {
  .zones {
    display: flex;
    gap: 4px;
    flex-direction: column;
  }
  .check{
    color: green;
    font-size: 25px;
  }

}
</style>
