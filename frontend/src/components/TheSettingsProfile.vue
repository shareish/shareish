<template>
  <section class="settings column">
    <div class="media mb-5">
      <div class="media-left box">
        <b-image v-if="user.images.length > 0" :src="user.images[0].url" ratio="1by1" />
        <b-image v-else ratio="1by1" src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg"></b-image>
      </div>
      <div class="media-content box">
        <h4 class="title is-size-5 mb-3">
          <b-tooltip multilined position="is-bottom">
            <template v-slot:content>
              <p v-html="$t('info-profile-picture-recommendation')"></p>
            </template>
            {{ $tc('profile-picture', user.images.length) }} ({{ user.images.length }})
            <i class="icon far fa-question-circle"></i>
          </b-tooltip>
        </h4>
        <div id="profile-images" class="columns is-mobile is-flex-wrap-wrap">
          <template v-if="user.images.length > 0">
            <template v-for="(image, index) in user.images">
              <div :key="index" v-if="index < maxImagesToShow[imagesPreviewColumnSizeClass]" class="column" :class="imagesPreviewColumnSizeClass">
                <figure class="image">
                  <b-image :src="image.url" ratio="1by1" />
                </figure>
              </div>
            </template>
            <div v-if="user.images.length > maxImagesToShow[imagesPreviewColumnSizeClass]" class="column" :class="imagesPreviewColumnSizeClass">
              <div class="square image-placeholder" @click="manageProfilePictures()">
                <div class="square-content">
                  <p><small>{{ $tc('and-n-more', user.images.length - maxImagesToShow[imagesPreviewColumnSizeClass]) }}</small></p>
                </div>
              </div>
            </div>
          </template>
          <template v-else>
            <div class="column" :class="imagesPreviewColumnSizeClass">
              <div class="square image-placeholder" @click="manageProfilePictures()">
                <div class="square-content">
                  <p><small>{{ $t('no-images') }}</small></p>
                </div>
              </div>
            </div>
          </template>
        </div>
        <b-button type="is-primary" @click="manageProfilePictures()">{{ $t('manage-profile-picture') }}</b-button>
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
        <b-input v-model="internalUser['description']" name="description" type="textarea" />
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
            <b-input v-model="internalUser['instagram_url']" name="instagram_url" type="text" />
          </b-field>
        </div>
      </div>
    </div>
    <b-button :label="$t('save')" type="is-primary" :loading="waitingFormResponse" @click="save" />
  </section>
</template>


<script>
import axios from 'axios';
import ErrorHandler from "@/mixins/ErrorHandler";
import TheManageProfilePicturesModal from "@/components/TheManageProfilePicturesModal.vue";
import WindowSize from "@/mixins/WindowSize";

export default {
  name: 'TheSettingsProfile',
  mixins: [ErrorHandler, WindowSize],
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
      imagesPreviewColumnSizeClass: 'is-2',
      maxImagesToShow: {
        'is-one-third': 2,
        'is-one-quarter': 3,
        'is-one-fifth': 4,
        'is-2': 5
      }
    }
  },
  created() {
    document.title = "Shareish | Settings: Profile";
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

          this.internalUser = (await axios.patch("/api/v1/webusers/me/", tempUser)).data;

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
    },
    updatePictures() {

    },
    manageProfilePictures() {
      this.$buefy.modal.open({
        parent: this,
        props: {
          user: this.user
        },
        events: {updatePictures: this.updatePictures},
        component: TheManageProfilePicturesModal,
        hasModalCard: true,
        trapFocus: true,
      });
    },
    windowWidthChanged() {
      let imagesPreviewColumnSizeClass = 'is-2';
      if (this.windowWidth < 1340) {
        imagesPreviewColumnSizeClass = 'is-one-fifth';
        if (this.windowWidth < 1190) {
          imagesPreviewColumnSizeClass = 'is-one-quarter';
          if (this.windowWidth < 1070) {
            imagesPreviewColumnSizeClass = 'is-one-third';
            if (this.windowWidth < 1024) {
              imagesPreviewColumnSizeClass = 'is-one-quarter';
              if (this.windowWidth < 840) {
                imagesPreviewColumnSizeClass = 'is-one-third';
                if (this.windowWidth < 769) {
                  imagesPreviewColumnSizeClass = 'is-one-quarter';
                  if (this.windowWidth < 550) {
                    imagesPreviewColumnSizeClass = 'is-one-third';
                  }
                }
              }
            }
          }
        }
      }
      this.imagesPreviewColumnSizeClass = imagesPreviewColumnSizeClass;
    }
  }
};
</script>

<style scoped>
.media-left {
  width: 200px;
}

.square {
  position: relative;
  width: 100%;
  overflow: hidden;
}
.square:before {
  content: "";
  display: block;
  padding-top: 100%;
}
.square-content {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
}

#profile-images .image-placeholder {
  cursor: pointer;
  background-color: #3eaf7c;
}

#profile-images .image-placeholder p {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
}

@media screen and (max-width: 1023px) {
  .media {
    display: block;
  }

  .media-left {
    margin: 0 auto;
  }

  .tile.is-ancestor, .tile.is-parent {
    display: block;
  }
}
</style>
