(self.webpackJsonp=self.webpackJsonp||[]).push([[90],{177:function(e,t,o){"use strict";var a=o(3),i=o(0);class n extends i.a{static get styles(){return i.c`
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
    `}render(){return i.f`
      ${this.header?i.f`
            <div class="card-header">${this.header}</div>
          `:i.f``}
      <slot></slot>
    `}}Object(a.c)([Object(i.g)()],n.prototype,"header",void 0),customElements.define("ha-card",n)},179:function(e,t,o){"use strict";o.d(t,"a",function(){return n});o(109);const a=customElements.get("iron-icon");let i=!1;class n extends a{listen(e,t,a){super.listen(e,t,a),i||"mdi"!==this._iconsetName||(i=!0,o.e(76).then(o.bind(null,210)))}}customElements.define("ha-icon",n)},195:function(e,t,o){"use strict";var a=o(3),i=o(0),n=(o(222),o(206));const s=customElements.get("mwc-switch");let r=class extends s{firstUpdated(){super.firstUpdated(),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)"),this.classList.toggle("slotted",Boolean(this._slot.assignedNodes().length))}static get styles(){return[n.a,i.c`
        :host {
          display: flex;
          flex-direction: row;
          align-items: center;
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
          background-color: var(--paper-toggle-button-unchecked-button-color);
          border-color: var(--paper-toggle-button-unchecked-button-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
          background-color: var(--paper-toggle-button-unchecked-bar-color);
          border-color: var(--paper-toggle-button-unchecked-bar-color);
        }
        :host(.slotted) .mdc-switch {
          margin-right: 24px;
        }
      `]}};Object(a.c)([Object(i.h)("slot")],r.prototype,"_slot",void 0),r=Object(a.c)([Object(i.d)("ha-switch")],r)},217:function(e,t,o){"use strict";o(109);var a=o(179);customElements.define("ha-icon-next",class extends a.a{connectedCallback(){super.connectedCallback(),setTimeout(()=>{this.icon="ltr"===window.getComputedStyle(this).direction?"hass:chevron-right":"hass:chevron-left"},100)}})},263:function(e,t,o){"use strict";var a=o(3),i=(o(109),o(182),o(143),o(177),o(217),o(0));const n=[{page:"ais_dom_config_update",caption:"Oprogramowanie bramki",description:"Aktualizacja systemu i synchronizacja bramki z Portalem Integratora"},{page:"ais_dom_config_wifi",caption:"Sieć WiFi",description:"Ustawienia połączenia z siecią WiFi"},{page:"ais_dom_config_display",caption:"Ekran",description:"Ustawienia ekranu"},{page:"ais_dom_config_tts",caption:"Głos asystenta",description:"Ustawienia głosu asystenta"},{page:"ais_dom_config_night",caption:"Tryb nocny",description:"Ustawienie godzin, w których asystent ma działać ciszej"},{page:"ais_dom_config_remote",caption:"Zdalny dostęp",description:"Konfiguracja zdalnego dostępu do bramki"},{page:"ais_dom_config_power",caption:"Zatrzymanie bramki",description:"Restart lub wyłączenie bramki"}];let s=class extends i.a{render(){return i.f`
      <ha-card>
        ${n.map(({page:e,caption:t,description:o})=>i.f`
              <a href=${`/config/${e}`}>
                <paper-item>
                  <paper-item-body two-line=""
                    >${`${t}`}
                    <div secondary>${`${o}`}</div>
                  </paper-item-body>
                  <ha-icon-next></ha-icon-next>
                </paper-item>
              </a>
            `)}
      </ha-card>
    `}static get styles(){return i.c`
      a {
        text-decoration: none;
        color: var(--primary-text-color);
      }
    `}};Object(a.c)([Object(i.g)()],s.prototype,"hass",void 0),Object(a.c)([Object(i.g)()],s.prototype,"showAdvanced",void 0),s=Object(a.c)([Object(i.d)("ha-config-ais-dom-navigation")],s)},449:function(e,t,o){"use strict";o.d(t,"a",function(){return a});const a=e=>e.callWS({type:"webhook/list"})},765:function(e,t,o){"use strict";o.r(t);o(218),o(150),o(108);var a=o(4),i=o(30),n=(o(151),o(95),o(263),o(18)),s=o(0),r=(o(143),o(182),o(187),o(177),o(449));const c=(e,t)=>{Object(n.a)(e,"show-dialog",{dialogTag:"dialog-manage-ais-cloudhook",dialogImport:()=>Promise.all([o.e(0),o.e(1),o.e(124),o.e(16)]).then(o.bind(null,739)),dialogParams:t})};customElements.define("ais-webhooks",class extends s.a{constructor(){super()}static get properties(){return{hass:{},_localHooks:{}}}connectedCallback(){super.connectedCallback(),this._fetchData()}render(){return s.f`
      ${this.renderStyle()}
      <ha-card header="Wywołania zwrotne HTTP">
        <div class="card-content">
          Wywołania zwrotne HTTP (Webhook) używane są do udostępniania
          powiadomień o zdarzeniach. Wszystko, co jest skonfigurowane do
          uruchamiania przez wywołanie zwrotne, ma publicznie dostępny unikalny
          adres URL, aby umożliwić wysyłanie danych do Asystenta domowego z
          dowolnego miejsca. ${this._renderBody()}

          <div class="footer">
            <a href="https://sviete.github.io/AIS-docs" target="_blank">
              Dowiedz się więcej o zwrotnym wywołaniu HTTP.
            </a>
          </div>
        </div>
      </ha-card>
    `}_renderBody(){return this._localHooks?1===this._localHooks.length?s.f`
        <div class="body-text">
          Wygląda na to, że nie masz jeszcze zdefiniowanych żadnych wywołań
          zwrotnych. Rozpocznij od skonfigurowania
          <a href="/config/integrations">
            integracji opartej na wywołaniu zwrotnym
          </a>
          lub przez tworzenie
          <a href="/config/automation/new"> automatyzacji typu webhook </a>.
        </div>
      `:this._localHooks.map(e=>s.f`
        ${"aisdomprocesscommandfromframe"===e.webhook_id?s.f`
              <div></div>
            `:s.f`
              <div class="webhook" .entry="${e}">
                <paper-item-body two-line>
                  <div>
                    ${e.name}
                    ${e.domain===e.name.toLowerCase()?"":` (${e.domain})`}
                  </div>
                  <div secondary>${e.webhook_id}</div>
                </paper-item-body>
                <mwc-button @click="${this._handleManageButton}">
                  Pokaż
                </mwc-button>
              </div>
            `}
      `):s.f`
        <div class="body-text">Pobieranie…</div>
      `}_showDialog(e){const t=this._localHooks.find(t=>t.webhook_id===e);c(this,{webhook:t})}_handleManageButton(e){const t=e.currentTarget.parentElement.entry;this._showDialog(t.webhook_id)}async _fetchData(){this._localHooks=this.hass.config.components.includes("webhook")?await Object(r.a)(this.hass):[]}renderStyle(){return s.f`
      <style>
        .body-text {
          padding: 8px 0;
        }
        .webhook {
          display: flex;
          padding: 4px 0;
        }
        .progress {
          margin-right: 16px;
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        .footer {
          padding-top: 16px;
        }
        .body-text a,
        .footer a {
          color: var(--primary-color);
        }
      </style>
    `}});o(195);customElements.define("ha-config-ais-dom-config-remote",class extends i.a{static get template(){return a.a`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 32px;
        }
        a {
          color: var(--primary-color);
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
        ha-card > div#ha-switch-id {
          margin: -4px 0;
          position: absolute;
          right: 8px;
          top: 32px;
        }
        .card-actions a {
          text-decoration: none;
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Zdalny dostęp</span>
            <span slot="introduction"
              >W tej sekcji możesz skonfigurować zdalny dostęp do bramki</span
            >
            <ha-card header="Szyfrowany tunel">
              <div id="ha-switch-id">
                <ha-switch
                  checked="{{remoteConnected}}"
                  on-change="changeRemote"
                ></ha-switch>
              </div>
              <div class="card-content">
                Tunel zapewnia bezpieczne zdalne połączenie z Twoim urządzeniem
                kiedy jesteś z dala od domu. Twoja bramka dostępna
                [[remoteInfo]] z Internetu pod adresem
                <a href="[[remoteDomain]]" target="_blank">[[remoteDomain]]</a>.
                <div class="center-container" style="height:100px">
                  <div on-click="showBarcodeInfo">
                    <svg style="width:48px;height:48px" viewBox="0 0 24 24">
                      <path
                        fill="#ffffff"
                        d="M3,11H5V13H3V11M11,5H13V9H11V5M9,11H13V15H11V13H9V11M15,11H17V13H19V11H21V13H19V15H21V19H19V21H17V19H13V21H11V17H15V15H17V13H15V11M19,19V15H17V19H19M15,3H21V9H15V3M17,5V7H19V5H17M3,3H9V9H3V3M5,5V7H7V5H5M3,15H9V21H3V15M5,17V19H7V17H5Z"
                      />
                    </svg>
                  </div>
                  Kliknij obrazek z kodem by go powiększyć, a następnie zeskanuj
                  kod QR za pomocą aplikacji na telefonie.
                </div>
              </div>
              <div class="card-actions">
                <a
                  href="https://sviete.github.io/AIS-docs/docs/en/ais_bramka_remote_www_index.html"
                  target="_blank"
                >
                  <mwc-button>Dowiedz się jak to działa</mwc-button>
                </a>
              </div>
            </ha-card>

            <ais-webhooks hass="[[hass]]"></ais-webhooks>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,showAdvanced:Boolean,remoteInfo:{type:String,value:"jest"},remoteDomain:{type:String,computed:"_computeRemoteDomain(hass)"},remoteConnected:{type:Boolean,computed:"_computeRremoteConnected(hass)"}}}_computeRemoteDomain(e){return"https://"+e.states["sensor.ais_secure_android_id_dom"].state+".paczka.pro"}_computeRremoteConnected(e){return"on"===e.states["input_boolean.ais_remote_access"].state?(this.remoteInfo="jest",!0):(this.remoteInfo="będzie",!1)}changeRemote(){this.hass.callService("input_boolean","toggle",{entity_id:"input_boolean.ais_remote_access"})}showBarcodeInfo(){Object(n.a)(this,"hass-more-info",{entityId:"camera.remote_access"})}})}}]);
//# sourceMappingURL=chunk.105d5c5640d97ea241e0.js.map