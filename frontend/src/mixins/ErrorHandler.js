import axios from "axios";

export default {
  data: () => ({
    code_t48xGa: null,
    message_v0sDM7: null
  }),
  methods: {
    snackbarError(error, options = {}) {
      const replace = 'replace' in options ? options['replace'] : true;
      let showErrorCode = 'showErrorCode' in options ? options['showErrorCode'] : true;

      if (this.isFromAxios(error)) {
        // Error received from Axios
        if (error.code === 'ERR_NETWORK') {
          this.message_v0sDM7 = this.$t('connection-error');
        } else {
          this.code_t48xGa = error.response.status;

          if (typeof error.response.data === 'string') {
            this.message_v0sDM7 = error.response.data;
          } else {
            const data = error.response.data;
            if (typeof data === 'object') {
              if (this._keyInDictIsString('message', data)) {
                this.message_v0sDM7 = data.message;
              } else if (this._keyInDictIsString('error', data)) {
                this.message_v0sDM7 = data.error;
              } else if (this._keyInDictIsString('key', data)) {
                this.message_v0sDM7 = this.$t('error_keys__' + data.key);
              } else if (this._keyInDictIsString('detail', data)) {
                if (data.detail === 'Invalid token.') {
                    axios.defaults.headers.common["Authorization"] = "";
                    localStorage.removeItem("token");
                    this.$store.commit('removeToken');
                    this.$store.commit('removeUserID');
                    showErrorCode=false;
                    this.message_v0sDM7 = this.$t('notif-error-invalid-token-disconnected');
                    this.$router.push("/log-in");
                } else {
		              this.message_v0sDM7 = data.detail;
		            }
              } else {
                this._unableToParse(error);
              }
            } else {
              this._unableToParse(error);
            }
          }
        }
      } else if (typeof error === 'object') {
        if (this._keyInDictIsString('message', error)) {
          // Error is a casual Exception that have been caught
          this.message_v0sDM7 = error.message;
        } else if (this._keyInDictIsString('key', error)) {
          this.message_v0sDM7 = this.$t('error_keys__' + error.key);
        } else {
          this._unableToParse(error);
        }
      } else if (typeof error === 'string') {
        // Error is sent from Vue file intentionally
        this.message_v0sDM7 = error;
      } else {
        this._unableToParse(error);
      }

      // Building error message
      let snackbarMessage = "";
      if (this.code_t48xGa != null && showErrorCode)
        snackbarMessage += `Error ${this.code_t48xGa}: `;
      snackbarMessage += (this.message_v0sDM7 !== "") ? this.message_v0sDM7 : "No message provided.";

      // Displaying the error
      this.$buefy.snackbar.open({
        duration: options['timeout'] ? options['timeout'] :  4000,
        type: 'is-danger',
        message: snackbarMessage,
        pauseOnHover: true,
        queue: replace,
        position: 'is-bottom-right',
	actionText: null  
      });

      // Reset the component fields
      this._reset();
    },
    fullErrorHandling(error) {
      if (this.isSerializationError(error)) {
        // This is a serialization error
        for (const [key, value] of Object.entries(error.response.data.serializer_errors)) {
          if (typeof value === 'string') {
            this.snackbarError(`(${key}) ${value}`);
          } else if (Array.isArray(value)) {
            for (const message of value)
              this.snackbarError(`(${key}) ${message}`, {'replace': false});
          }
        }
      } else {
        this.snackbarError(error);
      }
    },
    snackbarErrorFromKey(key) {
      this.snackbarError(this.$t('error_keys__' + key));
    },
    isKeyedError(error) {
      return this.isFromAxios(error) && error.code !== 'ERR_NETWORK' && typeof error.response.data !== 'string' && this._keyInDictIsString('key', error.response.data);
    },
    getErrorKey(error) {
      if (this.isKeyedError(error))
        return error.response.data.key;
      return null;
    },
    _reset() {
      this.code_t48xGa = null;
      this.message_v0sDM7 = null;
    },
    _unableToParse(error) {
      this.message_v0sDM7 = "Unable to parse error, please check console.";
      console.log(error);
    },
    isFromAxios(obj) {
      return (typeof obj === 'object' && (obj.constructor.name === 'AxiosError' || obj.name === 'AxiosError'));
    },
    isSerializationError(error) {
      return (this.isFromAxios(error) && typeof error.response.data === 'object' && 'serializer_errors' in error.response.data);
    },
    _keyInDictIsString(elem, dict) {
      return elem in dict && typeof dict[elem] === 'string'
    }
  }
}
