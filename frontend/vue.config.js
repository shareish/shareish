module.exports = {
 
  pwa: {
    
    name: 'shareish',
    themeColor: '#4DBA87',
    msTileColor: '#000000',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: 'black',

    manifestOptions: {
      name: 'Shareish',
      short_name: 'Shareish',
      start_url: '/',
      display: 'standalone',
      theme_color: '#4DBA87',
      description : 'Shareish est un application solidaire !'
    },
    
    workboxPluginMode: 'InjectManifest',
    workboxOptions: {
      // swSrc is required in InjectManifest mode.
      swSrc: 'dev/sw.js',
      // ...other Workbox options...
    }
  }
};
