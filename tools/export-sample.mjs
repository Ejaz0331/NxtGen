import {writeFileSync,mkdirSync} from 'node:fs';
import {sampleData,csv,select,sum,channels,forecast} from '../app/dist/engine.js';
const rows=sampleData(),s=select(rows),f=forecast(rows,s.end);
writeFileSync(new URL('../app/dist/sample.csv',import.meta.url),csv(rows));
mkdirSync(new URL('../tmp/',import.meta.url),{recursive:true});
writeFileSync(new URL('../tmp/demo-results.json',import.meta.url),JSON.stringify({rows:rows.length,start:s.start,end:s.end,revenue:sum(s.current,'revenue'),orders:sum(s.current,'orders'),units:sum(s.current,'units'),newCustomers:sum(s.current,'new_customers'),channels:channels(s.current),forecast:f},null,2));
console.log('Sample CSV and computed demonstration results written.');
