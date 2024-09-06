<template>
  <div id="layout-no-navbar">
    <slot />
    <footer class="footer">
      <div class="container">
        <div class="columns">
          <div class="column">
            <h6 class="title is-4 mb-4">Shareish</h6>
            <a href="https://www.montefiore.uliege.be/">
              <img src="../assets/montefiore_institute.svg" alt="Montefiore Institute, ULiège">
            </a>
            <address class="custom-flex-column mt-2">
	        <span class="mb-2">{{ $t('developers') }}: Adrien Guilliams, Florent Banneux, Ulysse Rubens, Adrien Hoyoux, Ogulcan Sevinç, Pierre Chapeau, Olivier Gason, Christophe Lejeune, Raphaël Marée, <a href="https://github.com/shareish/shareish/blob/main/CONTRIBUTING.md">{{ $t('and_you') }}</a></span>
	            <span>{{ $t('project_coordination') }}: <a href="https://people.montefiore.uliege.be/maree/">Raphaël Marée</a></span>
            </address>
          </div>
          <div class="column">
            <h6 class="title is-4 mb-4">
              {{ $t('useful-links') }}
            </h6>
            <div class="custom-flex-column">
	      <a href="https://doi.org/10.14254/1795-6889.2024.20-2.4">{{ $t('scientific_paper') }} @ Human Technology 2024</a>
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
	      <a href="https://github.com/shareish/shareish/discussions/categories/ideas">{{ $t('suggest_idea') }}</a>
	      <a href="https://mapstodon.space/@shareish">{{ $t('follow_us') }} <img alt="Shareish on Mastodon" src="../assets/mastodon.png" width="32" style="vertical-align: middle; margin-top: -3px; margin-left: 5px;"></a>
	      <a href="https://matrix.to/#/#shareish:matrix.org">{{ $t('chat_with_us') }} <img alt="Shareish on Matrix" src="../assets/matrix-logo.png" width="50" style="vertical-align: middle; margin-top: -3px; margin-left: 5px;"></a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: "NoNavbarLayout"
}
</script>

<style scoped>
.custom-flex-column {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
</style>
