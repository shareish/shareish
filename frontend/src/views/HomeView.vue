<template>
  <div class="home">
    <h1 class="title">Welcome to SHAREISH</h1>
    <h2 class="subtitle">About us</h2>
    <p>
      Shareish is a Master Thesis project by Adrien Guilliams under the supervision of Raphaël Marée.
      Shareish is an open-source web platform created to foster local indirect exchanges and citizen mutual aid.
      Shareish is centered on a display of the different items on a map (<a @click="goto('/dashboard')" class="text-reset">can be seen here</a>) based on tiles provided by OpenStreetMap (<a href="https://www.openstreetmap.org/">official website here</a>).
      If you want to launch this initiative in your region, you can go on <a href="https://github.com/shareish">https://github.com/shareish</a> to see how to deploy this yourself.
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
