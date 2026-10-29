"""Generate the submission pitch from actual deterministic application results.
Requires reportlab. Run node tools/export-sample.mjs first.
"""
import json, os
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT=Path(__file__).resolve().parent.parent
DATA=json.loads((ROOT/'tmp/demo-results.json').read_text())
OUT=ROOT/'submission'; OUT.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('Segoe','C:/Windows/Fonts/segoeui.ttf'))
pdfmetrics.registerFont(TTFont('SegoeBold','C:/Windows/Fonts/segoeuib.ttf'))
W,H=1280,720
NAVY='#172c30'; GREEN='#bfe998'; INK='#263c35'; MUTED='#71816b'; PAPER='#f5f6ef'
c=canvas.Canvas(str(OUT/'NxtGen-Pitch.pdf'),pagesize=(W,H))
c.setTitle('NxtGen Demand - Team NxtGen');c.setAuthor('Team NxtGen');c.setSubject('Customers, Channels & Demand submission pitch')

def rect(x,y,w,h,color):
    c.setFillColor(HexColor(color));c.rect(x,y,w,h,fill=1,stroke=0)
def text(s,x,y,size=22,color=INK,bold=False):
    c.setFillColor(HexColor(color));c.setFont('SegoeBold' if bold else 'Segoe',size);c.drawString(x,y,s)
def para(s,x,top,width=1050,size=23,color=MUTED,leading=None):
    style=ParagraphStyle('body',fontName='Segoe',fontSize=size,leading=leading or size*1.45,textColor=HexColor(color))
    p=Paragraph(s,style);_,height=p.wrap(width,600)
    if top-height<50:raise ValueError('Paragraph overflows page')
    p.drawOn(c,x,top-height);return top-height
def page(n,title,section):
    rect(0,0,W,H,PAPER);text('NxtGen.',64,657,21,INK,True);text(section.upper(),220,660,12,MUTED)
    text(title,64,566,43,INK,True);text('TEAM NXTGEN   /   CUSTOMERS, CHANNELS & DEMAND',64,30,10,MUTED);text(f'{n:02d} / 07',1163,30,11,MUTED)
def end():c.showPage()
def number(n):return f'{n:,}'

rect(0,0,W,H,NAVY)
text('CUSTOMERS, CHANNELS & DEMAND',70,640,14,GREEN)
text('NxtGen.',64,425,106,GREEN,True)
text('Customer demand, made clear.',70,345,38,'#f1f5ed')
para('A shared view of sales channels and a transparent plan for the next two weeks.',72,288,850,25,'#a9bcb1')
text('TEAM NXTGEN',72,80,15,GREEN,True);text('Working prototype  /  Synthetic demonstration',72,50,12,'#a9bcb1');end()

page(2,'The weekly planning gap','Problem')
text('WHO',65,475,13,MUTED,True);text('Small retail teams',65,428,30,INK,True)
para('Selling the same products through direct orders, marketplaces, social channels, and shops.',65,395,470,25)
text('WHAT THEY NEED TO KNOW',665,475,13,MUTED,True)
para('Which products are moving?<br/><br/>How does revenue compare with channel spend?<br/><br/>Could current stock cover the next two weeks?',665,430,520,26,INK)
para('Separate exports make these questions harder to answer in one place. This is our design hypothesis. Customer interviews and measured outcomes are future validation work.',65,140,1115,20);end()

page(3,'One CSV. A shared demand view.','Working product')
para('Import aggregate sales, compare the selected period, and export a plan with the assumptions attached.',65,500,1080,25)
stats=[('REVENUE (INR)',number(DATA['revenue'])),('ORDERS',number(DATA['orders'])),('UNITS SOLD',number(DATA['units']))]
for i,(label,value) in enumerate(stats):
    x=65+i*397;text(label,x,365,13,MUTED,True);text(value,x,305,49,INK,True)
para('Overview filters update the totals, daily trend, product ranking, and revenue mix. The latest date in the file anchors the reporting period.',65,238,1080,25)
para('Computed demo: 29 September to 26 October 2026. 672 synthetic source rows over 56 days. Amounts use INR. No real customer data.',65,115,1100,16);end()

page(4,'Channel efficiency, with context','Channel insights')
cols=[65,355,610,865,1070]
for label,x in zip(['CHANNEL','REVENUE (INR)','SPEND (INR)','REV / SPEND','COST / NEW'],cols):text(label,x,470,13,MUTED,True)
for i,a in enumerate(DATA['channels']):
    y=410-i*65
    for value,x in zip([a['channel'],number(a['revenue']),number(a['spend']),f"{a['roas']:.2f}x",f"{a['cac']:.0f}"],cols):text(value,x,y,24,INK,i==3)
    c.setStrokeColor(HexColor('#dce3d2'));c.line(65,y-20,1205,y-20)
para('In this synthetic example, Direct has the highest recorded revenue per rupee of spend. A team could review margin and capacity before testing a budget change.',65,158,1110,21)
para('Ratios are descriptive. They do not measure profit or causal attribution. Supplied new-customer counts can overlap across channels.',65,106,1110,14);end()

