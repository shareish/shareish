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
      <template #default="{ option }">
        <span v-html="option"></span>
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
        address: this.value,
        data: []  ,
        geolocation : null,
        response: null
      };
    },
    created(){
      this.geolocation = this.location;
    },
    methods: {
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
          
          let nameAdress = '';
          let address = '';

          if (name) nameAdress += '<b>' + name +'<br>' +'</b>';
          if (housenumber) address += (address ? `,${housenumber}` : housenumber);

          if(city) address += (address ? `, ${city}` : city);
          if(country) address += (address ? `, ${country}` : country);
          if(osm_value) address += (address ? `,${osm_value}` : osm_value);
                    
          address = nameAdress + address;
          
          switch (osm_key) {
            case "amenity":
              switch (osm_value) {
                case "give_box":
                  this.AddSuggestiontoCategory(this.$t("givebox"), address);
                  break;
                case "public_bookcase":
                  this.AddSuggestiontoCategory("PUBLIC BOOKCASE", address);
                  break;
                case "food_sharing":
                  this.AddSuggestiontoCategory("FOOD SHARING", address);
                  break;
                case "freeshop":
                  this.AddSuggestiontoCategory("FREE SHOP", address);
                  break;
                case "drinking_water":
                  this.AddSuggestiontoCategory("DRINKING WATER", address);
                  break;
                case "social_facility":
                  this.AddSuggestiontoCategory("SOCIAL FACILITY", address);
                  break;
                case "emergency":
                  this.AddSuggestiontoCategory("emergency", address);
                  break;
              }
              break;
            default:
              this.AddSuggestiontoCategory("OTHERS...", address);
              break;
          }
        });
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
        },
        location(newValue){
          this.geolocation = newValue;
        }
    }
  };
  </script>
  