export const FIELDS = ['date','channel','product','orders','units','revenue','spend','new_customers'];
export function sampleData() {
  const rows=[];
  for(let d=0;d<56;d++) for(let c=0;c<4;c++) for(let p=0;p<3;p++) {
    const date=new Date(Date.UTC(2026,8,1+d)).toISOString().slice(0,10);
    const orders=Math.max(1,Math.round((8+c*3+p*2)*(1+d/150)*(1+[.04,-.09,-.04,.02,.1,.32,.23][d%7])+(d*7+c*3+p)%5));
    const units=orders+Math.round(orders*.28), revenue=units*[450,780,1200][p];
    rows.push({date,channel:['Direct','Marketplace','Social','Retail'][c],product:['Everyday tee','Canvas tote','Weekend hoodie'][p],orders,units,revenue,spend:Math.round(revenue*[.07,.18,.25,.12][c]),new_customers:Math.round(orders*[.32,.61,.75,.24][c])});
  }
  return rows;
}
export function parseCSV(text) {
  if(text.length>5_000_000) throw Error('File exceeds the 5 MB limit.');
  const records=[]; let row=[],cell='',quoted=false;
  text=text.replace(/^\uFEFF/,'');
  for(let i=0;i<text.length;i++) {const ch=text[i];
    if(ch==='"') {if(quoted&&text[i+1]==='"'){cell+='"';i++;}else if(quoted||cell==='') quoted=!quoted; else throw Error('Unexpected quote in CSV.');}
    else if(ch===','&&!quoted){row.push(cell);cell='';}
    else if((ch==='\n'||ch==='\r')&&!quoted){if(ch==='\r'&&text[i+1]==='\n')i++; row.push(cell);if(row.some(x=>x.trim()))records.push(row);row=[];cell='';}
    else cell+=ch;
  }
  if(quoted)throw Error('CSV has an unclosed quoted field.');
  row.push(cell);if(row.some(x=>x.trim()))records.push(row);
  const headers=(records.shift()||[]).map(x=>x.trim());
  if(headers.length!==FIELDS.length||FIELDS.some(x=>!headers.includes(x)))throw Error('Use the eight column names in the sample CSV.');
  if(!records.length||records.length>50000)throw Error('CSV must contain 1 to 50,000 data rows.');
  const result=records.map((values,i)=>{
    if(values.length!==headers.length)throw Error(`Row ${i+2}: incorrect column count.`);
    const r=Object.fromEntries(headers.map((h,j)=>[h,values[j].trim()]));
    if(!/^\d{4}-\d{2}-\d{2}$/.test(r.date)||Number.isNaN(Date.parse(r.date+'T00:00:00Z'))||new Date(r.date+'T00:00:00Z').toISOString().slice(0,10)!==r.date)throw Error(`Row ${i+2}: use a valid YYYY-MM-DD date.`);
    if(!r.channel||!r.product||r.channel.length>80||r.product.length>80)throw Error(`Row ${i+2}: channel and product need 1 to 80 characters.`);
    for(const key of FIELDS.slice(3)){if(r[key]===''||!Number.isFinite(Number(r[key]))||Number(r[key])<0||Number(r[key])>1e12)throw Error(`Row ${i+2}: ${key} must be a nonnegative number.`);r[key]=Number(r[key]);}
    if(['orders','units','new_customers'].some(k=>!Number.isInteger(r[k])))throw Error(`Row ${i+2}: counts must be whole numbers.`);
    if(r.units<r.orders||r.new_customers>r.orders)throw Error(`Row ${i+2}: units must be at least orders, and new customers cannot exceed orders.`);
    return r;
  });
  return result;
}
export function csv(rows){return [FIELDS.join(','),...rows.map(r=>FIELDS.map(k=>'"'+String(r[k]).replaceAll('"','""')+'"').join(','))].join('\r\n');}
export const sum=(rows,key)=>rows.reduce((s,r)=>s+r[key],0);
export function select(rows,{channel='All',product='All',days=28}={}) {
  const end=rows.reduce((m,r)=>r.date>m?r.date:m,'');
  const shift=n=>new Date(Date.parse(end+'T00:00:00Z')-n*86400000).toISOString().slice(0,10);
  const start=shift(days-1),previous=shift(days*2-1);
  const matching=rows.filter(r=>(channel==='All'||r.channel===channel)&&(product==='All'||r.product===product));
  return {end,start,current:matching.filter(r=>r.date>=start),previous:matching.filter(r=>r.date>=previous&&r.date<start),all:matching};
}
export function daily(rows,start,end){const map=new Map();for(const r of rows)map.set(r.date,(map.get(r.date)||0)+r.units);const out=[];for(let t=Date.parse(start+'T00:00:00Z');t<=Date.parse(end+'T00:00:00Z');t+=86400000){const date=new Date(t).toISOString().slice(0,10);out.push({date,units:map.get(date)||0});}return out;}
export function forecast(rows,end,horizon=14){
  if(!rows.length)return {points:[],total:0,growth:0};
  const start=new Date(Date.parse(end+'T00:00:00Z')-27*86400000).toISOString().slice(0,10);
  const observedDays=new Set(rows.filter(r=>r.date>=start&&r.date<=end).map(r=>r.date)).size;
  if(observedDays<14)return {points:[],total:0,growth:0};
  const history=daily(rows,start,end),last=history.slice(-7),before=history.slice(-14,-7);
  const mean=sum(last,'units')/7,prior=sum(before,'units')/7;
  const growth=prior?Math.max(-.25,Math.min(.25,mean/prior-1)):0;
  const points=Array.from({length:horizon},(_,i)=>{
    const date=new Date(Date.parse(end+'T00:00:00Z')+(i+1)*86400000).toISOString().slice(0,10);
    const units=Math.round(last[i%7].units*(1+growth*((i+1)/7)));
    return {date,units,low:Math.floor(units*.8),high:Math.ceil(units*1.2)};
  });return {points,total:sum(points,'units'),growth};
}
export function channels(rows){return [...new Set(rows.map(r=>r.channel))].map(channel=>{const r=rows.filter(x=>x.channel===channel);const revenue=sum(r,'revenue'),spend=sum(r,'spend'),customers=sum(r,'new_customers');return {channel,orders:sum(r,'orders'),revenue,spend,customers,roas:spend?revenue/spend:null,cac:customers?spend/customers:null};}).sort((a,b)=>b.revenue-a.revenue);}
