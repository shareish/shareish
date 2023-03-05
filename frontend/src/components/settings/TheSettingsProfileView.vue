<template>
  <section class="settings column">
    <div class="tile is-ancestor">
      <div class="tile is-parent">
        <div class="tile is-child box">
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
      </div>
      <div class="tile is-parent">
        <div class="tile is-child box">
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
      </div>
    </div>
    <div class="tile is-ancestor">
      <div class="tile is-parent">
        <div class="tile is-child box">
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
      <div class="tile is-parent">
        <div class="tile is-child box">
          <b-field :label="$t('avatar')">
            <template #label> {{ $t('avatar') }}
              <b-tooltip :label="$t('help_avatar')" multilined position="is-right">
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-field :class="{'has-name': !!file}" class="file is-primary">
              <b-upload v-model="file" accept="image/*" class="file-label" validationMessage="Please select a file">
                <span class="file-cta">
                  <b-icon class="file-icon" icon="upload"></b-icon>
                  <span class="file-label">Click to upload</span>
                </span>
                <span v-if="file" class="file-name">{{ file.name }}</span>
              </b-upload>
            </b-field>
          </b-field>
        </div>
      </div>
    </div>
    <div class="box">
      <b-field key="description" :message="errors.first('description')" :type="{'is-danger': errors.has('description')}">
        <template #label>
          <b-tooltip key="description" :label="$t('help_biography')" multilined position="is-right">
            {{ $t('biography') }}
            <i class="icon far fa-question-circle"></i>
          </b-tooltip>
        </template>
        <b-input v-model="internalUser['description']" v-validate="'required'" name="description" type="textarea" />
      </b-field>
    </div>
    <div class="tile is-ancestor">
      <div class="tile is-parent">
        <div class="tile is-child box">
          <b-field key="homepage_url" :message="errors.first('homepage_url')" :type="{'is-danger': errors.has('homepage_url')}">
            <template #label>
              <b-tooltip key="homepage_url" :label="$t('help_homepage')" multilined position="is-right">
                {{ $t('homepage-link') }}
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-input v-model="internalUser['homepage_url']" v-validate="'url'" name="homepage_url" type="text" />
          </b-field>
        </div>
      </div>
      <div class="tile is-parent">
        <div class="tile is-child box">
          <b-field key="facebook_url" :message="errors.first('facebook_url')" :type="{'is-danger': errors.has('facebook_url')}">
            <template #label>
              <b-tooltip key="facebook_url" :label="$t('help_facebook')" multilined position="is-right">
                {{ $t('facebook-link') }}
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-input v-model="internalUser['facebook_url']" v-validate="'url'" name="facebook_url" type="text" />
          </b-field>
        </div>
      </div>
      <div class="tile is-parent">
        <div class="tile is-child box">
          <b-field key="instagram_url" :message="errors.first('instagram_url')" :type="{'is-danger': errors.has('instagram_url')}">
            <template #label>
              <b-tooltip key="instagram_url" :label="$t('help_instagram')" multilined position="is-right">
                {{ $t('instagram-link') }}
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-input v-model="internalUser['instagram_url']" v-validate="'url'" name="instagram_url" type="text" />
          </b-field>
        </div>
      </div>
    </div>
    <b-button :label="$t('save')" type="is-primary" @click="save" />
  </section>
</template>


<script>
import axios from 'axios';
import ErrorHandler from "@/components/ErrorHandler";

export default {
  name: 'TheSettingsProfileView',
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
      file: null
    }
  },
  created() {
    document.title = 'Shareish | Settings: Profile';
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

          this.internalUser = (await axios.patch('/api/v1/webusers/me/', tempUser)).data;

          if (this.file) {
            let data = new FormData();
            data.append('user_id', this.internalUser['id']);
            data.append('image', this.file);
            let image_url = (await axios.post('/api/v1/user_image/', data)).data;
            this.internalUser.images.push(image_url);
            this.file = null;
          }

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
