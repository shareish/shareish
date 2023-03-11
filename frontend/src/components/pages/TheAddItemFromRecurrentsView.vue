<template>
  <div id="page-add-item-from-recurrents">
    <h1 class="title has-text-centered mb-6">
      {{ $t('add-new-item-from-recurrents') }}
      <b-tooltip :label="$t('help_add_item')" multilined position="is-bottom">
        <i class="icon far fa-question-circle"></i>
      </b-tooltip>
    </h1>
    <recurrent-items-list></recurrent-items-list>
  </div>
</template>

<script>
import RecurrentItemsList from "@/components/RecurrentItemsList";

export default {
  name: 'TheAddItemFromRecurrentsView',
  components: {RecurrentItemsList},
  created() {
    document.title = `Shareish | ${this.$t('add-new-item-from-recurrents')}`;
  }
};
</script>
