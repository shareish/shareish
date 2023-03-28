<template>
  <span :class="color" class="item-type tag is-normal">{{ $t(this.text) }}</span>
</template>

<script>
const itemTypeIcons = {
  "DN": "is-success",
  "LN": "is-warning",
  "RQ": "is-danger",
  "EV": "is-purple"
}

const itemTypeSlug = {
  "DN": "donation",
  "LN": "loan",
  "RQ": "request",
  "EV": "event"
}

export default {
  name: 'ItemTypeTag',
  props: {
    type: {
      type: String,
      required: true,
      validator: function (value) {
        return ["DN", "LN", "RQ", "EV"].indexOf(value) !== -1;
      }
    }
  },
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
  .item-type.tag {
    font-style: normal;
  }
</style>
