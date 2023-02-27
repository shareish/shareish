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
    <b-button :label="$t('save')" type="is-primary" @click="save" />
  </section>
</template>


<script>
import axios from 'axios';

export default {
  name: 'SettingsAccount',
  $_veeValidate: {
    validator: 'new'
  },
  props: {
    user: Object
  },
  data() {
    return {
      internalUser: null
    }
  },
  created() {
    document.title = 'Shareish | Settings: Account';
    this.internalUser = {...this.user};
  },
  methods: {
    async save() {
      let result = await this.$validator.validateAll();
      if (result) {
        try {
          let tempUser = {...this.internalUser}
          delete tempUser.images;
          delete tempUser.items;

          this.internalUser = (await axios.patch('/api/v1/users/me/', tempUser)).data;

          this.$buefy.snackbar.open({
            duration: 5000,
            type: 'is-success',
            message: this.$t('notif-success-user-update'),
            pauseOnHover: true,
          });

          this.$emit('updateUser', this.internalUser);
        } catch (error) {
          console.log(error);
          this.$buefy.snackbar.open({
            duration: 5000,
            type: 'is-danger',
            message: this.$t('notif-error-user-update'),
            pauseOnHover: true,
          })
        }
      }
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
