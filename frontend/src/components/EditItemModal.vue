<template>
  <form @submit.prevent="save()">
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">{{$t('edit-item')}}</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')"/>
      </header>
      <section class="modal-card-body">
        <b-field :label="$t('name')">
          <b-input v-model="internalItem.name" />
        </b-field>
        <b-field :label="$t('item-type')">
          <b-select v-model="internalItem.item_type" expanded>
            <option value="BR">{{ $t('request') }}</option>
            <option value="DN">{{ $t('donation') }}</option>
            <option value="LN">{{ $t('loan') }}</option>
          </b-select>
        </b-field>
        <div class="columns">
          <category-selector class="column" :number="1" v-model="internalItem.category1"
                             :nullable="false" expanded/>
          <category-selector class="column" :number="2" v-model="internalItem.category2"
                             :nullable="false" expanded/>
          <category-selector class="column" :number="3" v-model="internalItem.category3"
                             :nullable="false" expanded/>
        </div>
        <b-field :label="$t('address')">
          <b-input v-model="internalItem.address" />
        </b-field>
        <b-field :label="$t('description')">
          <b-input type="textarea" expanded v-model="internalItem.description" />
        </b-field>
        <b-field grouped>
          <b-field :label="$t('start-date')" expanded>
            <b-datetimepicker
              icon-pack="fas"
              icon="calendar"
              v-model="internalItem.startdate"
            >
            </b-datetimepicker>
          </b-field>
          <b-field :label="$t('end-date')" expanded>
            <b-datetimepicker
              icon-pack="fas"
              icon="calendar"
              v-model="internalItem.enddate"
              :min-date="internalItem.startdate"
            >
            </b-datetimepicker>
          </b-field>
        </b-field>
        <b-field>
          <b-checkbox v-model="internalItem.is_recurrent">
            <strong>{{$t('save-as-recurrent-item')}}</strong>
          </b-checkbox>
        </b-field>

        <b-field
          :label="$t('item-image')"
          :message="$t('item-image-info')"
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
import moment from 'moment/moment';
import CategorySelector from '@/components/CategorySelector';

export default {
  name: 'EditItemModal',
  components: {CategorySelector},
  props: {
    item: Object,
    address: String,
  },
  data() {
    return {
      internalItem: {},
      displayErrors: false,
      file: null,
    }
  },
  computed: {
  },
  methods: {
    async save() {

      try {
        let startDate;
        if (this.internalItem.startdate) {
          startDate = moment(this.internalItem.startdate).format('YYYY-MM-DD[T]HH:mm:ss');
        }
        else {
          startDate = moment().format('YYYY-MM-DD[T]HH:mm:ss');
        }

        let endDate;
        if (this.internalItem.enddate) {
          endDate = moment(this.internalItem.enddate).format('YYYY-MM-DD[T]HH:mm:ss');
        }

        let item = (await axios.patch(`/api/v1/items/${this.item.id}/`, {
          name: this.internalItem.name,
          item_type: this.internalItem.item_type,
          category1: this.internalItem.category1,
          category2: (this.internalItem.category2) ? this.internalItem.category2 : '',
          category3: (this.internalItem.category3) ? this.internalItem.category3 : '',
          description: this.internalItem.description,
          location: this.internalItem.address,
          is_recurrent: this.internalItem.is_recurrent,
          startdate: startDate,
          enddate: endDate,
        })).data;

        if (this.file) {
          let data = new FormData();
          data.append('itemID', this.item.id);
          data.append('image', this.file);
          const image = (await axios.post('/api/v1/images/', data)).data;
          item.images = [image.url];
          this.file = null;
        }

        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('notif-success-item-update'),
          pauseOnHover: true,
        });
        this.$emit('close');
        this.$emit('updateItem', item);
      }
      catch(error) {
        console.log(error);
        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-danger',
          message: this.$t('notif-error-item-update'),
          pauseOnHover: true,
        })
      }
    },
  },
  mounted() {
    this.internalItem = {...this.item};
    if (this.internalItem.startdate) {
        this.internalItem.startdate = new Date(this.internalItem.startdate);
    }
    if (this.internalItem.enddate) {
        this.internalItem.enddate = new Date(this.internalItem.enddate);
    }
    this.internalItem.address = this.address;
    delete this.internalItem.images;
  }
};
</script>

<style scoped>

</style>