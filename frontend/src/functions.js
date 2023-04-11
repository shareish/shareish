export const scrollParentToChild = function(parent, child) {
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
      if (Math.abs(scrollTop) < Math.abs(scrollBot)) {
        // we're near the top of the list
        parent.scrollTop += scrollTop;
      } else {
        // we're near the bottom of the list
        parent.scrollTop += scrollBot;
      }
    }
  }
}

export const rem = function (number) {
  return number * 16;
}

export const isDict = function (dict) {
  return Object.keys(dict).length === 0;
}

export const isArr = function (arr) {
  return Array.isArray(arr);
}

export const isDictEmpty = function (dict) {
  return isDict(dict) && Object.keys(dict).length === 0;
}

export const isArrEmpty = function (arr) {
  return isArr(arr) && arr.length === 0;
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

export class Geolocation {
  constructor(param1, param2 = null) {
    if (typeof param1 === 'object') {
      this.latitude = param1.coords.latitude;
      this.longitude = param1.coords.longitude;
    } else {
      this.latitude = param1;
      this.longitude = param2;
    }
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