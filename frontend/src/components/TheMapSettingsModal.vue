<template>
  <b-loading v-if="loading" :active="true" :is-full-page="false" />
  <div v-else class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">{{ $tc('settings') }}</p>
      <button class="delete" type="button" @click="$emit('close')" />
    </header>
    <section class="modal-card-body">
      <h1 class="title is-size-4 mb-2">Overpass & Falling Fruit</h1>
      <p class="subtitle is-size-6 mt-0 mb-5">{{ $t('define-elements-to-see-on-map') }}</p>
      <div class="buttons mb-4">
        <b-button type="is-primary" @click="selectAll">{{ $t('select-all') }}</b-button>
        <b-button type="is-danger" class="ml-1" @click="deselectAll">{{ $t('deselect-all') }}</b-button>
      </div>
      <div id="ecats-checkboxes" class="columns is-flex-wrap-wrap">
        <div v-for="(extraCategory, index) in map_ecats" :key="index" class="column is-half">
          <b-field>
            <b-checkbox v-model="ecatsCheckboxes" :native-value="extraCategory.category" type="is-primary">
              {{ $tc('map_ecat_' + extraCategory.category, 0) }}
            </b-checkbox>
          </b-field>
        </div>
      </div>
    </section>
    <footer class="modal-card-foot">
      <b-button :label="$t('cancel')" @click="$emit('close')" />
      <b-button :label="$t('save')" type="is-primary" :loading="waitingFormResponse" @click="save" />
    </footer>
  </div>
</template>

<script>
import ErrorHandler from "@/mixins/ErrorHandler";
import WindowSize from "@/mixins/WindowSize";
import axios from "axios";

export default {
  name: 'TheMapSettingsModal',
  mixins: [ErrorHandler, WindowSize],
  props: {
    map_ecats: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      waitingFormResponse: false,
      loading: false,
      ecatsCheckboxes: []
    }
  },
  created() {
    for (const i in this.map_ecats) {
      if (this.map_ecats[i].selected === true)
        this.ecatsCheckboxes.push(this.map_ecats[i].category)
    }
  },
  computed: {
    userId() {
      return Number(this.$store.state.user.id);
    }
  },
  methods: {
    async save() {
      this.waitingFormResponse =  true;

      try {
        const data = new FormData();
        for (const [index, extraCategory] of Object.entries(this.map_ecats))
          data.append('map_ecats[]', JSON.stringify({
            'category': extraCategory.category,
            'selected': extraCategory.selected
          }));

        await axios.patch(`/api/v1/webusers/${this.userId}`, data);

        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('map-settings-saved'),
          pauseOnHover: true,
          queue: false
        });

        for (const i in this.map_ecats)
          this.map_ecats[i].selected = this.ecatsCheckboxes.includes(this.map_ecats[i].category);

        this.$emit('close');
      }
      catch (error) {
        this.snackbarError(error);
      }

      this.waitingFormResponse =  false;
    },
    selectAll() {
      for (const i in this.map_ecats) {
        if (!this.ecatsCheckboxes.includes(this.map_ecats[i].category))
          this.ecatsCheckboxes.push(this.map_ecats[i].category);
      }
    },
    deselectAll() {
      this.ecatsCheckboxes = [];
    },
  }
}
</script>

<style scoped>

</style>
