(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["b0161b3c"],{4546:function(e,t,n){"use strict";var a=n("e793"),o=n.n(a);o.a},5118:function(e,t,n){(function(e){var a="undefined"!==typeof e&&e||"undefined"!==typeof self&&self||window,o=Function.prototype.apply;function i(e,t){this._id=e,this._clearFn=t}t.setTimeout=function(){return new i(o.call(setTimeout,a,arguments),clearTimeout)},t.setInterval=function(){return new i(o.call(setInterval,a,arguments),clearInterval)},t.clearTimeout=t.clearInterval=function(e){e&&e.close()},i.prototype.unref=i.prototype.ref=function(){},i.prototype.close=function(){this._clearFn.call(a,this._id)},t.enroll=function(e,t){clearTimeout(e._idleTimeoutId),e._idleTimeout=t},t.unenroll=function(e){clearTimeout(e._idleTimeoutId),e._idleTimeout=-1},t._unrefActive=t.active=function(e){clearTimeout(e._idleTimeoutId);var t=e._idleTimeout;t>=0&&(e._idleTimeoutId=setTimeout(function(){e._onTimeout&&e._onTimeout()},t))},n("6017"),t.setImmediate="undefined"!==typeof self&&self.setImmediate||"undefined"!==typeof e&&e.setImmediate||this&&this.setImmediate,t.clearImmediate="undefined"!==typeof self&&self.clearImmediate||"undefined"!==typeof e&&e.clearImmediate||this&&this.clearImmediate}).call(this,n("c8ba"))},6017:function(e,t,n){(function(e,t){(function(e,n){"use strict";if(!e.setImmediate){var a,o=1,i={},s=!1,c=e.document,r=Object.getPrototypeOf&&Object.getPrototypeOf(e);r=r&&r.setTimeout?r:e,"[object process]"==={}.toString.call(e.process)?m():p()?y():e.MessageChannel?h():c&&"onreadystatechange"in c.createElement("script")?v():g(),r.setImmediate=u,r.clearImmediate=l}function u(e){"function"!==typeof e&&(e=new Function(""+e));for(var t=new Array(arguments.length-1),n=0;n<t.length;n++)t[n]=arguments[n+1];var s={callback:e,args:t};return i[o]=s,a(o),o++}function l(e){delete i[e]}function f(e){var t=e.callback,a=e.args;switch(a.length){case 0:t();break;case 1:t(a[0]);break;case 2:t(a[0],a[1]);break;case 3:t(a[0],a[1],a[2]);break;default:t.apply(n,a);break}}function d(e){if(s)setTimeout(d,0,e);else{var t=i[e];if(t){s=!0;try{f(t)}finally{l(e),s=!1}}}}function m(){a=function(e){t.nextTick(function(){d(e)})}}function p(){if(e.postMessage&&!e.importScripts){var t=!0,n=e.onmessage;return e.onmessage=function(){t=!1},e.postMessage("","*"),e.onmessage=n,t}}function y(){var t="setImmediate$"+Math.random()+"$",n=function(n){n.source===e&&"string"===typeof n.data&&0===n.data.indexOf(t)&&d(+n.data.slice(t.length))};e.addEventListener?e.addEventListener("message",n,!1):e.attachEvent("onmessage",n),a=function(n){e.postMessage(t+n,"*")}}function h(){var e=new MessageChannel;e.port1.onmessage=function(e){var t=e.data;d(t)},a=function(t){e.port2.postMessage(t)}}function v(){var e=c.documentElement;a=function(t){var n=c.createElement("script");n.onreadystatechange=function(){d(t),n.onreadystatechange=null,e.removeChild(n),n=null},e.appendChild(n)}}function g(){a=function(e){setTimeout(d,0,e)}}})("undefined"===typeof self?"undefined"===typeof e?this:e:self)}).call(this,n("c8ba"),n("4362"))},8041:function(e,t,n){"use strict";var a=n("d924"),o=n.n(a);o.a},"8b24":function(e,t,n){"use strict";n.r(t);var a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("Player",{staticClass:"fixed-center"})],1)},o=[],i=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("video",{attrs:{id:"player",autoplay:"autoplay",muted:"muted",loop:"loop",playsinline:"playsinline",preload:"metadata","data-aos":"fade-up"},domProps:{muted:!0},on:{canplay:e.onCanPlayThrough}},[n("source",{attrs:{src:e.source,type:e.type}}),e._v("\n    Your browser does not support MP4 Format videos or HTML5 Video.\n")])},s=[],c=n("bc3a"),r=n("5118"),u={name:"Player",beforeMount:function(){this.reload()},data:function(){return{source:"https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_2mb.mp4",type:"video/mp4",state:"stop"}},methods:{onCanPlayThrough:function(e){e.target.muted=!0,e.target.play(),e.target.pause(),e.target.play()},actByState:function(e){this.source="stop"!==e?e+".mp4":""},getState:function(){var e=this;c["axios"].get("/current/").then(function(t){var n=t.data["state"];n!==e.state&&(e.actByState(n),e.state=n)})},reload:function(){Object(r["setTimeout"])(function(){this.getState()}.bind(this),1e3)}}},l=u,f=(n("4546"),n("2877")),d=Object(f["a"])(l,i,s,!1,null,"0e16742e",null),m=d.exports,p={name:"PageIndex",components:{Player:m},data:function(){return{}}},y=p,h=(n("8041"),Object(f["a"])(y,a,o,!1,null,null,null));t["default"]=h.exports},d924:function(e,t,n){},e793:function(e,t,n){}}]);