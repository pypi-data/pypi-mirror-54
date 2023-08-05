/*! For license information please see browse.a2c9ab9dcf982584669b.js.LICENSE */
!function(t,e){"object"==typeof exports&&"object"==typeof module?module.exports=e():"function"==typeof define&&define.amd?define([],e):"object"==typeof exports?exports.browse=e():(t.swh=t.swh||{},t.swh.browse=e())}(window,(function(){return function(t){var e={};function n(o){if(e[o])return e[o].exports;var i=e[o]={i:o,l:!1,exports:{}};return t[o].call(i.exports,i,i.exports,n),i.l=!0,i.exports}return n.m=t,n.c=e,n.d=function(t,e,o){n.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:o})},n.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.t=function(t,e){if(1&e&&(t=n(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var o=Object.create(null);if(n.r(o),Object.defineProperty(o,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var i in t)n.d(o,i,function(e){return t[e]}.bind(null,i));return o},n.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return n.d(e,"a",e),e},n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},n.p="/static/",n(n.s=190)}({1:function(t,e,n){"use strict";function o(t){if(!t.ok)throw t;return t}function i(t){for(var e=0;e<t.length;++e)if(!t[e].ok)throw t[e];return t}function r(t){return"/static/"+t}function s(t,e,n){return void 0===e&&(e={}),void 0===n&&(n=null),e["X-CSRFToken"]=Cookies.get("csrftoken"),fetch(t,{credentials:"include",headers:e,method:"POST",body:n})}function a(t,e){return new RegExp("(?:git|https?|git@)(?:\\:\\/\\/)?"+e+"[/|:][A-Za-z0-9-]+?\\/[\\w\\.-]+\\/?(?!=.git)(?:\\.git(?:\\/?|\\#[\\w\\.\\-_]+)?)?$").test(t)}function c(){history.replaceState("",document.title,window.location.pathname+window.location.search)}function u(t,e){var n=window.getSelection();n.removeAllRanges();var o=document.createRange();o.setStart(t,0),"#text"!==e.nodeName?o.setEnd(e,e.childNodes.length):o.setEnd(e,e.textContent.length),n.addRange(o)}function l(t,e,n){void 0===n&&(n=!1);var o="",i="";return n&&(o='<button type="button" class="close" data-dismiss="alert" aria-label="Close">\n        <span aria-hidden="true">&times;</span>\n      </button>',i="alert-dismissible"),'<div class="alert alert-'+t+" "+i+'" role="alert">'+e+o+"</div>"}n.d(e,"b",(function(){return o})),n.d(e,"c",(function(){return i})),n.d(e,"h",(function(){return r})),n.d(e,"a",(function(){return s})),n.d(e,"e",(function(){return a})),n.d(e,"f",(function(){return c})),n.d(e,"g",(function(){return u})),n.d(e,"d",(function(){return l}))},114:function(t,e,n){var o;o=function(){return function(t){var e={};function n(o){if(e[o])return e[o].exports;var i=e[o]={i:o,l:!1,exports:{}};return t[o].call(i.exports,i,i.exports,n),i.l=!0,i.exports}return n.m=t,n.c=e,n.d=function(t,e,o){n.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:o})},n.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.t=function(t,e){if(1&e&&(t=n(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var o=Object.create(null);if(n.r(o),Object.defineProperty(o,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var i in t)n.d(o,i,function(e){return t[e]}.bind(null,i));return o},n.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return n.d(e,"a",e),e},n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},n.p="",n(n.s=0)}([function(t,e,n){"use strict";var o="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},i=function(){function t(t,e){for(var n=0;n<e.length;n++){var o=e[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(t,o.key,o)}}return function(e,n,o){return n&&t(e.prototype,n),o&&t(e,o),e}}(),r=c(n(1)),s=c(n(3)),a=c(n(4));function c(t){return t&&t.__esModule?t:{default:t}}var u=function(t){function e(t,n){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,e);var o=function(t,e){if(!t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!e||"object"!=typeof e&&"function"!=typeof e?t:e}(this,(e.__proto__||Object.getPrototypeOf(e)).call(this));return o.resolveOptions(n),o.listenClick(t),o}return function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function, not "+typeof e);t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,enumerable:!1,writable:!0,configurable:!0}}),e&&(Object.setPrototypeOf?Object.setPrototypeOf(t,e):t.__proto__=e)}(e,t),i(e,[{key:"resolveOptions",value:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};this.action="function"==typeof t.action?t.action:this.defaultAction,this.target="function"==typeof t.target?t.target:this.defaultTarget,this.text="function"==typeof t.text?t.text:this.defaultText,this.container="object"===o(t.container)?t.container:document.body}},{key:"listenClick",value:function(t){var e=this;this.listener=(0,a.default)(t,"click",(function(t){return e.onClick(t)}))}},{key:"onClick",value:function(t){var e=t.delegateTarget||t.currentTarget;this.clipboardAction&&(this.clipboardAction=null),this.clipboardAction=new r.default({action:this.action(e),target:this.target(e),text:this.text(e),container:this.container,trigger:e,emitter:this})}},{key:"defaultAction",value:function(t){return l("action",t)}},{key:"defaultTarget",value:function(t){var e=l("target",t);if(e)return document.querySelector(e)}},{key:"defaultText",value:function(t){return l("text",t)}},{key:"destroy",value:function(){this.listener.destroy(),this.clipboardAction&&(this.clipboardAction.destroy(),this.clipboardAction=null)}}],[{key:"isSupported",value:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:["copy","cut"],e="string"==typeof t?[t]:t,n=!!document.queryCommandSupported;return e.forEach((function(t){n=n&&!!document.queryCommandSupported(t)})),n}}]),e}(s.default);function l(t,e){var n="data-clipboard-"+t;if(e.hasAttribute(n))return e.getAttribute(n)}t.exports=u},function(t,e,n){"use strict";var o,i="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},r=function(){function t(t,e){for(var n=0;n<e.length;n++){var o=e[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(t,o.key,o)}}return function(e,n,o){return n&&t(e.prototype,n),o&&t(e,o),e}}(),s=n(2),a=(o=s)&&o.__esModule?o:{default:o},c=function(){function t(e){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),this.resolveOptions(e),this.initSelection()}return r(t,[{key:"resolveOptions",value:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};this.action=t.action,this.container=t.container,this.emitter=t.emitter,this.target=t.target,this.text=t.text,this.trigger=t.trigger,this.selectedText=""}},{key:"initSelection",value:function(){this.text?this.selectFake():this.target&&this.selectTarget()}},{key:"selectFake",value:function(){var t=this,e="rtl"==document.documentElement.getAttribute("dir");this.removeFake(),this.fakeHandlerCallback=function(){return t.removeFake()},this.fakeHandler=this.container.addEventListener("click",this.fakeHandlerCallback)||!0,this.fakeElem=document.createElement("textarea"),this.fakeElem.style.fontSize="12pt",this.fakeElem.style.border="0",this.fakeElem.style.padding="0",this.fakeElem.style.margin="0",this.fakeElem.style.position="absolute",this.fakeElem.style[e?"right":"left"]="-9999px";var n=window.pageYOffset||document.documentElement.scrollTop;this.fakeElem.style.top=n+"px",this.fakeElem.setAttribute("readonly",""),this.fakeElem.value=this.text,this.container.appendChild(this.fakeElem),this.selectedText=(0,a.default)(this.fakeElem),this.copyText()}},{key:"removeFake",value:function(){this.fakeHandler&&(this.container.removeEventListener("click",this.fakeHandlerCallback),this.fakeHandler=null,this.fakeHandlerCallback=null),this.fakeElem&&(this.container.removeChild(this.fakeElem),this.fakeElem=null)}},{key:"selectTarget",value:function(){this.selectedText=(0,a.default)(this.target),this.copyText()}},{key:"copyText",value:function(){var t=void 0;try{t=document.execCommand(this.action)}catch(e){t=!1}this.handleResult(t)}},{key:"handleResult",value:function(t){this.emitter.emit(t?"success":"error",{action:this.action,text:this.selectedText,trigger:this.trigger,clearSelection:this.clearSelection.bind(this)})}},{key:"clearSelection",value:function(){this.trigger&&this.trigger.focus(),window.getSelection().removeAllRanges()}},{key:"destroy",value:function(){this.removeFake()}},{key:"action",set:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"copy";if(this._action=t,"copy"!==this._action&&"cut"!==this._action)throw new Error('Invalid "action" value, use either "copy" or "cut"')},get:function(){return this._action}},{key:"target",set:function(t){if(void 0!==t){if(!t||"object"!==(void 0===t?"undefined":i(t))||1!==t.nodeType)throw new Error('Invalid "target" value, use a valid Element');if("copy"===this.action&&t.hasAttribute("disabled"))throw new Error('Invalid "target" attribute. Please use "readonly" instead of "disabled" attribute');if("cut"===this.action&&(t.hasAttribute("readonly")||t.hasAttribute("disabled")))throw new Error('Invalid "target" attribute. You can\'t cut text from elements with "readonly" or "disabled" attributes');this._target=t}},get:function(){return this._target}}]),t}();t.exports=c},function(t,e){t.exports=function(t){var e;if("SELECT"===t.nodeName)t.focus(),e=t.value;else if("INPUT"===t.nodeName||"TEXTAREA"===t.nodeName){var n=t.hasAttribute("readonly");n||t.setAttribute("readonly",""),t.select(),t.setSelectionRange(0,t.value.length),n||t.removeAttribute("readonly"),e=t.value}else{t.hasAttribute("contenteditable")&&t.focus();var o=window.getSelection(),i=document.createRange();i.selectNodeContents(t),o.removeAllRanges(),o.addRange(i),e=o.toString()}return e}},function(t,e){function n(){}n.prototype={on:function(t,e,n){var o=this.e||(this.e={});return(o[t]||(o[t]=[])).push({fn:e,ctx:n}),this},once:function(t,e,n){var o=this;function i(){o.off(t,i),e.apply(n,arguments)}return i._=e,this.on(t,i,n)},emit:function(t){for(var e=[].slice.call(arguments,1),n=((this.e||(this.e={}))[t]||[]).slice(),o=0,i=n.length;o<i;o++)n[o].fn.apply(n[o].ctx,e);return this},off:function(t,e){var n=this.e||(this.e={}),o=n[t],i=[];if(o&&e)for(var r=0,s=o.length;r<s;r++)o[r].fn!==e&&o[r].fn._!==e&&i.push(o[r]);return i.length?n[t]=i:delete n[t],this}},t.exports=n},function(t,e,n){var o=n(5),i=n(6);t.exports=function(t,e,n){if(!t&&!e&&!n)throw new Error("Missing required arguments");if(!o.string(e))throw new TypeError("Second argument must be a String");if(!o.fn(n))throw new TypeError("Third argument must be a Function");if(o.node(t))return function(t,e,n){return t.addEventListener(e,n),{destroy:function(){t.removeEventListener(e,n)}}}(t,e,n);if(o.nodeList(t))return function(t,e,n){return Array.prototype.forEach.call(t,(function(t){t.addEventListener(e,n)})),{destroy:function(){Array.prototype.forEach.call(t,(function(t){t.removeEventListener(e,n)}))}}}(t,e,n);if(o.string(t))return function(t,e,n){return i(document.body,t,e,n)}(t,e,n);throw new TypeError("First argument must be a String, HTMLElement, HTMLCollection, or NodeList")}},function(t,e){e.node=function(t){return void 0!==t&&t instanceof HTMLElement&&1===t.nodeType},e.nodeList=function(t){var n=Object.prototype.toString.call(t);return void 0!==t&&("[object NodeList]"===n||"[object HTMLCollection]"===n)&&"length"in t&&(0===t.length||e.node(t[0]))},e.string=function(t){return"string"==typeof t||t instanceof String},e.fn=function(t){return"[object Function]"===Object.prototype.toString.call(t)}},function(t,e,n){var o=n(7);function i(t,e,n,o,i){var s=r.apply(this,arguments);return t.addEventListener(n,s,i),{destroy:function(){t.removeEventListener(n,s,i)}}}function r(t,e,n,i){return function(n){n.delegateTarget=o(n.target,e),n.delegateTarget&&i.call(t,n)}}t.exports=function(t,e,n,o,r){return"function"==typeof t.addEventListener?i.apply(null,arguments):"function"==typeof n?i.bind(null,document).apply(null,arguments):("string"==typeof t&&(t=document.querySelectorAll(t)),Array.prototype.map.call(t,(function(t){return i(t,e,n,o,r)})))}},function(t,e){var n=9;if("undefined"!=typeof Element&&!Element.prototype.matches){var o=Element.prototype;o.matches=o.matchesSelector||o.mozMatchesSelector||o.msMatchesSelector||o.oMatchesSelector||o.webkitMatchesSelector}t.exports=function(t,e){for(;t&&t.nodeType!==n;){if("function"==typeof t.matches&&t.matches(e))return t;t=t.parentNode}}}])},t.exports=o()},120:function(t,e,n){"use strict";function o(t,e){function n(){$(".swh-releases-switch").removeClass("active"),$(".swh-branches-switch").addClass("active"),$("#swh-tab-releases").removeClass("active"),$("#swh-tab-branches").addClass("active")}function o(){$(".swh-branches-switch").removeClass("active"),$(".swh-releases-switch").addClass("active"),$("#swh-tab-branches").removeClass("active"),$("#swh-tab-releases").addClass("active")}$(document).ready((function(){$(".dropdown-menu a.swh-branches-switch").click((function(t){n(),t.stopPropagation()})),$(".dropdown-menu a.swh-releases-switch").click((function(t){o(),t.stopPropagation()}));var i=!1;$("#swh-branches-releases-dd").on("show.bs.dropdown",(function(){if(!i){var t=$(".swh-branches-releases").width();$(".swh-branches-releases").width(t+25),i=!0}})),t&&(e?n():o())}))}n.d(e,"a",(function(){return o}))},121:function(t,e,n){"use strict";n.d(e,"a",(function(){return p}));var o,i=n(180),r=n(1),s=100,a=2*s,c=0,u=null,l=!1;function f(){$("#origin-search-results tbody tr").remove()}function d(t,e){var n=e%a;if(t.length>0){$("#swh-origin-search-results").show(),$("#swh-no-result").hide(),f();for(var o=$("#origin-search-results tbody"),i=function(e){var n=t[e],i=Urls.browse_origin(n.url),r='<tr id="origin-'+e+'" class="swh-search-result-entry swh-tr-hover-highlight">';r+='<td style="width: 120px;">'+n.type+"</td>",r+='<td style="white-space: nowrap;"><a href="'+encodeURI(i)+'">'+encodeURI(n.url)+"</a></td>",r+='<td class="swh-visit-status" id="visit-status-origin-'+e+'"><i title="Checking visit status" class="fa fa-refresh fa-spin"></i></td>',r+="</tr>",o.append(r);var s=Urls.api_1_origin_visit_latest(n.url);fetch(s+="?require_snapshot=true").then((function(t){return t.json()})).then((function(t){$("#visit-status-origin-"+e).children().remove(),t?$("#visit-status-origin-"+e).append('<i title="Origin has at least one full visit by Software Heritage" class="fa fa-check"></i>'):($("#visit-status-origin-"+e).append('<i title="Origin has not yet been visited by Software Heritage or does not have at least one full visit" class="fa fa-times"></i>'),$("#swh-filter-empty-visits").prop("checked")&&$("#origin-"+e).remove())}))},r=n;r<n+s&&r<t.length;++r)i(r);setTimeout((function(){$("#origin-search-results tbody tr").removeAttr("style")}))}else $("#swh-origin-search-results").hide(),$("#swh-no-result").text("No origins matching the search criteria were found."),$("#swh-no-result").show();t.length-n<s||t.length<a&&n+s===t.length?$("#origins-next-results-button").addClass("disabled"):$("#origins-next-results-button").removeClass("disabled"),e>0?$("#origins-prev-results-button").removeClass("disabled"):$("#origins-prev-results-button").addClass("disabled"),l=!1,setTimeout((function(){window.scrollTo(0,0)}))}function h(t,e,n,s){var a;if($("#swh-search-origin-metadata").prop("checked"))a=Urls.api_1_origin_metadata_search()+"?fulltext="+t;else{o=t;for(var c=t.trim().replace(/\s+/g," ").split(" "),h=0;h<c.length;++h)c[h]=c[h].replace(/[|\\{}()[\]^$+*?.]/g,"\\\\\\$&");if(c.length<7){var p=[];Object(i.a)(c,(function(t){return p.push(t.join(".*"))}));var g=p.join("|");a=Urls.browse_origin_search(g)+"?regexp=true"}else a=Urls.browse_origin_search(c.join(".*"))+"?regexp=true"}var v=a+"&limit="+e+"&offset="+n+"&with_visit="+$("#swh-search-origins-with-visit").prop("checked");f(),$(".swh-loading").addClass("show"),fetch(v).then(r.b).then((function(t){return t.json()})).then((function(t){u=t,$(".swh-loading").removeClass("show"),d(t,s)})).catch((function(t){$(".swh-loading").removeClass("show"),l=!1,$("#swh-origin-search-results").hide(),$("#swh-no-result").text("Error "+t.status+": "+t.statusText),$("#swh-no-result").show()}))}function p(){$(document).ready((function(){$("#swh-search-origins").submit((function(t){t.preventDefault();var e=$("#origins-url-patterns").val().trim(),n=$("#swh-search-origins-with-visit").prop("checked"),o=$("#swh-filter-empty-visits").prop("checked"),i=$("#swh-search-origin-metadata").prop("checked"),r="?q="+encodeURIComponent(e);n&&(r+="&with_visit"),o&&(r+="&with_content"),i&&(r+="&search_metadata"),window.location.search=r})),$("#origins-next-results-button").click((function(t){$("#origins-next-results-button").hasClass("disabled")||l||(l=!0,c+=s,!u||c>=a&&c%a==0?h(o,a,c,c):d(u,c),t.preventDefault())})),$("#origins-prev-results-button").click((function(t){$("#origins-prev-results-button").hasClass("disabled")||l||(l=!0,c-=s,!u||c>0&&(c+s)%a==0?h(o,a,c+s-a,c):d(u,c),t.preventDefault())}));var t=new URLSearchParams(window.location.search),e=t.get("q"),n=t.has("with_visit"),i=t.has("with_content"),f=t.has("search_metadata");e&&($("#origins-url-patterns").val(e),$("#swh-search-origins-with-visit").prop("checked",n),$("#swh-filter-empty-visits").prop("checked",i),$("#swh-search-origin-metadata").prop("checked",f),function(){$("#swh-no-result").hide();var t=$("#origins-url-patterns").val();c=0,l=!0;var e=Urls.api_1_resolve_swh_pid(t);fetch(e).then(r.b).then((function(t){return t.json()})).then((function(t){window.location=t.browse_url})).catch((function(e){t.startsWith("swh:")?e.json().then((function(t){$("#swh-origin-search-results").hide(),$(".swh-search-pagination").hide(),$("#swh-no-result").text(t.reason),$("#swh-no-result").show()})):($("#swh-origin-search-results").show(),$(".swh-search-pagination").show(),h(t,a,c,c))}))}())}))}},122:function(t,e,n){"use strict";var o=n(13);$(document).ready((function(){$(".dropdown-submenu a.dropdown-item").on("click",(function(t){$(t.target).next("div").toggle(),"none"!==$(t.target).next("div").css("display")?$(t.target).focus():$(t.target).blur(),t.stopPropagation(),t.preventDefault()})),$(".swh-popover-toggler").popover({boundary:"viewport",container:"body",html:!0,placement:function(){return $(window).width()<o.b?"top":"right"},template:'<div class="popover" role="tooltip">\n                 <div class="arrow"></div>\n                 <h3 class="popover-header"></h3>\n                 <div class="popover-body swh-popover"></div>\n               </div>',content:function(){var t=$(this).attr("data-popover-content");return $(t).children(".popover-body").remove().html()},title:function(){var t=$(this).attr("data-popover-content");return $(t).children(".popover-heading").html()},offset:"50vh",sanitize:!1}),$(".swh-vault-menu a.dropdown-item").on("click",(function(t){$(".swh-popover-toggler").popover("hide")})),$(".swh-popover-toggler").on("show.bs.popover",(function(t){$(".swh-popover-toggler:not(#"+t.currentTarget.id+")").popover("hide"),$(".swh-vault-menu .dropdown-menu").hide()})),$(".swh-actions-dropdown").on("hide.bs.dropdown",(function(){$(".swh-vault-menu .dropdown-menu").hide(),$(".swh-popover-toggler").popover("hide")})),$("body").on("click",(function(t){$(t.target).parents(".swh-popover").length&&t.stopPropagation()}))}))},123:function(t,e,n){"use strict";n.d(e,"a",(function(){return s})),n.d(e,"c",(function(){return a})),n.d(e,"b",(function(){return u}));var o=n(114),i=n.n(o),r=(n(196),n(197),n(13));function s(t){t.preventDefault(),$(t.target).tab("show")}function a(t){t.stopPropagation();var e=$(t.target).closest(".swh-id-ui").find(".swh-id"),n=";origin="+$(t.target).data("swh-origin"),o=e.text();$(t.target).prop("checked")?-1===o.indexOf(n)&&(o+=n):o=o.replace(n,""),e.text(o),e.attr("href","/"+o+"/")}function c(t){for(var e=$(t).closest(".swh-id-ui").find(".swh-id"),n=e.text(),o=[],i=";lines=",r=new RegExp(/L(\d+)/g),s=r.exec(window.location.hash);s;)o.push(parseInt(s[1])),s=r.exec(window.location.hash);o.length>0&&(i+=o[0]),o.length>1&&(i+="-"+o[1]),$(t).prop("checked")?(n=n.replace(/;lines=\d+-*\d*/g,""),n+=i):n=n.replace(i,""),e.text(n),e.attr("href","/"+n+"/")}function u(t){t.stopPropagation(),window.location.hash&&c(t.target)}$(document).ready((function(){new i.a(".btn-swh-id-copy",{text:function(t){return $(t).closest(".swh-id-ui").find(".swh-id").text()}}),new i.a(".btn-swh-id-url-copy",{text:function(t){var e=$(t).closest(".swh-id-ui").find(".swh-id").text();return window.location.origin+"/"+e+"/"}}),.7*window.innerWidth>1e3&&$("#swh-identifiers").css("width","1000px");var t={tabLocation:"right",offset:function(){return $(window).width()<r.b?"250px":"200px"}};(window.innerHeight<600||window.innerWidth<500)&&(t.otherOffset="20px"),$("#swh-identifiers").tabSlideOut(t),$("#swh-identifiers").css("display","block"),$(".swh-id-option-origin").trigger("click"),$(".swh-id-option-lines").trigger("click"),$(window).on("hashchange",(function(){c(".swh-id-option-lines")}))}))},13:function(t,e,n){"use strict";n.d(e,"b",(function(){return i})),n.d(e,"a",(function(){return r})),n.d(e,"c",(function(){return s}));var o=n(1),i=768,r=992,s=Object(o.h)("img/swh-spinner.gif")},180:function(t,e,n){"use strict";function o(t,e,n){var o=t[e];t[e]=t[n],t[n]=o}function i(t,e,n){if(1===(n=n||t.length))e(t);else for(var r=1;r<=n;r+=1){i(t,e,n-1);o(t,(n%2?1:r)-1,n-1)}}n.d(e,"a",(function(){return i}))},190:function(t,e,n){t.exports=n(191)},191:function(t,e,n){"use strict";n.r(e);n(192),n(193),n(194),n(195);var o=n(120);n.d(e,"initSnapshotNavigation",(function(){return o.a}));var i=n(121);n.d(e,"initOriginSearch",(function(){return i.a}));n(122);var r=n(123);n.d(e,"swhIdObjectTypeToggled",(function(){return r.a})),n.d(e,"swhIdOptionOriginToggled",(function(){return r.c})),n.d(e,"swhIdOptionLinesToggled",(function(){return r.b}))},192:function(t,e,n){},193:function(t,e,n){},194:function(t,e,n){},195:function(t,e,n){},196:function(t,e){!function(t){t.fn.tabSlideOut=function(e){function n(t){return parseInt(t.outerHeight()+1,10)+"px"}function o(){var e=t(window).height();return"top"!==a&&"bottom"!==a||(e=t(window).width()),e-parseInt(s.otherOffset)-parseInt(s.offset)}var i=this;function r(){return i.hasClass("ui-slideouttab-open")}if("string"==typeof e)switch(e){case"open":return this.trigger("open"),this;case"close":return this.trigger("close"),this;case"isOpen":return r();case"toggle":return this.trigger("toggle"),this;case"bounce":return this.trigger("bounce"),this;default:throw new Error("Invalid tabSlideOut command")}else{var s=t.extend({tabLocation:"left",tabHandle:".handle",action:"click",hoverTimeout:5e3,offset:"200px",offsetReverse:!1,otherOffset:null,handleOffset:null,handleOffsetReverse:!1,bounceDistance:"50px",bounceTimes:4,bounceSpeed:300,tabImage:null,tabImageHeight:null,tabImageWidth:null,onLoadSlideOut:!1,clickScreenToClose:!0,clickScreenToCloseFilters:[".ui-slideouttab-panel"],onOpen:function(){},onClose:function(){}},e||{}),a=s.tabLocation,c=s.tabHandle=t(s.tabHandle,i);if(i.addClass("ui-slideouttab-panel").addClass("ui-slideouttab-"+a),s.offsetReverse&&i.addClass("ui-slideouttab-panel-reverse"),c.addClass("ui-slideouttab-handle"),s.handleOffsetReverse&&c.addClass("ui-slideouttab-handle-reverse"),s.toggleButton=t(s.toggleButton),null!==s.tabImage){var u=0,l=0;if(null!==s.tabImageHeight&&null!==s.tabImageWidth)u=s.tabImageHeight,l=s.tabImageWidth;else{var f=new Image;f.src=s.tabImage,u=f.naturalHeight,l=f.naturalWidth}c.addClass("ui-slideouttab-handle-image"),c.css({background:"url("+s.tabImage+") no-repeat",width:l,height:u})}"top"===a||"bottom"===a?(s.panelOffsetFrom=s.offsetReverse?"right":"left",s.handleOffsetFrom=s.handleOffsetReverse?"right":"left"):(s.panelOffsetFrom=s.offsetReverse?"bottom":"top",s.handleOffsetFrom=s.handleOffsetReverse?"bottom":"top"),null===s.handleOffset&&(s.handleOffset="-"+function(t,e){return parseInt(t.css("border-"+e+"-width"),10)}(i,s.handleOffsetFrom)+"px"),"top"===a||"bottom"===a?(i.css(s.panelOffsetFrom,s.offset),c.css(s.handleOffsetFrom,s.handleOffset),null!==s.otherOffset&&(i.css("width",o()+"px"),t(window).resize((function(){i.css("width",o()+"px")}))),"top"===a?c.css({bottom:"-"+n(c)}):c.css({top:"-"+n(c)})):(i.css(s.panelOffsetFrom,s.offset),c.css(s.handleOffsetFrom,s.handleOffset),null!==s.otherOffset&&(i.css("height",o()+"px"),t(window).resize((function(){i.css("height",o()+"px")}))),"left"===a?c.css({right:"0"}):c.css({left:"0"})),c.click((function(t){t.preventDefault()})),s.toggleButton.click((function(t){t.preventDefault()})),i.addClass("ui-slideouttab-ready");var d=function(){i.removeClass("ui-slideouttab-open").trigger("slideouttabclose"),s.onClose()},h=function(){i.addClass("ui-slideouttab-open").trigger("slideouttabopen"),s.onOpen()},p=function(){r()?d():h()},g=[];g[a]="-="+s.bounceDistance;var v=[];v[a]="+="+s.bounceDistance;if(s.clickScreenToClose&&t(document).click((function(e){if(r()&&!i[0].contains(e.target)){for(var n=t(e.target),o=0;o<s.clickScreenToCloseFilters.length;o++){var a=s.clickScreenToCloseFilters[o];if("string"==typeof a){if(n.is(a)||n.parents().is(a))return}else if("function"==typeof a&&a.call(i,e))return}d()}})),"click"===s.action)c.click((function(t){p()}));else if("hover"===s.action){var b=null;i.hover((function(){r()||h(),b=null}),(function(){r()&&null===b&&(b=setTimeout((function(){b&&d(),b=null}),s.hoverTimeout))})),c.click((function(t){r()&&d()}))}s.onLoadSlideOut&&(h(),setTimeout(h,500)),i.on("open",(function(t){r()||h()})),i.on("close",(function(t){r()&&d()})),i.on("toggle",(function(t){p()})),i.on("bounce",(function(t){r()?function(){for(var t=i,e=0;e<s.bounceTimes;e++)t=t.animate(g,s.bounceSpeed).animate(v,s.bounceSpeed);i.trigger("slideouttabbounce")}():function(){for(var t=i,e=0;e<s.bounceTimes;e++)t=t.animate(v,s.bounceSpeed).animate(g,s.bounceSpeed);i.trigger("slideouttabbounce")}()}))}return this}}(jQuery)},197:function(t,e,n){}})}));
//# sourceMappingURL=browse.a2c9ab9dcf982584669b.js.map