<template>
    <b-autocomplete
      rounded
      v-model="address"
      placeholder="e.g. jQuery"
      icon="fas fa-search"
      clearable
      @input="$emit('input', $event)"
      :data="this.suggestions"
      expanded
      >
      <template #empty>{{ $t('no_result') }}</template>
    </b-autocomplete>
</template>

  
  <script>
  import axios from 'axios';
  
  export default {
    name: "AutoComplete",
    props: { 
      value: String,
    },
    data() {
      return {
        address: this.value,
        suggestions: []
      };
    },
    methods: {
      async getSuggestion() {
      this.suggestions = [];
      try {
        const response = await axios.get('https://photon.komoot.io/api/?q=' + this.address + "&limit=5" + "&lang=" + this.$i18n.locale);
        const suggestions = response.data.features.map(feature => {
          const { housenumber,street,name,country, county, city, postcode } = feature.properties;
          let address = '';
          if (housenumber) address += (address ? `${housenumber}` : housenumber);
          if (street) address += (address ? `, ${street}` : street);
          if (country) address += (address ? `, ${country}` : country);
          if(name) address += (address ? `, ${name}` : name)
          if (city) address += (address ? `, ${city}` : city);
          if (postcode) address += (address ? `, ${postcode}` : postcode);
          if (county) address += (address ? `, ${county}` : county);
          return address;
        });
    this.suggestions = suggestions;
  } catch (error) {
    console.error('Error fetching suggestions:', error);
    this.suggestions = [];
  }
}
    },
    watch: {    
        address(newValue) {
        this.getSuggestion();
        },
        value(newValue){
          this.address = this.value
        }
    }
  };
  </script>
  