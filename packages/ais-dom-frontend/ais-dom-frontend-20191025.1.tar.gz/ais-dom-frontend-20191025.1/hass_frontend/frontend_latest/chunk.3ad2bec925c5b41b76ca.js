/*! For license information please see chunk.3ad2bec925c5b41b76ca.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[20],{200:function(e,t,a){"use strict";a(199);var o=a(72),s=a(1),r=a(126);const i={getTabbableNodes:function(e){var t=[];return this._collectTabbableNodes(e,t)?r.a._sortByTabIndex(t):t},_collectTabbableNodes:function(e,t){if(e.nodeType!==Node.ELEMENT_NODE||!r.a._isVisible(e))return!1;var a,o=e,i=r.a._normalizedTabIndex(o),n=i>0;i>=0&&t.push(o),a="content"===o.localName||"slot"===o.localName?Object(s.a)(o).getDistributedNodes():Object(s.a)(o.shadowRoot||o.root||o).children;for(var l=0;l<a.length;l++)n=this._collectTabbableNodes(a[l],t)||n;return n}},n=customElements.get("paper-dialog"),l={get _focusableNodes(){return i.getTabbableNodes(this)}};customElements.define("ha-paper-dialog",class extends(Object(o.b)([l],n)){})},745:function(e,t,a){"use strict";a.r(t),a.d(t,"DialogManageAisCloudhook",function(){return n});var o=a(0),s=(a(86),a(83),a(213),a(200),a(56));function r(e,t,a){return t in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}const i="Publiczny unikalny adres URL – kliknij, aby skopiować do schowka.";class n extends o.a{constructor(...e){super(...e),r(this,"hass",void 0),r(this,"_params",void 0)}static get properties(){return{_params:{},hass:{}}}async showDialog(e){this._params=e,await this.updateComplete,this._dialog.open()}render(){if(!this._params)return o.f``;const{webhook:e}=this._params,t="https://"+this.hass.states["sensor.ais_secure_android_id_dom"].state+".paczka.pro/api/webhook/"+e.webhook_id;return o.f`
      <ha-paper-dialog with-backdrop>
        <h2>Wywołanie zwrotne dla ${e.name}</h2>
        <div>
          <p>
            Wywołanie zwrotne HTTP (Webhook) jest dostępny pod następującym
            adresem URL:
          </p>
          <paper-input
            label="${i}"
            value="${t}"
            @click="${this._copyClipboard}"
            @blur="${this._restoreLabel}"
          ></paper-input>
        </div>

        <div class="paper-dialog-buttons">
          <mwc-button @click="${this._closeDialog}">ZAMKNIJ</mwc-button>
        </div>
      </ha-paper-dialog>
    `}get _dialog(){return this.shadowRoot.querySelector("ha-paper-dialog")}get _paperInput(){return this.shadowRoot.querySelector("paper-input")}_closeDialog(){this._dialog.close()}_copyClipboard(e){const t=e.currentTarget,a=t.inputElement.inputElement;a.setSelectionRange(0,a.value.length);try{document.execCommand("kopiuj"),t.label="SKOPIOWANO DO SCHOWKA"}catch(o){}}_restoreLabel(){this._paperInput.label=i}static get styles(){return[s.a,o.c`
        ha-paper-dialog {
          width: 650px;
        }
        paper-input {
          margin-top: -8px;
        }
        button.link {
          color: var(--primary-color);
        }
        .paper-dialog-buttons a {
          text-decoration: none;
        }
      `]}}customElements.define("dialog-manage-ais-cloudhook",n)}}]);
//# sourceMappingURL=chunk.3ad2bec925c5b41b76ca.js.map