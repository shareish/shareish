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

<!--
<p><b>What is the rationale and purpose of this site and what is generalized exchange ?</b><br>
<i></i>

<p><b>Isn't it dangerous to trust unknown people ?</b><br>
<i></i>


<p><b>Do you plan to replace the whole economy with mutual aid or are you willing to kill other non-profit non-technological initiatives (such as "SEL")</b><br>
<i></i>
//-->

<p><b></b><br>
<i></i>

<p><b>Who created this website ?</b><br>
<i>The project was initiated at the XXX (anonymous for review). This is a team work by X, Y, Z, ... (anonymous for review).</i></p><br>

<p><b>Is is possible to launch my own Shareish server instance ?</b><br>
<i>Yes, Shareish is fully open-source and can be reused for any purposes in a decentralized way. If you want to launch this initiative in your area, city, region, organization,  you are free to install a server following our deployment procedure without any cost, and also to modify the code to fit your needs. We can also create a free redirection from e.g. http://mycity.shareish.org/ to your website and list it here. <br>If you are looking for collaboration or specific developments, feel free to contact us.</i></p><br>


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
    document.title = "Shareish | About Us"
  },
  methods:{
    goto(url) {
      this.$router.push(url)
    },
  }
}
</script>
