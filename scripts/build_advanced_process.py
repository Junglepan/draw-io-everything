#!/usr/bin/env python3
"""Original fictional process examples; editable draw.io XML, standard library only.
BPMN notation subset: https://www.omg.org/bpmn/Documents/BPMN_Section_3CMP.pdf
https://docs.camunda.io/docs/components/modeler/bpmn/bpmn-primer/
No executable BPMN or comprehensive conformance certification is claimed.
"""
from pathlib import Path
import xml.etree.ElementTree as E

OUT = Path(__file__).resolve().parents[1] / 'examples' / 'advanced'
INK='#263238'; MUTED='#64717A'; BLUE='#176B87'; ORANGE='#A65C20'
class Diagram:
    def __init__(self,name,w,h):
        self.name=name; self.w=w; self.h=h; self.n=0
        self.doc=E.Element('mxfile',host='app.diagrams.net',type='device')
        d=E.SubElement(self.doc,'diagram',id=name,name=name)
        m=E.SubElement(d,'mxGraphModel',dx=str(w),dy=str(h),grid='1',gridSize='10',page='1',pageScale='1',pageWidth=str(w),pageHeight=str(h),background='#FFFFFF')
        self.root=E.SubElement(m,'root'); E.SubElement(self.root,'mxCell',id='0'); E.SubElement(self.root,'mxCell',id='1',parent='0')
    def node(self,id,text,x,y,w,h,style=''):
        c=E.SubElement(self.root,'mxCell',id=id,value=text,vertex='1',parent='1',style='html=1;whiteSpace=wrap;fontFamily=Helvetica;fontSize=18;fontColor='+INK+';strokeColor='+INK+';strokeWidth=1.5;fillColor=#FFFFFF;'+style)
        E.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
        return id
    def text(self,id,text,x,y,w,h=30,size=18,color=INK):
        return self.node(id,text,x,y,w,h,f'text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize={size};fontColor={color};')
    def task(self,id,title,sub,x,y,w=170):
        return self.node(id,f'<b>{title}</b><br><font color="{MUTED}" style="font-size:13px">{sub}</font>',x,y,w,72,'rounded=1;arcSize=12;spacing=8;')
    def event(self,id,label,x,y,end=False,msg=False):
        self.node(id,'✉' if msg else '',x,y,38,38,'ellipse;aspect=fixed;strokeWidth='+('3.5' if end else '1.5')+';fontSize=21;')
        self.text(id+'-label',label,x-42,y+44,125,38,14)
        return id
    def gate(self,id,label,x,y):
        self.node(id,'×',x,y,54,54,'rhombus;fontSize=30;')
        self.text(id+'-label',label,x-35,y-39,140,30,15)
        return id
    def edge(self,s,t,label='',points=(),ports=(1,.5,0,.5),message=False,color=INK):
        self.n+=1; a,b,c,d=ports
        st=f'edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;fontFamily=Helvetica;fontSize=14;fontColor={color};strokeColor={color};strokeWidth=1.5;endArrow=block;endFill=1;labelBackgroundColor=#FFFFFF;exitX={a};exitY={b};entryX={c};entryY={d};'
        if message: st+='dashed=1;dashPattern=7 5;startArrow=oval;startFill=0;endArrow=open;endFill=0;'
        cell=E.SubElement(self.root,'mxCell',id=f'edge-{self.n}',value=label,edge='1',parent='1',source=s,target=t,style=st)
        geo=E.SubElement(cell,'mxGeometry',relative='1',attrib={'as':'geometry'})
        if points:
            ar=E.SubElement(geo,'Array',attrib={'as':'points'})
            for x,y in points: E.SubElement(ar,'mxPoint',x=str(x),y=str(y))
    def save(self):
        OUT.mkdir(parents=True,exist_ok=True); E.indent(self.doc)
        E.ElementTree(self.doc).write(OUT/(self.name+'.drawio'),encoding='utf-8',xml_declaration=True)

