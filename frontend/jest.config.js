module.exports = {
  preset: '@vue/cli-plugin-unit-jest',
  transformIgnorePatterns: [
    '/node_modules/(?!leaflet)/' 
  ],
  setupFilesAfterEnv: ['./__tests__/components/setupVue.js'],
  testMatch: ['**/__tests__/unit/**/*.spec.js'],
}