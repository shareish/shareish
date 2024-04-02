module.exports = {
  preset: '@vue/cli-plugin-unit-jest',
  transformIgnorePatterns: [
    '/node_modules/(?!leaflet)/' 
  ],
  setupFilesAfterEnv: ['./tests/unit/setupVue.js']
}