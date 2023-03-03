<template>
  <div>
    <h1 class="title">{{ $t('my-recurrent-items') }}</h1>
    <b-loading v-if="loading" :active="loading" :is-full-page="false" />
    <template v-else>
      <div v-if="items && items.length" class="columns">
        <div v-for="item in items" :key="`${item.id}-item-card-recurrent`" class="column is-one-quarter">
          <item-card :item="item" :recurrent-list="true" @submitAgain="$emit('submitAgain', $event)" />
        </div>
      </div>
      <div v-else>{{ $t('no-items') }}</div>
    </template>
  </div>
</template>

<script>
import ItemCard from '@/components/ItemCard';
import axios from 'axios';
import ErrorHandler from "@/components/ErrorHandler";

export default {
  name: 'RecurrentItemsList',
  mixins: [ErrorHandler],
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
        this.items = (await axios.get('/api/v1/recurrents/')).data;
      }
      catch (error) {
        this.snackbarError(error);
      }
    }
  },
  async mounted() {
    this.loading = true;
    await Promise.all([
      this.fetchItems()
    ]);
    this.loading = false;
  }
};
</script>

<style scoped>
.columns {
  flex-wrap: wrap;
  align-content: flex-start;
}

.column:not(.is-narrow) {
  min-width: 25rem;
}
</style>
