<template>
  <div id="page-log-in" class="columns">
    <div class="column is-6 is-offset-3">
      <h1 class="title">{{ $t('log-in') }}</h1>
      <b-message v-if="!responseOK" :title="$t('error_keys__BAD_LOGIN')" type="is-danger">
        {{ $t('error_keys__ACCOUNT_DOESNT_EXIST') }}
      </b-message>
        <b-field :label="$t('email-or-username')" :message="errors.first('authValue')" :type="{'is-danger': errors.has('authValue')}">
          <b-input v-model="authValue" name="authValue" icon-pack="fas" icon="user" icon-right="close-circle" icon-right-clickable
                @icon-right-click="clearAuthIconClick" 
                v-validate="'required'"
                />
        </b-field>
      <b-message v-if="showDisabledAccountLink" title="Account disabled" type="is-primary">
        {{ $t('help_login-disabled-account') }} <router-link :to="{name: 'recoverAccount'}">{{ $t('click-here') }}</router-link>.
      </b-message>
      <b-message v-if="showScheduledDeletionAccountLink" title="Account scheduled for deletion" type="is-danger">
        <span v-html="$t('help_login-scheduled-deletion-account', {x: daysBeforeDeletion})" /> <router-link :to="{name: 'recoverAccount'}">{{ $t('click-here') }}</router-link>.
      </b-message> 
      <b-field :label="$t('password')" :message="errors.first('password')" :type="{'is-danger': errors.has('password')}">
        <b-input v-model="password" name="password" password-reveal type="password" icon-pack="fas" icon="lock" v-validate="'required'"/>
      </b-field>
      <router-link :to="{name: 'resetPassword'}">{{ $t('password-forgotten-?') }}</router-link>
      <b-button class="mt-4 ml-0" type="is-primary" :loading="waitingFormResponse" @click="submitForm" expanded>{{ $t('log-in') }}</b-button>
      <hr class="mt-5"> 
      <span> {{ $t('thirdpartyconnection') }}</span>
      <div class="mt-4">
        <b-tooltip :label="$t('google_connect')">
          <router-link to="#">
            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 128 128">
                <path fill="#fff" d="M44.59 4.21a63.28 63.28 0 0 0 4.33 120.9a67.6 67.6 0 0 0 32.36.35a57.13 57.13 0 0 0 25.9-13.46a57.44 57.44 0 0 0 16-26.26a74.33 74.33 0 0 0 1.61-33.58H65.27v24.69h34.47a29.72 29.72 0 0 1-12.66 19.52a36.16 36.16 0 0 1-13.93 5.5a41.29 41.29 0 0 1-15.1 0A37.16 37.16 0 0 1 44 95.74a39.3 39.3 0 0 1-14.5-19.42a38.31 38.31 0 0 1 0-24.63a39.25 39.25 0 0 1 9.18-14.91A37.17 37.17 0 0 1 76.13 27a34.28 34.28 0 0 1 13.64 8q5.83-5.8 11.64-11.63c2-2.09 4.18-4.08 6.15-6.22A61.22 61.22 0 0 0 87.2 4.59a64 64 0 0 0-42.61-.38z"/>
                <path fill="#e33629" d="M44.59 4.21a64 64 0 0 1 42.61.37a61.22 61.22 0 0 1 20.35 12.62c-2 2.14-4.11 4.14-6.15 6.22Q95.58 29.23 89.77 35a34.28 34.28 0 0 0-13.64-8a37.17 37.17 0 0 0-37.46 9.74a39.25 39.25 0 0 0-9.18 14.91L8.76 35.6A63.53 63.53 0 0 1 44.59 4.21z"/>
                <path fill="#f8bd00" d="M3.26 51.5a62.93 62.93 0 0 1 5.5-15.9l20.73 16.09a38.31 38.31 0 0 0 0 24.63q-10.36 8-20.73 16.08a63.33 63.33 0 0 1-5.5-40.9z"/>
                <path fill="#587dbd" d="M65.27 52.15h59.52a74.33 74.33 0 0 1-1.61 33.58a57.44 57.44 0 0 1-16 26.26c-6.69-5.22-13.41-10.4-20.1-15.62a29.72 29.72 0 0 0 12.66-19.54H65.27c-.01-8.22 0-16.45 0-24.68z"/>
                <path fill="#319f43" d="M8.75 92.4q10.37-8 20.73-16.08A39.3 39.3 0 0 0 44 95.74a37.16 37.16 0 0 0 14.08 6.08a41.29 41.29 0 0 0 15.1 0a36.16 36.16 0 0 0 13.93-5.5c6.69 5.22 13.41 10.4 20.1 15.62a57.13 57.13 0 0 1-25.9 13.47a67.6 67.6 0 0 1-32.36-.35a63 63 0 0 1-23-11.59A63.73 63.73 0 0 1 8.75 92.4z"/>
            </svg>
          </router-link>
        </b-tooltip>
        <b-tooltip :label="$t('facebook_connect')">
          <router-link to="#" class="ml-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 256 256">
                <path fill="#1877F2" d="M256 128C256 57.308 198.692 0 128 0C57.308 0 0 57.307 0 128c0 63.888 46.808 116.843 108 126.445V165H75.5v-37H108V99.8c0-32.08 19.11-49.8 48.347-49.8C170.352 50 185 52.5 185 52.5V84h-16.14C152.958 84 148 93.867 148 103.99V128h35.5l-5.675 37H148v89.445c61.192-9.602 108-62.556 108-126.445"/>
                <path fill="#FFF" d="m177.825 165l5.675-37H148v-24.01C148 93.866 152.959 84 168.86 84H185V52.5S170.352 50 156.347 50C127.11 50 108 67.72 108 99.8V128H75.5v37H108v89.445A128.959 128.959 0 0 0 128 256a128.9 128.9 0 0 0 20-1.555V165h29.825"/>
            </svg>
          </router-link>
        </b-tooltip>
        <b-tooltip :label="$t('instagram_connect')">
          <router-link to="#" class="ml-4">
              <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 256 256">
                <g fill="none">
                    <rect width="256" height="256" fill="url(#skillIconsInstagram0)" rx="60"/>
                    <rect width="256" height="256" fill="url(#skillIconsInstagram1)" rx="60"/>
                    <path fill="#fff" d="M128.009 28c-27.158 0-30.567.119-41.233.604c-10.646.488-17.913 2.173-24.271 4.646c-6.578 2.554-12.157 5.971-17.715 11.531c-5.563 5.559-8.98 11.138-11.542 17.713c-2.48 6.36-4.167 13.63-4.646 24.271c-.477 10.667-.602 14.077-.602 41.236s.12 30.557.604 41.223c.49 10.646 2.175 17.913 4.646 24.271c2.556 6.578 5.973 12.157 11.533 17.715c5.557 5.563 11.136 8.988 17.709 11.542c6.363 2.473 13.631 4.158 24.275 4.646c10.667.485 14.073.604 41.23.604c27.161 0 30.559-.119 41.225-.604c10.646-.488 17.921-2.173 24.284-4.646c6.575-2.554 12.146-5.979 17.702-11.542c5.563-5.558 8.979-11.137 11.542-17.712c2.458-6.361 4.146-13.63 4.646-24.272c.479-10.666.604-14.066.604-41.225s-.125-30.567-.604-41.234c-.5-10.646-2.188-17.912-4.646-24.27c-2.563-6.578-5.979-12.157-11.542-17.716c-5.562-5.562-11.125-8.979-17.708-11.53c-6.375-2.474-13.646-4.16-24.292-4.647c-10.667-.485-14.063-.604-41.23-.604h.031Zm-8.971 18.021c2.663-.004 5.634 0 8.971 0c26.701 0 29.865.096 40.409.575c9.75.446 15.042 2.075 18.567 3.444c4.667 1.812 7.994 3.979 11.492 7.48c3.5 3.5 5.666 6.833 7.483 11.5c1.369 3.52 3 8.812 3.444 18.562c.479 10.542.583 13.708.583 40.396c0 26.688-.104 29.855-.583 40.396c-.446 9.75-2.075 15.042-3.444 18.563c-1.812 4.667-3.983 7.99-7.483 11.488c-3.5 3.5-6.823 5.666-11.492 7.479c-3.521 1.375-8.817 3-18.567 3.446c-10.542.479-13.708.583-40.409.583c-26.702 0-29.867-.104-40.408-.583c-9.75-.45-15.042-2.079-18.57-3.448c-4.666-1.813-8-3.979-11.5-7.479s-5.666-6.825-7.483-11.494c-1.369-3.521-3-8.813-3.444-18.563c-.479-10.542-.575-13.708-.575-40.413c0-26.704.096-29.854.575-40.396c.446-9.75 2.075-15.042 3.444-18.567c1.813-4.667 3.983-8 7.484-11.5c3.5-3.5 6.833-5.667 11.5-7.483c3.525-1.375 8.819-3 18.569-3.448c9.225-.417 12.8-.542 31.437-.563v.025Zm62.351 16.604c-6.625 0-12 5.37-12 11.996c0 6.625 5.375 12 12 12s12-5.375 12-12s-5.375-12-12-12v.004Zm-53.38 14.021c-28.36 0-51.354 22.994-51.354 51.355c0 28.361 22.994 51.344 51.354 51.344c28.361 0 51.347-22.983 51.347-51.344c0-28.36-22.988-51.355-51.349-51.355h.002Zm0 18.021c18.409 0 33.334 14.923 33.334 33.334c0 18.409-14.925 33.334-33.334 33.334c-18.41 0-33.333-14.925-33.333-33.334c0-18.411 14.923-33.334 33.333-33.334Z"/>
                    <defs>
                        <radialGradient id="skillIconsInstagram0" cx="0" cy="0" r="1" gradientTransform="matrix(0 -253.715 235.975 0 68 275.717)" gradientUnits="userSpaceOnUse">
                            <stop stop-color="#FD5"/>
                            <stop offset=".1" stop-color="#FD5"/>
                            <stop offset=".5" stop-color="#FF543E"/>
                            <stop offset="1" stop-color="#C837AB"/>
                        </radialGradient>
                        <radialGradient id="skillIconsInstagram1" cx="0" cy="0" r="1" gradientTransform="matrix(22.25952 111.2061 -458.39518 91.75449 -42.881 18.441)" gradientUnits="userSpaceOnUse">
                            <stop stop-color="#3771C8"/>
                            <stop offset=".128" stop-color="#3771C8"/>
                            <stop offset="1" stop-color="#60F" stop-opacity="0"/>
                        </radialGradient>
                    </defs>
                </g>
            </svg>
          </router-link>
        </b-tooltip>
        <b-tooltip :label="$t('mastodon_connect')">
          <router-link to="#" class="ml-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 256 274">
              <path fill="#3088D4" d="M249.874 164.085c-3.753 19.307-33.613 40.438-67.908 44.533c-17.883 2.134-35.49 4.095-54.266 3.234c-30.705-1.407-54.933-7.33-54.933-7.33c0 2.99.184 5.836.553 8.498c3.992 30.302 30.047 32.118 54.728 32.964c24.912.852 47.094-6.142 47.094-6.142l1.023 22.521s-17.425 9.357-48.465 11.078c-17.116.94-38.369-.43-63.122-6.983c-53.686-14.21-62.92-71.436-64.332-129.502c-.43-17.24-.165-33.497-.165-47.094c0-59.375 38.903-76.779 38.903-76.779C58.6 4.074 92.259.286 127.25 0h.86c34.991.286 68.673 4.074 88.287 13.083c0 0 38.901 17.404 38.901 76.78c0 0 .488 43.807-5.425 74.222"/>
              <path fill="#FFF" d="M209.413 94.469v71.894H180.93V96.582c0-14.71-6.19-22.176-18.57-22.176c-13.687 0-20.547 8.857-20.547 26.37v38.195h-28.315v-38.195c0-17.513-6.862-26.37-20.55-26.37c-12.379 0-18.568 7.466-18.568 22.176v69.78H45.897V94.47c0-14.694 3.741-26.37 11.256-35.009c7.75-8.638 17.898-13.066 30.496-13.066c14.575 0 25.613 5.602 32.911 16.808l7.095 11.893l7.096-11.893c7.296-11.206 18.334-16.808 32.911-16.808c12.597 0 22.745 4.428 30.496 13.066c7.513 8.639 11.255 20.315 11.255 35.009"/>
          </svg>
          </router-link>
        </b-tooltip>
        <b-tooltip :label="$t('osm_connect')">
          <router-link to="#" class="ml-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" viewBox="0 0 72 72">
                <path fill="none" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m21 13l-2 5l5 2l2 9l-5 5l2 3l-3 2v1l5 7l4-2m5.5 11l1.5-3l3-2l7 4l5-1v-4l-2-2l1.5-3.5"/>
                <g fill="#B1CC33">
                    <path fill-rule="evenodd" d="m25 13l-13-1v12l.997 11.04L12 47v12l13 1l11-1l12 1l12-1V47l-.997-11.96L60 24V12l-12 1l-12-1l-11 1Z" clip-rule="evenodd"/>
                    <path d="m12 12l.077-.997A1 1 0 0 0 11 12h1Zm13 1l-.077.997c.056.004.112.004.168-.001L25 13ZM12 24h-1a1 1 0 0 0 .004.09L12 24Zm.997 11.04l.996.083a.998.998 0 0 0 0-.173l-.996.09ZM12 47l-.996-.083A1 1 0 0 0 11 47h1Zm0 12h-1a1 1 0 0 0 .923.997L12 59Zm13 1l-.077.997c.056.004.112.004.168-.001L25 60Zm11-1l.083-.996a.995.995 0 0 0-.173 0L36 59Zm12 1l-.083.996a.92.92 0 0 0 .166 0L48 60Zm12-1l.083.996A1 1 0 0 0 61 59h-1Zm0-12h1a1 1 0 0 0-.004-.083L60 47Zm-.997-11.96l-.996-.09a.998.998 0 0 0 0 .173l.996-.083ZM60 24l.996.09A1 1 0 0 0 61 24h-1Zm0-12h1a1 1 0 0 0-1.083-.996L60 12Zm-12 1l-.083.996a.92.92 0 0 0 .166 0L48 13Zm-12-1l.083-.996a.995.995 0 0 0-.173 0L36 12Zm-24.077.997l13 1l.154-1.994l-13-1l-.154 1.994ZM13 24V12h-2v12h2Zm.993 10.95l-.997-11.04l-1.992.18l.997 11.04l1.992-.18Zm-.997 12.133l.997-11.96L12 34.957l-.996 11.96l1.992.166ZM13 59V47h-2v12h2Zm12.077.003l-13-1l-.154 1.994l13 1l.154-1.994Zm10.832-.999l-11 1l.181 1.992l11-1l-.18-1.992Zm12.174 1l-12-1l-.166 1.992l12 1l.166-1.992Zm11.834-1l-12 1l.166 1.992l12-1l-.166-1.992ZM59 47v12h2V47h-2Zm-.993-11.877l.997 11.96l1.992-.166L60 34.957l-1.993.166Zm.997-11.213l-.997 11.04l1.992.18l.997-11.04l-1.992-.18ZM59 12v12h2V12h-2Zm-10.917 1.996l12-1l-.166-1.992l-12 1l.166 1.992Zm-12.166-1l12 1l.166-1.992l-12-1l-.166 1.992Zm-10.827 1l11-1l-.18-1.992l-11 1l.18 1.992Z"/>
                </g>
                <path fill="none" stroke="#EA5A47" stroke-linejoin="round" stroke-width="2" d="m21 13l-2 5l5 2l2 9l-5 5l2 3l-3 2v1l5 7l4-2l4 6l-2 6l2 2l3-6l3-2l7 4l5-1v-4l-2-2l3-7l8-1"/>
                <path fill="#5C9E31" fill-rule="evenodd" d="M16 49a3 3 0 1 0-3-3v8a5.029 5.029 0 0 0-1 1v4h8.9a5 5 0 0 0-4.9-6a2 2 0 1 1 0-4Zm41.25 4.9a2.55 2.55 0 1 0 2.55 2.55v-6.8c.322-.241.608-.528.85-.85v-5.1a4.25 4.25 0 1 0-3.4 6.8a1.7 1.7 0 1 1 0 3.4Z" clip-rule="evenodd"/>
                <path fill="#92D3F5" fill-rule="evenodd" d="M48.867 39.867c-.61.088-1.233.133-1.867.133c-7.18 0-13-5.82-13-13c0-.634.045-1.258.133-1.867A11 11 0 0 0 28 35c0 6.075 4.925 11 11 11a11 11 0 0 0 9.867-6.133Z" clip-rule="evenodd"/>
                <path fill="#5C9E31" fill-rule="evenodd" d="M31.5 19a4.5 4.5 0 0 0 3.742-7h-7.484a4.5 4.5 0 0 0 3.742 7Z" clip-rule="evenodd"/>
                <path fill="#B1CC33" d="M56.707 33.425c3.317-5.199 1.791-12.102-3.407-15.419s-12.1-1.792-15.418 3.407c-3.318 5.198-1.792 12.101 3.406 15.418c5.199 3.317 12.102 1.792 15.419-3.406Z"/>
                <path fill="#92D3F5" fill-rule="evenodd" d="M50.973 14.618A7 7 0 0 1 44 21a4 4 0 0 0 0 8a7 7 0 0 1 5.968 10.66c-.953.222-1.947.34-2.968.34c-4.02 0-7.615-1.825-10-4.693V18.693A12.973 12.973 0 0 1 47 14c1.386 0 2.72.217 3.973.618Z" clip-rule="evenodd"/>
                <path fill="#5C9E31" d="M56.764 33.79c1.46-2.29 2.284-6.515 1.698-9.168c-.401-1.816-2.655-3.84-3.899-5.158c.649 2.354 1.039 7.35-2.185 11.972c-2.736 3.92-6.69 5.635-8.948 6.057c4.25 1.283 10.831.218 13.334-3.703Z"/>
                <path fill="#61B2E4" fill-rule="evenodd" d="M50.569 33.575a7.026 7.026 0 0 1 .253 4.001c-2.509.614-5.247.565-7.392-.083c1.795-.336 4.663-1.488 7.139-3.918Z" clip-rule="evenodd"/>
                <path fill="#D0CFCE" d="M55.101 15.185a14.432 14.432 0 0 0-10.937-1.937a14.424 14.424 0 0 0-9.104 6.365c-4.304 6.746-2.318 15.737 4.428 20.041c6.745 4.305 15.735 2.32 20.041-4.427a14.417 14.417 0 0 0 1.937-10.937a14.42 14.42 0 0 0-6.365-9.105Zm1.836 18.388c-2.178 3.415-5.881 5.281-9.66 5.281a11.36 11.36 0 0 1-6.135-1.792c-5.317-3.393-6.882-10.48-3.49-15.795a11.361 11.361 0 0 1 7.175-5.016a11.363 11.363 0 0 1 8.621 1.527a11.36 11.36 0 0 1 5.016 7.174a11.36 11.36 0 0 1-1.527 8.621Z"/>
                <path fill="#3F3F3F" d="m34.767 41.21l-6.918 10.334l-3.711 5.816c-.478.75.38 3.21 1.13 3.688c.36.23 2.532.011 2.532.011l11.524-17.192l-4.557-2.658Z"/>
                <path fill="none" stroke="#fff" stroke-linecap="round" stroke-width="2" d="M42.5 21H52m-12 3h13m-14 3h13"/>
                <g fill="none" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
                    <path stroke-miterlimit="10" d="M59.537 35.067c4.307-6.568 2.327-15.289-4.423-19.48c-6.75-4.19-15.712-2.263-20.02 4.304c-4.306 6.568-2.325 15.289 4.424 19.48c6.75 4.19 15.712 2.263 20.02-4.304Z"/>
                    <path stroke-miterlimit="10" d="M56.639 33.267c3.285-5.01 1.774-11.663-3.374-14.86c-5.15-3.196-11.986-1.726-15.272 3.284c-3.285 5.01-1.774 11.662 3.374 14.859c5.15 3.197 11.986 1.727 15.272-3.283Zm-21.862 8.177l4.364 2.709l-10.396 15.853c-.743 1.133-2.322 1.444-3.526.696c-1.205-.748-1.58-2.272-.838-3.405l10.396-15.853Z"/>
                    <path d="M40 12.333L36 12l-11 1l-13-1v12l.997 11.04L12 47v12l9 .692m33.266-47.214L60 12v4.5m-.625 23L60 47v12l-12 1l-12-1l-3.5.318"/>
                </g>
            </svg>
          </router-link>
      </b-tooltip>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ErrorHandler from "@/mixins/ErrorHandler";

