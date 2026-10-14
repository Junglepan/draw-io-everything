"""Generate the original gallery sources. Rendering requires draw.io Desktop.
Run: python3 scripts/build_gallery.py
These are illustrative layouts, not a general-purpose auto-layout engine.
"""
from pathlib import Path
import xml.etree.ElementTree as E

OUT = Path(__file__).resolve().parents[1] / 'examples'
BLUE, TEAL, AMBER, GRAY = '#EAF2FF', '#E6F5F0', '#FFF3DA', '#F1F4F8'
class Diagram:
    def __init__(self, slug, title, subtitle):
        self.slug = slug
        self.doc = E.Element('mxfile', host='drawio-everything')
        page = E.SubElement(self.doc, 'diagram', id=slug, name=title)
        model = E.SubElement(page, 'mxGraphModel', grid='1', gridSize='10', page='1', pageWidth='1120', pageHeight='700')
        self.root = E.SubElement(model, 'root'); E.SubElement(self.root, 'mxCell', id='0'); E.SubElement(self.root, 'mxCell', id='1', parent='0')
        self.i = 1
        self.box('', 0, 0, 1120, 700, '#FFFFFF', 'strokeColor=none;')
        self.text('DRAWIO / EVERYTHING', 40, 28, 1000, 24, 13, '#3973D6')
        self.text(title, 40, 66, 1040, 48, 30, '#172B4D', True)
        self.text(subtitle, 40, 121, 1040, 32, 15, '#5E6C84')
        self.text('原创示例 · 虚构业务内容  /  Editable in draw.io', 40, 654, 1040, 22, 12, '#6B778C')
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
        c=E.SubElement(self.root,'mxCell',id=f'e{self.i}',value=label,style='edgeStyle=orthogonalEdgeStyle;rounded=0;html=0;endArrow=block;endFill=1;strokeColor=#6B7F99;strokeWidth=1.5;fontFamily=Arial;fontSize=13;fontColor=#344563;labelBackgroundColor=#FFFFFF;'+extra,edge='1',parent='1',source=a,target=b)
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

# 01 — Main axis with explicitly labelled alternative branches.
d=Diagram('01-flow','流程图 · 清晰的判断与汇合','单一阅读方向 / 条件贴近分支 / 结果回归主线')
a=d.box('收到申请',60,310,150,60,TEAL,'rounded=1;arcSize=50;'); b=d.box('资料完整？',280,280,140,120,AMBER,'shape=rhombus;'); c=d.box('自动校验',510,230); e=d.box('补充资料',510,420); f=d.box('进入人工审核',830,310,210,70)
d.edge(a,b);d.edge(b,c,'是');d.edge(b,e,'否');d.edge(c,f,'校验通过');d.edge(e,f,'补充完成');d.save()
# 02 — Responsibility lanes (not a claim of BPMN conformance).
d=Diagram('02-swimlane','泳道图 · 看清每一次交接','责任分区 / 阶段对齐 / 跨角色流程')
for y,t,c in [(190,'申请人',BLUE),(330,'业务系统',TEAL),(470,'审核人',AMBER)]:
 d.group(t,40,y,1040,125,c)
