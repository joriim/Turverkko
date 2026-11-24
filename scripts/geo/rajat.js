const tc=require('./tc/package/dist/topojson-client.js');
const topo=require('./package/countries-50m.json');
const fc=tc.feature(topo,topo.objects.countries);
const keep={"246":"FI","752":"SE","233":"EE","428":"LV","372":"IE","276":"DE","826":"GB","578":"NO","208":"DK","440":"LT","528":"NL","616":"PL","643":"RU","112":"BY","056":"BE","250":"FR","040":"AT","203":"CZ","756":"CH","442":"LU"};
const B=[-11.5,47.5,33,71.5], out={};
const inb=([x,y])=>x>=B[0]&&x<=B[2]&&y>=B[1]&&y<=B[3];
for(const f of fc.features){const c=keep[f.id]; if(!c) continue;
 const polys=f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.coordinates;
 const rings=[];
 for(const p of polys){const r=p[0]; if(!r.some(inb)) continue;
   let pts=[],last=null; for(const [x,y] of r){const q=[Math.round(Math.max(B[0],Math.min(B[2],x))*10)/10,Math.round(Math.max(B[1],Math.min(B[3],y))*10)/10]; if(!last||q[0]!==last[0]||q[1]!==last[1]){pts.push(q);last=q}}
   if(pts.length<4) continue;
   // area filter
   let a=0;for(let i=0;i<pts.length;i++){const [x1,y1]=pts[i],[x2,y2]=pts[(i+1)%pts.length];a+=x1*y2-x2*y1}
   if(Math.abs(a)/2<0.02) continue;
   rings.push(pts.flat().map(v=>+v.toFixed(1)));}
 if(rings.length) out[c]=rings;}
const s=JSON.stringify(out);
require('fs').writeFileSync('geo.json',s); console.log(s.length, Object.keys(out).map(k=>k+':'+out[k].length).join(' '));
