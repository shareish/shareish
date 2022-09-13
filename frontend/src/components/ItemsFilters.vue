<template>
  <b-field grouped>
    <b-field expanded :label="$t('what-are-you-looking-for')">
      <b-input :placeholder="$t('search...')"
        type="search"
        icon-pack="fas"
        icon="search">
      </b-input>
    </b-field>
    <b-field :label="$t('item-type')">
      <b-select>
        <option value=null>{{ $t('all') }}</option>
        <option value="BR">{{ $t('request') }}</option>
        <option value="DN">{{ $t('donation') }}</option>
        <option value="LN">{{ $t('loan') }}</option>
      </b-select>
    </b-field>
    <category-selector number="1"></category-selector>
    <category-selector number="2"></category-selector>
    <category-selector number="3"></category-selector>
  </b-field>
</template>

<script>
import CategorySelector from '@/components/CategorySelector';
export default {
  name: 'ItemsFilters',
  components: {CategorySelector}
};
</script>

<style scoped>

</style>