a=d.box('提交申请',240,230,160,55,'#FFFFFF');b=d.box('检查必填项',480,370,160,55,'#FFFFFF');c=d.box('确认并归档',880,370,160,55,'#FFFFFF');e=d.box('审核申请',700,510,160,55,'#FFFFFF')
d.edge(a,b,'提交');d.edge(b,e,'完整');d.edge(e,c,'批准');d.save()
# 03 — Boundaries first.
d=Diagram('03-cloud','部署架构 · 先边界，后组件','示意环境 / 网络边界明确 / 重复实例保持一致')
d.group('生产网络 · 单区域示意',260,190,810,400)
d.group('接入区',280,250,220,300,BLUE);d.group('应用区',520,250,240,300,TEAL);d.group('数据区',780,250,270,300,AMBER)
a=d.box('外部客户端',40,350,180,70);b=d.box('负载均衡',300,350,180,70,'#FFFFFF');c=d.box('服务实例 A',550,320,180,65,'#FFFFFF');e=d.box('服务实例 B',550,430,180,65,'#FFFFFF');f=d.box('业务数据库',820,365,190,80,'#FFFFFF','shape=cylinder;')
d.edge(a,b,'HTTPS');d.edge(b,c,extra='exitX=1;exitY=0.3;entryX=0;entryY=0.5;');d.edge(b,e,extra='exitX=1;exitY=0.7;entryX=0;entryY=0.5;',points=[(510,400),(510,462)]);d.edge(c,f,'读写',extra='exitX=1;exitY=0.5;entryX=0;entryY=0.3;');d.edge(e,f,extra='exitX=1;exitY=0.5;entryX=0;entryY=0.7;');d.save()
# 04 — Repeated units, distinct control plane.
d=Diagram('04-cluster','集群组件 · 重复结构与控制关系','同构节点 / 独立控制面 / 控制关系不等于业务请求')
d.group('控制面（简化）',40,200,300,400,BLUE);a=d.box('API Server',100,290,180,65,'#FFFFFF');b=d.box('Scheduler',100,415,180,65,'#FFFFFF');d.edge(b,a,'API')
for x,i in [(420,1),(770,2)]:
 d.group(f'工作节点 {i}',x,200,310,400,TEAL); k=d.box('kubelet',x+60,290,190,65,'#FFFFFF');d.box('应用 Pod',x+60,415,190,65,'#FFFFFF');d.edge(k,a,'注册 / 状态','dashed=1;exitX=0.5;exitY=0;entryX=0.5;entryY=0;',points=[(x+155,160 if i==2 else 250),(190,160 if i==2 else 250)])
d.text('虚线：组件间控制 API 通信；省略内部组件与应用流量。',60,612,990,24,13);d.save()
# 05 — Fixed-coordinate sequence messages.
d=Diagram('05-sequence','时序图 · 分阶段讲清交互','参与者列 / 时间自上而下 / 请求与返回分离')
xs=[150,420,690,960]
for x,t in zip(xs,['用户','订单服务','库存服务','通知服务']):
 d.box(t,x-90,190,180,55,BLUE);d.line(x,245,x,600,extra='dashed=1;')
d.box('01  创建订单',60,260,1000,34,GRAY,'strokeColor=none;align=left;fontSize=13;')
d.line(150,325,420,325,'提交订单','endArrow=block;endFill=1;');d.line(420,380,690,380,'预留库存','endArrow=block;endFill=1;');d.line(690,435,420,435,'预留成功','dashed=1;endArrow=open;')
d.box('02  通知与响应',60,470,1000,34,GRAY,'strokeColor=none;align=left;fontSize=13;');d.line(420,535,960,535,'异步发布创建事件','endArrow=open;');d.line(420,585,150,585,'返回订单编号','dashed=1;endArrow=open;');d.save()
# 06 — Context, homogeneous abstraction.
d=Diagram('06-context','系统上下文 · 聚焦一个系统','人和系统 / 关系说明 / 责任边界')
d.group('业务组织边界',280,200,550,400,GRAY)
a=d.box('客户\n[人员]\n查询与提交订单',40,335,190,110,TEAL);b=d.box('订单平台\n[软件系统]\n管理订单全生命周期',440,330,240,120,BLUE);c=d.box('支付平台\n[外部系统]\n处理支付交易',870,235,210,110,AMBER);e=d.box('配送平台\n[外部系统]\n安排履约配送',870,465,210,110,AMBER)
d.edge(a,b,'下单 / 查询');d.edge(b,c,'发起支付');d.edge(b,e,'提交配送任务');d.save()
# 07 — Ownership by containment, one colour dimension.
d=Diagram('07-application','应用资产 · 归属与状态各司其职','业务能力分组 / 等尺寸卡片 / 单一状态维度')
for x,t,apps in [(40,'客户经营',['客户门户','会员中心','活动管理']),(400,'交易履约',['订单中心','库存管理','配送调度']),(760,'经营分析',['指标平台','报表中心','旧版看板'])]:
 d.group(t,x,200,320,360)
 for i,label in enumerate(apps):
  retiring=label=='旧版看板';d.box(label+('\n△ 计划退役' if retiring else '\n● 使用中'),x+30,265+i*90,260,70,AMBER if retiring else TEAL)
