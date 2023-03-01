export default {
  data: () => ({
    code: null,
    message: null
  }),
  methods: {
    snackbarError(error) {
      if (this.isFromAxios()) {
        // Error received from Axios
        this.code = error.response.status;

        if (typeof error.response.data === 'string') {
          this.message = error.response.data;
        } else if (typeof data === "object") {
          if ("message" in error.response.data && typeof error.response.data.message === 'string') {
            this.message = error.response.data.message;
          } else if ("error" in error.response.data && typeof error.response.data.error === 'string') {
            this.message = error.response.data.error;
          } else {
            this.unableToParse();
          }
        } else {
          this.unableToParse();
        }
      } else if (typeof error === "object") {
        if ("message" in error && typeof error.message === 'string') {
          // Error is a casual Exception that have been caught
          this.message = error.message;
        } else {
          this.unableToParse();
        }
      } else if (typeof error === 'string') {
        // Error is sent from Vue file intendedly
        this.message = error;
      } else {
        this.unableToParse();
      }

      // Building error message
      let message = "Error";
      if (this.code != null)
        message += ` ${this.code}`;
      message += ": ";
      if (this.message != null)
        message += `${this.message}`;
      else
        message += "No message provided.";

      // Displaying the error
      this.$buefy.snackbar.open({
        duration: 5000,
        type: 'is-danger',
        message: message,
        pauseOnHover: true,
      });

      // Reset the component fields
      this.reset();
    },
    fullErrorHandling(error) {
      if (this.isSerializationError(error)) {
        // This is a serialization error
        for (const [key, value] of Object.entries(error.response.data.serializer_errors))
          this.snackbarError(`(${key}) ${value}`);
      } else {
        this.snackbarError(error);
      }
    },
    reset() {
      this.code = null;
      this.message = null;
    },
    unableToParse() {
      this.message = "Unable to parse error, please check console.";
      console.log(error);
    },
    isFromAxios(obj) {
      return (typeof obj === "object" && obj.constructor.name === "AxiosError");
    },
    isSerializationError(error) {
      return (this.isFromAxios(error) && typeof error.response.data === "object" && "serializer_errors" in error.response.data);
    }
  }
}
