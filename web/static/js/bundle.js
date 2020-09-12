!function(t){var e={};function n(r){if(e[r])return e[r].exports;var i=e[r]={i:r,l:!1,exports:{}};return t[r].call(i.exports,i,i.exports,n),i.l=!0,i.exports}n.m=t,n.c=e,n.d=function(t,e,r){n.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:r})},n.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.t=function(t,e){if(1&e&&(t=n(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var r=Object.create(null);if(n.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var i in t)n.d(r,i,function(e){return t[e]}.bind(null,i));return r},n.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return n.d(e,"a",e),e},n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},n.p="",n(n.s=16)}([function(t,e,n){t.exports=n(9)},function(t,e){function n(t,e,n,r,i,o,s){try{var a=t[o](s),u=a.value}catch(t){return void n(t)}a.done?e(u):Promise.resolve(u).then(r,i)}t.exports=function(t){return function(){var e=this,r=arguments;return new Promise((function(i,o){var s=t.apply(e,r);function a(t){n(s,i,o,a,u,"next",t)}function u(t){n(s,i,o,a,u,"throw",t)}a(void 0)}))}}},function(t,e){t.exports=function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}},function(t,e){function n(t,e){for(var n=0;n<e.length;n++){var r=e[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(t,r.key,r)}}t.exports=function(t,e,r){return e&&n(t.prototype,e),r&&n(t,r),t}},function(t,e){t.exports=function(t,e,n){return e in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}},function(t,e){t.exports=function(t,e){(null==e||e>t.length)&&(e=t.length);for(var n=0,r=new Array(e);n<e;n++)r[n]=t[n];return r}},function(t,e){},function(t,e,n){var r=n(10),i=n(11),o=n(12),s=n(13);t.exports=function(t){return r(t)||i(t)||o(t)||s()}},function(t,e,n){
/*!
 * 
 *   typed.js - A JavaScript Typing Animation Library
 *   Author: Matt Boldt <me@mattboldt.com>
 *   Version: v2.0.11
 *   Url: https://github.com/mattboldt/typed.js
 *   License(s): MIT
 * 
 */
var r;r=function(){return function(t){var e={};function n(r){if(e[r])return e[r].exports;var i=e[r]={exports:{},id:r,loaded:!1};return t[r].call(i.exports,i,i.exports,n),i.loaded=!0,i.exports}return n.m=t,n.c=e,n.p="",n(0)}([function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var r=function(){function t(t,e){for(var n=0;n<e.length;n++){var r=e[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(t,r.key,r)}}return function(e,n,r){return n&&t(e.prototype,n),r&&t(e,r),e}}(),i=n(1),o=n(3),s=function(){function t(e,n){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),i.initializer.load(this,n,e),this.begin()}return r(t,[{key:"toggle",value:function(){this.pause.status?this.start():this.stop()}},{key:"stop",value:function(){this.typingComplete||this.pause.status||(this.toggleBlinking(!0),this.pause.status=!0,this.options.onStop(this.arrayPos,this))}},{key:"start",value:function(){this.typingComplete||this.pause.status&&(this.pause.status=!1,this.pause.typewrite?this.typewrite(this.pause.curString,this.pause.curStrPos):this.backspace(this.pause.curString,this.pause.curStrPos),this.options.onStart(this.arrayPos,this))}},{key:"destroy",value:function(){this.reset(!1),this.options.onDestroy(this)}},{key:"reset",value:function(){var t=arguments.length<=0||void 0===arguments[0]||arguments[0];clearInterval(this.timeout),this.replaceText(""),this.cursor&&this.cursor.parentNode&&(this.cursor.parentNode.removeChild(this.cursor),this.cursor=null),this.strPos=0,this.arrayPos=0,this.curLoop=0,t&&(this.insertCursor(),this.options.onReset(this),this.begin())}},{key:"begin",value:function(){var t=this;this.options.onBegin(this),this.typingComplete=!1,this.shuffleStringsIfNeeded(this),this.insertCursor(),this.bindInputFocusEvents&&this.bindFocusEvents(),this.timeout=setTimeout((function(){t.currentElContent&&0!==t.currentElContent.length?t.backspace(t.currentElContent,t.currentElContent.length):t.typewrite(t.strings[t.sequence[t.arrayPos]],t.strPos)}),this.startDelay)}},{key:"typewrite",value:function(t,e){var n=this;this.fadeOut&&this.el.classList.contains(this.fadeOutClass)&&(this.el.classList.remove(this.fadeOutClass),this.cursor&&this.cursor.classList.remove(this.fadeOutClass));var r=this.humanizer(this.typeSpeed),i=1;!0!==this.pause.status?this.timeout=setTimeout((function(){e=o.htmlParser.typeHtmlChars(t,e,n);var r=0,s=t.substr(e);if("^"===s.charAt(0)&&/^\^\d+/.test(s)){var a=1;a+=(s=/\d+/.exec(s)[0]).length,r=parseInt(s),n.temporaryPause=!0,n.options.onTypingPaused(n.arrayPos,n),t=t.substring(0,e)+t.substring(e+a),n.toggleBlinking(!0)}if("`"===s.charAt(0)){for(;"`"!==t.substr(e+i).charAt(0)&&(i++,!(e+i>t.length)););var u=t.substring(0,e),c=t.substring(u.length+1,e+i),l=t.substring(e+i+1);t=u+c+l,i--}n.timeout=setTimeout((function(){n.toggleBlinking(!1),e>=t.length?n.doneTyping(t,e):n.keepTyping(t,e,i),n.temporaryPause&&(n.temporaryPause=!1,n.options.onTypingResumed(n.arrayPos,n))}),r)}),r):this.setPauseStatus(t,e,!0)}},{key:"keepTyping",value:function(t,e,n){0===e&&(this.toggleBlinking(!1),this.options.preStringTyped(this.arrayPos,this)),e+=n;var r=t.substr(0,e);this.replaceText(r),this.typewrite(t,e)}},{key:"doneTyping",value:function(t,e){var n=this;this.options.onStringTyped(this.arrayPos,this),this.toggleBlinking(!0),this.arrayPos===this.strings.length-1&&(this.complete(),!1===this.loop||this.curLoop===this.loopCount)||(this.timeout=setTimeout((function(){n.backspace(t,e)}),this.backDelay))}},{key:"backspace",value:function(t,e){var n=this;if(!0!==this.pause.status){if(this.fadeOut)return this.initFadeOut();this.toggleBlinking(!1);var r=this.humanizer(this.backSpeed);this.timeout=setTimeout((function(){e=o.htmlParser.backSpaceHtmlChars(t,e,n);var r=t.substr(0,e);if(n.replaceText(r),n.smartBackspace){var i=n.strings[n.arrayPos+1];i&&r===i.substr(0,e)?n.stopNum=e:n.stopNum=0}e>n.stopNum?(e--,n.backspace(t,e)):e<=n.stopNum&&(n.arrayPos++,n.arrayPos===n.strings.length?(n.arrayPos=0,n.options.onLastStringBackspaced(),n.shuffleStringsIfNeeded(),n.begin()):n.typewrite(n.strings[n.sequence[n.arrayPos]],e))}),r)}else this.setPauseStatus(t,e,!0)}},{key:"complete",value:function(){this.options.onComplete(this),this.loop?this.curLoop++:this.typingComplete=!0}},{key:"setPauseStatus",value:function(t,e,n){this.pause.typewrite=n,this.pause.curString=t,this.pause.curStrPos=e}},{key:"toggleBlinking",value:function(t){this.cursor&&(this.pause.status||this.cursorBlinking!==t&&(this.cursorBlinking=t,t?this.cursor.classList.add("typed-cursor--blink"):this.cursor.classList.remove("typed-cursor--blink")))}},{key:"humanizer",value:function(t){return Math.round(Math.random()*t/2)+t}},{key:"shuffleStringsIfNeeded",value:function(){this.shuffle&&(this.sequence=this.sequence.sort((function(){return Math.random()-.5})))}},{key:"initFadeOut",value:function(){var t=this;return this.el.className+=" "+this.fadeOutClass,this.cursor&&(this.cursor.className+=" "+this.fadeOutClass),setTimeout((function(){t.arrayPos++,t.replaceText(""),t.strings.length>t.arrayPos?t.typewrite(t.strings[t.sequence[t.arrayPos]],0):(t.typewrite(t.strings[0],0),t.arrayPos=0)}),this.fadeOutDelay)}},{key:"replaceText",value:function(t){this.attr?this.el.setAttribute(this.attr,t):this.isInput?this.el.value=t:"html"===this.contentType?this.el.innerHTML=t:this.el.textContent=t}},{key:"bindFocusEvents",value:function(){var t=this;this.isInput&&(this.el.addEventListener("focus",(function(e){t.stop()})),this.el.addEventListener("blur",(function(e){t.el.value&&0!==t.el.value.length||t.start()})))}},{key:"insertCursor",value:function(){this.showCursor&&(this.cursor||(this.cursor=document.createElement("span"),this.cursor.className="typed-cursor",this.cursor.innerHTML=this.cursorChar,this.el.parentNode&&this.el.parentNode.insertBefore(this.cursor,this.el.nextSibling)))}}]),t}();e.default=s,t.exports=e.default},function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var r,i=Object.assign||function(t){for(var e=1;e<arguments.length;e++){var n=arguments[e];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(t[r]=n[r])}return t},o=function(){function t(t,e){for(var n=0;n<e.length;n++){var r=e[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(t,r.key,r)}}return function(e,n,r){return n&&t(e.prototype,n),r&&t(e,r),e}}(),s=n(2),a=(r=s)&&r.__esModule?r:{default:r},u=function(){function t(){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t)}return o(t,[{key:"load",value:function(t,e,n){if(t.el="string"==typeof n?document.querySelector(n):n,t.options=i({},a.default,e),t.isInput="input"===t.el.tagName.toLowerCase(),t.attr=t.options.attr,t.bindInputFocusEvents=t.options.bindInputFocusEvents,t.showCursor=!t.isInput&&t.options.showCursor,t.cursorChar=t.options.cursorChar,t.cursorBlinking=!0,t.elContent=t.attr?t.el.getAttribute(t.attr):t.el.textContent,t.contentType=t.options.contentType,t.typeSpeed=t.options.typeSpeed,t.startDelay=t.options.startDelay,t.backSpeed=t.options.backSpeed,t.smartBackspace=t.options.smartBackspace,t.backDelay=t.options.backDelay,t.fadeOut=t.options.fadeOut,t.fadeOutClass=t.options.fadeOutClass,t.fadeOutDelay=t.options.fadeOutDelay,t.isPaused=!1,t.strings=t.options.strings.map((function(t){return t.trim()})),"string"==typeof t.options.stringsElement?t.stringsElement=document.querySelector(t.options.stringsElement):t.stringsElement=t.options.stringsElement,t.stringsElement){t.strings=[],t.stringsElement.style.display="none";var r=Array.prototype.slice.apply(t.stringsElement.children),o=r.length;if(o)for(var s=0;s<o;s+=1){var u=r[s];t.strings.push(u.innerHTML.trim())}}for(var s in t.strPos=0,t.arrayPos=0,t.stopNum=0,t.loop=t.options.loop,t.loopCount=t.options.loopCount,t.curLoop=0,t.shuffle=t.options.shuffle,t.sequence=[],t.pause={status:!1,typewrite:!0,curString:"",curStrPos:0},t.typingComplete=!1,t.strings)t.sequence[s]=s;t.currentElContent=this.getCurrentElContent(t),t.autoInsertCss=t.options.autoInsertCss,this.appendAnimationCss(t)}},{key:"getCurrentElContent",value:function(t){return t.attr?t.el.getAttribute(t.attr):t.isInput?t.el.value:"html"===t.contentType?t.el.innerHTML:t.el.textContent}},{key:"appendAnimationCss",value:function(t){if(t.autoInsertCss&&(t.showCursor||t.fadeOut)&&!document.querySelector("[data-typed-js-css]")){var e=document.createElement("style");e.type="text/css",e.setAttribute("data-typed-js-css",!0);var n="";t.showCursor&&(n+="\n        .typed-cursor{\n          opacity: 1;\n        }\n        .typed-cursor.typed-cursor--blink{\n          animation: typedjsBlink 0.7s infinite;\n          -webkit-animation: typedjsBlink 0.7s infinite;\n                  animation: typedjsBlink 0.7s infinite;\n        }\n        @keyframes typedjsBlink{\n          50% { opacity: 0.0; }\n        }\n        @-webkit-keyframes typedjsBlink{\n          0% { opacity: 1; }\n          50% { opacity: 0.0; }\n          100% { opacity: 1; }\n        }\n      "),t.fadeOut&&(n+="\n        .typed-fade-out{\n          opacity: 0;\n          transition: opacity .25s;\n        }\n        .typed-cursor.typed-cursor--blink.typed-fade-out{\n          -webkit-animation: 0;\n          animation: 0;\n        }\n      "),0!==e.length&&(e.innerHTML=n,document.body.appendChild(e))}}}]),t}();e.default=u;var c=new u;e.initializer=c},function(t,e){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n={strings:["These are the default values...","You know what you should do?","Use your own!","Have a great day!"],stringsElement:null,typeSpeed:0,startDelay:0,backSpeed:0,smartBackspace:!0,shuffle:!1,backDelay:700,fadeOut:!1,fadeOutClass:"typed-fade-out",fadeOutDelay:500,loop:!1,loopCount:1/0,showCursor:!0,cursorChar:"|",autoInsertCss:!0,attr:null,bindInputFocusEvents:!1,contentType:"html",onBegin:function(t){},onComplete:function(t){},preStringTyped:function(t,e){},onStringTyped:function(t,e){},onLastStringBackspaced:function(t){},onTypingPaused:function(t,e){},onTypingResumed:function(t,e){},onReset:function(t){},onStop:function(t,e){},onStart:function(t,e){},onDestroy:function(t){}};e.default=n,t.exports=e.default},function(t,e){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=function(){function t(t,e){for(var n=0;n<e.length;n++){var r=e[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(t,r.key,r)}}return function(e,n,r){return n&&t(e.prototype,n),r&&t(e,r),e}}(),r=function(){function t(){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t)}return n(t,[{key:"typeHtmlChars",value:function(t,e,n){if("html"!==n.contentType)return e;var r=t.substr(e).charAt(0);if("<"===r||"&"===r){var i="";for(i="<"===r?">":";";t.substr(e+1).charAt(0)!==i&&!(1+ ++e>t.length););e++}return e}},{key:"backSpaceHtmlChars",value:function(t,e,n){if("html"!==n.contentType)return e;var r=t.substr(e).charAt(0);if(">"===r||";"===r){var i="";for(i=">"===r?"<":"&";t.substr(e-1).charAt(0)!==i&&!(--e<0););e--}return e}}]),t}();e.default=r;var i=new r;e.htmlParser=i}])},t.exports=r()},function(t,e,n){var r=function(t){"use strict";var e=Object.prototype,n=e.hasOwnProperty,r="function"==typeof Symbol?Symbol:{},i=r.iterator||"@@iterator",o=r.asyncIterator||"@@asyncIterator",s=r.toStringTag||"@@toStringTag";function a(t,e,n){return Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}),t[e]}try{a({},"")}catch(t){a=function(t,e,n){return t[e]=n}}function u(t,e,n,r){var i=e&&e.prototype instanceof h?e:h,o=Object.create(i.prototype),s=new E(r||[]);return o._invoke=function(t,e,n){var r="suspendedStart";return function(i,o){if("executing"===r)throw new Error("Generator is already running");if("completed"===r){if("throw"===i)throw o;return P()}for(n.method=i,n.arg=o;;){var s=n.delegate;if(s){var a=w(s,n);if(a){if(a===l)continue;return a}}if("next"===n.method)n.sent=n._sent=n.arg;else if("throw"===n.method){if("suspendedStart"===r)throw r="completed",n.arg;n.dispatchException(n.arg)}else"return"===n.method&&n.abrupt("return",n.arg);r="executing";var u=c(t,e,n);if("normal"===u.type){if(r=n.done?"completed":"suspendedYield",u.arg===l)continue;return{value:u.arg,done:n.done}}"throw"===u.type&&(r="completed",n.method="throw",n.arg=u.arg)}}}(t,n,s),o}function c(t,e,n){try{return{type:"normal",arg:t.call(e,n)}}catch(t){return{type:"throw",arg:t}}}t.wrap=u;var l={};function h(){}function p(){}function f(){}var d={};d[i]=function(){return this};var y=Object.getPrototypeOf,v=y&&y(y(C([])));v&&v!==e&&n.call(v,i)&&(d=v);var m=f.prototype=h.prototype=Object.create(d);function g(t){["next","throw","return"].forEach((function(e){a(t,e,(function(t){return this._invoke(e,t)}))}))}function b(t,e){var r;this._invoke=function(i,o){function s(){return new e((function(r,s){!function r(i,o,s,a){var u=c(t[i],t,o);if("throw"!==u.type){var l=u.arg,h=l.value;return h&&"object"==typeof h&&n.call(h,"__await")?e.resolve(h.__await).then((function(t){r("next",t,s,a)}),(function(t){r("throw",t,s,a)})):e.resolve(h).then((function(t){l.value=t,s(l)}),(function(t){return r("throw",t,s,a)}))}a(u.arg)}(i,o,r,s)}))}return r=r?r.then(s,s):s()}}function w(t,e){var n=t.iterator[e.method];if(void 0===n){if(e.delegate=null,"throw"===e.method){if(t.iterator.return&&(e.method="return",e.arg=void 0,w(t,e),"throw"===e.method))return l;e.method="throw",e.arg=new TypeError("The iterator does not provide a 'throw' method")}return l}var r=c(n,t.iterator,e.arg);if("throw"===r.type)return e.method="throw",e.arg=r.arg,e.delegate=null,l;var i=r.arg;return i?i.done?(e[t.resultName]=i.value,e.next=t.nextLoc,"return"!==e.method&&(e.method="next",e.arg=void 0),e.delegate=null,l):i:(e.method="throw",e.arg=new TypeError("iterator result is not an object"),e.delegate=null,l)}function k(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function x(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function E(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(k,this),this.reset(!0)}function C(t){if(t){var e=t[i];if(e)return e.call(t);if("function"==typeof t.next)return t;if(!isNaN(t.length)){var r=-1,o=function e(){for(;++r<t.length;)if(n.call(t,r))return e.value=t[r],e.done=!1,e;return e.value=void 0,e.done=!0,e};return o.next=o}}return{next:P}}function P(){return{value:void 0,done:!0}}return p.prototype=m.constructor=f,f.constructor=p,p.displayName=a(f,s,"GeneratorFunction"),t.isGeneratorFunction=function(t){var e="function"==typeof t&&t.constructor;return!!e&&(e===p||"GeneratorFunction"===(e.displayName||e.name))},t.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,f):(t.__proto__=f,a(t,s,"GeneratorFunction")),t.prototype=Object.create(m),t},t.awrap=function(t){return{__await:t}},g(b.prototype),b.prototype[o]=function(){return this},t.AsyncIterator=b,t.async=function(e,n,r,i,o){void 0===o&&(o=Promise);var s=new b(u(e,n,r,i),o);return t.isGeneratorFunction(n)?s:s.next().then((function(t){return t.done?t.value:s.next()}))},g(m),a(m,s,"Generator"),m[i]=function(){return this},m.toString=function(){return"[object Generator]"},t.keys=function(t){var e=[];for(var n in t)e.push(n);return e.reverse(),function n(){for(;e.length;){var r=e.pop();if(r in t)return n.value=r,n.done=!1,n}return n.done=!0,n}},t.values=C,E.prototype={constructor:E,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=void 0,this.done=!1,this.delegate=null,this.method="next",this.arg=void 0,this.tryEntries.forEach(x),!t)for(var e in this)"t"===e.charAt(0)&&n.call(this,e)&&!isNaN(+e.slice(1))&&(this[e]=void 0)},stop:function(){this.done=!0;var t=this.tryEntries[0].completion;if("throw"===t.type)throw t.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var e=this;function r(n,r){return s.type="throw",s.arg=t,e.next=n,r&&(e.method="next",e.arg=void 0),!!r}for(var i=this.tryEntries.length-1;i>=0;--i){var o=this.tryEntries[i],s=o.completion;if("root"===o.tryLoc)return r("end");if(o.tryLoc<=this.prev){var a=n.call(o,"catchLoc"),u=n.call(o,"finallyLoc");if(a&&u){if(this.prev<o.catchLoc)return r(o.catchLoc,!0);if(this.prev<o.finallyLoc)return r(o.finallyLoc)}else if(a){if(this.prev<o.catchLoc)return r(o.catchLoc,!0)}else{if(!u)throw new Error("try statement without catch or finally");if(this.prev<o.finallyLoc)return r(o.finallyLoc)}}}},abrupt:function(t,e){for(var r=this.tryEntries.length-1;r>=0;--r){var i=this.tryEntries[r];if(i.tryLoc<=this.prev&&n.call(i,"finallyLoc")&&this.prev<i.finallyLoc){var o=i;break}}o&&("break"===t||"continue"===t)&&o.tryLoc<=e&&e<=o.finallyLoc&&(o=null);var s=o?o.completion:{};return s.type=t,s.arg=e,o?(this.method="next",this.next=o.finallyLoc,l):this.complete(s)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),l},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var n=this.tryEntries[e];if(n.finallyLoc===t)return this.complete(n.completion,n.afterLoc),x(n),l}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var n=this.tryEntries[e];if(n.tryLoc===t){var r=n.completion;if("throw"===r.type){var i=r.arg;x(n)}return i}}throw new Error("illegal catch attempt")},delegateYield:function(t,e,n){return this.delegate={iterator:C(t),resultName:e,nextLoc:n},"next"===this.method&&(this.arg=void 0),l}},t}(t.exports);try{regeneratorRuntime=r}catch(t){Function("r","regeneratorRuntime = r")(r)}},function(t,e,n){var r=n(5);t.exports=function(t){if(Array.isArray(t))return r(t)}},function(t,e){t.exports=function(t){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(t))return Array.from(t)}},function(t,e,n){var r=n(5);t.exports=function(t,e){if(t){if("string"==typeof t)return r(t,e);var n=Object.prototype.toString.call(t).slice(8,-1);return"Object"===n&&t.constructor&&(n=t.constructor.name),"Map"===n||"Set"===n?Array.from(t):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?r(t,e):void 0}}},function(t,e){t.exports=function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}},function(t,e,n){},function(t,e,n){},function(t,e,n){"use strict";n.r(e);var r=n(0),i=n.n(r),o=n(1),s=n.n(o),a=n(2),u=n.n(a),c=n(3),l=n.n(c),h=n(6),p=n.n(h),f=n(7),d=n.n(f),y=n(4),v=n.n(y),m=n(8),g=n.n(m),b=function(){function t(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"informational message";u()(this,t),this.message=e,this.render(),this.initEventListeners()}return l()(t,[{key:"initEventListeners",value:function(){var t=this;document.body.addEventListener("pointerdown",(function(e){t.moving.classList.remove("rotate"),t.animated.classList.add("scalemove")}))}},{key:"addTypewriterEffect",value:function(t,e){return new g.a(t,{strings:[e],loop:!0,fadeOut:!0,typeSpeed:0,smartBackspace:!1,backDelay:15e3})}},{key:"render",value:function(){var t=document.createElement("div");return t.innerHTML=this.template,this.element=t.firstElementChild,this.typewriter=this.element.querySelector(".typewriter"),this.animated=this.element.querySelector(".loading__svg"),this.moving=this.element.querySelector(".moving-path"),this.addTypewriterEffect(this.typewriter,this.message),this.element}},{key:"show",value:function(t){(t||document.body).append(this.element)}},{key:"remove",value:function(){this.element.remove()}},{key:"destroy",value:function(){this.remove()}},{key:"template",get:function(){return'\n        <div class="loading">\n          <div class="loading__text loading__text_header" data-element="header">\n            <span>terminal vt-40k</span>\n          </div>\n          <div class="loading__text loading__text_footer" data-element="footer">\n            <span class="typewriter"></span>\n          </div>\n          <svg\n             xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n             xmlns:svg="http://www.w3.org/2000/svg"\n             xmlns="http://www.w3.org/2000/svg"\n             width="100%"\n             viewBox="-50 0 300 300"\n             preserveAspectRatio="xMidYMid meet"\n             class="loading__svg animate-centered"\n             >\n            <g>\n              <path\n                 class="rotate animate-centered moving-path"\n                 d="m 111.12889,225.48471 c 0,-4.9861 0.10956,-6.6404 0.44591,-6.73175 0.24525,-0.0665 2.13145,-0.47913 4.19152,-0.91671 3.26514,-0.69356 7.57314,-1.92241 9.28895,-2.64969 0.42175,-0.17878 1.29049,1.09292 3.74561,5.48317 1.7581,3.14377 3.29052,5.7164 3.40543,5.71697 0.18145,9.1e-4 15.99402,-8.8305 16.32504,-9.11758 0.0685,-0.0593 -1.32561,-2.64714 -3.09787,-5.75059 l -3.22235,-5.64261 1.31423,-1.2163 c 4.84898,-4.48772 6.1866,-5.7915 7.83435,-7.63606 l 1.85313,-2.07455 5.71502,3.41228 c 3.14327,1.87676 5.83431,3.41141 5.98009,3.41035 0.28576,-0.002 9.84946,-16.05443 9.65629,-16.20777 -0.0639,-0.0507 -2.52422,-1.50693 -5.46723,-3.2359 -2.94301,-1.72897 -5.54386,-3.31827 -5.77968,-3.53179 -0.33034,-0.29906 -0.18669,-1.0708 0.62542,-3.36042 1.09396,-3.08404 2.59443,-8.75325 3.01359,-11.38607 l 0.24137,-1.51609 h 6.74646 6.74645 v -9.44555 -9.44557 l -6.83047,-0.0969 -6.83048,-0.0969 -0.85075,-3.81255 c -0.46792,-2.09689 -1.32499,-5.22718 -1.90461,-6.95618 -0.93394,-2.78597 -0.99137,-3.19025 -0.5046,-3.55346 0.30206,-0.22543 2.94602,-1.75044 5.87548,-3.38891 2.92946,-1.63848 5.32888,-3.07307 5.33204,-3.18795 0.005,-0.1746 -8.80759,-15.96974 -9.10195,-16.31414 -0.0534,-0.0625 -2.68626,1.34213 -5.85082,3.12135 -3.16452,1.77922 -5.83415,3.23496 -5.93244,3.23496 -0.18772,0 -10.4993,-10.44262 -10.50036,-10.6338 -3.1e-4,-0.0607 1.51473,-2.668334 3.36685,-5.794773 l 3.36746,-5.6844 -7.0239,-4.149185 c -3.86315,-2.281975 -7.53288,-4.455213 -8.15495,-4.82934 l -1.13104,-0.680242 -3.45328,5.74355 c -2.73124,4.542665 -3.57623,5.694581 -4.0415,5.509328 -2.71412,-1.080686 -8.40285,-2.764047 -11.55758,-3.420052 l -3.83483,-0.797418 v -6.895035 -6.895034 h -9.45328 -9.453249 v 6.895034 6.895035 l -3.834831,0.803979 c -2.109131,0.442198 -5.279557,1.27022 -7.045354,1.840065 -3.804254,1.227682 -2.985712,1.860828 -7.061355,-5.462068 -2.14964,-3.862344 -3.069125,-5.207176 -3.462091,-5.063803 -0.492124,0.179548 -15.716124,8.66274 -15.998823,8.914979 -0.06849,0.06107 1.336092,2.707914 3.121304,5.881849 1.785212,3.173947 3.245889,5.832721 3.245889,5.908411 0,0.0757 -2.506377,2.61237 -5.569746,5.63708 l -5.569695,5.49946 -5.388499,-3.18275 c -2.963648,-1.75052 -5.548294,-3.12947 -5.743705,-3.06434 -0.407388,0.13579 -9.464397,15.21722 -9.472041,15.77254 -0.0052,0.20123 2.402329,1.78082 5.34468,3.51019 2.942349,1.72937 5.430943,3.27577 5.530204,3.43643 0.09932,0.16068 -0.371462,1.95215 -1.046109,3.98108 -0.674644,2.02891 -1.585569,5.41461 -2.024137,7.52375 l -0.797448,3.83481 H 29.555617 22.66058 v 9.45327 9.45326 h 6.924846 6.924795 l 0.241374,1.51609 c 0.357604,2.24604 1.82842,7.98903 2.671676,10.43138 0.884173,2.5612 1.47413,1.95026 -5.788139,5.99407 -2.891139,1.60985 -5.25887,3.02517 -5.261724,3.14518 -0.0052,0.19558 8.822975,16.00736 9.111481,16.32022 0.06539,0.071 2.690887,-1.33368 5.834459,-3.12136 3.14357,-1.78769 5.85331,-3.25034 6.021717,-3.25034 0.168416,0 1.155711,1.04707 2.194024,2.32681 1.03831,1.27975 3.482116,3.83078 5.430689,5.66895 l 3.542856,3.34213 -3.431468,5.79773 c -2.796159,4.72445 -3.344233,5.87788 -2.96049,6.23068 0.710976,0.65362 15.199287,9.09587 15.610037,9.09587 0.196431,0 1.747453,-2.36779 3.446652,-5.26174 1.699248,-2.89394 3.279417,-5.46685 3.511518,-5.71759 0.339666,-0.36695 1.252577,-0.17828 4.680019,0.96726 2.341896,0.78273 5.742892,1.70362 7.557707,2.04645 l 3.299752,0.62331 v 6.70332 6.70333 h 9.453249 9.45328 z M 97.573251,202.83781 C 84.438613,201.61334 72.670744,195.72115 64.266469,186.16109 48.75289,168.51403 47.86775,142.5266 62.129465,123.41996 c 2.384799,-3.19497 7.43098,-8.09892 10.816895,-10.51199 5.344065,-3.80861 12.774641,-7.02727 19.298421,-8.35938 4.16593,-0.85065 12.681349,-1.04852 16.922079,-0.39323 18.85618,2.91373 34.23963,15.80244 39.95984,33.4796 3.21843,9.94577 3.16839,21.59591 -0.13457,31.34171 -5.1106,15.07937 -17.07683,26.85441 -32.17936,31.66517 -6.04658,1.92608 -13.2793,2.75162 -19.239529,2.19597 z"\n              />\n              <path\n                 d="m 101.20176,112.91532 c -13.774557,0.03 -26.200564,5.34772 -29.244413,20.57018 -3.595452,10.97068 5.513253,19.81677 1.789449,27.00328 -0.995186,1.71316 -0.467973,6.6172 0.470278,7.71583 2.709636,1.92354 4.506483,5.59956 5.309214,7.40255 1.087613,2.51125 2.191395,3.891 6.004514,2.2251 0.27332,-0.11216 1.385033,-0.1024 1.335208,0.64989 -1.281977,4.12053 -1.022437,8.33222 -0.983092,12.4955 0.04664,0.80537 2.601551,1.14849 2.698769,0.92165 0.769793,-1.24666 0.291157,-2.18944 0.817668,-3.31556 0.604221,-1.05931 1.410991,-0.45299 1.399011,-0.0167 0.127716,1.86257 0.207831,2.96109 1.547892,2.96109 0.378225,0.0343 0.926025,0.006 1.245409,-0.0637 0.804063,-0.17642 0.571321,-0.7423 1.098883,-2.39864 0.288799,-0.88427 1.461147,-0.75405 1.736952,-0.15362 0.480996,1.09369 -0.251995,2.67114 1.862196,2.50499 2.142512,0.0155 0.897398,-1.50776 1.715682,-2.53335 0.71408,-0.73466 1.80191,-0.44387 2.09143,0.0212 0.4699,0.81412 -0.50423,2.32768 1.5597,2.33011 1.70251,0.0585 1.08282,-1.52605 1.53374,-2.36555 0.36938,-0.64541 1.52221,-1.11767 1.87163,-0.026 0.36028,1.13336 -0.0278,2.53649 1.97562,2.48372 1.8442,-0.0226 1.52511,-1.41975 2.05364,-2.53571 0.4002,-1.01475 2.03037,-0.97366 2.10089,0.005 l 0.36864,2.7862 c -0.0318,0.36665 3.22072,-0.0906 3.29969,-0.30156 1.08734,-6.32407 -1.23484,-11.69786 -1.14209,-12.69125 0,0 0.64803,-1.34995 1.29368,-0.97525 3.31268,1.92249 5.82429,0.0806 6.6483,-1.72721 0.68398,-0.63918 3.81782,-6.30935 6.2561,-9.04643 1.07001,-2.22338 0.47479,-4.37837 -0.23895,-6.35228 -3.26053,-9.46045 2.31483,-17.15603 1.05618,-24.97116 -3.30633,-15.34206 -15.75727,-22.63181 -29.53182,-22.60188 z m -16.3125,44.56604 c 0.890623,-0.003 1.38444,0.17944 1.70859,0.29539 3.670882,1.3131 9.337377,3.95872 10.84943,5.65277 0.06062,0.23964 0.01652,0.82146 -0.803491,1.33521 -0.385637,0.24159 -7.564525,3.56129 -12.182269,3.99379 -0.697635,0.17805 -1.795372,-0.89622 -2.074887,-1.4179 -2.367973,-4.41972 -3.719828,-8.78265 2.502627,-9.85926 z m 34.35615,0.23632 c 6.22244,1.07661 4.87061,5.43718 2.50263,9.85688 -0.27952,0.5217 -1.3749,1.59832 -2.07253,1.42029 -4.61774,-0.4325 -11.79664,-3.75221 -12.18226,-3.9938 -0.82008,-0.51375 -0.86417,-1.09795 -0.80349,-1.33757 1.51204,-1.69405 7.17616,-4.33731 10.84705,-5.65041 0.32415,-0.11595 0.81796,-0.29927 1.7086,-0.29539 z m -17.28802,10.40894 c 2.18948,1.08276 3.69968,7.72942 3.67477,8.17667 -2.4e-4,0.38413 -0.44329,1.49851 -1.96619,2.1694 -0.10805,0.006 -0.13315,-0.0329 -0.18433,-0.0968 -1.09466,-1.36766 -1.08692,-1.47795 -1.56679,-1.46518 -0.27454,0.007 -0.55319,0.40448 -1.2005,1.36829 -0.10296,0.15327 -0.09,0.15428 -0.26941,0.15596 -1.207248,-0.28194 -1.998552,-1.23139 -2.292306,-2.1316 -0.108499,-0.58094 1.845691,-7.4466 3.804756,-8.17665 z"\n             />\n            </g>\n          </svg>\n        </div>\n      '}}]),t}(),w=(n(14),n(15),function(){function t(){u()(this,t),v()(this,"element",void 0),v()(this,"subElements",{}),v()(this,"components",{})}var e,n;return l()(t,[{key:"initComponents",value:(n=s()(i.a.mark((function t(){var e;return i.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return e=new b("Duis nostrud pariatur duis do ullamco ad incididunt. Commodo amet minim sint eiusmod proident culpa voluptate. Mollit et consectetur adipisicing ut. Aute qui irure irure proident non dolor."),this.components.loading=e,t.abrupt("return",this.components);case 4:case"end":return t.stop()}}),t,this)}))),function(){return n.apply(this,arguments)})},{key:"render",value:(e=s()(i.a.mark((function t(){var e;return i.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return(e=document.createElement("div")).innerHTML=this.template,this.element=e.firstElementChild,this.subElements=this.getSubElements(this.element),t.next=6,this.initComponents();case 6:return this.renderComponents(),t.abrupt("return",this.element);case 8:case"end":return t.stop()}}),t,this)}))),function(){return e.apply(this,arguments)})},{key:"renderComponents",value:function(){var t=this;Object.keys(this.components).forEach((function(e){var n=t.subElements[e],r=t.components[e].element;n.append(r)}))}},{key:"getSubElements",value:function(t){var e=t.querySelectorAll("[data-element]");return d()(e).reduce((function(t,e){return t[e.dataset.element]=e,t}),{})}},{key:"remove",value:function(){this.element.remove()}},{key:"destroy",value:function(){this.remove();for(var t=0,e=Object.values(this.components);t<e.length;t++){e[t].destroy()}}},{key:"template",get:function(){return'\n      <div class="page">\n        <div class="content__loading" data-element="loading"></div>\n      </div>\n    '}}]),t}()),k={hack:p.a,main:w},x=function(t,e){return E.apply(this,arguments)};function E(){return(E=s()(i.a.mark((function t(e,n){var r,o;return i.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return r=new(k[e]||k.main),t.next=4,r.render();case 4:return(o=document.querySelector(".screen__content")).innerHTML="",o.appendChild(r.element),t.abrupt("return",r);case 8:case"end":return t.stop()}}),t)})))).apply(this,arguments)}function C(t,e){var n;if("undefined"==typeof Symbol||null==t[Symbol.iterator]){if(Array.isArray(t)||(n=function(t,e){if(!t)return;if("string"==typeof t)return P(t,e);var n=Object.prototype.toString.call(t).slice(8,-1);"Object"===n&&t.constructor&&(n=t.constructor.name);if("Map"===n||"Set"===n)return Array.from(t);if("Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return P(t,e)}(t))||e&&t&&"number"==typeof t.length){n&&(t=n);var r=0,i=function(){};return{s:i,n:function(){return r>=t.length?{done:!0}:{done:!1,value:t[r++]}},e:function(t){throw t},f:i}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var o,s=!0,a=!1;return{s:function(){n=t[Symbol.iterator]()},n:function(){var t=n.next();return s=t.done,t},e:function(t){a=!0,o=t},f:function(){try{s||null==n.return||n.return()}finally{if(a)throw o}}}}function P(t,e){(null==e||e>t.length)&&(e=t.length);for(var n=0,r=new Array(e);n<e;n++)r[n]=t[n];return r}(function(){function t(){u()(this,t),this.routes=[],this.initEventListeners()}var e,n;return l()(t,[{key:"initEventListeners",value:function(){var t=this;document.addEventListener("click",(function(e){var n=e.target.closest("a");if(n){var r=n.getAttribute("href");r&&r.startsWith("/")&&(e.preventDefault(),t.navigate(r))}}))}},{key:"route",value:(n=s()(i.a.mark((function t(){var e,n,r,o,s;return i.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:e=decodeURI(window.location.pathname).replace(/^\/|\/$/,""),r=C(this.routes),t.prev=2,r.s();case 4:if((o=r.n()).done){t.next=14;break}if(s=o.value,!(n=e.match(s.pattern))){t.next=12;break}return t.next=10,this.changePage(s.path,n);case 10:return this.page=t.sent,t.abrupt("break",14);case 12:t.next=4;break;case 14:t.next=19;break;case 16:t.prev=16,t.t0=t.catch(2),r.e(t.t0);case 19:return t.prev=19,r.f(),t.finish(19);case 22:if(n){t.next=26;break}return t.next=25,this.changePage(this.notFoundPagePath);case 25:this.page=t.sent;case 26:document.dispatchEvent(new CustomEvent("route",{detail:{page:this.page}}));case 27:case"end":return t.stop()}}),t,this,[[2,16,19,22]])}))),function(){return n.apply(this,arguments)})},{key:"changePage",value:(e=s()(i.a.mark((function t(e,n){return i.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return this.page&&this.page.destroy&&this.page.destroy(),t.abrupt("return",x(e,n));case 2:case"end":return t.stop()}}),t,this)}))),function(t,n){return e.apply(this,arguments)})},{key:"navigate",value:function(t){history.pushState(null,null,t),this.route()}},{key:"addRoute",value:function(t,e){return this.routes.push({pattern:t,path:e}),this}},{key:"setNotFoundPagePath",value:function(t){return this.notFoundPagePath=t,this}},{key:"listen",value:function(){var t=this;window.addEventListener("popstate",(function(){return t.route()})),this.route()}}],[{key:"instance",value:function(){return this._instance||(this._instance=new t),this._instance}}]),t})().instance().addRoute(/^$/,"main").addRoute(/^hack$/,"hack").setNotFoundPagePath("main").listen()}]);