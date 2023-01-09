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
	<template v-for="{field, validationRules, type, translationKey,helpTranslationKey} in editableFields">
	  <b-field :key="field" :type="{'is-danger': errors.has(field)}" :message="errors.first(field)">
	    <template #label> 
	      <b-tooltip position="is-right" :key="field" :label="$t(helpTranslationKey)" multilined>{{$t(translationKey)}} <i class="icon far fa-question-circle"></i> </b-tooltip>
	    </template>
	  <b-input
            v-model="internalUser[field]"
            :name="field"
            v-validate="validationRules"
            :type="type"
            :password-reveal="field === 'password'"
            />
	 
	  </b-field>
	</template>
        <b-field
          :label="$t('avatar')"
          :message="$t('avatar-info')"
          >
	  <template #label> {{$t('avatar')}}
	  <b-tooltip position="is-right" :label="$t('help_avatar')" multilined> <i class="icon far fa-question-circle"></i></b-tooltip></template>
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
      user: Object,
      address: String,
  },
  $_veeValidate: {validator: 'new'},
  data() {
    return {
	internalUser: {},
	//address : null,
      displayErrors: false,
      file: null,
    }
  },
  computed: {
    editableFields() {
      return [
          {field: 'first_name', validationRules: 'required', type: 'text', translationKey: 'firstname', helpTranslationKey: 'help_firstname'},
        {field: 'last_name', validationRules: 'required', type: 'text', translationKey: 'lastname', helpTranslationKey: 'help_lastname'},
        {field: 'username', validationRules: 'required', type: 'text', translationKey: 'username', helpTranslationKey: 'help_username'},
        {field: 'email', validationRules: 'required|email', type: 'text', translationKey: 'email', helpTranslationKey: 'help_email'},
	{field: 'ref_location', validationRules: '', type: 'text', translationKey: 'reflocation', helpTranslationKey: 'help_ref_location'},
	{field: 'dwithin_notifications', validationRules: 'numeric|max_value:1000|min_value:0', type: 'text', translationKey: 'dwithin_notif', helpTranslationKey: 'help_dwithin'},  
        // {field: 'password', validationRules: 'min:8', type: 'password', translationKey: 'password'},
        {field: 'description', validationRules: '', type: 'textarea', translationKey: 'biography', helpTranslationKey: 'help_biography'},
        {field: 'homepage_url', validationRules: '', type: 'text', translationKey: 'homepage-link', helpTranslationKey: 'help_homepage'},
        {field: 'facebook_url', validationRules: '', type: 'text', translationKey: 'facebook-link', helpTranslationKey: 'help_facebook'},
        {field: 'instagram_url', validationRules: '', type: 'text', translationKey: 'instagram-link', helpTranslationKey: 'help_instagram'},
	
      ];
    },
  },
  methods: {
    async fetchAddress() {
      if (this.internalUser.ref_location === null) {
        return;
      }

      try {
        this.internalUser.ref_location = (await axios.post(
          `/api/v1/address/`,
          this.internalUser.ref_location
        )).data;
      }
      catch (error) {
        console.log(JSON.stringify(error));
      }
    },
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

    async mounted() {
    this.internalUser = {...this.user};
    await this.fetchAddress();    
    delete this.internalUser.image;
    delete this.internalUser.items;
  }

    
};
</script>

<style scoped>

</style>
