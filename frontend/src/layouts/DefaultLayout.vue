<template>
  <div id="wrapper" class="wrapper">
    <the-navbar />
    <section class="section">
      <slot />
    </section>
    <footer class="footer">
      <div class="container">
        <div class="columns">
          <div class="column">
            <h6 class="title is-4 mb-4">Shareish</h6>
            <a href="https://www.montefiore.uliege.be/">
              <img src="../assets/montefiore_institute.svg" alt="Montefiore Institute, ULiège">
            </a>
            <address class="custom-flex-column mt-2">
              <span class="mb-2">{{ $t('developers') }}: Adrien Guilliams, Ulysse Rubens, Florent Banneux, Pierre Chapeau, Raphaël Marée</span>
	         <span>{{ $t('project_coordination') }}: <a href="https://people.montefiore.uliege.be/maree/">Raphaël Marée</a></span>
            </address>
          </div>
          <div class="column">
            <h6 class="title is-4 mb-4">
              {{ $t('useful-links') }}
            </h6>
            <div class="custom-flex-column">
              <a href="https://doi.org/10.1145/3593743.3593790">{{ $t('scientific_paper') }} @ Communities & Technologies 2023</a>
              <a href="https://github.com/shareish" class="mt-3">
		{{ $t('open_source_code') }}
                <img alt="https://github.com/shareish" src="../assets/GitHub-Mark-32px.png" style="vertical-align: middle; margin-top: -3px; margin-left: 5px;">
              </a>
	      
            </div>
          </div>
          <div class="column">
            <h6 class="title is-4 mb-4">
              {{ $t('contact') }}
            </h6>
            <div class="custom-flex-column">
              <a href="mailto:info@shareish.org">info@shareish.org</a>
	      <a href="https://github.com/shareish/shareish/issues">{{ $t('report_bug') }}</a>
	      <a href="https://mapstodon.space/@shareish">{{ $t('follow_us') }} <img alt="Shareish on Mastodon" src="../assets/mastodon.png" width="32" style="vertical-align: middle; margin-top: -3px; margin-left: 5px;"></a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import TheNavbar from "@/components/TheNavbar.vue";

export default {
  name: "DefaultLayout",
  components: {TheNavbar}
}
</script>

<style scoped>
.wrapper {
  display: flex;
  height: 100%;
  width: 100%;
  flex-direction: column;
  background: white;
  margin-right: auto;
  margin-left: auto;
}

.custom-flex-column {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
</style>
