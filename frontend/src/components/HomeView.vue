<template>
  <div class="home">
    <h1 class="title">{{$t('welcome')}} {{$t('on')}} SHAREISH ({{$t('shareish_title')}})</h1>
    <h2 class="subtitle">{{$t('about-us')}}</h2>

<p>{{$t('shareish_description')}}.<br><br>
<a @click="goto('/sign-up')" class="text-reset">{{$t('after_registration')}}</a> {{$t('andet')}} <a @click="goto('/log-in')" class="text-reset">{{$t('logged_in')}}</a>, Shareish {{$t('offers')}} <a @click="goto('/map')" class="text-reset">{{$t('interactive_map')}}</a> {{$t('shareish_description2')}}.</p><br>

<!--<b-image :src="require('@/assets/shareish-screenshot.png')" :rounded="rounded"></b-image>//-->
<!--
<p>Existing Shareish instances:</p>
<ul><li><a href="https://shareish.org/">Shareish demonstration server</a></li>
</ul>
//-->

<br>
<h2 class="subtitle"><b>{{$t('faq')}}</b></h2>


<p><b>{{$t('faq_nothing')}} </b><br>
  <i>{{$t('faq_nothing_answer')}}. </i></p><br>

<p><b>{{$t('faq_examples')}} </b><br>
<i>{{$t('faq_examples_answer')}}. </i></p><br>

<!-- can you give me exemples of services: promener chiens, faire courses, aller à la pharmacie, déposer qqun quelque part, citer exemple covid etc.... //-->

<p><b>{{$t('faq_everything')}}</b><br>
<i>{{$t('faq_everything_answer')}} </i></p><br>

<p><b>{{$t('faq_colors')}}</b><br>
<i>{{$t('faq_colors_answer')}} </i></p><br>


<p><b>{{$t('faq_address')}}</b><br>
<i>{{$t('faq_address_answer')}} </i></p><br>

<p><b>{{$t('faq_device')}}</b><br>
<i>{{$t('faq_device_answer')}} </i></p><br>


<p><b>{{$t('faq_data_collection')}}</b><br>
  <i>{{$t('faq_data_collection_answer')}}.</i></p><br>

<p><b>{{$t('faq_public_resources')}}</b><br>
<i>{{$t('faq_public_resources_answer')}} <a href="https://wiki.openstreetmap.org/wiki/Editors">editor tools</a>, <a href="https://mapcomplete.osm.be/">MapComplete</a> (web), <a href="https://wiki.openstreetmap.org/wiki/StreetComplete">StreetComplete</a> (Android), <a href="https://wiki.openstreetmap.org/wiki/OSM_Contributor">OSMand Contributor</a> (Android), <a href="https://wiki.openstreetmap.org/wiki/Go_Map!!">Go Map!!!</a> (macOS). 
</i>
</p><br>

<p><b>{{$t('faq_how_to_contribute')}}</b><br>
<i>{{$t('faq_how_to_contribute_answer')}}</i></p><br>

<p><b>{{$t('faq_local_instance')}} </b><br>
<i>{{$t('faq_local_instance_answer')}}</i></p><br>


<p><b>{{$t('faq_who')}}</b><br>
<i>{{$t('faq_who_answer')}} </i></p><br>


<p><b>{{$t('faq_further')}}</b><br>
<i>{{$t('faq_further_answer')}} <a href="mailto:info@shareish.org">info@shareish.org</a>.</i>

</p>




</div>





</template>

<script>

export default {
  name: 'HomeView',
  components: {
  },
  mounted() {
    document.title = "Shareish"
  },
  methods:{
    goto(url) {
      this.$router.push(url)
    },
  }
}
</script>
