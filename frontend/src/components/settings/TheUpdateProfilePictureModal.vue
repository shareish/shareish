<template>
  <b-loading v-if="loading" :active="true" :is-full-page="false" />
  <div v-else class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">{{ $t('profile-picture') }}</p>
      <button class="delete" type="button" @click="$emit('close')" />
    </header>
    <section class="modal-card-body">
      <div class="media mb-3">
        <div class="media-left">
          <b-image class="image" v-if="preview !== null" :src="preview" ratio="1by1" />
          <b-image class="image" v-else-if="user.images.length > 0" :src="user.images[0]" ratio="1by1" />
          <b-image class="image" v-else ratio="1by1" src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg"></b-image>
        </div>
        <div class="media-content">
          <h2 class="title is-size-5 mb-4">{{ $t('current-profile-picture') }}</h2>
          <b-field class="file is-primary">
            <b-upload v-model="fileSelected" accept="image/*" class="file-label">
              <span class="file-cta">
                <b-icon class="file-icon" icon="upload"></b-icon>
                <span class="file-label">{{ $t('upload-a-new-one') }}</span>
              </span>
            </b-upload>
          </b-field>
        </div>
      </div>
      <div id="profile-images">
        <hr />
        <h2 class="title is-size-5 mb-3">{{ $t('current-profile-pictures') }}</h2>
        <p class="mb-5" v-html="$t('info-already-uploaded-profile-pictures')"></p>
        <div v-if="user.images.length > 0" class="columns is-mobile is-flex-wrap-wrap">
          <div v-for="(image, index) in user.images" :key="index" class="column" :class="imagesPreviewColumnSizeClass">
            <div class="square">
              <figure class="image" @click="reuseImage(index)">
                <b-image :src="image" ratio="1by1" />
              </figure>
              <div class="remove" @click="clickRemoveImage(index)">
                <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
                  <path d="M195.2 195.2a64 64 0 0 1 90.496 0L512 421.504 738.304 195.2a64 64 0 0 1 90.496 90.496L602.496 512 828.8 738.304a64 64 0 0 1-90.496 90.496L512 602.496 285.696 828.8a64 64 0 0 1-90.496-90.496L421.504 512 195.2 285.696a64 64 0 0 1 0-90.496z" />
                </svg>
              </div>
            </div>
          </div>
        </div>
        <p v-else><em>{{ $t('info-no-profile-picture-uploaded-yet') }}</em></p>
      </div>
    </section>
    <footer class="modal-card-foot">
      <b-button :label="$t('cancel')" @click="$emit('close')" />
      <b-button :label="$t('save')" type="is-primary" :loading="waitingFormResponse" @click="save" />
    </footer>
  </div>
</template>

<script>
import ErrorHandler from "@/components/ErrorHandler";
import WindowSize from "@/components/WindowSize";
import axios from "axios";

export default {
  name: 'TheUpdateProfilePictureModal',
  mixins: [ErrorHandler, WindowSize],
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      waitingFormResponse: false,
      imagesPreviewColumnSizeClass: 'is-one-fifth',
      loading: false,
      fileSelected: null,
      filename: null,
      preview: null
    }
  },
  watch: {
    fileSelected() {
      if (this.fileSelected !== null) {
        this.processImage(this.fileSelected);
        this.fileSelected = null;
      }
    }
  },
  methods: {
    async processImage(file) {
      this.loading = true;

      this.filename = file.name;
      const reader = new FileReader();
      reader.addEventListener('load', () => {
        this.preview = reader.result
      });
      reader.readAsDataURL(file);

      this.loading = false;
    },
    clickRemoveImage(index) {
      this.$buefy.dialog.confirm({
        title: this.$t('removing-picture'),
        message: this.$t('removing-picture-confirmation'),
        confirmText: this.$t('remove'),
        cancelText: this.$t('cancel'),
        type: 'is-danger',
        hasIcon: true,
        onConfirm: () => this.removeImage(index)
      });
    },
    async reuseImage(index) {
      this.$buefy.toast.open("Re-use process not done yet!");
      // Re-use image process
    },
    async removeImage(index) {
      this.$buefy.toast.open("Remove process not done yet!");
      // Remove image process

      // try {
      //   await axios.delete("/api/v1/user_image/", data);
      //   this.$buefy.toast.open('Picture removed!');
      // } catch (error) {
      //   this.snackbarError(error);
      // }
    },
    async save() {
      this.waitingFormResponse =  true;

      if (this.filename !== null) {
        let data = new FormData();
        data.append('user_id', this.user['id']);

        const blob = await (await fetch(this.preview)).blob();
        const image = new File([blob], this.filename);
        data.append('image', image);

        let image_url = (await axios.post("/api/v1/user_image/", data)).data;
        this.user.images.unshift(image_url);
        this.$emit('close');
      } else {
        this.$emit('close');
      }

      this.waitingFormResponse =  false;
    }
  }
}
</script>

<style scoped>
#profile-images .square {
  position: relative;
}

#profile-images .square .image {
  cursor: pointer;
}

#profile-images .square .remove {
  position: absolute;
  top: 8px;
  right: 8px;
  height: 20%;
  width: 20%;
  padding: 5px;
  border-radius: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  cursor: pointer;
}

#profile-images .square .remove svg {
  position: absolute;
  top: 50%;
  left: 50%;
  height: 60%;
  width: 60%;
  transform: translate(-50%, -50%);
  fill: white;
}

.media .media-left .image {
  height: 128px;
  width: 128px;
}
</style>