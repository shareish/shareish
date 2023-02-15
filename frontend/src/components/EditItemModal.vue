<template>
  <form @submit.prevent="save()">
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">{{ $t('edit-item') }}</p>
        <button class="delete" type="button" @click="$emit('close')" />
      </header>
      <section class="modal-card-body">
        <b-field :label="$t('name')">
          <b-input v-model="internalItem.name" />
        </b-field>
        <b-field>
          <template #label>
            {{ $t('item-type') }}
            <b-tooltip :label="$t('help_item_type')" multilined position="is-right">
              <i class="icon far fa-question-circle"></i>
            </b-tooltip>
          </template>
          <b-select v-model="internalItem.item_type" expanded>
            <option value="BR">{{ $t('request') }}</option>
            <option value="DN">{{ $t('donation') }}</option>
            <option value="LN">{{ $t('loan') }}</option>
            <option value="EV">{{ $t('event') }}</option>
          </b-select>
        </b-field>
        <div class="columns">
          <b-tooltip :label="$t('help_item_category')" multilined position="is-top">
            <category-selector v-model="internalItem.category1" :nullable="false" :number="1" class="column" expanded />
            <category-selector v-model="internalItem.category2" :nullable="false" :number="2" class="column" expanded />
            <category-selector v-model="internalItem.category3" :nullable="false" :number="3" class="column" expanded />
          </b-tooltip>
        </div>
        <b-field>
          <template #label>
            {{ $t('address') }}
            <b-tooltip :label="$t('help_item_address')" multilined position="is-right">
              <i class="icon far fa-question-circle"></i>
            </b-tooltip>
          </template>
          <b-input v-model="internalItem.address" />
        </b-field>
        <b-field>
          <template #label>
            {{ $t('description') }}
            <b-tooltip :label="$t('help_item_description')" multilined position="is-right">
              <i class="icon far fa-question-circle"></i>
            </b-tooltip>
          </template>
          <b-input v-model="internalItem.description" expanded type="textarea" />
        </b-field>
        <b-field grouped>
          <b-field expanded>
            <template #label>
              {{ $t('start-date') }}
              <b-tooltip :label="$t('help_item_start_date')" multilined position="is-top">
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-datetimepicker v-model="internalItem.startdate" icon="calendar" icon-pack="fas">
            </b-datetimepicker>
          </b-field>
          <b-field expanded>
            <template #label> {{ $t('end-date') }}
              <b-tooltip :label="$t('help_item_end_date')" multilined position="is-top">
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-datetimepicker v-model="internalItem.enddate" :min-date="internalItem.startdate" icon="calendar" icon-pack="fas">
            </b-datetimepicker>
          </b-field>
        </b-field>
        <b-field>
          <b-checkbox v-model="internalItem.is_recurrent">
            <strong>{{ $t('save-as-recurrent-item') }}</strong>
            <b-tooltip :label="$t('help_item_recurrent')" multilined position="is-top">
              <i class="icon far fa-question-circle"></i>
            </b-tooltip>
          </b-checkbox>
        </b-field>

        <b-field :label="$t('item-image')" :message="$t('item-image-info')">
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
      </section>
      <footer class="modal-card-foot">
        <b-button :label="$t('cancel')" @click="$emit('close')" />
        <b-button :label="$t('save')" type="is-primary" @click="save" />
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
  computed: {},
  methods: {
    async save() {
      try {
        let startDate;
        if (this.internalItem.startdate) {
          startDate = moment(this.internalItem.startdate).format('YYYY-MM-DD[T]HH:mm:ss');
        } else {
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
      } catch (error) {
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
