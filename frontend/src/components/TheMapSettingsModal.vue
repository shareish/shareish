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
      <b-field v-for="(map_ecat, index) in map_ecats_copy" :key="index">
        <b-checkbox v-model="map_ecat.selected" type="is-primary">
          {{ $tc('map_ecat_' + map_ecat.category, 0) }}
        </b-checkbox>
      </b-field>
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
      map_ecats_copy: []
    }
  },
  created() {
    for (const i in this.map_ecats)
      this.map_ecats_copy[i] = {...this.map_ecats[i]};
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
        for (const [index, map_ecat] of Object.entries(this.map_ecats_copy))
          data.append('map_ecats[]', JSON.stringify({'category': map_ecat.category, 'selected': map_ecat.selected}));

        await axios.patch(`/api/v1/webusers/${this.userId}`, data);

        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('map-settings-saved'),
          pauseOnHover: true,
          queue: false
        });

        for (const i in this.map_ecats)
          this.map_ecats[i].selected = this.map_ecats_copy[i].selected;

        this.$emit('close');
      }
      catch (error) {
        this.snackbarError(error);
      }

      this.waitingFormResponse =  false;
    }
  }
}
</script>

<style scoped>

</style>