def returns():
    d=Diagram('returns-collaboration',2440,1290)
    d.text('title','跨组织退货协作 · 从申请到结算',40,30,2100,50,32)
    d.text('subtitle','NORTHSTAR COMMERCE  /  虚构业务场景  /  BPMN 协作视图（表示法子集）',42,86,2200,30,16,MUTED)
    d.node('customer','客户  /  独立参与者 · 内部过程不展开',40,150,2360,85,'fillColor=#F1F7F8;strokeColor=#176B87;align=left;spacingLeft=25;fontStyle=1;fontColor=#176B87;')
    for i,(title,y,h) in enumerate([('客户服务',330,270),('仓储质检',600,285),('财务结算',885,260)]):
        d.node('lane-'+str(i),'',40,y,2360,h,'fillColor='+('#FAFBFC' if i%2==0 else '#FFFFFF')+';strokeColor=#A6B0B6;')
        d.node('lane-title-'+str(i),title,40,y,110,h,'fillColor=#EDF0F2;strokeColor=#A6B0B6;fontStyle=1;verticalLabelPosition=middle;')
    d.text('pool-title','NORTHSTAR · 企业内部流程',950,290,900,30,18)
    d.event('request','收到申请',190,392,msg=True)
    d.task('review','核验退货资格','人工 · 订单 / 时效 / 品类',270,375)
    d.gate('eligible','符合退货政策？',500,384)
    d.task('instructions','发送退货指引','通知 · RMA / 地址 / 包装',630,375)
    d.task('reject','告知拒绝原因','通知 · 附申诉入口',630,505)
    d.event('rejected','申请关闭',930,522,True)
    d.task('receive','接收并登记包裹','人工 · 扫码绑定 RMA',890,680)
    d.task('inspect','检查商品与凭证','人工 · 数量 / 状态 / 配件',1120,680)
    d.gate('quality','可全额退款？',1360,689)
    d.task('restock','确认全额退款','处理 · 更新可售库存',1510,630)
    d.task('partial','核定折价方案','人工 · 留存证据与金额',1510,760)
    d.task('offer','发送折价方案','通知 · 金额 / 处置说明',1740,760)
    d.task('answer','接收客户答复','接收 · 本例假设最终答复',1960,760)
    d.gate('accepted','接受方案？',2200,769)
    d.task('shipback','退回商品并结案','处理 · 本例不收退回运费',2150,625,190)
    d.event('closed','退回完成',2350,642,True)
    d.gate('merge','退款路径汇合',1730,960)
    d.task('pay','执行原路退款','服务 · 幂等键 = RMA',1840,951)
    d.task('notify','通知结算结果','通知 · 金额 / 凭证',2070,951)
    d.event('done','退货完成',2310,968,True)
    d.edge('request','review'); d.edge('review','eligible')
    d.edge('eligible','instructions','是')
    d.edge('eligible','reject','否',[(527,541)],(.5,1,0,.5))
    d.edge('reject','rejected')
    d.edge('instructions','receive','',[(835,411),(835,716)])
    d.edge('receive','inspect'); d.edge('inspect','quality')
    d.edge('quality','restock','是',[(1450,716),(1450,666)])
    d.edge('quality','partial','否',[(1387,796)],(.5,1,0,.5))
    d.edge('partial','offer'); d.edge('offer','answer'); d.edge('answer','accepted')
    d.edge('accepted','shipback','否',[(2227,710)],(.5,0,.5,1))
    d.edge('shipback','closed')
    d.edge('restock','merge','全额',[(1710,666),(1710,920),(1757,920)],(1,.5,.5,0))
    d.edge('accepted','merge','是 · 按协商金额',[(2227,870),(1695,870),(1695,987)],(.5,1,0,.5))
    d.edge('merge','pay'); d.edge('pay','notify'); d.edge('notify','done')
    d.edge('customer','request','退货申请',ports=(.072,1,.5,0),message=True,color=BLUE)
    d.edge('instructions','customer','退货指引',ports=(.5,0,.287,1),message=True,color=BLUE)
    d.edge('reject','customer','拒绝原因',[(815,541),(815,270)],(1,.5,.328,1),True,BLUE)
    d.edge('offer','customer','折价方案',[(1825,575),(1825,260)],(.5,0,.756,1),True,BLUE)
    d.edge('customer','answer','客户答复',[(2045,270),(2045,575)],(.850,1,.5,0),True,BLUE)
    d.edge('notify','customer','退款通知',[(2155,1090),(2390,1090),(2390,255)],(.5,1,.995,1),True,BLUE)
    d.text('legend','实线实心箭头：池内顺序流    ·    蓝色虚线空心箭头：跨池消息流    ·    ×：排他网关    ·    粗边圆：结束事件',42,1170,2300,35,16)
    d.text('notes','范围：收到实物后的质检与退款；运输、未答复超时、退款失败补偿在独立子流程展开。此图不是可执行 BPMN XML，未做完整规范认证。',42,1215,2330,35,15,MUTED)
    d.save()

