<template>
  <div id="page-error-404" class="has-text-centered py-6">
    <h1 class="title">{{ $t('this-page-doesnt-exist') }}...</h1>
    <p class="subtitle">{{ $t('to-get-back-to-home') }}, <router-link :to="{name: 'home'}">{{ $t('click-here') }}</router-link>.</p>
  </div>
</template>

<script>
export default {
  name: "TheError404View"
}
</script>

<style scoped>

</style>