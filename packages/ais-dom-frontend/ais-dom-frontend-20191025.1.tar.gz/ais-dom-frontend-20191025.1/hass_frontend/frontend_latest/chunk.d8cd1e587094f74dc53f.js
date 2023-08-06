/*! For license information please see chunk.d8cd1e587094f74dc53f.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[18],{153:function(t,e){t.exports=function(t,e){var a=0,i={};t.addEventListener("message",function(e){var a=e.data;if("RPC"===a.type)if(a.id){var r=i[a.id];r&&(delete i[a.id],a.error?r[1](Object.assign(Error(a.error.message),a.error)):r[0](a.result))}else{var n=document.createEvent("Event");n.initEvent(a.method,!1,!1),n.data=a.params,t.dispatchEvent(n)}}),e.forEach(function(e){t[e]=function(){for(var r=[],n=arguments.length;n--;)r[n]=arguments[n];return new Promise(function(n,s){var o=++a;i[o]=[n,s],t.postMessage({type:"RPC",id:o,method:e,params:r})})}})}},182:function(t,e,a){"use strict";a(3),a(45),a(42),a(54);var i=a(5),r=a(4);Object(i.a)({_template:r.a`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},190:function(t,e,a){"use strict";a(3),a(45),a(54),a(144);var i=a(5),r=a(4),n=a(119);Object(i.a)({_template:r.a`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[n.a]})},197:function(t,e,a){"use strict";a.d(e,"a",function(){return r});var i=a(13);a.d(e,"b",function(){return i.c}),a.d(e,"c",function(){return i.f}),a.d(e,"d",function(){return i.g}),a.d(e,"e",function(){return i.h}),a.d(e,"f",function(){return i.i}),a.d(e,"g",function(){return i.j});class r extends i.a{createRenderRoot(){return this.attachShadow({mode:"open",delegatesFocus:!0})}click(){this.formElement&&(this.formElement.focus(),this.formElement.click())}setAriaLabel(t){this.formElement&&this.formElement.setAttribute("aria-label",t)}firstUpdated(){super.firstUpdated(),this.mdcRoot.addEventListener("change",t=>{this.dispatchEvent(new Event("change",t))})}}},247:function(t,e,a){"use strict";a(3);var i=a(5);Object(i.a)({is:"app-route",properties:{route:{type:Object,notify:!0},pattern:{type:String},data:{type:Object,value:function(){return{}},notify:!0},autoActivate:{type:Boolean,value:!1},_queryParamsUpdating:{type:Boolean,value:!1},queryParams:{type:Object,value:function(){return{}},notify:!0},tail:{type:Object,value:function(){return{path:null,prefix:null,__queryParams:null}},notify:!0},active:{type:Boolean,notify:!0,readOnly:!0},_matched:{type:String,value:""}},observers:["__tryToMatch(route.path, pattern)","__updatePathOnDataChange(data.*)","__tailPathChanged(tail.path)","__routeQueryParamsChanged(route.__queryParams)","__tailQueryParamsChanged(tail.__queryParams)","__queryParamsChanged(queryParams.*)"],created:function(){this.linkPaths("route.__queryParams","tail.__queryParams"),this.linkPaths("tail.__queryParams","route.__queryParams")},__routeQueryParamsChanged:function(t){if(t&&this.tail){if(this.tail.__queryParams!==t&&this.set("tail.__queryParams",t),!this.active||this._queryParamsUpdating)return;var e={},a=!1;for(var i in t)e[i]=t[i],!a&&this.queryParams&&t[i]===this.queryParams[i]||(a=!0);for(var i in this.queryParams)if(a||!(i in t)){a=!0;break}if(!a)return;this._queryParamsUpdating=!0,this.set("queryParams",e),this._queryParamsUpdating=!1}},__tailQueryParamsChanged:function(t){t&&this.route&&this.route.__queryParams!=t&&this.set("route.__queryParams",t)},__queryParamsChanged:function(t){this.active&&!this._queryParamsUpdating&&this.set("route.__"+t.path,t.value)},__resetProperties:function(){this._setActive(!1),this._matched=null},__tryToMatch:function(){if(this.route){var t=this.route.path,e=this.pattern;if(this.autoActivate&&""===t&&(t="/"),e)if(t){for(var a=t.split("/"),i=e.split("/"),r=[],n={},s=0;s<i.length;s++){var o=i[s];if(!o&&""!==o)break;var l=a.shift();if(!l&&""!==l)return void this.__resetProperties();if(r.push(l),":"==o.charAt(0))n[o.slice(1)]=l;else if(o!==l)return void this.__resetProperties()}this._matched=r.join("/");var h={};this.active||(h.active=!0);var u=this.route.prefix+this._matched,c=a.join("/");for(var p in a.length>0&&(c="/"+c),this.tail&&this.tail.prefix===u&&this.tail.path===c||(h.tail={prefix:u,path:c,__queryParams:this.route.__queryParams}),h.data=n,this._dataInUrl={},n)this._dataInUrl[p]=n[p];this.setProperties?this.setProperties(h,!0):this.__setMulti(h)}else this.__resetProperties()}},__tailPathChanged:function(t){if(this.active){var e=t,a=this._matched;e&&("/"!==e.charAt(0)&&(e="/"+e),a+=e),this.set("route.path",a)}},__updatePathOnDataChange:function(){if(this.route&&this.active){var t=this.__getLink({});t!==this.__getLink(this._dataInUrl)&&this.set("route.path",t)}},__getLink:function(t){var e={tail:null};for(var a in this.data)e[a]=this.data[a];for(var a in t)e[a]=t[a];var i=this.pattern.split("/").map(function(t){return":"==t[0]&&(t=e[t.slice(1)]),t},this);return e.tail&&e.tail.path&&(i.length>0&&"/"===e.tail.path.charAt(0)?i.push(e.tail.path.slice(1)):i.push(e.tail.path)),i.join("/")},__setMulti:function(t){for(var e in t)this._propertySetter(e,t[e]);void 0!==t.data&&(this._pathEffector("data",this.data),this._notifyChange("data")),void 0!==t.active&&(this._pathEffector("active",this.active),this._notifyChange("active")),void 0!==t.tail&&(this._pathEffector("tail",this.tail),this._notifyChange("tail"))}})},320:function(t,e,a){"use strict";function i(t){if(!t||"object"!=typeof t)return t;if("[object Date]"==Object.prototype.toString.call(t))return new Date(t.getTime());if(Array.isArray(t))return t.map(i);var e={};return Object.keys(t).forEach(function(a){e[a]=i(t[a])}),e}a.d(e,"a",function(){return i})},372:function(t,e,a){"use strict";a.d(e,"a",function(){return c});var i=a(10);const r=(t,e)=>{const a=t.startNode.parentNode,r=void 0===e?t.endNode:e.startNode,n=a.insertBefore(Object(i.e)(),r);a.insertBefore(Object(i.e)(),r);const s=new i.b(t.options);return s.insertAfterNode(n),s},n=(t,e)=>(t.setValue(e),t.commit(),t),s=(t,e,a)=>{const r=t.startNode.parentNode,n=a?a.startNode:t.endNode,s=e.endNode.nextSibling;s!==n&&Object(i.j)(r,e.startNode,s,n)},o=t=>{Object(i.i)(t.startNode.parentNode,t.startNode,t.endNode.nextSibling)},l=(t,e,a)=>{const i=new Map;for(let r=e;r<=a;r++)i.set(t[r],r);return i},h=new WeakMap,u=new WeakMap,c=Object(i.f)((t,e,a)=>{let c;return void 0===a?a=e:void 0!==e&&(c=e),e=>{if(!(e instanceof i.b))throw new Error("repeat can only be used in text bindings");const p=h.get(e)||[],f=u.get(e)||[],d=[],y=[],_=[];let v,m,g=0;for(const i of t)_[g]=c?c(i,g):g,y[g]=a(i,g),g++;let P=0,b=p.length-1,q=0,j=y.length-1;for(;P<=b&&q<=j;)if(null===p[P])P++;else if(null===p[b])b--;else if(f[P]===_[q])d[q]=n(p[P],y[q]),P++,q++;else if(f[b]===_[j])d[j]=n(p[b],y[j]),b--,j--;else if(f[P]===_[j])d[j]=n(p[P],y[j]),s(e,p[P],d[j+1]),P++,j--;else if(f[b]===_[q])d[q]=n(p[b],y[q]),s(e,p[b],p[P]),b--,q++;else if(void 0===v&&(v=l(_,q,j),m=l(f,P,b)),v.has(f[P]))if(v.has(f[b])){const t=m.get(_[q]),a=void 0!==t?p[t]:null;if(null===a){const t=r(e,p[P]);n(t,y[q]),d[q]=t}else d[q]=n(a,y[q]),s(e,a,p[P]),p[t]=null;q++}else o(p[b]),b--;else o(p[P]),P++;for(;q<=j;){const t=r(e,d[j+1]);n(t,y[q]),d[q++]=t}for(;P<=b;){const t=p[P++];null!==t&&o(t)}h.set(e,d),u.set(e,_)}})}}]);
//# sourceMappingURL=chunk.d8cd1e587094f74dc53f.js.map