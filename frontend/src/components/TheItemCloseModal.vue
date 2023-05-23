<template>
  <b-loading v-if="loading" :active="true" :is-full-page="false" />
  <div v-else class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">{{ $tc('cloturer-the-item') }}</p>
      <button class="delete" type="button" @click="$emit('close')" />
    </header>
    <section class="modal-card-body">
      <p class="mb-5">{{ $t('help_item-close') }}</p>
      <p class="mb-3"><b>{{ $t('why-item-close') }}</b></p>
      <b-field>
          <b-radio v-model="closingReasonRadioGroup" native-value="ON">{{ $t('close-option-' + item.type + '-on-shareish') }}</b-radio>
      </b-field>
      <b-field>
          <b-radio v-model="closingReasonRadioGroup" native-value="OUT">{{ $t('close-option-' + item.type + '-outside-shareish') }}</b-radio>
      </b-field>
      <b-field>
          <b-radio v-model="closingReasonRadioGroup" native-value="NOT">{{ $t('close-option-' + item.type + '-not') }}</b-radio>
      </b-field>
      <b-field>
          <b-radio v-model="closingReasonRadioGroup" native-value="OTH">{{ $t('close-option-other') }}</b-radio>
      </b-field>
    </section>
    <footer class="modal-card-foot">
      <b-button :label="$t('cancel')" @click="$emit('close')" />
      <b-button :label="$t('confirm-cloturer')" type="is-danger" :loading="waitingFormResponse" @click="confirmClose" />
    </footer>
  </div>
</template>

<script>
import ErrorHandler from "@/mixins/ErrorHandler";
import axios from "axios";

export default {
  name: 'TheItemCloseModal',
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
      loading: false,
      closingReasonRadioGroup: null
    }
  },
  computed: {
    itemId() {
      return this.item.id;
    }
  },
  methods: {
    async confirmClose() {
      this.waitingFormResponse =  true;

      const data = new FormData();
      data.append('reason', this.closingReasonRadioGroup);

      try {
        await axios.post(`/api/v1/items/${this.itemId}/close`, data);
        await this.$router.push("/items");

        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('notif-success-item-close'),
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
