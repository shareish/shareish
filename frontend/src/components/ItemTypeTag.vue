<template>
  <span :class="color" class="item-type tag is-normal">{{ $t(this.text) }}</span>
</template>

<script>
const itemTypeIcons = {
  "DN": "is-success",
  "LN": "is-warning",
  "BR": "is-danger",
  "EV": "is-purple"
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
