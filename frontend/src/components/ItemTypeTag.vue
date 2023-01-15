<template>
  <span class="tag is-normal" :class="color">{{$t(this.text)}}</span>
</template>

<script>


const itemTypeIcons = {
    "DN": "is-success",
    "LN": "is-warning",
    "BR": "is-danger",
    "EV": "is-info"
}

const itemTypeSlug = {
    "DN": "donation",
    "LN": "loan",
    "BR": "request",
    "EV": "event"
}

export default {
  name: 'ItemTypeTag',
  props: ['type'],
  computed: {
    color() {
      return itemTypeIcons[this.type];
    },
    text() {
      return itemTypeSlug[this.type];
    }
  }
};
</script>

<style scoped>

</style>
