<template>
    <b-autocomplete
      rounded
      v-model="address"
      group-field="type"
      group-options="suggestions"
      placeholder="e.g. jQuery"
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
  
  export default {
    name: "AutoComplete",
    props: { 
      value: String,
    },
    data() {
      return {
        address: this.value,
        data: []  
      };
    },
    methods: {
      async getSuggestion() {
        try {
          const response = await axios.get('https://photon.komoot.io/api/?q=' + this.address + "&limit=5" + "&lang=" + this.$i18n.locale);
          response.data.features.forEach(feature => {
            
            const { housenumber, street, name, country, county, city, postcode, osm_value } = feature.properties;
            
            let address = '';
            
            if (housenumber) address += (address ? `${housenumber}` : housenumber);
            if (street) address += (address ? `, ${street}` : street);
            if (country) address += (address ? `, ${country}` : country);
            if (name) address += (address ? `, ${name}` : name)
            if (city) address += (address ? `, ${city}` : city);
            if (postcode) address += (address ? `, ${postcode}` : postcode);
            if (county) address += (address ? `, ${county}` : county);
    
            switch (osm_value) {
                case 'give_box':
                  if(this.data.some(obj => obj.type === 'GIVE BOX')){
                    const giveBoxIndex = this.data.findIndex(obj => obj.type === "GIVE BOX");
                    this.data[giveBoxIndex].suggestions.push(address);
                  }
                  else{
                    this.data.push({'type': 'GIVE BOX', 'suggestions': [address]})
                  }
                  break;

                case 'public_bookcase':
                  if(this.data.some(obj => obj.type === 'PUBLIC BOOKCASE')){
                      const giveBoxIndex = this.data.findIndex(obj => obj.type === "PUBLIC BOOKCASE");
                      this.data[giveBoxIndex].suggestions.push(address);
                  }
                  else{
                    this.data.push({'type': 'PUBLIC BOOKCASE', 'suggestions': [address]})
                  }
                  break;
                
                default:
                  if(this.data.some(obj => obj.type === 'AUTRES...')){
                      const giveBoxIndex = this.data.findIndex(obj => obj.type === "AUTRES...");
                      this.data[giveBoxIndex].suggestions.push(address);
                    }
                    else{
                      this.data.push({'type': 'AUTRES...', 'suggestions': [address]})
                    }
            }

          });
        } catch (error) {
          console.error('Error fetching suggestions:', error);
          this.data = [];
        }
      }
    },
    watch: {    
        address(newValue) {
          this.data = [];
          if(newValue.length >= 3){
            
            this.getSuggestion();
          }
            
        },
        value(newValue){
          this.address = this.value
        }
    }
  };
  </script>
  