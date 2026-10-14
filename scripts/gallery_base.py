"""Generate the original gallery sources. Rendering requires draw.io Desktop.
Run: python3 scripts/build_gallery.py
These are illustrative layouts, not a general-purpose auto-layout engine.
"""
from pathlib import Path
import xml.etree.ElementTree as E

OUT = Path(__file__).resolve().parents[1] / 'examples'
BLUE, TEAL, AMBER, GRAY = '#EAF2FF', '#E6F5F0', '#FFF3DA', '#F1F4F8'
class Diagram:
    def __init__(self, slug, title, subtitle, width=1120, height=700):
        self.slug = slug
        self.doc = E.Element('mxfile', host='drawio-everything')
        page = E.SubElement(self.doc, 'diagram', id=slug, name=title)
        model = E.SubElement(page, 'mxGraphModel', grid='1', gridSize='10', page='1', pageWidth=str(width), pageHeight=str(height))
        self.root = E.SubElement(model, 'root'); E.SubElement(self.root, 'mxCell', id='0'); E.SubElement(self.root, 'mxCell', id='1', parent='0')
        self.i = 1
        self.box('', 0, 0, width, height, '#FFFFFF', 'strokeColor=none;')
        self.text('DRAWIO / EVERYTHING', 40, 28, 1000, 24, 13, '#3973D6')
        self.text(title, 40, 66, 1040, 48, 30, '#172B4D', True)
        self.text(subtitle, 40, 121, 1040, 32, 15, '#5E6C84')
        self.text('原创示例 · 虚构业务内容  /  Editable in draw.io', 40, height-46, width-80, 22, 12, '#6B778C')
    def box(self, value, x, y, w=180, h=66, fill=BLUE, extra=''):
        self.i += 1; ident=f'n{self.i}'
        style=f'rounded=1;whiteSpace=wrap;html=0;fontFamily=Arial;fontSize=17;fontColor=#172B4D;fillColor={fill};strokeColor=#B8C6D9;arcSize=12;spacing=10;{extra}'
        cell=E.SubElement(self.root,'mxCell',id=ident,value=value,style=style,vertex='1',parent='1')
        E.SubElement(cell,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
        return ident
    def text(self,value,x,y,w,h,size=16,color='#172B4D',bold=False):
        return self.box(value,x,y,w,h,'none',f'strokeColor=none;align=left;verticalAlign=middle;spacing=0;fontSize={size};fontColor={color};fontStyle={1 if bold else 0};')
    def group(self,title,x,y,w,h,fill=GRAY):
        self.box('',x,y,w,h,fill,'strokeColor=none;arcSize=6;')
        self.text(title,x+20,y+12,w-40,30,17,'#344563',True)
    def edge(self,a,b,label='',extra='',points=None):
        self.i+=1
        c=E.SubElement(self.root,'mxCell',id=f'e{self.i}',value=label,style='edgeStyle=orthogonalEdgeStyle;rounded=1;arcSize=16;html=0;endArrow=block;endFill=1;strokeColor=#6B7F99;strokeWidth=1.5;fontFamily=Arial;fontSize=13;fontColor=#344563;labelBackgroundColor=#FFFFFF;'+extra,edge='1',parent='1',source=a,target=b)
        g=E.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
        if points:
            arr=E.SubElement(g,'Array',attrib={'as':'points'})
            for x,y in points: E.SubElement(arr,'mxPoint',x=str(x),y=str(y))
    def line(self,x1,y1,x2,y2,label='',extra=''):
        self.i+=1
        c=E.SubElement(self.root,'mxCell',id=f'e{self.i}',value=label,style='endArrow=none;strokeColor=#A5B4C7;fontFamily=Arial;fontSize=14;labelBackgroundColor=#FFFFFF;'+extra,edge='1',parent='1')
        g=E.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
        E.SubElement(g,'mxPoint',x=str(x1),y=str(y1),attrib={'as':'sourcePoint'}); E.SubElement(g,'mxPoint',x=str(x2),y=str(y2),attrib={'as':'targetPoint'})
    def save(self):
        E.indent(self.doc); E.ElementTree(self.doc).write(OUT/(self.slug+'.drawio'),encoding='utf-8',xml_declaration=True)

