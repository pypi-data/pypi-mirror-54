/*
 *  /MathJax/jax/output/HTML-CSS/autoload/mtable.js
 *
 *  Copyright (c) 2009-2018 The MathJax Consortium
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

MathJax.Hub.Register.StartupHook("HTML-CSS Jax Ready",function(){var c="2.7.5";var a=MathJax.ElementJax.mml,b=MathJax.OutputJax["HTML-CSS"];a.mtable.Augment({toHTML:function(r){r=this.HTMLcreateSpan(r);if(this.data.length===0){return r}var I=this.getValues("columnalign","rowalign","columnspacing","rowspacing","columnwidth","equalcolumns","equalrows","columnlines","rowlines","frame","framespacing","align","useHeight","width","side","minlabelspacing");var aM=I.width.match(/%$/);var ay=b.createStack(r);var aJ=this.HTMLgetScale(),aB=this.HTMLgetMu(r),aC=-1;var aq=[],au=[],aj=[],aw=[],av=[],ae,ad,ap=-1,ac,ao,X,aH,Q,aE,aR=[],aW;var G=b.FONTDATA.lineH*aJ*I.useHeight,N=b.FONTDATA.lineD*aJ*I.useHeight;for(ae=0,ac=this.data.length;ae<ac;ae++){aH=this.data[ae];X=(aH.type==="mlabeledtr"?aC:0);aw[ae]=[];aq[ae]=G;au[ae]=N;for(ad=X,ao=aH.data.length+X;ad<ao;ad++){if(aj[ad]==null){if(ad>ap){ap=ad}av[ad]=b.createStack(b.createBox(ay));aj[ad]=-b.BIGDIMEN}aw[ae][ad]=b.createBox(av[ad]);aR.push(aH.data[ad-X].toHTML(aw[ae][ad]))}}b.MeasureSpans(aR);for(ae=0,ac=this.data.length;ae<ac;ae++){aH=this.data[ae];X=(aH.type==="mlabeledtr"?aC:0);for(ad=X,ao=aH.data.length+X;ad<ao;ad++){Q=aH.data[ad-X];if(Q.isMultiline){aw[ae][ad].style.width="100%"}if(Q.isEmbellished()){aE=Q.CoreMO();var aV=aE.Get("minsize",true);if(aV){var aO=aE.HTMLspanElement().bbox;if(aE.HTMLcanStretch("Vertical")){aW=aO.h+aO.d;if(aW){aV=b.length2em(aV,aB,aW);if(aV*aO.h/aW>aq[ae]){aq[ae]=aV*aO.h/aW}if(aV*aO.d/aW>au[ae]){au[ae]=aV*aO.d/aW}}}else{if(aE.HTMLcanStretch("Horizontal")){aV=b.length2em(aV,aB,aO.w);if(aV>aj[ad]){aj[ad]=aV}}}}}if(aw[ae][ad].bbox.h>aq[ae]){aq[ae]=aw[ae][ad].bbox.h}if(aw[ae][ad].bbox.d>au[ae]){au[ae]=aw[ae][ad].bbox.d}if(aw[ae][ad].bbox.w>aj[ad]){aj[ad]=aw[ae][ad].bbox.w}}}var aG=MathJax.Hub.SplitList;var aA=aG(I.columnspacing),aT=aG(I.rowspacing),e=aG(I.columnalign),B=aG(I.rowalign),d=aG(I.columnlines),w=aG(I.rowlines),aP=aG(I.columnwidth),U=[];for(ae=0,ac=aA.length;ae<ac;ae++){aA[ae]=b.length2em(aA[ae],aB)}for(ae=0,ac=aT.length;ae<ac;ae++){aT[ae]=b.length2em(aT[ae],aB)}while(aA.length<ap){aA.push(aA[aA.length-1])}while(e.length<=ap){e.push(e[e.length-1])}while(d.length<ap){d.push(d[d.length-1])}while(aP.length<=ap){aP.push(aP[aP.length-1])}while(aT.length<aw.length){aT.push(aT[aT.length-1])}while(B.length<=aw.length){B.push(B[B.length-1])}while(w.length<aw.length){w.push(w[w.length-1])}if(av[aC]){e[aC]=(I.side.substr(0,1)==="l"?"left":"right");aA[aC]=-aj[aC]}for(ae=0,ac=aw.length;ae<ac;ae++){aH=this.data[ae];U[ae]=[];if(aH.rowalign){B[ae]=aH.rowalign}if(aH.columnalign){U[ae]=aG(aH.columnalign);while(U[ae].length<=ap){U[ae].push(U[ae][U[ae].length-1])}}}if(I.equalrows){var aF=Math.max.apply(Math,aq),V=Math.max.apply(Math,au);for(ae=0,ac=aw.length;ae<ac;ae++){X=((aF+V)-(aq[ae]+au[ae]))/2;aq[ae]+=X;au[ae]+=X}}aW=aq[0]+au[aw.length-1];for(ae=0,ac=aw.length-1;ae<ac;ae++){aW+=Math.max(0,au[ae]+aq[ae+1]+aT[ae])}var aL=0,aK=0,aZ,g=aW;if(I.frame!=="none"||(I.columnlines+I.rowlines).match(/solid|dashed/)){var v=aG(I.framespacing);if(v.length!=2){v=aG(this.defaults.framespacing)}aL=b.length2em(v[0],aB);aK=b.length2em(v[1],aB);g=aW+2*aK}var ai,aY,aa="";if(typeof(I.align)!=="string"){I.align=String(I.align)}if(I.align.match(/(top|bottom|center|baseline|axis)( +(-?\d+))?/)){aa=RegExp.$3||"";I.align=RegExp.$1}else{I.align=this.defaults.align}if(aa!==""){aa=parseInt(aa);if(aa<0){aa=aw.length+1+aa}if(aa<1){aa=1}else{if(aa>aw.length){aa=aw.length}}ai=0;aY=-(aW+aK)+aq[0];for(ae=0,ac=aa-1;ae<ac;ae++){var L=Math.max(0,au[ae]+aq[ae+1]+aT[ae]);ai+=L;aY+=L}}else{ai=({top:-(aq[0]+aK),bottom:aW+aK-aq[0],center:aW/2-aq[0],baseline:aW/2-aq[0],axis:aW/2+b.TeX.axis_height*aJ-aq[0]})[I.align];aY=({top:-(aW+2*aK),bottom:0,center:-(aW/2+aK),baseline:-(aW/2+aK),axis:b.TeX.axis_height*aJ-aW/2-aK})[I.align]}var ab,af=0,z=0,K=0,Z=0,ag=0,am=[],at=[],R=1;if(I.equalcolumns&&I.width!=="auto"){if(aM){ab=(100/(ap+1)).toFixed(2).replace(/\.?0+$/,"")+"%";for(ae=0,ac=Math.min(ap+1,aP.length);ae<ac;ae++){aP[ae]=ab}ab=0;af=1;ag=ap+1;for(ae=0,ac=Math.min(ap+1,aA.length);ae<ac;ae++){ab+=aA[ae]}}else{ab=b.length2em(I.width,aB);for(ae=0,ac=Math.min(ap,aA.length);ae<ac;ae++){ab-=aA[ae]}ab/=ap;for(ae=0,ac=Math.min(ap+1,aP.length);ae<ac;ae++){aj[ae]=ab}}}else{for(ae=0,ac=Math.min(ap+1,aP.length);ae<ac;ae++){if(aP[ae]==="auto"){z+=aj[ae]}else{if(aP[ae]==="fit"){at[ag]=ae;ag++;z+=aj[ae]}else{if(aP[ae].match(/%$/)){am[Z]=ae;Z++;K+=aj[ae];af+=b.length2em(aP[ae],aB,1)}else{aj[ae]=b.length2em(aP[ae],aB);z+=aj[ae]}}}}if(aM){ab=0;for(ae=0,ac=Math.min(ap,aA.length);ae<ac;ae++){ab+=aA[ae]}if(af>0.98){R=0.98/af;af=0.98}}else{if(I.width==="auto"){if(af>0.98){R=K/(z+K);ab=z+K}else{ab=z/(1-af)}}else{ab=b.length2em(I.width,aB);for(ae=0,ac=Math.min(ap,aA.length);ae<ac;ae++){ab-=aA[ae]}}for(ae=0,ac=am.length;ae<ac;ae++){aj[am[ae]]=b.length2em(aP[am[ae]],aB,ab*R);z+=aj[am[ae]]}if(Math.abs(ab-z)>0.01){if(ag&&ab>z){ab=(ab-z)/ag;for(ae=0,ac=at.length;ae<ac;ae++){aj[at[ae]]+=ab}}else{ab=ab/z;for(ad=0;ad<=ap;ad++){aj[ad]*=ab}}}if(I.equalcolumns){var O=Math.max.apply(Math,aj);for(ad=0;ad<=ap;ad++){aj[ad]=O}}}}var S=ai,o,q,aU;X=(av[aC]?aC:0);for(ad=X;ad<=ap;ad++){for(ae=0,ac=aw.length;ae<ac;ae++){if(aw[ae][ad]){X=(this.data[ae].type==="mlabeledtr"?aC:0);Q=this.data[ae].data[ad-X];if(Q.HTMLcanStretch("Horizontal")){aw[ae][ad].bbox=Q.HTMLstretchH(av[ad],aj[ad]).bbox}else{if(Q.HTMLcanStretch("Vertical")){aE=Q.CoreMO();var aN=aE.symmetric;aE.symmetric=false;aw[ae][ad].bbox=Q.HTMLstretchV(av[ad],aq[ae],au[ae]).bbox;aw[ae][ad].HH=null;if(aw[ae][ad].bbox.h>aq[ae]){aw[ae][ad].bbox.H=aw[ae][ad].bbox.h;aw[ae][ad].bbox.h=aq[ae]}if(aw[ae][ad].bbox.d>au[ae]){aw[ae][ad].bbox.D=aw[ae][ad].bbox.d;aw[ae][ad].bbox.d=au[ae]}aE.symmetric=aN}}aU=Q.rowalign||this.data[ae].rowalign||B[ae];o=({top:aq[ae]-aw[ae][ad].bbox.h,bottom:aw[ae][ad].bbox.d-au[ae],center:((aq[ae]-au[ae])-(aw[ae][ad].bbox.h-aw[ae][ad].bbox.d))/2,baseline:0,axis:0})[aU]||0;aU=(Q.columnalign||U[ae][ad]||e[ad]);b.alignBox(aw[ae][ad],aU,S+o)}if(ae<aw.length-1){S-=Math.max(0,au[ae]+aq[ae+1]+aT[ae])}}S=ai}if(aM){var E=b.createBox(ay);E.style.left=E.style.top=0;E.style.right=b.Em(ab+2*aL);E.style.display="inline-block";E.style.height="0px";if(b.msieRelativeWidthBug){E=b.createBox(E);E.style.position="relative";E.style.height="1em";E.style.width="100%";E.bbox=ay.bbox}var aS=0,a0=aL,k,l;if(ag){k=100*(1-af)/ag,l=z/ag}else{k=100*(1-af)/(ap+1);l=z/(ap+1)}for(ad=0;ad<=ap;ad++){b.placeBox(av[ad].parentNode,0,0);av[ad].style.position="relative";av[ad].style.left=b.Em(a0);av[ad].style.width="100%";av[ad].parentNode.parentNode.removeChild(av[ad].parentNode);var al=b.createBox(E);b.addBox(al,av[ad]);av[ad]=al;var h=al.style;h.display="inline-block";h.left=aS+"%";if(aP[ad].match(/%$/)){var t=parseFloat(aP[ad])*R;if(ag===0){h.width=(k+t)+"%";aS+=k+t;al=b.createBox(al);b.addBox(al,av[ad].firstChild);al.style.left=0;al.style.right=b.Em(l);a0-=l}else{h.width=t+"%";aS+=t}}else{if(aP[ad]==="fit"||ag===0){h.width=k+"%";al=b.createBox(al);b.addBox(al,av[ad].firstChild);al.style.left=0;al.style.right=b.Em(l-aj[ad]);a0+=aj[ad]-l;aS+=k}else{h.width=b.Em(aj[ad]);a0+=aj[ad]}}if(b.msieRelativeWidthBug){b.addText(al.firstChild,b.NBSP);al.firstChild.style.position="relative"}a0+=aA[ad];if(d[ad]!=="none"&&ad<ap&&ad!==aC){q=b.createBox(E);q.style.left=aS+"%";q=b.createRule(q,g,0,1.25/b.em);q.style.position="absolute";q.bbox={h:g,d:0,w:0,rw:1.25/b.em,lw:0};q.parentNode.bbox=ay.bbox;b.placeBox(q,a0-aA[ad]/2,aY,true);q.style.borderStyle=d[ad]}}}else{var T=aL;for(ad=0;ad<=ap;ad++){if(!av[ad].bbox.width){b.setStackWidth(av[ad],aj[ad])}if(aP[ad]!=="auto"&&aP[ad]!=="fit"){av[ad].bbox.width=aj[ad];av[ad].bbox.isFixed=true}b.placeBox(av[ad].parentNode,T,0);T+=aj[ad]+aA[ad];if(d[ad]!=="none"&&ad<ap&&ad!==aC){q=b.createRule(ay,g,0,1.25/b.em);b.addBox(ay,q);q.bbox={h:g,d:0,w:0,rw:1.25/b.em,lw:0};b.placeBox(q,T-aA[ad]/2,aY,true);q.style.borderStyle=d[ad]}}}ay.bbox.d=-aY;ay.bbox.h=g+aY;b.setStackWidth(ay,ay.bbox.w+aL);aZ=ay.bbox.w;var ah;if(I.frame!=="none"){ah=b.createFrame(ay,g,0,aZ,1.25/b.em,I.frame);b.addBox(ay,ah);b.placeBox(ah,0,aY,true);if(aM){ah.style.width="100%"}}S=ai;for(ae=0,ac=aw.length-1;ae<ac;ae++){o=Math.max(0,au[ae]+aq[ae+1]+aT[ae]);if(w[ae]!==a.LINES.NONE&&w[ae]!==""){q=b.createRule(ay,1.25/b.em,0,aZ);b.addBox(ay,q);q.bbox={h:1.25/b.em,d:0,w:aZ,rw:aZ,lw:0};b.placeBox(q,0,S-au[ae]-(o-au[ae]-aq[ae+1])/2,true);if(w[ae]===a.LINES.DASHED){q.style.borderTopStyle="dashed"}if(aM){q.style.width="100%"}}S-=o}if(aM){r.bbox.width=I.width;ay.style.width="100%"}if(av[aC]){var ax=ay.bbox.w;var ar=this.getValues("indentalignfirst","indentshiftfirst","indentalign","indentshift");if(ar.indentalignfirst!==a.INDENTALIGN.INDENTALIGN){ar.indentalign=ar.indentalignfirst}if(ar.indentalign===a.INDENTALIGN.AUTO){ar.indentalign=this.displayAlign}if(ar.indentshiftfirst!==a.INDENTSHIFT.INDENTSHIFT){ar.indentshift=ar.indentshiftfirst}if(ar.indentshift==="auto"){ar.indentshift="0"}var an=b.length2em(ar.indentshift,aB,b.cwidth);var aD=b.length2em(I.minlabelspacing,aB,b.cwidth);var aX=aD+av[aC].bbox.w,az=0,ak=ax;var aI=b.length2em(this.displayIndent,aB,b.cwidth);X=(e[aC]===a.INDENTALIGN.RIGHT?-1:1);if(ar.indentalign===a.INDENTALIGN.CENTER){ak+=2*(aX-X*(an+aI));an+=aI}else{if(e[aC]===ar.indentalign){if(aI<0){az=X*aI;aI=0}an+=X*aI;if(aX>X*an){an=X*aX}an+=az;ak+=X*an}else{ak+=aX-X*an+aI;an-=X*aI}}var aQ=b.createStack(r,false,"100%");b.addBox(aQ,ay);b.alignBox(ay,ar.indentalign,0,an);av[aC].parentNode.parentNode.removeChild(av[aC].parentNode);b.addBox(aQ,av[aC]);b.alignBox(av[aC],e[aC],0);if(b.msieRelativeWidthBug){ay.style.top=av[aC].style.top=""}if(aM){ay.style.width=I.width;r.bbox.width="100%"}av[aC].style[X===1?"marginLeft":"marginRight"]=b.Em(X*az);r.bbox.tw=ak;r.style.minWidth=r.bbox.minWidth=b.Em(ak);aQ.style.minWidth=aQ.bbox.minWidth=b.Em(ak/aJ)}if(!aM){this.HTMLhandleSpace(r)}var u=this.HTMLhandleColor(r);if(u&&aM){if(!ah){ah=b.createFrame(ay,g,0,aZ,0,"none");b.addBox(ay,ah);b.placeBox(ah,0,aY,true);ah.style.width="100%"}ah.style.backgroundColor=u.style.backgroundColor;ah.parentNode.insertBefore(ah,ah.parentNode.firstChild);u.parentNode.removeChild(u)}return r},HTMLhandleSpace:function(d){d.bbox.keepPadding=true;d.bbox.exact=true;if(!this.hasFrame&&d.bbox.width==null){d.firstChild.style.marginLeft=d.firstChild.style.marginRight=b.Em(1/6);d.bbox.w+=1/3;d.bbox.rw+=1/3;d.bbox.lw+=1/6}this.SUPER(arguments).HTMLhandleSpace.call(this,d)}});a.mtd.Augment({toHTML:function(e,d,g){e=this.HTMLcreateSpan(e);if(this.data[0]){var f=this.data[0].toHTML(e);if(g!=null){f=this.data[0].HTMLstretchV(e,d,g)}else{if(d!=null){f=this.data[0].HTMLstretchH(e,d)}}e.bbox=f.bbox}this.HTMLhandleSpace(e);this.HTMLhandleColor(e);return e},HTMLstretchH:a.mbase.HTMLstretchH,HTMLstretchV:a.mbase.HTMLstretchV});MathJax.Hub.Startup.signal.Post("HTML-CSS mtable Ready");MathJax.Ajax.loadComplete(b.autoloadDir+"/mtable.js")});