def reconciliation():
    d=Diagram('reconciliation-flow',1720,2260)
    d.text('title','批量对账 · 有限重试与可恢复退出',50,30,1500,50,32)
    d.text('subtitle','虚构结算平台  /  每批最多 500 条记录  /  单笔独立提交，取消不撤销已完成记录',52,90,1500,30,17,MUTED)
    d.node('loop-container','',210,660,1150,1300,'rounded=1;arcSize=2;strokeColor=#A65C20;fillColor=#FFFCF7;')
    d.text('loop-title','02  单笔循环  /  每次读取下一条记录',240,680,850,35,20,ORANGE)
    d.text('phase1','01  批次准备',50,160,240,35,20,MUTED)
    d.text('phase3','03  收尾与审计',50,1950,240,35,20,MUTED)
    def t(id,a,b,x,y): return d.task(id,a,b,x,y,220)
    def g(id,a,x,y):
        return d.node(id,a,x,y,150,90,'rhombus;fontSize=16;spacing=5;')
    d.node('start','开始',580,155,160,55,'rounded=1;arcSize=100;fontStyle=1;')
    t('load','读取批次清单','IO · 冻结账期与输入摘要',550,250)
    g('valid','清单有效？',585,375)
    t('invalid','登记校验失败','异常 · 不写入任何明细',1040,385)
    t('confirm','等待操作员确认','人工 · 选择运行或取消',550,510)
    g('run','确认运行？',1090,510)
    t('next','读取下一条记录','游标 · 本笔 attempt 初始化为 1',550,740)
    g('exists','仍有记录？',585,865)
    g('cancel','收到取消？',585,1010)
    t('fetch','获取外部结算结果','API · 超时 / 限流允许重试',550,1155)
    g('ok','调用成功？',585,1290)
    g('retry','可重试且<br>attempt &lt; 3？',1075,1290)
    t('backoff','等待退避并增加计数','控制 · 2s / 4s，然后再请求',1040,1145)
    t('failed','登记单笔失败','异常 · 保留请求号与错误码',1040,1440)
    t('match','匹配订单与金额','规则 · 币种一致 / 误差 ≤ 0.01',550,1440)
    g('same','匹配一致？',585,1570)
    t('diff','登记差异待复核','业务 · 不自动修正账务',1040,1580)
    t('commit','提交单笔成功结果','事务 · 使用唯一对账键去重',550,1710)
    t('checkpoint','保存结果与检查点','提交后前移游标；继续下一笔',550,1880)
    t('stop','标记批次为已取消','保留已完成结果与恢复游标',1380,1015)
    t('summary','生成批次汇总','成功 / 差异 / 失败 / 未处理',550,2010)
    t('audit','写入审计并释放锁','记录操作者、输入摘要与终态',1040,2010)
    d.node('end','结束',1070,2160,160,55,'rounded=1;arcSize=100;strokeWidth=2.5;fontStyle=1;')
    v=(.5,1,.5,0)
    d.edge('start','load',ports=v);d.edge('load','valid',ports=v)
    d.edge('valid','confirm','是',ports=v);d.edge('valid','invalid','否')
    d.edge('confirm','run');d.edge('run','next','是',[(1165,635),(660,635)],(.5,1,.5,0))
    d.edge('run','stop','否',[(1490,555)],(1,.5,.5,0))
    d.edge('next','exists',ports=v);d.edge('exists','cancel','是',ports=v)
    d.edge('exists','summary','否 · 遍历完成',[(140,910),(140,2046)],(0,.5,0,.5))
    d.edge('cancel','fetch','否',ports=v);d.edge('cancel','stop','是')
    d.edge('fetch','ok',ports=v);d.edge('ok','match','是',ports=v)
    d.edge('ok','retry','否');d.edge('retry','backoff','是',ports=(.5,0,.5,1))
    d.edge('backoff','fetch','重试',ports=(0,.5,1,.5))
    d.edge('retry','failed','否',ports=v)
    d.edge('match','same',ports=v);d.edge('same','commit','是',ports=v)
    d.edge('same','diff','否')
    d.edge('failed','checkpoint','失败',[(1310,1476),(1310,1916)],(1,.5,1,.5))
    d.edge('diff','checkpoint','差异',[(1150,1840),(850,1840),(850,1916)],(.5,1,1,.5))
    d.edge('commit','checkpoint',ports=v)
    d.edge('checkpoint','next','下一笔',[(310,1916),(310,776)],(0,.5,0,.5))
    d.edge('stop','summary','取消',[(1490,1980),(594,1980)],(.5,1,.2,0))
    d.edge('invalid','summary','输入失败',[(1660,421),(1660,1995),(726,1995)],(1,.5,.8,0))
    d.edge('summary','audit');d.edge('audit','end',ports=v)
    d.text('legend','表示法：矩形 = 操作；菱形 = 条件；圆角端点 = 开始 / 结束。橙色边界仅表示重复范围。',50,2220,1510,30,15,MUTED)
    d.save()

if __name__=='__main__':
    returns(); reconciliation()
    print('Generated 2 editable process examples in', OUT)
