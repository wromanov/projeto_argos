// PROTOTYPE_ONLY — rendering of deterministic local fixtures and demonstrative feedback.
(() => {
 const root=document.documentElement, query=new URLSearchParams(location.search);
 const fixtureName=root.dataset.argosPrototypeFixture==="long"?"long":"default";
 const state=root.dataset.argosPrototypeState||"default", demo=query.get("demo")||"";
 // Canonical DS component display rules override the browser's default [hidden] rule.
 // Keep P3 harness variants and demonstrative feedback semantically hidden without local CSS.
 const syncHidden=(node)=>{if(node.hidden)node.style.setProperty("display","none");else node.style.removeProperty("display");};
 document.querySelectorAll("[hidden]").forEach(syncHidden);
 new MutationObserver((changes)=>changes.forEach((change)=>{if(change.attributeName==="hidden")syncHidden(change.target);})).observe(document.body,{attributes:true,subtree:true,attributeFilter:["hidden"]});
 const read=(obj,path)=>path.split(".").reduce((v,k)=>v==null?undefined:v[k],obj);
 const put=(node,value)=>{if(value==null)return;if(node.matches("input,textarea,select"))node.value=String(value);else node.textContent=String(value);};
 const cell=(value)=>{const n=document.createElement("td");n.textContent=value||"—";return n;};
 const badge=(value,tone="neutral")=>{const n=document.createElement("span");n.className="argos-badge argos-badge--"+tone;n.textContent=value;return n;};
 const link=(text,href,route)=>{const n=document.createElement("a");n.textContent=text;n.href=href;if(route)n.dataset.conceptualRoute=route;return n;};
 function options(node,pairs){if(!node)return;node.replaceChildren();pairs.forEach(([value,label])=>{const o=document.createElement("option");o.value=value;o.textContent=label;node.append(o);});}

 function rowsActivities(items){const body=document.querySelector('[data-fixture-table="activities"]');if(!body)return;body.replaceChildren();items.forEach(x=>{const tr=document.createElement("tr"),td=document.createElement("td");td.append(badge(x.type),document.createTextNode(" "));const a=link(x.title,"scr-act-create-001.html?mode=edit&fixture="+fixtureName,"/cameras/atividades/<pk>/editar/");const strong=document.createElement("strong");strong.textContent=x.title;a.replaceChildren(strong);td.append(a,document.createElement("br"));const d=document.createElement("span");d.className="argos-state__copy";d.textContent=x.description;td.append(d);tr.append(td,cell(x.occurred),cell(x.responsible),cell(x.user),cell(x.created));const action=document.createElement("td");action.append(link("Editar","scr-act-create-001.html?mode=edit&fixture="+fixtureName,"/cameras/atividades/<pk>/editar/"));tr.append(action);body.append(tr);});}
 function rowsEvents(items,camera){const body=document.querySelector(camera?'[data-table="camera-events"]':'[data-table="events"]');if(!body)return;body.replaceChildren();items.forEach(x=>{const tr=document.createElement("tr");tr.append(cell(x.time));const td=document.createElement("td"),a=link(x.code,"scr-event-detail-001.html?event="+encodeURIComponent(x.id)+"&fixture="+fixtureName,"/eventos/<pk>/");const strong=document.createElement("strong");strong.textContent=x.code;a.replaceChildren(strong);td.append(a,document.createElement("br"));const summary=document.createElement("span");summary.className="argos-state__copy";summary.textContent=x.summary;td.append(summary);tr.append(td);const cat=document.createElement("td");cat.append(badge(x.category,"info"));tr.append(cat,cell(x.user));if(!camera)tr.append(cell(x.entity));const origin=document.createElement("td");origin.append(badge(x.origin));tr.append(origin);body.append(tr);});}
 function chipFilters(categories,origins,search){const region=document.querySelector("#active-filters");if(!region)return;region.replaceChildren();const cat=document.querySelector("[data-categories]"),org=document.querySelector("[data-origins]");const labels=[];if(search)labels.push("Pesquisa: "+search);categories.forEach(v=>{const o=Array.from(cat.options).find(x=>x.value===v);if(o)labels.push("Categoria: "+o.textContent);});origins.forEach(v=>{const o=Array.from(org.options).find(x=>x.value===v);if(o)labels.push("Origem: "+o.textContent);});labels.forEach(v=>region.append(badge(v,"info")));region.hidden=!labels.length;const note=document.querySelector("#filter-note");if(note)note.hidden=!labels.length;}
 function selectedFilters(categories,origins,search=""){const cat=document.querySelector("[data-categories]"),org=document.querySelector("[data-origins]");if(cat)Array.from(cat.options).forEach(o=>o.selected=categories.includes(o.value));if(org)Array.from(org.options).forEach(o=>o.selected=origins.includes(o.value));const q=document.querySelector("#event-q");if(q)q.value=search;chipFilters(categories,origins,search);}
 function demoSuccess(){const n=document.querySelector("#demo-feedback");if(n){n.hidden=false;n.focus();}}
 async function start(){
  try{
   const response=await fetch("../../fixtures/p3-c/fixtures.json",{cache:"no-store"});if(!response.ok)throw Error("fixture");
   const source=await response.json(),data=source[fixtureName]||source.default;
   document.querySelectorAll("[data-fixture-value]").forEach(n=>put(n,read(data,n.dataset.fixtureValue)));
   document.querySelectorAll("[data-types]").forEach(n=>options(n,data.types));

   document.querySelectorAll("[data-categories]").forEach(n=>options(n,data.categories));
   document.querySelectorAll("[data-origins]").forEach(n=>options(n,data.origins));
   document.querySelectorAll("[data-replacements]").forEach(n=>{options(n,data.replacement);const showSelection=()=>{const item=data.replacement.find(x=>x[0]===n.value);const name=document.querySelector("[data-replacement-name]"),id=document.querySelector("[data-replacement-id]");if(item&&name)name.textContent=item[1].split(" · ")[0];if(item&&id)id.textContent=item[0]+" · Estoque";};n.addEventListener("change",showSelection);showSelection();});
   document.querySelectorAll("[data-fixture-value]").forEach(n=>put(n,read(data,n.dataset.fixtureValue)));
   const type=document.querySelector('[name="tipo"]');if(type)type.value=query.get("mode")==="edit"?data.activityEdit.tipo:data.activityForm.tipo;
   const cameraContext=document.querySelector("[data-current-situation]");if(cameraContext&&document.querySelector("[data-state-target]")&&fixtureName==="long"){cameraContext.textContent="Estoque";document.querySelector("[data-state-target]").value="PRODUCAO";}
   const missing=document.querySelector("[data-missing]");if(missing&&data.governance.missing.length)missing.textContent="Campos pendentes para Produção: "+data.governance.missing.join(", ")+".";
   const complete=document.querySelector("[data-completeness]");if(complete&&data.governance.missing.length){complete.className="argos-badge argos-badge--warning";complete.textContent="Cadastro incompleto";}
rowsActivities(data.activities);rowsEvents(data.events,false);rowsEvents(data.events.filter((_,i)=>i<5),true);
   if(state==="error"&&document.querySelector("[data-audit-period-start]")){const from=document.querySelector("[data-audit-period-start]"),to=document.querySelector("[data-audit-period-end]");from.value="2026-09-28";to.value="2026-09-27";[from,to].forEach(n=>{n.setAttribute("aria-invalid","true");n.setAttribute("aria-describedby","audit-period-error");});}
   if(query.get("mode")==="edit"&&document.querySelector("[data-create-title]")){document.querySelector('meta[name="argos-screen-id"]').content="SCR-ACT-EDIT-001";const editRecord=document.querySelector("[data-edit-record]");if(editRecord)editRecord.hidden=false;const editId=document.querySelector("[data-activity-edit-id]");if(editId)editId.textContent=data.activityEdit.id;document.title="Editar atividade — ARGOS";document.querySelector("[data-create-title]").hidden=true;document.querySelector("[data-edit-title]").hidden=false;document.querySelector(".argos-page-title").textContent="Editar atividade";const button=document.querySelector("[data-demo-action]");if(button)button.textContent="Demonstrar salvamento das alterações";["tipo","titulo","descricao","ocorrida_em","responsavel"].forEach(k=>{const n=document.querySelector('[name="'+k+'"]');if(n)put(n,data.activityEdit[k]);});}
   document.querySelectorAll("[data-validation-error-for]").forEach(m=>{if(state==="error"){const c=document.getElementById(m.dataset.validationErrorFor);if(c){c.setAttribute("aria-invalid","true");c.setAttribute("aria-describedby",m.id);}}});
   if(demo==="selected")selectedFilters(["CAMERA","ATIVIDADE"],["WEB","ADMIN"],"camera");
   document.querySelector("[data-apply-filters]")?.addEventListener("click",()=>{const cats=Array.from(document.querySelector("[data-categories]").selectedOptions).map(o=>o.value),orgs=Array.from(document.querySelector("[data-origins]").selectedOptions).map(o=>o.value);chipFilters(cats,orgs,document.querySelector("#event-q").value);});
   document.querySelector("[data-demo-action]")?.addEventListener("click",()=>{if(state==="error"){document.querySelector("[aria-invalid='true']")?.focus();return;}demoSuccess();});
   document.querySelector("[data-demo-form]")?.addEventListener("submit",e=>e.preventDefault());
   if(demo==="success")demoSuccess();
   if(demo==="focus")document.querySelector(".argos-docs-content .argos-input, .argos-docs-content .argos-select")?.focus();
   const nav=document.querySelector(".argos-docs-nav"),activeNav=nav?.querySelector("[aria-current=page]");
   if(nav&&activeNav&&matchMedia("(max-width: 680px)").matches)nav.scrollLeft=Math.max(0,activeNav.offsetLeft+activeNav.offsetWidth-nav.clientWidth);
   root.dataset.argosP3cReady="true";
  }catch(_){const n=document.querySelector("#fixture-load-error");if(n)n.hidden=false;else console.error("Fixture P3-C indisponível.");}
 }
 start();
})();
