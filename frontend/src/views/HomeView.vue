<template>
  <div class="home">
    <h1 class="title">Welcome to SHAREISH</h1>
    <h2 class="subtitle">About us</h2>

<p>Shareish is an open-source web platform to foster generalized exchanges and citizen mutual aid. Shareish relies on an interactive map where specific itemps are shown (<a @click="goto('/dashboard')" class="text-reset">can be seen here</a>). The map is based on tiles provided by OpenStreetMap (<a href="https://www.openstreetmap.org/">official website here</a>).</p>

<p>The project was initiated at the XXX (anonymous for review). This is a team work by X, Y, Z, ... (anonymous for review) </p>

<p>This server is a demonstration server for testing purposes.</p>

<p>If you want to launch this initiative in your area, city, region, organization,  you are free to install a server following our deployment procedure (see XXX) without any cost, and also to modify the code to fit your needs. We can also create a free redirection from e.g. http://mycity.shareish.org/ to your website and list it here.. If you are looking for collaboration or specific developments, feel free to contact us.</p>

<p><br>Existing Shareish instances:</p>
<ul><li><a href="https://shareish.org/">Shareish demonstration server</a></li></ul>
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
