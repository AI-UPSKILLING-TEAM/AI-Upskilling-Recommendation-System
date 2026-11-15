"""Build the review report from the authoritative Markdown and measured evidence."""
from pathlib import Path
import re,json,sys
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,KeepTogether,Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing,Rect,String,Line,Polygon

ROOT=Path(__file__).resolve().parents[1]
font=Path('C:/Windows/Fonts/segoeui.ttf');bold=Path('C:/Windows/Fonts/segoeuib.ttf')
if font.exists() and bold.exists():
 pdfmetrics.registerFont(TTFont('Body',str(font)));pdfmetrics.registerFont(TTFont('BodyBold',str(bold)))
 pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='Body',boldItalic='BodyBold')
else:
 pdfmetrics.registerFontFamily('Body',normal='Helvetica',bold='Helvetica-Bold',italic='Helvetica-Oblique',boldItalic='Helvetica-BoldOblique')
 # Alias via style selection when portable fonts are unavailable.
FONT='Body' if font.exists() and bold.exists() else 'Helvetica'
BOLD='BodyBold' if FONT=='Body' else 'Helvetica-Bold'
styles=getSampleStyleSheet()
for key in ['BodyText','Normal']:styles[key].fontName=FONT
styles.add(ParagraphStyle(name='BodyCustom',fontName=FONT,fontSize=9.2,leading=13.6,spaceAfter=6))
styles.add(ParagraphStyle(name='H1Custom',fontName=BOLD,fontSize=22,leading=28,textColor=colors.HexColor('#10223c'),spaceAfter=16))
styles.add(ParagraphStyle(name='H2Custom',fontName=BOLD,fontSize=13,leading=18,textColor=colors.HexColor('#205ac3'),spaceBefore=13,spaceAfter=7,keepWithNext=True))
styles.add(ParagraphStyle(name='TableCustom',fontName=FONT,fontSize=7.2,leading=10,spaceAfter=0,wordWrap='CJK'))
styles.add(ParagraphStyle(name='SmallCustom',fontName=FONT,fontSize=8,leading=11,textColor=colors.HexColor('#56657b'),spaceAfter=6))
styles.add(ParagraphStyle(name='CoverCustom',fontName=BOLD,fontSize=31,leading=38,textColor=colors.HexColor('#10223c'),spaceAfter=16))

def inline(value):
 value=escape(value).replace('–','-').replace('—','-').replace('’',"'").replace('“','"').replace('”','"')
 value=re.sub(r'`([^`]+)`',r'<font color="#205ac3">\1</font>',value)
 value=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',value)
 value=re.sub(r'\[([^]]+)\]\(([^)]+)\)',r'\1 (\2)',value)
 return value

def para(text,style='BodyCustom'):return Paragraph(inline(text),styles[style])

def table(rows):
 count=len(rows[0]);width=507
 if count==4 and rows[0][0].strip()=='ID':widths=[43,186,170,108]
 elif count==5:widths=[37,132,40,35,263]
 else:widths=[width/count]*count
 data=[[para(cell.strip(),'TableCustom') for cell in row] for row in rows]
 t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6edf9')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#9fb2cd')),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#dce4ef')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f7f9fc')]),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7)]))
 return t

def markdown(path):
 lines=path.read_text(encoding='utf-8-sig').splitlines();items=[];i=0
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    row=lines[i].strip().strip('|').split('|')
    if not all(re.fullmatch(r'\s*:?-+:?\s*',x) for x in row):rows.append(row)
    i+=1
   items.append(table(rows));items.append(Spacer(1,8));continue
  if line.startswith('## '):items.append(para(line[3:],'H2Custom'))
  elif line.startswith('# '):items.append(para(line[2:],'H1Custom'))
  elif line.startswith('```'):
   code=[];i+=1
   while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
   items.append(para(' / '.join(code),'SmallCustom'))
  else:items.append(para(line))
  i+=1
 return items

