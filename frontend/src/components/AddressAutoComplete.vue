<template>
  <b-autocomplete
    rounded
    open-on-focus
    ref="autocomplete"
    v-model="address"
    group-field="type"
    group-options="suggestions"
    :placeholder="$t('address')"
    icon="fas fa-search"
    icon-right="fas fa-times-circle" 
    icon-right-clickable 
    @icon-right-click="clearAddress"
    clear-on-select
    @input="addressChange"
    @select="onOptionSelect"
    :data="this.data"
    expanded
    >
    <template #empty>{{ $t('no_result') }}</template>
    <template #default="{ option }">
      <span> 
        <b>{{ option.name || option.street}}</b><br/>
        <span v-if="option.osm_value && option.osm_value !== 'unclassified' && option.osm_value !== 'yes'"> {{ option.osm_value }},</span>
        <span v-if="option.housenumber"> {{ option.housenumber }}, </span>
        <span v-if="option.postcode"> {{ option.postcode }}</span>
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
    name: "AddressAutoComplete",
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
        addressSelected: false,
      };
    },
    created(){
      if(this.location) this.geolocation = this.location;
      if(this.value) this.address = this.value;
      
    },
    methods: {
      getSuggestion: debounce(async function() {
        this.data = [];
        try {

          if(this.geolocation){
            this.response = await axios.get('https://photon.komoot.io/api/?q=' + this.address + "&limit=10" + "&lang=" + this.$i18n.locale+ "&lon=" + this.geolocation.longitude + "&lat=" + this.geolocation.latitude);
          }
          else{
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
            
          const {housenumber,street,name,country, city,osm_key,osm_value,postcode} = feature.properties;
          
          let suggestion = {
            housenumber: housenumber || null,
            street: street || null,
            name: name || null,
            city: city || null,
            country: country || null,
            osm_value: osm_value || null,
            postcode: postcode || null,
            address: `${housenumber ? housenumber +', ' : ""}${name ? name +', ' : ""}${street ? street +', ' : ""}${postcode ? postcode : ""} ${city ? city +', ' : ""}${country ? country : ""}`,
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
      },
      async addressChange(){
        this.data = [];
        if(!this.addressSelected){
          if(this.address && this.address.length > 3) await this.getSuggestion();
        }
        else{
          this.addressSelected = false;
        }
      },
      onOptionSelect(option) {
        this.addressSelected = true;
        this.address = option.address;
        this.$nextTick(() => {
          this.$refs.autocomplete.$emit('input', option.address);
        });
        this.$emit('input', this.address);
      },
      clearAddress(){
        this.address = "";
        this.$emit('input', this.address);
      }
    },
    watch: {   
      location(newValue){
        this.geolocation = newValue;
      },
      value(newValue){
        this.address = newValue;
      }
    }
  };
  </script>
  