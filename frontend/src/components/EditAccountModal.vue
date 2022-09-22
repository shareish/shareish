<template>
  <form @submit.prevent="save()">
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">{{$t('edit-my-account')}}</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')"/>
      </header>
      <section class="modal-card-body">
        <b-field
          v-for="{field, validationRules, type, translationKey} in editableFields"
          :key="field"
          :label="$t(translationKey)"
          :type="{'is-danger': errors.has(field)}"
          :message="errors.first(field)"
        >
          <b-input
            v-model="internalUser[field]"
            :name="field"
            v-validate="validationRules"
            :type="type"
            :password-reveal="field === 'password'"
          />
        </b-field>
        <b-field
          :label="$t('avatar')"
          :message="$t('avatar-info')"
        >
          <b-field
            class="file is-primary"
            :class="{'has-name': !!file}"
          >
            <b-upload v-model="file" class="file-label" accept="image/*" validationMessage="Please select a file">
            <span class="file-cta">
                <b-icon class="file-icon" icon="upload"></b-icon>
                <span class="file-label">Click to upload</span>
            </span>
              <span class="file-name" v-if="file">
                {{ file.name }}
            </span>
            </b-upload>
          </b-field>
        </b-field>
      </section>
      <footer class="modal-card-foot">
        <b-button
          :label="$t('cancel')"
          @click="$emit('close')" />
        <b-button
          :label="$t('save')"
          @click="save"
          type="is-primary" />
      </footer>
    </div>
  </form>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EditAccountModal',
  props: {
    user: Object
  },
  $_veeValidate: {validator: 'new'},
  data() {
    return {
      internalUser: {},
      displayErrors: false,
      file: null,
    }
  },
  computed: {
    editableFields() {
      return [
        {field: 'first_name', validationRules: 'required', type: 'text', translationKey: 'firstname'},
        {field: 'last_name', validationRules: 'required', type: 'text', translationKey: 'lastname'},
        {field: 'username', validationRules: 'required', type: 'text', translationKey: 'username'},
        {field: 'email', validationRules: 'required|email', type: 'text', translationKey: 'email'},
        // {field: 'password', validationRules: 'min:8', type: 'password', translationKey: 'password'},
        {field: 'description', validationRules: '', type: 'textarea', translationKey: 'biography'},
        {field: 'homepage_url', validationRules: '', type: 'text', translationKey: 'homepage-link'},
        {field: 'facebook_url', validationRules: '', type: 'text', translationKey: 'facebook-link'},
        {field: 'instagram_url', validationRules: '', type: 'text', translationKey: 'instagram-link'},
      ];
    },
  },
  methods: {
    async save() {
      let result = await this.$validator.validateAll();
      if(!result) {
        return;
      }

      try {
        if (this.file) {

        }
        let user = (await axios.patch('/api/v1/users/me/', this.internalUser)).data;

        if (this.file) {
          let data = new FormData();
          data.append('userID', this.user['id']);
          data.append('image', this.file);
          const image = (await axios.post('/api/v1/user_image/', data)).data;
          user.image = [image.url];
          this.file = null;
        }

        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('notif-success-user-update'),
          pauseOnHover: true,
        });
        this.$emit('close');
        this.$emit('updateUser', user);
      }
      catch(error) {
        console.log(error);
        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-danger',
          message: this.$t('notif-error-user-update'),
          pauseOnHover: true,
        })
      }
    },
  },
  mounted() {
    this.internalUser = {...this.user};
    delete this.internalUser.image;
    delete this.internalUser.items;
  }
};
</script>

<style scoped>

</style>