<template>
  <div class="home">
    <h1 class="title">Welcome to SHAREISH</h1>
    <h2 class="subtitle">About us</h2>

<p>Shareish is an open-source web platform to foster mutual aid and generalized exchange.<br>
Shareish offers an <a @click="goto('/dashboard')" class="text-reset">interactive map</a> where specific items (goods and services to give or to lend, requests for help) can be added/edited/viewed by registered users. Users can start conversations to get further details about an item/request or to arrange an appointment for the exchange. External public data (such as free drinking water sources) can also be displayed. Tiles and external data are provided by <a href="https://www.openstreetmap.org/">OpenStreetMap</a>.</p><br>

<p>This server is a demonstration server for testing purposes.<br>
<p>Existing Shareish instances:</p>
<ul><li><a href="https://shareish.org/">Shareish demonstration server</a></li>
</ul>

<br>
<h2><b>Frequently asked questions (FAQ)</b></h2>

<p><b></b><br>
<i></i>

<p><b>Who created this website ?</b><br>
<i>The project was initiated at the XXX (anonymous for review). This is a team work by X, Y, Z, ... (anonymous for review).</i></p><br>

<p><b>I have nothing to give/lend, can I still use Shareish ?</b><br>
<i>The short answer is: YES ! The long answer is: YES, by receiving a free item from others, you potentially release them from their feeling of indebtedness (as they were probably previously in the same situation than you are). Also consider that you might have items/skills in the future to give/lend, it is not an issue not to have right now, Shareish is promoting mutual aid, solidarity and indirect exchange over the long term. Anyway, please have a look at your belongings/skills, you might already have things/skills to share but you are not yet aware it might be useful for others. Feel free to reference them on the Shareish platform as others might be interested in the future. </i></p><br>

<p><b>Can I share/search everything ?</b><br>
<i>Yes, except items/services that are prohibited or regulated by law, false, misleading, harmful, or obscene. The Shareish developers (referred to hereafter as "The Shareish platform") are not liable for any Shareish web server content. The Shareish developers do not control, and are not responsible for content made available through any Shareish web server. Under no circumstances will the Shareish platform be liable in any way for any content or for any loss or damage of any kind incurred as a result of the use of any content made available via any Shareish web server. You acknowledge that not all content is pre-screened or approved by the Shareish platform, but that Shareish web server moderators/administrators shall have the right (but not the obligation) in its sole discretion to refuse, delete or move any content that is available via their Shareish web server, for violating the terms of use or for any other reason. </i></p><br>

<p><b>What information does Shareish collect about me ?</b><br>
<i>To become a member of a Shareish web server and access information, we collect (store in a database) personally identifiable information that you voluntarily provide through the Shareish website. We do require a basic level of data (an email address, a username, a password) so that you may then log in and receive notifications via email (when getting new messages). Optionnaly, you can also provide additional information (such as other social networks profile) and your geographic location so that the Shareish web server can display items in your geographic area. Shareish platform keep all functional data in a database as long as you have an active account. Shareish platform do not sell such information to third parties. Shareish web server does not utilize cookies. Shareish uses the HTTPS protocol so that all communications between your browser and the Shareish web server are encrypted. If you have any questions about the use of your personal information, please contact us (see below).
</i></p><br>

<p><b>I want to edit or add public resources (public bookcases, drinking water sources,...), how can I do it ?</b><br>
<i>On Shareish you can display specific resources created by users (called "items") and other public resources (such as drinking water sources). Specific items are stored in an internal Shareish database and editable on Shareish, but public resources are retrieved from the open-access OpenStreetMap database. To edit public resources, when you click on the map on it, we provide a link ("retrieved from OSM") to the corresponding OpenStreetMap node page where it is possible to edit it. An alternative is to use other existing <a href="https://wiki.openstreetmap.org/wiki/Editors">editor tools</a> working with the <a href="https://www.openstreetmap.org/">OpenStreetMap</a> database such as <a href="https://mapcomplete.osm.be/">MapComplete</a> (web page), <a href="https://wiki.openstreetmap.org/wiki/StreetComplete">StreetComplete</a> (Android App), <a href="https://wiki.openstreetmap.org/wiki/OSM_Contributor">OSMand Contributor</a> (Android App), <a href="https://wiki.openstreetmap.org/wiki/Go_Map!!">Go Map!!!</a> (iOS and macOS app). Those editors allow you to edit and add "POI" (point of interest) that are later available to the whole OpenStreetMap community. 
</i>
</p><br>

<p><b>How can I contribute to Shareish project ?</b><br>
<i>Give or lent for free your skills/belongings ! Also, you can send us constructive comments/issues, remarks, ... (see last question). If you are a computer scientist, you can contribute to the source code (solve current issues or implement new features). If you want to translate the website into your own language, we can let you know how to translate specific messages/sentences. In any case, talking about the project around you is already a nice way to contribute !</i></p><br>

<p><b>Is is possible to launch my own Shareish server instance in my city/community ?</b><br>
<i>Yes, Shareish is fully open-source and can be reused for any purposes in a decentralized way. If you want to launch this initiative in your area, city, region, community or organization,  you are free to install a Shareish web server following our deployment procedure, and also to modify the code to fit your specific needs. We can also create a free redirection from e.g. http://mycity.shareish.org/ to your website and list it here. Please note that the Shareish platform developers are not liable for any content on any decentralized Shareish web server.<br>If you are looking for collaboration or specific developments, feel free to contact us.</i></p><br>


<p><b>I have further comments, issues, remarks, questions, proposals, where should I send them ?</b><br>
<i>Nice comments are very welcome and we are open to new ideas. Bugs should be reported on <a href="https://github.com/anonymous">GitHub (through issues)</a>. You can <a href="mailto:info@shareish.org">send comments by e-mail</a>. </i>

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
