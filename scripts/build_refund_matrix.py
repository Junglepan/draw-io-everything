from pathlib import Path
import sys
import gallery_base as g
g.OUT=Path(__file__).resolve().parents[1] / 'examples' / 'advanced'
D=g.Diagram('refund-matrix','跨服务退款处理 · 责任 × 阶段','假设场景：规则审核通过后原路退款；支付未知状态先查询，明确可重试后才重试。',1800,1100)
cols=[(240,320,'01  受理申请'),(560,360,'02  规则审核'),(920,480,'03  执行退款'),(1400,340,'04  结果闭环')]
for x,w,t in cols:D.box(t,x,190,w,48,'#E9EEF5','rounded=0;strokeColor=#FFFFFF;fontStyle=1;')
rows=[(240,160,'售后服务','申请与状态管理','#EFF5FD','#DCE9FA'),(400,210,'审核服务','资格与金额校验','#F0F7F4','#DBECE3'),(610,240,'支付服务','渠道退款与核实','#FCF7ED','#F3E7CA'),(850,160,'通知服务','结果投递与去重','#F5F2FA','#E8DFF3')]
for y,h,title,sub,fill,head in rows:
 D.box('',240,y,1500,h,fill,'rounded=0;strokeColor=#FFFFFF;');D.box('',40,y,192,h,head,'rounded=0;strokeColor=none;');D.text(title,60,y+45,160,30,20,bold=True);D.text(sub,60,y+82,160,28,14)
for x in [560,920,1400]:D.line(x,240,x,1010,extra='dashed=1;strokeColor=#CFD8E3;')
def box(t,x,y,w=170,h=62):return D.box(t,x,y,w,h,'#FFFFFF','fontSize=16;strokeColor=#A4B5C9;')
def decision(t,x,y):return D.box(t,x,y,105,82,'#FFFFFF','shape=rhombus;rounded=0;spacing=3;fontSize=15;')
a=box('接收退款申请\n校验幂等键',275,285,120,70);b=box('创建售后单\n状态：待审核',415,285,120,70)
c=box('校验订单 / 退款窗口\n核对可退金额',590,435,170,70);q=decision('审核\n通过？',790,430)
r=box('记录拒绝原因',735,535,155,48)
e=box('创建退款指令\n固定退款请求号',955,285,200,70)
f=box('提交渠道退款\n复用同一请求号',955,650,200,70);s=decision('渠道\n结果？',1210,640)
u=box('查询渠道终态\n未知则继续核实',1185,765,185,62);retry=box('退避后重试\n仅明确可重试失败',955,765,200,62)
z=box('回写退款成功\n保存渠道流水号',1465,285,220,70)
n=box('发送结果通知\n按售后单 + 结果版本去重',1465,895,220,70)
D.edge(a,b)
D.edge(b,c,points=[(550,320),(550,470)])
D.edge(c,q)
D.edge(q,e,'是',extra='exitX=1;exitY=0.5;entryX=0;entryY=0.5;',points=[(910,471),(910,320)])
D.edge(q,r,'否',extra='exitX=0.5;exitY=1;entryX=0.5;entryY=0;')
D.edge(e,f,extra='exitX=0.5;exitY=1;entryX=0.5;entryY=0;')
D.edge(f,s)
D.edge(s,z,'成功',extra='exitX=1;exitY=0.5;entryX=0;entryY=0.5;',points=[(1380,681),(1380,320)])
D.edge(s,u,'未知',extra='exitX=0.5;exitY=1;entryX=0.5;entryY=0;')
D.edge(u,s,extra='exitX=1;exitY=0.5;entryX=1;entryY=0.7;',points=[(1385,796),(1385,697)])
D.edge(s,retry,'可重试失败',extra='exitX=0.15;exitY=1;entryX=0.5;entryY=0;',points=[(1226,744),(1055,744)])
D.edge(retry,f,extra='exitX=0;exitY=0.5;entryX=0;entryY=0.5;',points=[(935,796),(935,685)])
D.edge(z,n,'成功结果',extra='exitX=0.5;exitY=1;entryX=0.5;entryY=0;')
D.edge(r,n,'拒绝结果',extra='exitX=0.5;exitY=1;entryX=0;entryY=0.7;',points=[(812,980),(1440,980),(1440,939)])
D.text('读图说明：列 = 业务阶段 · 行 = 责任服务 · 箭头 = 处理顺序 / 交接；非严格 BPMN。',40,1022,1500,24,14)
D.text('范围：示例覆盖成功、审核拒绝、未知核实与可重试失败；不可重试失败转人工处理，未展开。',40,1048,1500,24,13)
# Hide generic footer to avoid overlap with scoped notes.
for cell in D.root.findall('mxCell'):
 if cell.get('value','').startswith('原创示例'):cell.set('value','')
D.save()
