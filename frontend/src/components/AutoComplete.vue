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
      @select="handleSelect"
      expanded
      >
      <template #empty>{{ $t('no_result') }}</template>
      <template #default="{ option }">
        <span> 
          <b>{{ option.name }}</b><br/>
          <span v-if="option.osm_value && option.osm_value !== 'unclassified'"> {{ option.osm_value }},</span>
          <span v-if="option.housenumber"> {{ option.housenumber }}, </span>
          <span v-if="option.city"> {{ option.city }},</span>
          <span v-if="option.country"> {{ option.country }}</span>
          
        </span>
      </template>
    </b-autocomplete>
</template>

  
  <script>
  import axios from 'axios';
  import { debounce } from 'lodash'; 


  
  export default {
    name: "AutoComplete",
    props: { 
      value: String,
      location: Object
    },
    data() {
      return {
        address: "",
        data: []  ,
        geolocation : null,
        response: null,
      };
    },
    created(){
      if(this.location) this.geolocation = this.location;
      if(this.value) this.address = this.value;
      
    },
    methods: {
      handleSelect(option){
        this.selected = true;
        let addressSelected = "";
        const {housenumber, name, city, country} = option;
        addressSelected = name + ", " + city + ", " + country;
        this.address = addressSelected;
        console.log(this.address);
      },
      getSuggestion: debounce(async function() {

        this.data = [];
        console.log("Get suggestion")
        try {

          if(this.geolocation){
            console.log(this.geolocation.longitude + "; " + this.geolocation.latitude)
            this.response = await axios.get('https://photon.komoot.io/api/?q=' + this.address + "&limit=10" + "&lang=" + this.$i18n.locale+ "&lon=" + this.geolocation.longitude + "&lat=" + this.geolocation.latitude);
          }
          else{
            console.log("No geolocation")
            this.response = await axios.get('https://photon.komoot.io/api/?q=' + this.address + "&limit=10" + "&lang=" + this.$i18n.locale);
          }  

          this.MapFeaturesToSuggestions(this.response);
            
        } catch (error) {
          console.error('Error fetching suggestions:', error);
          this.data = [];
        }
      },300),
      AddSuggestiontoCategory(category, address) {
        const categoryIndex = this.data.findIndex(obj => obj.type === category);

        if (categoryIndex !== -1) {
          this.data[categoryIndex].suggestions.push(address);
        } else {
          this.data.push({ type: category, suggestions: [address] });
        }
      },
      MapFeaturesToSuggestions(response){

        response.data.features.forEach(feature => {
            
          const { housenumber, name, country, city,osm_key,osm_value } = feature.properties;
          
          let suggestion = {
            housenumber: housenumber || null,
            name: name || null,
            city: city || null,
            country: country || null,
            osm_value: osm_value || null
          };
                    
          
          switch (osm_key) {
            case "amenity":
              switch (osm_value) {
                case "give_box":
                  this.AddSuggestiontoCategory(this.$t("givebox"), suggestion);
                  break;
                case "public_bookcase":
                  this.AddSuggestiontoCategory("PUBLIC BOOKCASE", suggestion);
                  break;
                case "food_sharing":
                  this.AddSuggestiontoCategory("FOOD SHARING", suggestion);
                  break;
                case "freeshop":
                  this.AddSuggestiontoCategory("FREE SHOP", suggestion);
                  break;
                case "drinking_water":
                  this.AddSuggestiontoCategory("DRINKING WATER", suggestion);
                  break;
                case "social_facility":
                  this.AddSuggestiontoCategory("SOCIAL FACILITY", suggestion);
                  break;
                case "emergency":
                  this.AddSuggestiontoCategory("emergency", suggestion);
                  break;
              }
              break;
            default:
              this.AddSuggestiontoCategory("OTHERS...", suggestion);
              break;
          }
        });
      }
    },
    watch: {   
        async address(newValue) {
          if(newValue && newValue.length >= 3){
            await this.getSuggestion();
          }
        },
        value(newValue){
          this.address = newValue;
        },
        location(newValue){
          this.geolocation = newValue;
        }
    }
  };
  </script>
  