page(5,'A transparent two-week stock scenario','Demand planner')
f=DATA['forecast'];text(number(f['total'])+' projected units',65,475,36,INK,True)
para('Recent weekday pattern + a capped weekly trend',65,430,750,22)
points=f['points']; left,right,bottom,top=70,810,175,365;mx=max(p['high'] for p in points)*1.08
c.setStrokeColor(HexColor('#dbe4d1'));c.line(left,bottom,right,bottom)
for i,p in enumerate(points):
    x=left+i*(right-left)/(len(points)-1);barw=26; y=bottom+p['units']/mx*(top-bottom)
    rect(x-13,bottom,barw,y-bottom,'#9bbd7a')
    if i in [0,6,13]:text(p['date'][5:],x-20,bottom-28,13,MUTED)
text('1,000 units available',900,345,22,INK,True);para(number(f['total']-1000)+' units below the baseline',900,310,300,23)
text('10,000 units available',900,225,22,INK,True);para(number(10000-f['total'])+' units above the baseline',900,190,300,23)
para('At least 14 observed dates required. Weekly trend capped at +/-25%. The +/-20% planning band is not a confidence interval. Review SKU stock and lead times before ordering.',65,104,1110,17);end()

page(6,'Simple to run. Private by design.','Implementation')
text('BROWSER APPLICATION',65,470,13,MUTED,True)
para('Static HTML, CSS, and JavaScript modules.<br/>No API key, database, or dependency installation.<br/>Imported CSV stays in memory for the session.',65,432,1020,27,INK)
text('RELIABILITY',65,255,13,MUTED,True)
para('Nine automated tests cover parsing, input validation, date windows, aggregation, and forecast edge cases. The local server responds successfully.',65,219,1070,25,INK)
para('Prototype scope: aggregate CSV analysis. Commerce connectors, customer deduplication, and automated purchasing are future work.',65,106,1090,17);end()

page(7,'A clear next step for validation','Scope and handoff')
text('AVAILABLE NOW',65,470,13,MUTED,True)
para('Working application and source code<br/>CSV import and downloadable action plan<br/>Setup guide, deployment workflow, and MIT license',65,432,1040,27,INK)
text('NEXT VALIDATION',65,267,13,MUTED,True)
para('Test the planning workflow with retailers. Backtest against a seasonal-naive baseline. Add product-level inventory and supplier lead times before a stock-planning pilot.',65,229,1080,25)
text('github.com/Ejaz0331/NxtGen',65,87,22,INK,True)
c.linkURL('https://github.com/Ejaz0331/NxtGen',(65,80,580,115),relative=0)
end();c.save()

narration=[
 'Meet NxtGen Demand, a working customer demand dashboard for small retail teams. It brings sales channels into a shared view and helps a team plan the next two weeks. This walkthrough uses synthetic data and computed application outputs.',
 'A retailer selling through several channels needs to know which products are moving, how revenue compares with channel spending, and whether stock could cover upcoming demand. NxtGen starts from a simple aggregate sales export. The problem is a design hypothesis that still needs customer validation.',
 f"The Overview offers period, channel, and product filters. For the sample period from September twenty ninth to October twenty sixth, the engine calculates {DATA['orders']} orders and {DATA['units']} units sold. The revenue total shown here is in Indian rupees. The same selection drives product rankings and the demand chart.",
 'Channel insights compares recorded revenue and spending. In this example, Direct has the highest revenue per rupee of recorded spend. The comparison can guide a margin and capacity review, but does not establish profit or marketing attribution. New customer counts can overlap between channels.',
 f"The demand planner projects {f['total']} units over the next fourteen days. It repeats the latest weekly pattern with a capped trend adjustment. Entering one thousand units available shows a baseline shortage. Ten thousand units shows a surplus. The planning range is illustrative and is not a statistical confidence interval.",
 'The app runs with Node and a browser, with no API keys or dependency installation. CSV validation checks dates and numeric counts. Imported data stays in memory and resets on refresh. Nine automated tests pass. This video presents computed results rather than a recorded browser session.',
 'The handoff includes source code, a sample CSV, an action plan export, setup and deployment instructions, a pitch PDF, and an MIT license. Next, we would test with retailers and backtest the forecast before an inventory pilot. NxtGen makes the assumptions visible so teams can review the next decision.'
]
(ROOT/'tmp/narration.json').write_text(json.dumps(narration),encoding='utf-8')
(ROOT/'docs/DEMO_SCRIPT.md').write_text('# Demo walkthrough script\n\nThis narrated walkthrough uses deterministic sample outputs. It is not a browser screen recording.\n\n'+ '\n\n'.join(f'## Scene {i+1}\n\n{s}' for i,s in enumerate(narration))+'\n',encoding='utf-8')
print('Created submission/NxtGen-Pitch.pdf and narration source.')
