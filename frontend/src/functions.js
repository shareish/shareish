import {LatLng} from "leaflet/dist/leaflet-src.esm";
import moment from "moment";
import axios from "axios";
import ErrorHandler from "@/mixins/ErrorHandler";

export async function logout(instance) {
  try {
    await axios.post("/api/v1/token/logout/");
    axios.defaults.headers.common["Authorization"] = "";
    localStorage.removeItem("token");
    instance.$store.commit('removeToken');
    instance.$store.commit('removeUserID');
    await instance.$router.push("/log-in");
  }
  catch (error) {
    ErrorHandler.methods.snackbarError(error);
  }
}

export const scrollParentToChild = function(parent, child, position = "top", offset = 0) {
  if (typeof parent === 'object' && typeof child === 'object' && parent !== null && child !== null) {
    // Functions from Mina on StackOverflow
    // Author: https://stackoverflow.com/users/11887902/mina
    // Answer: https://stackoverflow.com/a/73056973/6535806

    // Where is the parent on page
    const parentRect = parent.getBoundingClientRect();
    // What can you see?
    const parentViewableArea = {
      height: parent.clientHeight,
      width: parent.clientWidth
    };

    // Where is the child
    const childRect = child.getBoundingClientRect();
    // Is the child viewable?
    const isViewable = (childRect.top >= parentRect.top) && (childRect.bottom <= parentRect.top + parentViewableArea.height);

    // if you can't see the child try to scroll parent
    if (!isViewable) {
      // Should we scroll using top or bottom? Find the smaller ABS adjustment
      const scrollTop = childRect.top - parentRect.top;
      const scrollBot = childRect.bottom - parentRect.bottom;
      if (position === "top") {
        // we're near the top of the list
        parent.scrollTop += scrollTop + offset;
      } else {
        // we're near the bottom of the list
        parent.scrollTop += scrollBot + offset;
      }
    }
  }
}

export const rem = function (number) {
  return number * 16;
}

export const isDict = function (dict) {
  return typeof dict === 'object' && dict.constructor === Object;
}

export const isArr = function (arr) {
  return Array.isArray(arr);
}

export const isDictEmpty = function (dict) {
  return isDict(dict) && Object.keys(dict).length === 0;
}

export const isEmptyArray = function (arr) {
  return isArr(arr) && arr.length === 0;
}

export const isNotEmptyArray = function (arr) {
  return isArr(arr) && arr.length !== 0;
}

export const isInt = function(n) {
    return Number(n) === n && n % 1 === 0;
}

export const isFloat = function(n) {
    return Number(n) === n && n % 1 !== 0;
}

export const isNumber = function(n) {
    return isInt(n) || isFloat(n);
}

export const isString = function (s) {
  return typeof s === 'string' || s instanceof String;
}

export const isEmptyString = function (s) {
  return isString(s) && s.length === 0;
}

export const isNotEmptyString = function (s) {
  return isString(s) && s.length !== 0;
}

export const ucfirst = function (s) {
  return s[0].toUpperCase() + s.slice(1);
}

export const lcfirst = function (s) {
  return s[0].toUpperCase() + s.slice(1);
}

export const ucall = function (s) {
  return s.toUpperCase();
}

export const lcall = function (s) {
  return s.toLowerCase();
}

export class GeolocationCoords {
  constructor(param1, param2 = null) {
    this.longitude = 0;
    this.latitude = 0;
    this.leafletLatLng = new LatLng(0, 0);

    this.update(param1, param2);
  }

  update(param1, param2) {
    if (isArr(param1)) {
      if (isNumber(param1[0]) && isNumber(param1[1])) {
        this.longitude = param1[0];
        this.latitude = param1[1];
      }
    } else if (param1 instanceof GeolocationPosition) {
      this.longitude = param1.coords.longitude;
      this.latitude = param1.coords.latitude;
    } else if (typeof param1 === 'string') {
      const regex = /^SRID=4326;POINT \(-?[0-9]+(\.[0-9]+)? -?[0-9]+(\.[0-9]+)?\)$/
      if (regex.test(param1)) {
	let coords = param1.substring(17, param1.length - 1).split(" ");
        this.longitude = parseFloat(coords[0]);
        this.latitude = parseFloat(coords[1]);
      }
    } else {
      if (isNumber(param1) && isNumber(param2)) {
        this.longitude = param1;
        this.latitude = param2;
      }
    }

    this.leafletLatLng.lat = this.latitude;
    this.leafletLatLng.lng = this.longitude;
  }

  toString() {
    return "SRID=4326;POINT (" + this.longitude + " " + this.latitude + ")";
  }

  toRadians(deg) {
    return deg * (Math.PI / 180)
  }

  distanceFrom(geolocation) {
    let R = 6378.1370; // Radius of the earth in km
    let dLat = this.toRadians(geolocation.latitude - this.latitude);
    let dLon = this.toRadians(geolocation.longitude - this.longitude);
    let a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(this.toRadians(this.latitude)) * Math.cos(this.toRadians(geolocation.latitude)) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2);
    let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // Distance in kilometers
  }

  distanceTo(geolocation) {
    return this.distanceFrom(geolocation);
  }
}

export const formattedDateFromNow = function(date, locale) {
  return moment(date).locale(locale).fromNow();
}

export const formattedDate = function(date, locale, format = "LLLL") {
  return moment(date).locale(locale).format(format);
}

