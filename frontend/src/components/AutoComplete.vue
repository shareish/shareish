<template>
    <b-autocomplete
      rounded
      v-model="address"
      group-field="type"
      group-options="suggestions"
      :placeholder="$t('address')"
      icon="fas fa-search"
      clearable
      @input="$emit('input', $event)"
      :data="this.data"
      expanded
      >
      <template #empty>{{ $t('no_result') }}</template>
    </b-autocomplete>
</template>

  
  <script>
  import axios from 'axios';
  import Vue from 'vue';
  
  export default {
    name: "AutoComplete",
    props: { 
      value: String,
      location: Object
    },
    data() {
      return {
        address: this.value,
        data: []  ,
        geolocation : this.location,
      };
    },
    methods: {
      async getSuggestion() {
        this.data.splice(0);
        try {
          const response = await axios.get('https://photon.komoot.io/api/?q=' + this.address + "&limit=10" + "&lang=" + this.$i18n.locale+ "&lon=" + this.geolocation.longitude + "&lat=" + this.geolocation.latitude);
          response.data.features.forEach(feature => {
            
            const { housenumber, street, name, country, county, city, postcode, osm_key,osm_value } = feature.properties;
            
            let address = '';
            
            if (housenumber) address += (address ? `${housenumber}` : housenumber);
            if (street) address += (address ? `, ${street}` : street);
            if (country) address += (address ? `, ${country}` : country);
            if (name) address += (address ? `, ${name}` : name)
            if (city) address += (address ? `, ${city}` : city);
            if (postcode) address += (address ? `, ${postcode}` : postcode);
            if (county) address += (address ? `, ${county}` : county);

            if(osm_key === "amenity")
            {
              if(osm_value === "give_box")
              {
                this.AddSuggestiontoCategory(this.$t("givebox"),address);
              }
              else if(osm_value ==="public_bookcase"){
                this.AddSuggestiontoCategory("PUBLIC BOOKCASE",address);
              }
              else if(osm_value === "food_sharing"){
                this.AddSuggestiontoCategory("FOOD SHARING",address);
              }
              else if(osm_value === "freeshop"){
                this.AddSuggestiontoCategory("FREE SHOP",address);
              }
              else if(osm_value === "drinking_water"){
                this.AddSuggestiontoCategory("DRINKING WATER",address);
              }
              else if(osm_value === "social_facility")
              {
                this.AddSuggestiontoCategory("SOCIAL FACILITY",address);
              }
              else if(osm_value === "emergency"){
                this.AddSuggestiontoCategory("emergency",address);
              }
            }
            else{
                this.AddSuggestiontoCategory("OTHERS...",address)
            }
          });
        } catch (error) {
          console.error('Error fetching suggestions:', error);
          this.data = [];
        }
      },
      AddSuggestiontoCategory(category,address){
        if(this.data.some(obj => obj.type === category)){
          const giveBoxIndex = this.data.findIndex(obj => obj.type === category);
          this.data[giveBoxIndex].suggestions.push(address);
        }
        else{
          this.data.push({'type': category, 'suggestions': [address]})
        }
      }
    },
    watch: {   

        async address(newValue) {
          if(newValue.length >= 3){
            await this.getSuggestion();
          }
        },
        value(newValue){
          this.address = this.value
        }
    }
  };
  </script>
  