/*! For license information please see chunk.81a55faaa60b7cb3f09e.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[87],{119:function(t,e,a){"use strict";a.d(e,"a",function(){return r});a(5);var o=a(55),n=a(35);const r=[o.a,n.a,{hostAttributes:{role:"option",tabindex:"0"}}]},143:function(t,e,a){"use strict";a(5),a(45),a(144);var o=a(6),n=a(4),r=a(119);Object(o.a)({_template:n.a`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[r.a]})},144:function(t,e,a){"use strict";a(45),a(68),a(42),a(54);const o=document.createElement("template");o.setAttribute("style","display: none;"),o.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(o.content)},175:function(t,e,a){"use strict";var o=a(9);e.a=Object(o.a)(t=>(class extends t{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(t){return t}}))},177:function(t,e,a){"use strict";var o=a(3),n=a(0);class r extends n.a{static get styles(){return n.c`
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
    `}}Object(o.c)([Object(n.g)()],r.prototype,"header",void 0),customElements.define("ha-card",r)},179:function(t,e,a){"use strict";a.d(e,"a",function(){return r});a(109);const o=customElements.get("iron-icon");let n=!1;class r extends o{listen(t,e,o){super.listen(t,e,o),n||"mdi"!==this._iconsetName||(n=!0,a.e(76).then(a.bind(null,210)))}}customElements.define("ha-icon",r)},182:function(t,e,a){"use strict";a(5),a(45),a(42),a(54);var o=a(6),n=a(4);Object(o.a)({_template:n.a`
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
`,is:"paper-item-body"})},217:function(t,e,a){"use strict";a(109);var o=a(179);customElements.define("ha-icon-next",class extends o.a{connectedCallback(){super.connectedCallback(),setTimeout(()=>{this.icon="ltr"===window.getComputedStyle(this).direction?"hass:chevron-right":"hass:chevron-left"},100)}})},263:function(t,e,a){"use strict";var o=a(3),n=(a(109),a(182),a(143),a(177),a(217),a(0));const r=[{page:"ais_dom_config_update",caption:"Oprogramowanie bramki",description:"Aktualizacja systemu i synchronizacja bramki z Portalem Integratora"},{page:"ais_dom_config_wifi",caption:"Sieć WiFi",description:"Ustawienia połączenia z siecią WiFi"},{page:"ais_dom_config_display",caption:"Ekran",description:"Ustawienia ekranu"},{page:"ais_dom_config_tts",caption:"Głos asystenta",description:"Ustawienia głosu asystenta"},{page:"ais_dom_config_night",caption:"Tryb nocny",description:"Ustawienie godzin, w których asystent ma działać ciszej"},{page:"ais_dom_config_remote",caption:"Zdalny dostęp",description:"Konfiguracja zdalnego dostępu do bramki"},{page:"ais_dom_config_power",caption:"Zatrzymanie bramki",description:"Restart lub wyłączenie bramki"}];let i=class extends n.a{render(){return n.f`
      <ha-card>
        ${r.map(({page:t,caption:e,description:a})=>n.f`
              <a href=${`/config/${t}`}>
                <paper-item>
                  <paper-item-body two-line=""
                    >${`${e}`}
                    <div secondary>${`${a}`}</div>
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
    `}};Object(o.c)([Object(n.g)()],i.prototype,"hass",void 0),Object(o.c)([Object(n.g)()],i.prototype,"showAdvanced",void 0),i=Object(o.c)([Object(n.d)("ha-config-ais-dom-navigation")],i)},700:function(t,e,a){"use strict";a.r(e);a(218),a(150),a(108);var o=a(4),n=a(30),r=(a(151),a(95),a(263),a(175));customElements.define("ha-config-ais-dom-config-display",class extends(Object(r.a)(n.a)){static get template(){return o.a`
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
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        .content {
          padding-bottom: 24px;
          direction: ltr;
        }
        .account-row {
          display: flex;
          padding: 0 16px;
        }
        mwc-button {
          align-self: center;
        }
        .soon {
          font-style: italic;
          margin-top: 24px;
          text-align: center;
        }
        .nowrap {
          white-space: nowrap;
        }
        .wrap {
          white-space: normal;
        }
        .status {
          text-transform: capitalize;
          padding: 16px;
        }
        a {
          color: var(--primary-color);
        }
        .buttons {
          position: relative;
          width: 200px;
          height: 200px;
        }

        .button {
          position: absolute;
          width: 50px;
          height: 50px;
        }

        .arrow {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
        }

        .arrow-up {
          border-left: 12px solid transparent;
          border-right: 12px solid transparent;
          border-bottom: 16px solid black;
        }

        .arrow-right {
          border-top: 12px solid transparent;
          border-bottom: 12px solid transparent;
          border-left: 16px solid black;
        }

        .arrow-left {
          border-top: 12px solid transparent;
          border-bottom: 12px solid transparent;
          border-right: 16px solid black;
        }

        .arrow-down {
          border-left: 12px solid transparent;
          border-right: 12px solid transparent;
          border-top: 16px solid black;
        }

        .down {
          bottom: 0;
          left: 75px;
        }

        .left {
          top: 75px;
          left: 0;
        }

        .right {
          top: 75px;
          right: 0;
        }

        .up {
          top: 0;
          left: 75px;
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Ustawienia ekranu</span>
            <span slot="introduction"
              >Jeżeli obraz na monitorze lub telewizorze podłączonym do bramki
              za pomocą złącza HDMI jest ucięty lub przesunięty, to w tym
              miejscu możesz dostosować obraz do rozmiaru ekranu.</span
            >
            <ha-card header="Dostosuj obraz do rozmiaru ekranu">
              <div class="card-content">
                <div class="card-content" style="text-align: center;">
                  <div style="display: inline-block;">
                    <p>Powiększanie</p>
                    <div
                      class="buttons"
                      style="margin: 0 auto; display: table; border:solid 1px;"
                    >
                      <button
                        class="button up"
                        data-value="top"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-up arrow"></span>
                      </button>
                      <button
                        class="button down"
                        data-value="bottom"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-down arrow"></span>
                      </button>
                      <button
                        class="button right"
                        data-value="right"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-right arrow"></span>
                      </button>
                      <button
                        class="button left"
                        data-value="left"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-left arrow"></span>
                      </button>
                    </div>
                  </div>
                  <div
                    style="text-align: center; display: inline-block; margin: 30px;"
                  >
                    <p>Zmniejszanie</p>
                    <div
                      class="buttons"
                      style="margin: 0 auto; display: table;"
                    >
                      <button
                        class="button up"
                        data-value="-top"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-down arrow"></span>
                      </button>
                      <div
                        style="margin: 0 auto; height: 98px; width:98px; margin-top: 50px; margin-left: 50px; display: flex; border:solid 1px;"
                      ></div>
                      <button
                        class="button down"
                        data-value="-bottom"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-up arrow"></span>
                      </button>
                      <button
                        class="button right"
                        data-value="-right"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-left arrow"></span>
                      </button>
                      <button
                        class="button left"
                        data-value="-left"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-right arrow"></span>
                      </button>
                    </div>
                  </div>
                </div>
                <div class="card-actions" style="margin-top: 30px;">
                  <div>
                    <paper-icon-button
                      class="user-button"
                      icon="mdi:restore"
                      on-click="wmRestoreSettings"
                    ></paper-icon-button
                    ><mwc-button on-click="wmOverscan" data-value="reset"
                      >Reset ekranu do ustawień domyślnych</mwc-button
                    >
                  </div>
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean}}ready(){super.ready()}wmOverscan(t){this.hass.callService("ais_shell_command","change_wm_overscan",{value:t.currentTarget.getAttribute("data-value")})}})}}]);
//# sourceMappingURL=chunk.81a55faaa60b7cb3f09e.js.map