export default {
  name: "TheLoginView",
  mixins: [ErrorHandler],
  $_veeValidate: {
    validator: 'new'
  },
  data() {
    return {
      authValue: '',
      password: '',
      waitingFormResponse: false,
      showDisabledAccountLink: false,
      showScheduledDeletionAccountLink: false,
      daysBeforeDeletion: 0,
      responseOK: true,
    }
  },
  created() {
    document.title = `Shareish | ${this.$t('log-in')}`;
  },
  methods: {
    clearAuthIconClick() {
        this.authValue = '';
    },
    async submitForm() {
      this.waitingFormResponse = true;

      let result = await this.$validator.validateAll();

      if(result){
        const formData = {
          authValue: this.authValue,
          password: this.password
        }

        try {
          const auth = (await axios.post("/api/v1/auth/login/", formData)).data;

          axios.defaults.headers.common["Authorization"] = "Token " + auth['token'];
          this.$store.commit('setToken', auth['token']);
          localStorage.setItem("token", auth['token']);
          this.$store.commit('setUserID', auth['id']);
          localStorage.setItem("user_id", auth['id']);
          
          await this.$router.push('/map');
        }
        catch (error) {
          if (this.isKeyedError(error)) {
            const key = this.getErrorKey(error);
            console.log(key);
            if (key === 'DISABLED_ACCOUNT') {
              this.showDisabledAccountLink = true;
            } else if (key === 'SCHEDULED_DELETION_ACCOUNT') {
              this.showScheduledDeletionAccountLink = true;
              this.daysBeforeDeletion = Number(error.response.data.days_left);
            }
          }
          this.responseOK = false;
        }

      }

      this.waitingFormResponse = false;      
    }
  }
}
</script>
