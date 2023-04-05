<template>
  <div class="toggle-box" :class="{'is-rounded': rounded, 'is-opened': contentDisplayed}">
    <div class="title" :class="[finalTitleSize, type, {'is-outlined': outlined}]" @click="contentDisplayed = !contentDisplayed">
      <div class="columns is-mobile">
        <div class="column">{{ title }}</div>
        <div class="column" style="flex: 0 0 30px;"><i class="fas fa-chevron-down"></i></div>
      </div>
    </div>
    <div class="content">
      <div class="inner">
        <slot />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ToggleBox",
  props: {
    title: {
      type: String,
      required: true
    },
    titleSize: {
      type: Number,
      required: false,
      default: 5,
      validator: function (value) {
        return value >= 1 && value <= 6;
      }
    },
    type: {
      type: String,
      required: false,
      default: "is-primary",
      validator: function (value) {
        return ["is-primary"].indexOf(value) !== -1;
      }
    },
    rounded: {
      type: Boolean,
      required: false,
      default: true
    },
    outlined: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  data() {
    return {
      contentDisplayed: false
    }
  },
  created() {
    this.size = Math.floor(this.size);
  },
  computed: {
    finalTitleSize() {
      return 'is-size-' + this.titleSize;
    }
  }
}
</script>

<style lang="scss" scoped>
@import "../assets/styles/colors";

.toggle-box {
  .title {
    padding: 0.75rem;
    margin-bottom: 0 !important;
    cursor: pointer;

    &.is-outlined {
      background-color: #fff !important;
      border: 1px solid;

      &.is-primary {
        color: $primary;
        border-color: $primary;
      }
    }
    &:not(.is-outlined) {
      color: white;

      &.is-primary {
        background-color: $primary;
      }
    }

    .columns .column:last-child i {
      display: block;
      margin-top: 1px;
      transition: 0.2s;
    }
  }

  .content {
    height: 0;
    box-sizing: border-box;
    background: #f8f8f8;
    border-radius: 0 0 5px 5px;
    overflow: hidden;
    transition: 0.2s;

    .inner {
      padding: 0.75rem;
    }
  }

  &.is-rounded {
    .title {
      border-radius: 5px;
    }
  }

  &.is-opened {
    &.is-rounded {
      .title {
        border-radius: 5px 5px 0 0;
      }
    }

    .title {
      .columns .column:last-child i {
        margin-top: 0;
        transform: rotate(180deg);
      }
    }

    .content {
      height: auto;
    }
  }
}
</style>