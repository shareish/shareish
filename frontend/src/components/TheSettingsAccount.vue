<template>
  <section class="settings column">
    <div class="box">
      <h2 class="title">{{ $t('general-information') }}</h2>
      <div class="columns is-flex-wrap-wrap">
        <div class="column is-half">
          <b-field key="first_name" :message="errors.first('first_name')" :type="{'is-danger': errors.has('first_name')}">
            <template #label>
              <b-tooltip key="first_name" :label="$t('help_firstname')" multilined position="is-right">
                {{ $t('firstname') }}
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-input v-model="internalUser['first_name']" v-validate="'required'" name="first_name" type="text" />
          </b-field>
        </div>
        <div class="column is-half">
          <b-field key="last_name" :message="errors.first('last_name')" :type="{'is-danger': errors.has('last_name')}">
            <template #label>
              <b-tooltip key="last_name" :label="$t('help_lastname')" multilined position="is-right">
                {{ $t('lastname') }}
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-input v-model="internalUser['last_name']" v-validate="'required'" name="last_name" type="text" />
          </b-field>
        </div>
        <div class="column is-half">
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
        <div class="column is-half">
          <b-field key="username" :message="errors.first('username')" :type="{'is-danger': errors.has('username')}">
            <template #label>
              <b-tooltip key="username" :label="$t('help_username')" multilined position="is-right">
                {{ $t('username') }}
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-input v-model="internalUser['username']" v-validate="'required'" name="username" type="text" />
          </b-field>
        </div>
      </div>
    </div>
    <div class="box">
      <h2 class="title">{{ $t('privacy') }}</h2>
      <div class="columns is-mobile is-align-content-space-between is-align-items-center">
        <div class="column">
          <b-tooltip :label="$t('help_save-items-you-see')" multilined position="is-right">
            <p class="label">
              {{ $t('save-items-you-see') }}
              <i class="icon far fa-question-circle"></i>
            </p>
          </b-tooltip>
        </div>
        <div class="column" style="flex: 0 0 auto;">
          <b-button
              style="width: 120px;"
              :type="internalUser['save_item_viewing'] ? 'is-success' : 'is-danger'"
              @click="internalUser['save_item_viewing'] = !internalUser['save_item_viewing']"
          >
            {{ $t(internalUser['save_item_viewing'] ? 'yes' : 'no') }}
          </b-button>
        </div>
      </div>
    </div>
    <b-button :label="$t('save')" type="is-primary" :loading="waitingFormResponse" @click="save" />
  </section>
</template>


<script>
import axios from 'axios';
import ErrorHandler from "@/mixins/ErrorHandler";

export default {
  name: 'TheSettingsAccount',
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
      waitingFormResponse: false,
      timeouts: {}
    }
  },
  created() {
    document.title = 'Shareish | Settings: Account';
    this.internalUser = {
      'first_name': this.user.first_name,
      'last_name': this.user.last_name,
      'email': this.user.email,
      'username': this.user.username,
      'save_item_viewing': this.user.save_item_viewing
    };
  },
  methods: {
    async save() {
      this.waitingFormResponse = true;

      clearTimeout(this.timeouts['save']);
      this.timeouts['save'] = setTimeout(async () => {
        let result = await this.$validator.validateAll();
        if (result) {
          try {
            await axios.patch('/api/v1/webusers/me/', this.internalUser);

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
      }, 400);
    }
  }
};
</script>