d.text('● 使用中     △ 计划退役     |     卡片面积不表示成本或重要性',60,590,1000,35,15);d.save()
# 08 — Column lineage with an explicit focus.
d=Diagram('08-lineage','数据血缘 · 从资产定位到字段路径','横向上下游 / 局部字段展开 / 聚焦一条影响路径')
ports=[]
for x,title,fields in [(40,'原始订单',['order_id','amount']),(420,'清洗订单',['order_id','net_amount']),(800,'销售指标',['date','revenue'])]:
 d.group(title,x,230,280,310)
 d.text('数据表 / 展开相关字段',x+20,280,240,30,13,'#5E6C84')
 d.box(fields[0],x+20,335,240,55,'#FFFFFF')
 ports.append(d.box(fields[1],x+20,430,240,65,BLUE,'strokeColor=#3973D6;strokeWidth=2;'))
d.edge(ports[0],ports[1],'清洗','strokeColor=#3973D6;strokeWidth=2;');d.edge(ports[1],ports[2],'按日聚合','strokeColor=#3973D6;strokeWidth=2;');d.text('当前关注：金额 → 净额 → 收入；仅展示与此路径相关的字段。',60,580,1000,35,15);d.save()
# 09 — Backbone with local access zones.
d=Diagram('09-network','网络拓扑 · 稳定骨干与局部接入','物理区域分组 / 共享走线通道 / 连接不表示流量方向')
d.group('共享骨干',830,200,240,400,BLUE); core=d.box('核心交换机',860,360,180,80,'#FFFFFF')
for y,title in [(200,'区域 A'),(420,'区域 B')]:
 d.group(title,40,y,720,180,TEAL);a=d.box('终端 1',80,y+70,160,65,'#FFFFFF');b=d.box('终端 2',300,y+70,160,65,'#FFFFFF');s=d.box('接入交换机',540,y+70,180,65,'#FFFFFF');d.edge(a,s,extra='endArrow=none;exitX=0.5;exitY=1;entryX=0.5;entryY=1;',points=[(160,y+155),(630,y+155)]);d.edge(b,s,extra='endArrow=none;');d.edge(s,core,'上联','endArrow=none;')
d.save()
# 10 — Capability catalogue.
d=Diagram('10-capability','业务能力 · 用网格建立目录秩序','能力以名词命名 / 同层对齐 / 说明区独立')
for x,title,items in [(40,'客户管理',['客户识别','客户服务','权益管理']),(310,'交易管理',['订单管理','支付管理','售后管理']),(580,'履约管理',['库存管理','配送管理','履约监控'])]:
 d.group(title,x,200,240,400,BLUE)
 for i,t in enumerate(items): d.box(t,x+20,275+i*95,200,65,'#FFFFFF')
d.group('阅读说明',850,200,230,400,TEAL);d.text('列：一级能力\n\n卡片：二级能力\n\n位置表示归属\n\n本图不表达流程',875,270,180,260,16);d.save()
# 11 — Three regions, fan-in and fan-out.
d=Diagram('11-pipeline','数据流水线 · 输入、处理与消费','两翼汇聚与分发 / 中间主链路 / 阶段职责明确')
d.group('输入',40,220,230,350,BLUE);d.group('批处理流水线',310,220,500,350,TEAL);d.group('消费',850,220,230,350,AMBER)
a=d.box('业务数据',65,305,180,65,'#FFFFFF');b=d.box('事件日志',65,445,180,65,'#FFFFFF');c=d.box('抽取',330,370,130,70,'#FFFFFF');e=d.box('清洗',495,370,130,70,'#FFFFFF');f=d.box('汇总',660,370,130,70,'#FFFFFF');g=d.box('经营报表',875,305,180,65,'#FFFFFF');h=d.box('分析数据集',875,445,180,65,'#FFFFFF')
for u,v in [(a,c),(b,c),(c,e),(e,f),(f,g),(f,h)]:d.edge(u,v)
d.save()
print('Generated 11 editable diagrams.')
