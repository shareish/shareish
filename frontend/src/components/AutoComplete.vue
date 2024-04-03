<template>
    <b-autocomplete
      rounded
      v-model="address"
      placeholder="e.g. jQuery"
      icon="fas fa-search"
      clearable
      @input="$emit('input', $event)"
      :data="this.suggestions"
      expanded>
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
                const response = await axios.get('https://photon.komoot.io/api/?q=' + this.address);
                const suggestions = response.data.features.map(feature => {
                    const { country, county, city, postcode } = feature.properties;
                    let address = '';
                    if (country) address += country;
                    if (county) address += `, ${county}`;
                    if (city) address += `, ${city}`;
                    if (postcode) address += `, ${postcode}`;
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
        }
    }
  };
  </script>
  