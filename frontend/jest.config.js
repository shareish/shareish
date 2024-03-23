module.exports = {
  preset: '@vue/cli-plugin-unit-jest',
  transformIgnorePatterns: ['/node_modules/(?!lib-to-transform|other-lib)'],
  setupFilesAfterEnv: ['./tests/unit/setupVue.js']
}