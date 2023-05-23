<template>
  <b-loading v-if="loading" :active="true" :is-full-page="false" />
  <div v-else class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">{{ $tc('definitive-deletion') }}</p>
      <button class="delete" type="button" @click="$emit('close')" />
    </header>
    <section class="modal-card-body">
      <p v-html="$t('help_definitive-deletion')" />
    </section>
    <footer class="modal-card-foot">
      <b-button :label="$t('cancel')" @click="$emit('close')" />
      <b-button :label="$t('confirm')" type="is-danger" :loading="waitingFormResponse" @click="confirmDefinitiveDeletion" />
    </footer>
  </div>
</template>

<script>
import ErrorHandler from "@/mixins/ErrorHandler";
import axios from "axios";

export default {
  name: 'TheItemDefinitiveDeletion',
  mixins: [ErrorHandler],
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      waitingFormResponse: false,
      loading: false
    }
  },
  computed: {
    itemId() {
      return this.item.id;
    }
  },
  methods: {
    async confirmDefinitiveDeletion() {
      this.waitingFormResponse =  true;

      try {
        await axios.delete(`/api/v1/items/${this.itemId}`);
        await this.$router.push("/items");

        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('notif-success-item-definitive-deletion'),
          pauseOnHover: true
        });

        this.$emit('close');
      } catch (error) {
        this.snackbarError(error);
      }

      this.waitingFormResponse =  false;
    }
  }
}
</script>