def architecture():
 d=Drawing(507,265)
 boxes=[(12,180,150,65,'Browser client','Forms / dashboard'),(195,180,150,65,'Python API','Auth / data / validation'),(195,75,150,65,'Recommendation module','Gap analysis / TF-IDF'),(375,75,120,65,'SQLite','Persistent state')]
 for x,y,w,h,title,desc in boxes:
  d.add(Rect(x,y,w,h,rx=8,ry=8,fillColor=colors.HexColor('#eef3fb'),strokeColor=colors.HexColor('#9fb2cd')))
  d.add(String(x+w/2,y+h-24,title,fontName=BOLD,fontSize=10,textAnchor='middle',fillColor=colors.HexColor('#10223c')))
  d.add(String(x+w/2,y+18,desc,fontName=FONT,fontSize=8,textAnchor='middle',fillColor=colors.HexColor('#56657b')))
 for x1,y1,x2,y2 in [(162,212,195,212),(270,180,270,140),(345,105,375,105)]:
  d.add(Line(x1,y1,x2,y2,strokeColor=colors.HexColor('#205ac3'),strokeWidth=1.6))
 d.add(String(12,20,'Local coursework deployment: browser -> same-origin API -> SQLite',fontName=FONT,fontSize=10,fillColor=colors.HexColor('#10223c')))
 return d

def footer(c,doc):
 c.saveState();w,h=A4;c.setStrokeColor(colors.HexColor('#dce4ef'));c.line(44,38,w-44,38);c.setFont(FONT,7.5);c.setFillColor(colors.HexColor('#56657b'));c.drawString(44,25,'Project 22 | Candidate updated 26 October 2026');c.drawRightString(w-44,25,str(doc.page));c.restoreState()

def build(output):
 story=[Spacer(1,30),para('SOFTWARE ENGINEERING MINI-PROJECT','SmallCustom'),para('AI-Powered Upskilling\nRecommendation System'.replace('\n','<br/>'),'CoverCustom')]
 # Cover uses safe explicit HTML for its line break.
 story[-1]=Paragraph('AI-Powered Upskilling<br/>Recommendation System',styles['CoverCustom'])
 story.extend([para('Project 22 - Implementation and Review Package','H2Custom'),para('PES University | Computer Science and Engineering (AI & ML)'),Spacer(1,20),table([['Team member','SRN'],['Poojitha V','PES2UG24AM113'],['Manasa C','PES2UG25AM803'],['Shanmuga','PES2UG24AM083'],['Manish S','PES2UG24AM085']]),Spacer(1,20),para('Updated 26 October 2026. Includes a working application, newly created architecture and test plan, full SRS traceability, actual test evidence, sprint planning and demo recordings.'),para('Independent teammate review, owner merge and formal sprint acceptance/freeze remain genuine team process actions. Sprint 1 material is recovery evidence; the final Sprint 2 working demo was captured on 26 October. Approval-gated merge and release are prepared.','SmallCustom'),PageBreak(),para('Review map','H1Custom'),para('Read the measured verification results first, then review the architecture, acceptance plan and all 48 requirement mappings. The user manual provides exact run and demonstration steps. Process decisions and limitations are included, with no backdated approvals.'),architecture(),para('Source documents','H2Custom'),para('SRS_Project_ID_22.pdf: 15 pages, original functional and non-functional requirements, use-case diagram and ER diagram. SE_Mini_Project_Delivereables_Part-2.pdf: backlog, sprint, PR/Actions, recording, documentation and freeze requirements. The new SAD/Test Plan document the actual code; the earlier submitted versions were unavailable.'),PageBreak()])
 for name in ['TEST_EVIDENCE.md','SAD.md','TEST_PLAN.md','REQUIREMENTS_TRACEABILITY.md','SPRINT_PLAN.md','USER_MANUAL.md','RECOMMENDER_METHOD_AND_LIMITS.md','DEMO_RECORDING_GUIDE.md','DEVIATIONS_AND_PENDING.md','RELEASE_AND_FREEZE_CHECKLIST.md']:
  story.extend(markdown(ROOT/'docs'/name));story.append(PageBreak())
 story.extend([para('Reference-link audit','H1Custom'),para('All 19 reference links returned HTTP 200 at the recorded audit. Availability may change. This is a reachability check, not credential eligibility or course accreditation review.')])
 audit=json.loads((ROOT/'evidence/link-audit.json').read_text())
 story.append(table([['Reference','URL','Status']]+[[r['title'],r['url'],str(r.get('status',r['result']))] for r in audit]))
 doc=SimpleDocTemplate(str(output),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=44,bottomMargin=51,title='Project 22 - Complete Implementation and Review Package',author='AI Upskilling Team')
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
if __name__=='__main__':
 output=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'Project_22_Report.pdf';output.parent.mkdir(parents=True,exist_ok=True);build(output);print(output)
