export default {
  data: () => ({
    code: null,
    message: null
  }),
  methods: {
    snackbarError(error, replace = true) {
      if (this.isFromAxios(error)) {
        // Error received from Axios
        if (error.code === 'ERR_NETWORK') {
          this.message = this.$t('connection-error');
        } else {
          this.code = error.response.status;

          if (typeof error.response.data === 'string') {
            this.message = error.response.data;
          } else {
            const data = error.response.data;
            if (typeof data === 'object') {
              if (this.keyInDictIsString('message', data)) {
                this.message = data.message;
              } else if (this.keyInDictIsString('error', data)) {
                this.message = data.error;
              } else if (this.keyInDictIsString('detail', data)) {
                this.message = data.detail;
              } else {
                this.unableToParse(error);
              }
            } else {
              this.unableToParse(error);
            }
          }
        }
      } else if (typeof error === 'object') {
        if (this.keyInDictIsString('message', error)) {
          // Error is a casual Exception that have been caught
          this.message = error.message;
        } else {
          this.unableToParse(error);
        }
      } else if (typeof error === 'string') {
        // Error is sent from Vue file intendedly
        this.message = error;
      } else {
        this.unableToParse(error);
      }

      // Building error message
      let snackbarMessage = "";
      if (this.code != null)
        snackbarMessage += `Error ${this.code}: `;
      snackbarMessage += (this.message != null) ? this.message : "No message provided.";

      // Displaying the error
      this.$buefy.snackbar.open({
        duration: 5000,
        type: 'is-danger',
        message: snackbarMessage,
        pauseOnHover: true,
        queue: replace,
        position: 'is-bottom-right'
      });

      // Reset the component fields
      this.reset();
    },
    fullErrorHandling(error) {
      if (this.isSerializationError(error)) {
        // This is a serialization error
        for (const [key, value] of Object.entries(error.response.data.serializer_errors)) {
          if (typeof value === 'string') {
            this.snackbarError(`(${key}) ${value}`);
          } else if (Array.isArray(value)) {
            for (const message of value)
              this.snackbarError(`(${key}) ${message}`, false);
          }
        }
      } else {
        this.snackbarError(error);
      }
    },
    reset() {
      this.code = null;
      this.message = null;
    },
    unableToParse(error) {
      this.message = "Unable to parse error, please check console.";
      console.log(error);
    },
    isFromAxios(obj) {
      return (typeof obj === 'object' && obj.constructor.name === 'AxiosError');
    },
    isSerializationError(error) {
      return (this.isFromAxios(error) && typeof error.response.data === 'object' && 'serializer_errors' in error.response.data);
    },
    keyInDictIsString(elem, dict) {
      return elem in dict && typeof dict[elem] === 'string'
    }
  }
}
