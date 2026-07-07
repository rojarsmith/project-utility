# Tampermonkey

Unrestricted webpages

`hook.js`

```javascript
// Self-executing
(function() {
  'use strict'
  Object.defineProperty(document, 'cookie', {
    get: function() {
      //debugger;
      return "";
    },
    set: function(value) {
      debugger;
      return value;
    },
  });
})();
```

```javascript
(function () {
    'use strict';
    var cookieTemp = '';
    Object.defineProperty(document, 'cookie', {
        set: function (val) {
            if (val.indexOf('v') != -1) {
                debugger;
            }
            console.log('/Hook captures cookie settings->', val);
            cookieTemp = val;
            return val;
        },
        get: function () {
            return cookieTemp;
        },
    });
})();
```

```javascript
AAA = Function.prototype.constructor;
Function.prototype.constructor = function(a) {
  if (a == "debugger") {
    return function(){};
  }
  return AAA(a);
};
```

Modify the environment and modify the DOM BOM.

```javascript
const { JSDOM } = require('jsdom');
const dom = new JSDOM('<!DOCTYPE html><p></p>', {url: 'https://'});
window = dom.window;
document = window.document;
location = {}
```

