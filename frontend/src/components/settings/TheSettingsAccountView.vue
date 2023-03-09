<template>
  <section class="settings column">
    <div class="tile is-ancestor">
      <div class="tile is-parent">
        <div class="tile is-child box">
          <b-field key="email" :message="errors.first('email')" :type="{'is-danger': errors.has('email')}">
            <template #label>
              <b-tooltip key="email" :label="$t('help_email')" multilined position="is-right">
                {{ $t('email') }}
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-input v-model="internalUser['email']" v-validate="'required|email'" name="email" type="text" />
          </b-field>
        </div>
      </div>
    </div>
    <b-button :label="$t('save')" type="is-primary" :loading="waitingFormResponse" @click="save" />
  </section>
</template>


<script>
import axios from 'axios';
import ErrorHandler from "@/components/ErrorHandler";

export default {
  name: 'TheSettingsAccountView',
  mixins: [ErrorHandler],
  $_veeValidate: {
    validator: 'new'
  },
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      internalUser: null,
      waitingFormResponse: false
    }
  },
  created() {
    document.title = 'Shareish | Settings: Account';
    this.internalUser = {...this.user};
  },
  methods: {
    async save() {
      this.waitingFormResponse = true;

      let result = await this.$validator.validateAll();
      if (result) {
        try {
          let tempUser = {...this.internalUser}
          delete tempUser.images;
          delete tempUser.items;

          this.internalUser = (await axios.patch('/api/v1/webusers/me/', tempUser)).data;

          this.$buefy.snackbar.open({
            duration: 5000,
            type: 'is-success',
            message: this.$t('notif-success-user-update'),
            pauseOnHover: true,
          });

          this.$emit('updateUser', this.internalUser);
        }
        catch (error) {
          this.fullErrorHandling(error);
        }
      }

      this.waitingFormResponse = false;
    }
  }
};
</script>

<style scoped>
@media screen and (max-width: 1023px) {
  .tile.is-ancestor, .tile.is-parent {
    display: block;
  }
}
</style>
