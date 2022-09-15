<template>
  <div>
    <h1 class="title">{{$t('my-recurrent-items')}}</h1>
    <b-loading :active="loading" :is-full-page="false" v-if="loading" />
    <template v-else>
      <div class="columns" v-if="items && items.length">
        <div class="column is-one-quarter" v-for="item in items" :key="`${item.id}-item-card-recurrent`">
          <item-card :item="item" :recurrent-list="true" @submitAgain="$emit('submitAgain', $event)" />
        </div>
      </div>
      <div v-else>
        {{$t('no-items')}}
      </div>
    </template>

  </div>
</template>

<script>
import ItemCard from '@/components/ItemCard';
import axios from 'axios';

export default {
  name: 'RecurrentItemsList',
  components: {ItemCard},
  data() {
    return {
      items: [],
      loading: true,
    }
  },
  methods: {
    async fetchItems() {
      try {
        const uri = '/api/v1/recurrents/';
        this.items = (await axios.get(uri)).data;
      }
      catch (error) {
        console.log(error);
      }
    },
  },
  async mounted() {
    this.loading = true;
    await this.fetchItems();
    this.loading = false;
  }
};
</script>

<style scoped>
.columns {
  flex-wrap: wrap;
  /*justify-content: space-between;*/
  align-content: flex-start;
}

.column:not(.is-narrow) {
  /*max-width: 25rem;*/
  min-width: 25rem;
}
</style>