import Vue from "vue";
import Buefy from "buefy";
import i18n from "../../src/i18n";
import VeeValidate from "vee-validate";

Vue.use(VeeValidate, {
  i18nRootKey: 'validations',
  i18n,
  inject: false
});

Vue.use(Buefy);