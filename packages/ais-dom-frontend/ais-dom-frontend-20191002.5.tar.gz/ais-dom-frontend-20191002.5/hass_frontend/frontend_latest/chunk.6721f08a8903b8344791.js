/*! For license information please see chunk.6721f08a8903b8344791.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[94],{119:function(t,e,i){"use strict";i.d(e,"a",function(){return s});i(5);var a=i(55),n=i(35);const s=[a.a,n.a,{hostAttributes:{role:"option",tabindex:"0"}}]},143:function(t,e,i){"use strict";i(5),i(45),i(144);var a=i(6),n=i(4),s=i(119);Object(a.a)({_template:n.a`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[s.a]})},144:function(t,e,i){"use strict";i(45),i(68),i(42),i(54);const a=document.createElement("template");a.setAttribute("style","display: none;"),a.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(a.content)},175:function(t,e,i){"use strict";var a=i(9);e.a=Object(a.a)(t=>(class extends t{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(t){return t}}))},177:function(t,e,i){"use strict";var a=i(3),n=i(0);class s extends n.a{static get styles(){return n.c`
      :host {
        background: var(
          --ha-card-background,
          var(--paper-card-background-color, white)
        );
        border-radius: var(--ha-card-border-radius, 2px);
        box-shadow: var(
          --ha-card-box-shadow,
          0 2px 2px 0 rgba(0, 0, 0, 0.14),
          0 1px 5px 0 rgba(0, 0, 0, 0.12),
          0 3px 1px -2px rgba(0, 0, 0, 0.2)
        );
        color: var(--primary-text-color);
        display: block;
        transition: all 0.3s ease-out;
        position: relative;
      }

      .card-header,
      :host ::slotted(.card-header) {
        color: var(--ha-card-header-color, --primary-text-color);
        font-family: var(--ha-card-header-font-family, inherit);
        font-size: var(--ha-card-header-font-size, 24px);
        letter-spacing: -0.012em;
        line-height: 32px;
        padding: 24px 16px 16px;
        display: block;
      }

      :host ::slotted(.card-content:not(:first-child)),
      slot:not(:first-child)::slotted(.card-content) {
        padding-top: 0px;
        margin-top: -8px;
      }

      :host ::slotted(.card-content) {
        padding: 16px;
      }

      :host ::slotted(.card-actions) {
        border-top: 1px solid #e8e8e8;
        padding: 5px 16px;
      }
    `}render(){return n.f`
      ${this.header?n.f`
            <div class="card-header">${this.header}</div>
          `:n.f``}
      <slot></slot>
    `}}Object(a.c)([Object(n.g)()],s.prototype,"header",void 0),customElements.define("ha-card",s)},179:function(t,e,i){"use strict";i.d(e,"a",function(){return s});i(109);const a=customElements.get("iron-icon");let n=!1;class s extends a{listen(t,e,a){super.listen(t,e,a),n||"mdi"!==this._iconsetName||(n=!0,i.e(77).then(i.bind(null,210)))}}customElements.define("ha-icon",s)},182:function(t,e,i){"use strict";i(5),i(45),i(42),i(54);var a=i(6),n=i(4);Object(a.a)({_template:n.a`
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
`,is:"paper-item-body"})},187:function(t,e,i){"use strict";i(5),i(68),i(152);var a=i(6),n=i(4),s=i(125);const o=n.a`
  <style include="paper-spinner-styles"></style>

  <div id="spinnerContainer" class-name="[[__computeContainerClasses(active, __coolingDown)]]" on-animationend="__reset" on-webkit-animation-end="__reset">
    <div class="spinner-layer layer-1">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-2">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-3">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-4">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>
  </div>
`;o.setAttribute("strip-whitespace",""),Object(a.a)({_template:o,is:"paper-spinner",behaviors:[s.a]})},193:function(t,e,i){"use strict";var a={},n=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,s="[^\\s]+",o=/\[([^]*?)\]/gm,r=function(){};function c(t,e){for(var i=[],a=0,n=t.length;a<n;a++)i.push(t[a].substr(0,e));return i}function l(t){return function(e,i,a){var n=a[t].indexOf(i.charAt(0).toUpperCase()+i.substr(1).toLowerCase());~n&&(e.month=n)}}function d(t,e){for(t=String(t),e=e||2;t.length<e;)t="0"+t;return t}var h=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],p=["January","February","March","April","May","June","July","August","September","October","November","December"],u=c(p,3),m=c(h,3);a.i18n={dayNamesShort:m,dayNames:h,monthNamesShort:u,monthNames:p,amPm:["am","pm"],DoFn:function(t){return t+["th","st","nd","rd"][t%10>3?0:(t-t%10!=10)*t%10]}};var f={D:function(t){return t.getDate()},DD:function(t){return d(t.getDate())},Do:function(t,e){return e.DoFn(t.getDate())},d:function(t){return t.getDay()},dd:function(t){return d(t.getDay())},ddd:function(t,e){return e.dayNamesShort[t.getDay()]},dddd:function(t,e){return e.dayNames[t.getDay()]},M:function(t){return t.getMonth()+1},MM:function(t){return d(t.getMonth()+1)},MMM:function(t,e){return e.monthNamesShort[t.getMonth()]},MMMM:function(t,e){return e.monthNames[t.getMonth()]},YY:function(t){return d(String(t.getFullYear()),4).substr(2)},YYYY:function(t){return d(t.getFullYear(),4)},h:function(t){return t.getHours()%12||12},hh:function(t){return d(t.getHours()%12||12)},H:function(t){return t.getHours()},HH:function(t){return d(t.getHours())},m:function(t){return t.getMinutes()},mm:function(t){return d(t.getMinutes())},s:function(t){return t.getSeconds()},ss:function(t){return d(t.getSeconds())},S:function(t){return Math.round(t.getMilliseconds()/100)},SS:function(t){return d(Math.round(t.getMilliseconds()/10),2)},SSS:function(t){return d(t.getMilliseconds(),3)},a:function(t,e){return t.getHours()<12?e.amPm[0]:e.amPm[1]},A:function(t,e){return t.getHours()<12?e.amPm[0].toUpperCase():e.amPm[1].toUpperCase()},ZZ:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+d(100*Math.floor(Math.abs(e)/60)+Math.abs(e)%60,4)}},g={D:["\\d\\d?",function(t,e){t.day=e}],Do:["\\d\\d?"+s,function(t,e){t.day=parseInt(e,10)}],M:["\\d\\d?",function(t,e){t.month=e-1}],YY:["\\d\\d?",function(t,e){var i=+(""+(new Date).getFullYear()).substr(0,2);t.year=""+(e>68?i-1:i)+e}],h:["\\d\\d?",function(t,e){t.hour=e}],m:["\\d\\d?",function(t,e){t.minute=e}],s:["\\d\\d?",function(t,e){t.second=e}],YYYY:["\\d{4}",function(t,e){t.year=e}],S:["\\d",function(t,e){t.millisecond=100*e}],SS:["\\d{2}",function(t,e){t.millisecond=10*e}],SSS:["\\d{3}",function(t,e){t.millisecond=e}],d:["\\d\\d?",r],ddd:[s,r],MMM:[s,l("monthNamesShort")],MMMM:[s,l("monthNames")],a:[s,function(t,e,i){var a=e.toLowerCase();a===i.amPm[0]?t.isPm=!1:a===i.amPm[1]&&(t.isPm=!0)}],ZZ:["[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z",function(t,e){var i,a=(e+"").match(/([+-]|\d\d)/gi);a&&(i=60*a[1]+parseInt(a[2],10),t.timezoneOffset="+"===a[0]?i:-i)}]};g.dd=g.d,g.dddd=g.ddd,g.DD=g.D,g.mm=g.m,g.hh=g.H=g.HH=g.h,g.MM=g.M,g.ss=g.s,g.A=g.a,a.masks={default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"},a.format=function(t,e,i){var s=i||a.i18n;if("number"==typeof t&&(t=new Date(t)),"[object Date]"!==Object.prototype.toString.call(t)||isNaN(t.getTime()))throw new Error("Invalid Date in fecha.format");e=a.masks[e]||e||a.masks.default;var r=[];return(e=(e=e.replace(o,function(t,e){return r.push(e),"??"})).replace(n,function(e){return e in f?f[e](t,s):e.slice(1,e.length-1)})).replace(/\?\?/g,function(){return r.shift()})},a.parse=function(t,e,i){var s=i||a.i18n;if("string"!=typeof e)throw new Error("Invalid format in fecha.parse");if(e=a.masks[e]||e,t.length>1e3)return null;var o,r={},c=[],l=(o=e,o.replace(/[|\\{()[^$+*?.-]/g,"\\$&")).replace(n,function(t){if(g[t]){var e=g[t];return c.push(e[1]),"("+e[0]+")"}return t}),d=t.match(new RegExp(l,"i"));if(!d)return null;for(var h=1;h<d.length;h++)c[h-1](r,d[h],s);var p,u=new Date;return!0===r.isPm&&null!=r.hour&&12!=+r.hour?r.hour=+r.hour+12:!1===r.isPm&&12==+r.hour&&(r.hour=0),null!=r.timezoneOffset?(r.minute=+(r.minute||0)-+r.timezoneOffset,p=new Date(Date.UTC(r.year||u.getFullYear(),r.month||0,r.day||1,r.hour||0,r.minute||0,r.second||0,r.millisecond||0))):p=new Date(r.year||u.getFullYear(),r.month||0,r.day||1,r.hour||0,r.minute||0,r.second||0,r.millisecond||0),p},e.a=a},197:function(t,e,i){"use strict";i.d(e,"a",function(){return a});const a=(t,e,i=!1)=>{let a;return function(...n){const s=this,o=i&&!a;clearTimeout(a),a=setTimeout(()=>{a=null,i||t.apply(s,n)},e),o&&t.apply(s,n)}}},199:function(t,e,i){"use strict";var a=i(193);e.a=function(){try{(new Date).toLocaleString("i")}catch(t){return"RangeError"===t.name}return!1}()?(t,e)=>t.toLocaleString(e,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit"}):t=>a.a.format(t,"haDateTime")},201:function(t,e,i){"use strict";i.d(e,"b",function(){return a}),i.d(e,"a",function(){return n});const a=(t,e)=>t<e?-1:t>e?1:0,n=(t,e)=>a(t.toLowerCase(),e.toLowerCase())},213:function(t,e,i){"use strict";var a=i(193);e.a=function(){try{(new Date).toLocaleTimeString("i")}catch(t){return"RangeError"===t.name}return!1}()?(t,e)=>t.toLocaleTimeString(e,{hour:"numeric",minute:"2-digit"}):t=>a.a.format(t,"shortTime")},217:function(t,e,i){"use strict";i(109);var a=i(179);customElements.define("ha-icon-next",class extends a.a{connectedCallback(){super.connectedCallback(),setTimeout(()=>{this.icon="ltr"===window.getComputedStyle(this).direction?"hass:chevron-right":"hass:chevron-left"},100)}})},257:function(t,e,i){"use strict";i(187);var a=i(4),n=i(30),s=i(22),o=i(98),r=(i(108),i(12)),c=i(72),l=i(213);let d=null;customElements.define("ha-chart-base",class extends(Object(c.b)([o.a],n.a)){static get template(){return a.a`
      <style>
        :host {
          display: block;
        }
        .chartHeader {
          padding: 6px 0 0 0;
          width: 100%;
          display: flex;
          flex-direction: row;
        }
        .chartHeader > div {
          vertical-align: top;
          padding: 0 8px;
        }
        .chartHeader > div.chartTitle {
          padding-top: 8px;
          flex: 0 0 0;
          max-width: 30%;
        }
        .chartHeader > div.chartLegend {
          flex: 1 1;
          min-width: 70%;
        }
        :root {
          user-select: none;
          -moz-user-select: none;
          -webkit-user-select: none;
          -ms-user-select: none;
        }
        .chartTooltip {
          font-size: 90%;
          opacity: 1;
          position: absolute;
          background: rgba(80, 80, 80, 0.9);
          color: white;
          border-radius: 3px;
          pointer-events: none;
          transform: translate(-50%, 12px);
          z-index: 1000;
          width: 200px;
          transition: opacity 0.15s ease-in-out;
        }
        :host([rtl]) .chartTooltip {
          direction: rtl;
        }
        .chartLegend ul,
        .chartTooltip ul {
          display: inline-block;
          padding: 0 0px;
          margin: 5px 0 0 0;
          width: 100%;
        }
        .chartTooltip li {
          display: block;
          white-space: pre-line;
        }
        .chartTooltip .title {
          text-align: center;
          font-weight: 500;
        }
        .chartLegend li {
          display: inline-block;
          padding: 0 6px;
          max-width: 49%;
          text-overflow: ellipsis;
          white-space: nowrap;
          overflow: hidden;
          box-sizing: border-box;
        }
        .chartLegend li:nth-child(odd):last-of-type {
          /* Make last item take full width if it is odd-numbered. */
          max-width: 100%;
        }
        .chartLegend li[data-hidden] {
          text-decoration: line-through;
        }
        .chartLegend em,
        .chartTooltip em {
          border-radius: 5px;
          display: inline-block;
          height: 10px;
          margin-right: 4px;
          width: 10px;
        }
        :host([rtl]) .chartTooltip em {
          margin-right: inherit;
          margin-left: 4px;
        }
        paper-icon-button {
          color: var(--secondary-text-color);
        }
      </style>
      <template is="dom-if" if="[[unit]]">
        <div class="chartHeader">
          <div class="chartTitle">[[unit]]</div>
          <div class="chartLegend">
            <ul>
              <template is="dom-repeat" items="[[metas]]">
                <li on-click="_legendClick" data-hidden$="[[item.hidden]]">
                  <em style$="background-color:[[item.bgColor]]"></em>
                  [[item.label]]
                </li>
              </template>
            </ul>
          </div>
        </div>
      </template>
      <div id="chartTarget" style="height:40px; width:100%">
        <canvas id="chartCanvas"></canvas>
        <div
          class$="chartTooltip [[tooltip.yAlign]]"
          style$="opacity:[[tooltip.opacity]]; top:[[tooltip.top]]; left:[[tooltip.left]]; padding:[[tooltip.yPadding]]px [[tooltip.xPadding]]px"
        >
          <div class="title">[[tooltip.title]]</div>
          <div>
            <ul>
              <template is="dom-repeat" items="[[tooltip.lines]]">
                <li>
                  <em style$="background-color:[[item.bgColor]]"></em
                  >[[item.text]]
                </li>
              </template>
            </ul>
          </div>
        </div>
      </div>
    `}get chart(){return this._chart}static get properties(){return{data:Object,identifier:String,rendered:{type:Boolean,notify:!0,value:!1,readOnly:!0},metas:{type:Array,value:()=>[]},tooltip:{type:Object,value:()=>({opacity:"0",left:"0",top:"0",xPadding:"5",yPadding:"3"})},unit:Object,rtl:{type:Boolean,reflectToAttribute:!0}}}static get observers(){return["onPropsChange(data)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.onPropsChange(),this._resizeListener=(()=>{this._debouncer=s.a.debounce(this._debouncer,r.d.after(10),()=>{this._isAttached&&this.resizeChart()})}),"function"==typeof ResizeObserver?(this.resizeObserver=new ResizeObserver(t=>{t.forEach(()=>{this._resizeListener()})}),this.resizeObserver.observe(this.$.chartTarget)):this.addEventListener("iron-resize",this._resizeListener),null===d&&(d=Promise.all([i.e(11),i.e(147),i.e(75)]).then(i.bind(null,715))),d.then(t=>{this.ChartClass=t.default,this.onPropsChange()})}disconnectedCallback(){super.disconnectedCallback(),this._isAttached=!1,this.resizeObserver&&this.resizeObserver.unobserve(this.$.chartTarget),this.removeEventListener("iron-resize",this._resizeListener),void 0!==this._resizeTimer&&(clearInterval(this._resizeTimer),this._resizeTimer=void 0)}onPropsChange(){this._isAttached&&this.ChartClass&&this.data&&this.drawChart()}_customTooltips(t){if(0===t.opacity)return void this.set(["tooltip","opacity"],0);t.yAlign?this.set(["tooltip","yAlign"],t.yAlign):this.set(["tooltip","yAlign"],"no-transform");const e=t.title&&t.title[0]||"";this.set(["tooltip","title"],e);const i=t.body.map(t=>t.lines);t.body&&this.set(["tooltip","lines"],i.map((e,i)=>{const a=t.labelColors[i];return{color:a.borderColor,bgColor:a.backgroundColor,text:e.join("\n")}}));const a=this.$.chartTarget.clientWidth;let n=t.caretX;const s=this._chart.canvas.offsetTop+t.caretY;t.caretX+100>a?n=a-100:t.caretX<100&&(n=100),n+=this._chart.canvas.offsetLeft,this.tooltip={...this.tooltip,opacity:1,left:`${n}px`,top:`${s}px`}}_legendClick(t){(t=t||window.event).stopPropagation();let e=t.target||t.srcElement;for(;"LI"!==e.nodeName;)e=e.parentElement;const i=t.model.itemsIndex,a=this._chart.getDatasetMeta(i);a.hidden=null===a.hidden?!this._chart.data.datasets[i].hidden:null,this.set(["metas",i,"hidden"],this._chart.isDatasetVisible(i)?null:"hidden"),this._chart.update()}_drawLegend(){const t=this._chart,e=this._oldIdentifier&&this.identifier===this._oldIdentifier;this._oldIdentifier=this.identifier,this.set("metas",this._chart.data.datasets.map((i,a)=>({label:i.label,color:i.color,bgColor:i.backgroundColor,hidden:e&&a<this.metas.length?this.metas[a].hidden:!t.isDatasetVisible(a)})));let i=!1;if(e)for(let a=0;a<this.metas.length;a++){const e=t.getDatasetMeta(a);!!e.hidden!=!!this.metas[a].hidden&&(i=!0),e.hidden=!!this.metas[a].hidden||null}i&&t.update(),this.unit=this.data.unit}_formatTickValue(t,e,i){if(0===i.length)return t;const a=new Date(i[e].value);return Object(l.a)(a)}drawChart(){const t=this.data.data,e=this.$.chartCanvas;if(t.datasets&&t.datasets.length||this._chart){if("timeline"!==this.data.type&&t.datasets.length>0){const e=t.datasets.length,i=this.constructor.getColorList(e);for(let a=0;a<e;a++)t.datasets[a].borderColor=i[a].rgbString(),t.datasets[a].backgroundColor=i[a].alpha(.6).rgbaString()}if(this._chart)this._customTooltips({opacity:0}),this._chart.data=t,this._chart.update({duration:0}),this.isTimeline?this._chart.options.scales.yAxes[0].gridLines.display=t.length>1:!0===this.data.legend&&this._drawLegend(),this.resizeChart();else{if(!t.datasets)return;this._customTooltips({opacity:0});const i=[{afterRender:()=>this._setRendered(!0)}];let a={responsive:!0,maintainAspectRatio:!1,animation:{duration:0},hover:{animationDuration:0},responsiveAnimationDuration:0,tooltips:{enabled:!1,custom:this._customTooltips.bind(this)},legend:{display:!1},line:{spanGaps:!0},elements:{font:"12px 'Roboto', 'sans-serif'"},ticks:{fontFamily:"'Roboto', 'sans-serif'"}};(a=Chart.helpers.merge(a,this.data.options)).scales.xAxes[0].ticks.callback=this._formatTickValue,"timeline"===this.data.type?(this.set("isTimeline",!0),void 0!==this.data.colors&&(this._colorFunc=this.constructor.getColorGenerator(this.data.colors.staticColors,this.data.colors.staticColorIndex)),void 0!==this._colorFunc&&(a.elements.colorFunction=this._colorFunc),1===t.datasets.length&&(a.scales.yAxes[0].ticks?a.scales.yAxes[0].ticks.display=!1:a.scales.yAxes[0].ticks={display:!1},a.scales.yAxes[0].gridLines?a.scales.yAxes[0].gridLines.display=!1:a.scales.yAxes[0].gridLines={display:!1}),this.$.chartTarget.style.height="50px"):this.$.chartTarget.style.height="160px";const n={type:this.data.type,data:this.data.data,options:a,plugins:i};this._chart=new this.ChartClass(e,n),!0!==this.isTimeline&&!0===this.data.legend&&this._drawLegend(),this.resizeChart()}}}resizeChart(){this._chart&&(void 0!==this._resizeTimer?(clearInterval(this._resizeTimer),this._resizeTimer=void 0,this._resizeChart()):this._resizeTimer=setInterval(this.resizeChart.bind(this),10))}_resizeChart(){const t=this.$.chartTarget,e=this.data.data;if(0===e.datasets.length)return;if(!this.isTimeline)return void this._chart.resize();const i=this._chart.chartArea.top,a=this._chart.chartArea.bottom,n=this._chart.canvas.clientHeight;if(a>0&&(this._axisHeight=n-a+i),!this._axisHeight)return t.style.height="50px",this._chart.resize(),void this.resizeChart();if(this._axisHeight){const i=30*e.datasets.length+this._axisHeight+"px";t.style.height!==i&&(t.style.height=i),this._chart.resize()}}static getColorList(t){let e=!1;t>10&&(e=!0,t=Math.ceil(t/2));const i=360/t,a=[];for(let n=0;n<t;n++)a[n]=Color().hsl(i*n,80,38),e&&(a[n+t]=Color().hsl(i*n,80,62));return a}static getColorGenerator(t,e){const i=["ff0029","66a61e","377eb8","984ea3","00d2d5","ff7f00","af8d00","7f80cd","b3e900","c42e60","a65628","f781bf","8dd3c7","bebada","fb8072","80b1d3","fdb462","fccde5","bc80bd","ffed6f","c4eaff","cf8c00","1b9e77","d95f02","e7298a","e6ab02","a6761d","0097ff","00d067","f43600","4ba93b","5779bb","927acc","97ee3f","bf3947","9f5b00","f48758","8caed6","f2b94f","eff26e","e43872","d9b100","9d7a00","698cff","d9d9d9","00d27e","d06800","009f82","c49200","cbe8ff","fecddf","c27eb6","8cd2ce","c4b8d9","f883b0","a49100","f48800","27d0df","a04a9b"];function a(t){return Color("#"+i[t%i.length])}const n={};let s=0;return e>0&&(s=e),t&&Object.keys(t).forEach(e=>{const i=t[e];isFinite(i)?n[e.toLowerCase()]=a(i):n[e.toLowerCase()]=Color(t[e])}),function(t,e){let i;const o=e[3];if(null===o)return Color().hsl(0,40,38);if(void 0===o)return Color().hsl(120,40,38);const r=o.toLowerCase();return void 0===i&&(i=n[r]),void 0===i&&(i=a(s),s++,n[r]=i),i}}});var h=i(175),p=i(199);customElements.define("state-history-chart-line",class extends(Object(h.a)(n.a)){static get template(){return a.a`
      <style>
        :host {
          display: block;
          overflow: hidden;
          height: 0;
          transition: height 0.3s ease-in-out;
        }
      </style>
      <ha-chart-base
        id="chart"
        data="[[chartData]]"
        identifier="[[identifier]]"
        rendered="{{rendered}}"
      ></ha-chart-base>
    `}static get properties(){return{chartData:Object,data:Object,names:Object,unit:String,identifier:String,isSingleDevice:{type:Boolean,value:!1},endTime:Object,rendered:{type:Boolean,value:!1,observer:"_onRenderedChanged"}}}static get observers(){return["dataChanged(data, endTime, isSingleDevice)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.drawChart()}dataChanged(){this.drawChart()}_onRenderedChanged(t){t&&this.animateHeight()}animateHeight(){requestAnimationFrame(()=>requestAnimationFrame(()=>{this.style.height=this.$.chart.scrollHeight+"px"}))}drawChart(){const t=this.unit,e=this.data,i=[];let a;if(!this._isAttached)return;if(0===e.length)return;function n(t){const e=parseFloat(t);return isFinite(e)?e:null}(a=this.endTime||new Date(Math.max.apply(null,e.map(t=>new Date(t.states[t.states.length-1].last_changed)))))>new Date&&(a=new Date);const s=this.names||{};e.forEach(e=>{const o=e.domain,r=s[e.entity_id]||e.name;let c;const l=[];function d(t,e){e&&(t>a||(l.forEach((i,a)=>{i.data.push({x:t,y:e[a]})}),c=e))}function h(e,i,a){let n=!1,s=!1;a&&(n="origin"),i&&(s="before"),l.push({label:e,fill:n,steppedLine:s,pointRadius:0,data:[],unitText:t})}if("thermostat"===o||"climate"===o||"water_heater"===o){const t=e.states.some(t=>t.attributes&&t.attributes.hvac_action),i="climate"===o&&t?t=>"heating"===t.attributes.hvac_action:t=>"heat"===t.state,a="climate"===o&&t?t=>"cooling"===t.attributes.hvac_action:t=>"cool"===t.state,s=e.states.some(i),c=e.states.some(a),l=e.states.some(t=>t.attributes&&t.attributes.target_temp_high!==t.attributes.target_temp_low);h(r+" current temperature",!0),s&&h(r+" heating",!0,!0),c&&h(r+" cooling",!0,!0),l?(h(r+" target temperature high",!0),h(r+" target temperature low",!0)):h(r+" target temperature",!0),e.states.forEach(t=>{if(!t.attributes)return;const e=n(t.attributes.current_temperature),o=[e];if(s&&o.push(i(t)?e:null),c&&o.push(a(t)?e:null),l){const e=n(t.attributes.target_temp_high),i=n(t.attributes.target_temp_low);o.push(e,i),d(new Date(t.last_changed),o)}else{const e=n(t.attributes.temperature);o.push(e),d(new Date(t.last_changed),o)}})}else{h(r,"sensor"===o);let t=null,i=null,a=null;e.states.forEach(e=>{const s=n(e.state),o=new Date(e.last_changed);if(null!==s&&null!==a){const e=o.getTime(),n=a.getTime(),r=i.getTime();d(a,[(n-r)/(e-r)*(s-t)+t]),d(new Date(n+1),[null]),d(o,[s]),i=o,t=s,a=null}else null!==s&&null===a?(d(o,[s]),i=o,t=s):null===s&&null===a&&null!==t&&(a=o)})}d(a,c),Array.prototype.push.apply(i,l)});const o={type:"line",unit:t,legend:!this.isSingleDevice,options:{scales:{xAxes:[{type:"time",ticks:{major:{fontStyle:"bold"}}}],yAxes:[{ticks:{maxTicksLimit:7}}]},tooltips:{mode:"neareach",callbacks:{title:(t,e)=>{const i=t[0],a=e.datasets[i.datasetIndex].data[i.index].x;return Object(p.a)(a,this.hass.language)}}},hover:{mode:"neareach"},layout:{padding:{top:5}},elements:{line:{tension:.1,pointRadius:0,borderWidth:1.5},point:{hitRadius:5}},plugins:{filler:{propagate:!0}}},data:{labels:[],datasets:i}};this.chartData=o}});var u=i(96);customElements.define("state-history-chart-timeline",class extends(Object(h.a)(n.a)){static get template(){return a.a`
      <style>
        :host {
          display: block;
          opacity: 0;
          transition: opacity 0.3s ease-in-out;
        }
        :host([rendered]) {
          opacity: 1;
        }

        ha-chart-base {
          direction: ltr;
        }
      </style>
      <ha-chart-base
        data="[[chartData]]"
        rendered="{{rendered}}"
        rtl="{{rtl}}"
      ></ha-chart-base>
    `}static get properties(){return{hass:{type:Object},chartData:Object,data:{type:Object,observer:"dataChanged"},names:Object,noSingle:Boolean,endTime:Date,rendered:{type:Boolean,value:!1,reflectToAttribute:!0},rtl:{reflectToAttribute:!0,computed:"_computeRTL(hass)"}}}static get observers(){return["dataChanged(data, endTime, localize, language)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.drawChart()}dataChanged(){this.drawChart()}drawChart(){let t=this.data;if(!this._isAttached)return;t||(t=[]);const e=new Date(t.reduce((t,e)=>Math.min(t,new Date(e.data[0].last_changed)),new Date));let i=this.endTime||new Date(t.reduce((t,e)=>Math.max(t,new Date(e.data[e.data.length-1].last_changed)),e));i>new Date&&(i=new Date);const a=[],n=[],s=this.names||{};t.forEach(t=>{let o,r=null,c=null,l=e;const d=s[t.entity_id]||t.name,h=[];t.data.forEach(t=>{let e=t.state;void 0!==e&&""!==e||(e=null),new Date(t.last_changed)>i||(null!==r&&e!==r?(o=new Date(t.last_changed),h.push([l,o,c,r]),r=e,c=t.state_localize,l=o):null===r&&(r=e,c=t.state_localize,l=new Date(t.last_changed)))}),null!==r&&h.push([l,i,c,r]),n.push({data:h}),a.push(d)});const o={type:"timeline",options:{tooltips:{callbacks:{label:(t,e)=>{const i=e.datasets[t.datasetIndex].data[t.index],a=Object(p.a)(i[0],this.hass.language),n=Object(p.a)(i[1],this.hass.language);return[i[2],a,n]}}},scales:{xAxes:[{ticks:{major:{fontStyle:"bold"}}}],yAxes:[{afterSetDimensions:t=>{t.maxWidth=.18*t.chart.width},position:this._computeRTL?"right":"left"}]}},data:{labels:a,datasets:n},colors:{staticColors:{on:1,off:0,unavailable:"#a0a0a0",unknown:"#606060",idle:2},staticColorIndex:3}};this.chartData=o}_computeRTL(t){return Object(u.a)(t)}});customElements.define("state-history-charts",class extends(Object(h.a)(n.a)){static get template(){return a.a`
      <style>
        :host {
          display: block;
          /* height of single timeline chart = 58px */
          min-height: 58px;
        }
        .info {
          text-align: center;
          line-height: 58px;
          color: var(--secondary-text-color);
        }
      </style>
      <template
        is="dom-if"
        class="info"
        if="[[_computeIsLoading(isLoadingData)]]"
      >
        <div class="info">
          [[localize('ui.components.history_charts.loading_history')]]
        </div>
      </template>

      <template
        is="dom-if"
        class="info"
        if="[[_computeIsEmpty(isLoadingData, historyData)]]"
      >
        <div class="info">
          [[localize('ui.components.history_charts.no_history_found')]]
        </div>
      </template>

      <template is="dom-if" if="[[historyData.timeline.length]]">
        <state-history-chart-timeline
          hass="[[hass]]"
          data="[[historyData.timeline]]"
          end-time="[[_computeEndTime(endTime, upToNow, historyData)]]"
          no-single="[[noSingle]]"
          names="[[names]]"
        ></state-history-chart-timeline>
      </template>

      <template is="dom-repeat" items="[[historyData.line]]">
        <state-history-chart-line
          hass="[[hass]]"
          unit="[[item.unit]]"
          data="[[item.data]]"
          identifier="[[item.identifier]]"
          is-single-device="[[_computeIsSingleLineChart(item.data, noSingle)]]"
          end-time="[[_computeEndTime(endTime, upToNow, historyData)]]"
          names="[[names]]"
        ></state-history-chart-line>
      </template>
    `}static get properties(){return{hass:Object,historyData:{type:Object,value:null},names:Object,isLoadingData:Boolean,endTime:{type:Object},upToNow:Boolean,noSingle:Boolean}}_computeIsSingleLineChart(t,e){return!e&&t&&1===t.length}_computeIsEmpty(t,e){const i=!e||!e.timeline||!e.line||0===e.timeline.length&&0===e.line.length;return!t&&i}_computeIsLoading(t){return t&&!this.historyData}_computeEndTime(t,e){return e?new Date:t}})},263:function(t,e,i){"use strict";var a=i(3),n=(i(109),i(182),i(143),i(177),i(217),i(0));const s=[{page:"ais_dom_config_update",caption:"Oprogramowanie bramki",description:"Aktualizacja systemu i synchronizacja bramki z Portalem Integratora"},{page:"ais_dom_config_wifi",caption:"Sieć WiFi",description:"Ustawienia połączenia z siecią WiFi"},{page:"ais_dom_config_display",caption:"Ekran",description:"Ustawienia ekranu"},{page:"ais_dom_config_tts",caption:"Głos asystenta",description:"Ustawienia głosu asystenta"},{page:"ais_dom_config_night",caption:"Tryb nocny",description:"Ustawienie godzin, w których asystent ma działać ciszej"},{page:"ais_dom_config_remote",caption:"Zdalny dostęp",description:"Konfiguracja zdalnego dostępu do bramki"},{page:"ais_dom_config_power",caption:"Zatrzymanie bramki",description:"Restart lub wyłączenie bramki"}];let o=class extends n.a{render(){return n.f`
      <ha-card>
        ${s.map(({page:t,caption:e,description:i})=>n.f`
              <a href=${`/config/${t}`}>
                <paper-item>
                  <paper-item-body two-line=""
                    >${`${e}`}
                    <div secondary>${`${i}`}</div>
                  </paper-item-body>
                  <ha-icon-next></ha-icon-next>
                </paper-item>
              </a>
            `)}
      </ha-card>
    `}static get styles(){return n.c`
      a {
        text-decoration: none;
        color: var(--primary-text-color);
      }
    `}};Object(a.c)([Object(n.g)()],o.prototype,"hass",void 0),Object(a.c)([Object(n.g)()],o.prototype,"showAdvanced",void 0),o=Object(a.c)([Object(n.d)("ha-config-ais-dom-navigation")],o)},283:function(t,e,i){"use strict";i.d(e,"a",function(){return s}),i.d(e,"c",function(){return o}),i.d(e,"f",function(){return r}),i.d(e,"b",function(){return c}),i.d(e,"d",function(){return l}),i.d(e,"e",function(){return p}),i.d(e,"h",function(){return u}),i.d(e,"g",function(){return m});var a=i(197),n=i(13);const s=(t,e)=>t.callApi("POST","config/config_entries/flow",{handler:e}),o=(t,e)=>t.callApi("GET",`config/config_entries/flow/${e}`),r=(t,e,i)=>t.callApi("POST",`config/config_entries/flow/${e}`,i),c=(t,e)=>t.callApi("DELETE",`config/config_entries/flow/${e}`),l=t=>t.callApi("GET","config/config_entries/flow_handlers"),d=t=>t.sendMessagePromise({type:"config_entries/flow/progress"}),h=(t,e)=>t.subscribeEvents(Object(a.a)(()=>d(t).then(t=>e.setState(t,!0)),500,!0),"config_entry_discovered"),p=t=>Object(n.h)(t,"_configFlowProgress",d,h),u=(t,e)=>p(t.connection).subscribe(e),m=(t,e)=>{const i=e.context.title_placeholders||{},a=Object.keys(i);if(0===a.length)return t(`component.${e.handler}.config.title`);const n=[];return a.forEach(t=>{n.push(t),n.push(i[t])}),t(`component.${e.handler}.config.flow_title`,...n)}},301:function(t,e,i){"use strict";i.d(e,"b",function(){return n}),i.d(e,"a",function(){return s});const a=/^(\w+)\.(\w+)$/,n=t=>a.test(t),s=t=>t.toLowerCase().replace(/\s|\'/g,"_").replace(/\W/g,"").replace(/_{2,}/g,"_").replace(/_$/,"")},303:function(t,e,i){"use strict";i.d(e,"a",function(){return n}),i.d(e,"b",function(){return s});var a=i(18);const n=()=>Promise.all([i.e(0),i.e(1),i.e(2),i.e(6),i.e(33)]).then(i.bind(null,385)),s=(t,e,i)=>{Object(a.a)(t,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:n,dialogParams:Object.assign(Object.assign({},e),{flowConfig:i})})}},311:function(t,e,i){"use strict";i.d(e,"a",function(){return n});var a=i(301);const n=t=>{if(!t||!Array.isArray(t))throw new Error("Entities need to be an array");return t.map((t,e)=>{if("object"==typeof t&&!Array.isArray(t)&&t.type)return t;let i;if("string"==typeof t)i={entity:t};else{if("object"!=typeof t||Array.isArray(t))throw new Error(`Invalid entity specified at position ${e}.`);if(!t.entity)throw new Error(`Entity object at position ${e} is missing entity field.`);i=t}if(!Object(a.b)(i.entity))throw new Error(`Invalid entity ID at position ${e}: ${i.entity}`);return i})}},313:function(t,e,i){"use strict";i.d(e,"a",function(){return c}),i.d(e,"b",function(){return l});var a=i(283),n=i(0),s=i(58),o=i(303),r=i(201);const c=o.a,l=(t,e)=>Object(o.b)(t,e,{loadDevicesAndAreas:!0,getFlowHandlers:t=>Object(a.d)(t).then(e=>e.sort((e,i)=>Object(r.a)(t.localize(`component.${e}.config.title`),t.localize(`component.${i}.config.title`)))),createFlow:a.a,fetchFlow:a.c,handleFlowStep:a.f,deleteFlow:a.b,renderAbortDescription(t,e){const i=Object(s.b)(t.localize,`component.${e.handler}.config.abort.${e.reason}`,e.description_placeholders);return i?n.f`
            <ha-markdown allowsvg .content=${i}></ha-markdown>
          `:""},renderShowFormStepHeader:(t,e)=>t.localize(`component.${e.handler}.config.step.${e.step_id}.title`),renderShowFormStepDescription(t,e){const i=Object(s.b)(t.localize,`component.${e.handler}.config.step.${e.step_id}.description`,e.description_placeholders);return i?n.f`
            <ha-markdown allowsvg .content=${i}></ha-markdown>
          `:""},renderShowFormStepFieldLabel:(t,e,i)=>t.localize(`component.${e.handler}.config.step.${e.step_id}.data.${i.name}`),renderShowFormStepFieldError:(t,e,i)=>t.localize(`component.${e.handler}.config.error.${i}`),renderExternalStepHeader:(t,e)=>t.localize(`component.${e.handler}.config.step.${e.step_id}.title`),renderExternalStepDescription(t,e){const i=Object(s.b)(t.localize,`component.${e.handler}.config.${e.step_id}.description`,e.description_placeholders);return n.f`
        <p>
          ${t.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${i?n.f`
              <ha-markdown allowsvg .content=${i}></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(t,e){const i=Object(s.b)(t.localize,`component.${e.handler}.config.create_entry.${e.description||"default"}`,e.description_placeholders);return n.f`
        ${i?n.f`
              <ha-markdown allowsvg .content=${i}></ha-markdown>
            `:""}
        <p>Created config for ${e.title}.</p>
      `}})},699:function(t,e,i){"use strict";i.r(e);i(511),i(218),i(150),i(108);var a=i(4),n=i(30),s=(i(151),i(95),i(263),i(313)),o=i(18),r=(i(257),i(311));customElements.define("ha-config-ais-dom-config-wifi",class extends n.a{static get template(){return a.a`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 32px;
        }
        .border {
          margin: 32px auto 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.12);
          max-width: 1040px;
        }
        .narrow .border {
          max-width: 640px;
        }
        div.aisInfoRow {
          display: inline-block;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Połączenie WiFi</span>
            <span slot="introduction"
              >Możesz sprawdzić lub skonfigurować parametry połączenia
              WiFi</span
            >
            <ha-card header="Parametry sieci">
              <div class="card-content" style="display: flex;">
                <div style="text-align: center;">
                  <div class="aisInfoRow">Lokalna nazwa hosta</div>
                  <div class="aisInfoRow">
                    <mwc-button on-click="showLocalIpInfo"
                      >[[aisLocalHostName]]</mwc-button
                    ><paper-icon-button
                      class="user-button"
                      icon="hass:settings"
                      on-click="createFlowHostName"
                    ></paper-icon-button>
                  </div>
                </div>
                <div on-click="showLocalIpInfo" style="text-align: center;">
                  <div class="aisInfoRow">Lokalny adres IP</div>
                  <div class="aisInfoRow">
                    <mwc-button>[[aisLocalIP]]</mwc-button>
                  </div>
                </div>
                <div on-click="showWiFiSpeedInfo" style="text-align: center;">
                  <div class="aisInfoRow">Prędkość połączenia WiFi</div>
                  <div class="aisInfoRow">
                    <mwc-button>[[aisWiFiSpeed]]</mwc-button>
                  </div>
                </div>
              </div>
              <state-history-charts
                hass="[[hass]]"
                history-data="[[_stateHistory]]"
                is-loading-data="[[_stateHistoryLoading]]"
                names="[[_names]]"
                up-to-now
                no-single
              >
              </state-history-charts>
              <div class="card-actions">
                <div>
                  <paper-icon-button
                    class="user-button"
                    icon="hass:wifi"
                    on-click="showWiFiGroup"
                  ></paper-icon-button
                  ><mwc-button on-click="createFlowWifi"
                    >Konfigurator połączenia z siecą WiFi</mwc-button
                  >
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,showAdvanced:Boolean,aisLocalHostName:{type:String,computed:"_computeAisLocalHostName(hass)"},aisLocalIP:{type:String,computed:"_computeAisLocalIP(hass)"},aisWiFiSpeed:{type:String,computed:"_computeAisWiFiSpeed(hass)"},_config:Object,_names:Object,_entities:Array,_stateHistory:Object,_stateHistoryLoading:Boolean,_cacheConfig:Object}}computeClasses(t){return t?"content":"content narrow"}_computeAisLocalHostName(t){return t.states["sensor.local_host_name"].state}_computeAisLocalIP(t){return t.states["sensor.internal_ip_address"].state}_computeAisWiFiSpeed(t){return t.states["sensor.ais_wifi_service_current_network_info"].state}showWiFiGroup(){Object(o.a)(this,"hass-more-info",{entityId:"group.internet_status"})}showWiFiSpeedInfo(){Object(o.a)(this,"hass-more-info",{entityId:"sensor.ais_wifi_service_current_network_info"})}showLocalIpInfo(){Object(o.a)(this,"hass-more-info",{entityId:"sensor.internal_ip_address"})}_continueFlow(t){Object(s.b)(this,{continueFlowId:t,dialogClosedCallback:()=>{console.log("OK")}})}createFlowHostName(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_host"}).then(t=>{this._continueFlow(t.flow_id)})}createFlowWifi(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_wifi_service"}).then(t=>{console.log(t),this._continueFlow(t.flow_id)})}ready(){super.ready();const t=Object(r.a)(["sensor.ais_wifi_service_current_network_info"]);console.log(t);const e=[],i={};for(const a of t)e.push(a.entity),a.name&&(i[a.entity]=a.name);this.setProperties({_cacheConfig:{cacheKey:e.join(),hoursToShow:24,refresh:0},_entities:e,_names:i})}})}}]);
//# sourceMappingURL=chunk.6721f08a8903b8344791.js.map