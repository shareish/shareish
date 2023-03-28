import moment from "moment";

export const scrollParentToChild = function(parent, child, offset = 0) {
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

export const formattedDateFromNow = function(date, locale) {
  return moment(date).locale(locale).fromNow();
}

export const formattedDate = function(date, locale, format = "LLLL") {
  return moment(date).locale(locale).format(format);
}
