export default {
  data: () => ({
    // Place a ref attribute on any html tag to watch its properties
    windowResizeWatchedRefsProperties: {},
    windowHeight: window.innerHeight,
    windowWidth: window.innerWidth,
    windowSize: [window.innerHeight, window.innerWidth]
  }),
  mounted() {
    this.windowHeight = window.innerHeight;
    this.windowWidth = window.innerWidth;
    this.windowSize = [window.innerHeight, window.innerWidth];
    this.$nextTick(() => {
      window.addEventListener('resize', this.onWindowResize);
    });
    this.retrieveRefWatchedPropertiesValue();
    this.windowWidthChanged();
    this.windowHeightChanged();
    this.windowSizeChanged();
  },
  beforeDestroy() {
    // To prevent browser having 100s of listener
    // Remove the listener when the component is destroyed
    window.removeEventListener('resize', this.onWindowResize);
  },
  methods: {
    onWindowResize() {
      this.retrieveRefWatchedPropertiesValue();

      let windowSizeChanged = false;
      if (this.windowHeight !== window.innerHeight) {
        this.windowHeight = window.innerHeight;
        this.windowSize[0] = window.innerHeight;
        windowSizeChanged = true;
        this.windowHeightChanged();
      }
      if (this.windowWidth !== window.innerWidth) {
        this.windowWidth = window.innerWidth;
        this.windowSize[1] = window.innerWidth;
        windowSizeChanged = true;
        this.windowWidthChanged();
      }
      if (windowSizeChanged)
        this.windowSizeChanged();
    },
    retrieveRefWatchedPropertiesValue() {
      // Retrieve referenced elements' new properties' value
      for (let [key, properties] of Object.entries(this.windowResizeWatchedRefsProperties)) {
        if (key in this.$refs) {
          for (let property in properties) {
            if (property in this.$refs[key])
              this.windowResizeWatchedRefsProperties[key][property] = this.$refs[key][property];
          }
        }
      }
    },
    windowWidthChanged() {},
    windowHeightChanged() {},
    windowSizeChanged() {}
  }
}
