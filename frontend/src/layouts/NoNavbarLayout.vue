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
              <span class="mb-2">Developers: Adrien Guilliams, Ulysse Rubens, Florent Banneux, Pierre Chapeau, Raphaël Marée</span>
	            <span>Project coordination: <a href="https://people.montefiore.uliege.be/maree/">Raphaël Marée</a></span>
            </address>
          </div>
          <div class="column">
            <h6 class="title is-4 mb-4">
              {{ $t('useful-links') }}
            </h6>
            <div class="custom-flex-column">
              <a href="https://doi.org/10.1145/3593743.3593790">Scientific paper @ Communities & Technologies 2023</a>
              <a href="https://github.com/shareish" class="mt-3">
                Open source code on
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
