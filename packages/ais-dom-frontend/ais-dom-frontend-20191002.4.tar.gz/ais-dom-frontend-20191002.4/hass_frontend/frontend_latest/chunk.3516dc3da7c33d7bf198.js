(self.webpackJsonp=self.webpackJsonp||[]).push([[80],{197:function(e,t,i){"use strict";i.d(t,"a",function(){return o});const o=(e,t,i=!1)=>{let o;return function(...n){const a=this,c=i&&!o;clearTimeout(o),o=setTimeout(()=>{o=null,i||e.apply(a,n)},t),c&&e.apply(a,n)}}},201:function(e,t,i){"use strict";i.d(t,"b",function(){return o}),i.d(t,"a",function(){return n});const o=(e,t)=>e<t?-1:e>t?1:0,n=(e,t)=>o(e.toLowerCase(),t.toLowerCase())},283:function(e,t,i){"use strict";i.d(t,"a",function(){return a}),i.d(t,"c",function(){return c}),i.d(t,"f",function(){return r}),i.d(t,"b",function(){return s}),i.d(t,"d",function(){return l}),i.d(t,"e",function(){return h}),i.d(t,"h",function(){return u}),i.d(t,"g",function(){return g});var o=i(197),n=i(13);const a=(e,t)=>e.callApi("POST","config/config_entries/flow",{handler:t}),c=(e,t)=>e.callApi("GET",`config/config_entries/flow/${t}`),r=(e,t,i)=>e.callApi("POST",`config/config_entries/flow/${t}`,i),s=(e,t)=>e.callApi("DELETE",`config/config_entries/flow/${t}`),l=e=>e.callApi("GET","config/config_entries/flow_handlers"),d=e=>e.sendMessagePromise({type:"config_entries/flow/progress"}),p=(e,t)=>e.subscribeEvents(Object(o.a)(()=>d(e).then(e=>t.setState(e,!0)),500,!0),"config_entry_discovered"),h=e=>Object(n.h)(e,"_configFlowProgress",d,p),u=(e,t)=>h(e.connection).subscribe(t),g=(e,t)=>{const i=t.context.title_placeholders||{},o=Object.keys(i);if(0===o.length)return e(`component.${t.handler}.config.title`);const n=[];return o.forEach(e=>{n.push(e),n.push(i[e])}),e(`component.${t.handler}.config.flow_title`,...n)}},303:function(e,t,i){"use strict";i.d(t,"a",function(){return n}),i.d(t,"b",function(){return a});var o=i(18);const n=()=>Promise.all([i.e(0),i.e(1),i.e(2),i.e(6),i.e(32)]).then(i.bind(null,385)),a=(e,t,i)=>{Object(o.a)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:n,dialogParams:Object.assign(Object.assign({},t),{flowConfig:i})})}},313:function(e,t,i){"use strict";i.d(t,"a",function(){return s}),i.d(t,"b",function(){return l});var o=i(283),n=i(0),a=i(58),c=i(303),r=i(201);const s=c.a,l=(e,t)=>Object(c.b)(e,t,{loadDevicesAndAreas:!0,getFlowHandlers:e=>Object(o.d)(e).then(t=>t.sort((t,i)=>Object(r.a)(e.localize(`component.${t}.config.title`),e.localize(`component.${i}.config.title`)))),createFlow:o.a,fetchFlow:o.c,handleFlowStep:o.f,deleteFlow:o.b,renderAbortDescription(e,t){const i=Object(a.b)(e.localize,`component.${t.handler}.config.abort.${t.reason}`,t.description_placeholders);return i?n.f`
            <ha-markdown allowsvg .content=${i}></ha-markdown>
          `:""},renderShowFormStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`),renderShowFormStepDescription(e,t){const i=Object(a.b)(e.localize,`component.${t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return i?n.f`
            <ha-markdown allowsvg .content=${i}></ha-markdown>
          `:""},renderShowFormStepFieldLabel:(e,t,i)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.data.${i.name}`),renderShowFormStepFieldError:(e,t,i)=>e.localize(`component.${t.handler}.config.error.${i}`),renderExternalStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`),renderExternalStepDescription(e,t){const i=Object(a.b)(e.localize,`component.${t.handler}.config.${t.step_id}.description`,t.description_placeholders);return n.f`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${i?n.f`
              <ha-markdown allowsvg .content=${i}></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,t){const i=Object(a.b)(e.localize,`component.${t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return n.f`
        ${i?n.f`
              <ha-markdown allowsvg .content=${i}></ha-markdown>
            `:""}
        <p>Created config for ${t.title}.</p>
      `}})},329:function(e,t,i){"use strict";i.d(t,"b",function(){return o}),i.d(t,"a",function(){return n});const o=async(e,t=!1)=>{if(!e.parentNode)throw new Error("Cannot setup Leaflet map on disconnected element");const o=await i.e(144).then(i.t.bind(null,408,7));o.Icon.Default.imagePath="/static/images/leaflet/images/";const a=o.map(e),c=document.createElement("link");return c.setAttribute("href","/static/images/leaflet/leaflet.css"),c.setAttribute("rel","stylesheet"),e.parentNode.appendChild(c),a.setView([52.3731339,4.8903147],13),n(o,t).addTo(a),[a,o]},n=(e,t)=>e.tileLayer(`https://{s}.basemaps.cartocdn.com/${t?"dark_all":"light_all"}/{z}/{x}/{y}${e.Browser.retina?"@2x.png":".png"}`,{attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',subdomains:"abcd",minZoom:0,maxZoom:20})},406:function(e,t,i){"use strict";i.d(t,"b",function(){return o}),i.d(t,"a",function(){return n});const o=(e,t)=>e.callWS(Object.assign({type:"config/core/update"},t)),n=e=>e.callWS({type:"config/core/detect"})},445:function(e,t,i){"use strict";i.d(t,"a",function(){return a});var o=i(501),n=i.n(o);const a=()=>{const e=document.createElement("datalist");return e.id="timezones",Object.keys(n.a).forEach(t=>{const i=document.createElement("option");i.value=t,i.innerHTML=n.a[t],e.appendChild(i)}),e}},446:function(e,t,i){"use strict";var o=i(3),n=i(0),a=i(329),c=i(18);let r=class extends n.a{constructor(){super(...arguments),this.fitZoom=16}fitMap(){this._leafletMap&&this.location&&this._leafletMap.setView(this.location,this.fitZoom)}render(){return n.f`
      <div id="map"></div>
    `}firstUpdated(e){super.firstUpdated(e),this._initMap()}updated(e){super.updated(e),this.Leaflet&&(this._updateMarker(),this._ignoreFitToMap&&this._ignoreFitToMap===this.location||this.fitMap(),this._ignoreFitToMap=void 0)}get _mapEl(){return this.shadowRoot.querySelector("div")}async _initMap(){[this._leafletMap,this.Leaflet]=await Object(a.b)(this._mapEl),this._leafletMap.addEventListener("click",e=>this._updateLocation(e.latlng)),this._updateMarker(),this.fitMap(),this._leafletMap.invalidateSize()}_updateLocation(e){this.location=this._ignoreFitToMap=[e.lat,e.lng],Object(c.a)(this,"change",void 0,{bubbles:!1})}_updateMarker(){this.location?this._locationMarker?this._locationMarker.setLatLng(this.location):(this._locationMarker=this.Leaflet.marker(this.location,{draggable:!0}),this._locationMarker.addEventListener("dragend",e=>this._updateLocation(e.target.getLatLng())),this._leafletMap.addLayer(this._locationMarker)):this._locationMarker&&(this._locationMarker.remove(),this._locationMarker=void 0)}static get styles(){return n.c`
      :host {
        display: block;
        height: 300px;
      }
      #map {
        height: 100%;
      }
    `}};Object(o.c)([Object(n.g)()],r.prototype,"location",void 0),r=Object(o.c)([Object(n.d)("ha-location-editor")],r)},696:function(e,t,i){"use strict";i.r(t);var o=i(3),n=i(0),a=(i(85),i(93),i(297),i(267),i(145),i(406)),c=i(313),r=i(112),s=i(18),l=i(445);i(446);const d=[52.3731339,4.8903147];let p=class extends n.a{constructor(){super(...arguments),this._working=!1}render(){return n.f`
      <p>
        ${this.onboardingLocalize("ui.panel.page-onboarding.core-config.intro","name",this.hass.user.name)}
      </p>

      <paper-input
        .label=${this.onboardingLocalize("ui.panel.page-onboarding.core-config.location_name")}
        name="name"
        .disabled=${this._working}
        .value=${this._nameValue}
        @value-changed=${this._handleChange}
      ></paper-input>

      <div class="middle-text">
        <p>
          ${this.onboardingLocalize("ui.panel.page-onboarding.core-config.intro_location")}
        </p>
        <div class="row">
          <div>
            ${this.onboardingLocalize("ui.panel.page-onboarding.core-config.intro_location_detect")}
            Do tego jest potrzebne połączenie z Internetem.
          </div>
          <mwc-button @click=${this._connectWifi}>
            POŁĄCZ Z WIFI
          </mwc-button>
        </div>

        <div class="row">
          <div>
            Ustal swoją lokalizację po adresie IP wysyłając jednorazowe
            zapytanie do serwisu
            <span
              style="color:#FF9800; font-weight: bold;"
              @click=${this._detect}
              >ipapi.co</span
            >
          </div>
          <mwc-button @click=${this._detect}>
            ${this.onboardingLocalize("ui.panel.page-onboarding.core-config.button_detect")}
          </mwc-button>
        </div>
      </div>

      <div class="row">
        <ha-location-editor
          class="flex"
          .location=${this._locationValue}
          .fitZoom=${14}
          @change=${this._locationChanged}
          style="z-index:100"
        ></ha-location-editor>
      </div>

      <div class="row">
        <paper-input
          class="flex"
          .label=${this.hass.localize("ui.panel.config.core.section.core.core_config.time_zone")}
          name="timeZone"
          list="timezones"
          .disabled=${this._working}
          .value=${this._timeZoneValue}
          @value-changed=${this._handleChange}
        ></paper-input>

        <paper-input
          class="flex"
          .label=${this.hass.localize("ui.panel.config.core.section.core.core_config.elevation")}
          name="elevation"
          type="number"
          .disabled=${this._working}
          .value=${this._elevationValue}
          @value-changed=${this._handleChange}
        >
          <span slot="suffix">
            ${this.hass.localize("ui.panel.config.core.section.core.core_config.elevation_meters")}
          </span>
        </paper-input>
      </div>

      <div class="row">
        <div class="flex">
          ${this.hass.localize("ui.panel.config.core.section.core.core_config.unit_system")}
        </div>
        <paper-radio-group
          class="flex"
          .selected=${this._unitSystemValue}
          @selected-changed=${this._unitSystemChanged}
        >
          <paper-radio-button name="metric" .disabled=${this._working}>
            ${this.hass.localize("ui.panel.config.core.section.core.core_config.unit_system_metric")}
            <div class="secondary">
              ${this.hass.localize("ui.panel.config.core.section.core.core_config.metric_example")}
            </div>
          </paper-radio-button>
          <paper-radio-button name="imperial" .disabled=${this._working}>
            ${this.hass.localize("ui.panel.config.core.section.core.core_config.unit_system_imperial")}
            <div class="secondary">
              ${this.hass.localize("ui.panel.config.core.section.core.core_config.imperial_example")}
            </div>
          </paper-radio-button>
        </paper-radio-group>
      </div>

      <div class="footer">
        <mwc-button @click=${this._save} .disabled=${this._working}>
          ${this.onboardingLocalize("ui.panel.page-onboarding.core-config.finish")}
        </mwc-button>
      </div>
    `}firstUpdated(e){super.firstUpdated(e),setTimeout(()=>this.shadowRoot.querySelector("paper-input").focus(),100),this.addEventListener("keypress",e=>{13===e.keyCode&&this._save(e)}),this.shadowRoot.querySelector("[name=timeZone]").inputElement.appendChild(Object(l.a)())}get _nameValue(){return void 0!==this._name?this._name:this.onboardingLocalize("ui.panel.page-onboarding.core-config.location_name_default")}get _locationValue(){return this._location||d}get _elevationValue(){return void 0!==this._elevation?this._elevation:0}get _timeZoneValue(){return this._timeZone}get _unitSystemValue(){return void 0!==this._unitSystem?this._unitSystem:"metric"}_handleChange(e){const t=e.currentTarget;this[`_${t.name}`]=t.value}_locationChanged(e){this._location=e.currentTarget.location}_unitSystemChanged(e){this._unitSystem=e.detail.value}async _detect(){this._working=!0;try{const t=await Object(a.a)(this.hass);t.latitude&&t.longitude&&(this._location=[Number(t.latitude),Number(t.longitude)]),t.elevation&&(this._elevation=String(t.elevation)),t.unit_system&&(this._unitSystem=t.unit_system),t.time_zone&&(this._timeZone=t.time_zone)}catch(e){alert(`Failed to detect location information: ${e.message}`)}finally{this._working=!1}}_connectWifi(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_wifi_service"}).then(e=>{this._continueFlow(e.flow_id)})}_continueFlow(e){Object(c.b)(this,{continueFlowId:e,dialogClosedCallback:()=>{}})}async _save(e){e.preventDefault(),this._working=!0;try{const e=this._locationValue;await Object(a.b)(this.hass,{location_name:this._nameValue,latitude:e[0],longitude:e[1],elevation:Number(this._elevationValue),unit_system:this._unitSystemValue,time_zone:this._timeZoneValue||"UTC"});const i=await Object(r.b)(this.hass);Object(s.a)(this,"onboarding-step",{type:"core_config",result:i})}catch(t){this._working=!1,alert("FAIL")}}static get styles(){return n.c`
      .row {
        display: flex;
        flex-direction: row;
        margin: 0 -8px;
        align-items: center;
      }

      .secondary {
        color: var(--secondary-text-color);
      }

      .flex {
        flex: 1;
      }

      .middle-text {
        margin: 24px 0;
      }

      .row > * {
        margin: 0 8px;
      }
      .footer {
        margin-top: 16px;
        text-align: right;
      }
    `}};Object(o.c)([Object(n.g)()],p.prototype,"hass",void 0),Object(o.c)([Object(n.g)()],p.prototype,"onboardingLocalize",void 0),Object(o.c)([Object(n.g)()],p.prototype,"_working",void 0),Object(o.c)([Object(n.g)()],p.prototype,"_name",void 0),Object(o.c)([Object(n.g)()],p.prototype,"_location",void 0),Object(o.c)([Object(n.g)()],p.prototype,"_elevation",void 0),Object(o.c)([Object(n.g)()],p.prototype,"_unitSystem",void 0),Object(o.c)([Object(n.g)()],p.prototype,"_timeZone",void 0),p=Object(o.c)([Object(n.d)("onboarding-core-config")],p)}}]);
//# sourceMappingURL=chunk.3516dc3da7c33d7bf198.js.map