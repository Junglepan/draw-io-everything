"""Generate five compact, fictional process examples (native draw.io XML)."""
from gallery_base import Diagram, BLUE, TEAL, AMBER, GRAY

PURPLE='#F0EBFA'
RED='#FCEDEA'

def box(d,t,x,y,w=180,h=64,c=BLUE):
    return d.box(t,x,y,w,h,c,'fontSize=16;')
def edge(d,a,b,t='',extra='',points=None):
    d.edge(a,b,t,'rounded=1;arcSize=14;'+extra,points)
def note(d,t,y,w):
    d.text(t,40,y,w-80,42,13,'#5E6C84')

def flow():
    d=Diagram('01-flow','流程图 · 生产发布准入与回退','虚构场景：一次低风险发布窗口 / 条件明确，异常分支有去向',width=1120,height=1020)
    d.group('自动门禁',350,180,420,350,BLUE)
    a=box(d,'提交发布单\n版本 · 变更范围 · 回退方案',450,235,220,66,'#FFFFFF')
    b=box(d,'构建与测试\n单元测试 / 依赖扫描',450,345,220,66,'#FFFFFF')
    c=d.box('门禁通过？',490,440,140,90,AMBER,'shape=rhombus;fontSize=16;')
    fail=box(d,'修复并重新提交\n本次发布结束',65,450,230,70,RED)
    d.group('审批与执行',350,560,420,300,TEAL)
    approve=d.box('负责人批准？',490,590,140,90,AMBER,'shape=rhombus;fontSize=16;')
    cancel=box(d,'记录驳回原因\n本次发布结束',830,600,230,70,RED)
    canary=box(d,'灰度发布 5%\n观察错误率与 P95 延迟',450,730,220,70,'#FFFFFF')
    ok=d.box('指标正常？',490,850,140,90,AMBER,'shape=rhombus;fontSize=16;')
    full=box(d,'全量发布 · 留存审计\n发布完成',830,855,230,70,TEAL)
    rollback=box(d,'回退到上一稳定版本\n通知值班 · 留存审计',65,855,230,70,RED)
    edge(d,a,b);edge(d,b,c);edge(d,c,fail,'否', 'exitX=0;exitY=0.5;entryX=1;entryY=0.5;')
    edge(d,c,approve,'是');edge(d,approve,cancel,'否','exitX=1;exitY=0.5;entryX=0;entryY=0.5;');edge(d,approve,canary,'是');edge(d,canary,ok)
    edge(d,ok,full,'是','exitX=1;exitY=0.5;entryX=0;entryY=0.5;');edge(d,ok,rollback,'否','exitX=0;exitY=0.5;entryX=1;entryY=0.5;')
    d.text('观察窗口：10 分钟\n示例阈值：错误率 < 1%\n且 P95 不劣于基线 10%',805,735,275,80,14)
    d.save()

def swimlane():
    d=Diagram('02-swimlane','服务泳道 · 订单确认与库存补偿','虚构场景：库存先预留，再确认订单 / 展示服务责任与关键交接，非严格 BPMN',width=1400,height=960)
    for y,t,c in [(210,'订单服务',BLUE),(370,'库存服务',TEAL),(530,'支付服务',AMBER),(690,'通知服务',PURPLE)]:
        d.group('',40,y,1320,145,c);d.text(t,58,y+50,125,30,17,'#344563',True)
    for x,t in [(210,'01  接单与预留'),(510,'02  支付确认'),(830,'03  状态收敛'),(1140,'04  用户通知')]:d.text(t,x,170,230,28,14,'#5E6C84',True)
    a=box(d,'创建待支付订单',210,255,180,60,'#FFFFFF')
    b=box(d,'预留库存\n返回预留编号',210,415,180,64,'#FFFFFF')
    c=box(d,'发起支付并验签\n查询至确定终态',510,570,180,64,'#FFFFFF')
    q=d.box('支付成功？',735,557,140,90,'#FFFFFF','shape=rhombus;fontSize=15;')
    e=box(d,'订单置为已确认',925,255,180,60,'#FFFFFF')
    f=box(d,'扣减已预留库存',925,415,180,64,'#FFFFFF')
    g=box(d,'发送下单成功通知',1160,735,180,60,'#FFFFFF')
    h=box(d,'关闭失败订单',510,255,180,60,'#FFFFFF')
    i=box(d,'释放库存预留',510,415,180,64,'#FFFFFF')
    j=box(d,'发送关闭通知',735,735,180,60,'#FFFFFF')
    edge(d,a,b,'预留请求');edge(d,b,c,'预留成功','exitX=1;exitY=0.5;entryX=0;entryY=0.5;',[(450,447),(450,602)])
    edge(d,c,q,'结果回调')
    edge(d,q,e,'是','exitX=1;exitY=0.5;entryX=1;entryY=0.5;',[(1125,602),(1125,285)])
    edge(d,e,f,'确认扣减');edge(d,f,g,'确认事件','exitX=1;exitY=0.5;entryX=0.5;entryY=0;',[(1250,447)])
    edge(d,q,h,'否：失败 / 已确认关单','exitX=0.5;exitY=0;entryX=1;entryY=0.5;',[(805,285)])
    edge(d,h,i,'补偿请求');edge(d,i,j,'关闭事件','jumpStyle=arc;jumpSize=8;exitX=1;exitY=0.5;entryX=0.5;entryY=0;',[(720,447),(720,675),(825,675)])
    d.root.find("./mxCell[@id='e%s']/mxGeometry" % d.i).set('x','0.65')
    note(d,'范围：库存预留成功后的路径。支付结果先验签 / 查询；未知结果继续核实，不释放库存。回调与状态更新幂等。',850,1400)
    d.save()

def sequence():
    d=Diagram('05-sequence','时序图 · 下单预留与异步通知','虚构场景：同步预留 + 本地事务 Outbox / 区分返回、异步消息与失败分支',width=1280,height=1100)
    xs=[140,390,640,890,1140]
    for x,t in zip(xs,['客户端','订单服务','库存服务','事件总线','通知服务']):
        box(d,t,x-90,185,180,55,BLUE);d.line(x,240,x,970,extra='dashed=1;')
    def msg(a,b,y,t,ret=False,async_=False):
        d.line(xs[a],y,xs[b],y,t,('dashed=1;' if ret else '')+'endArrow='+('open' if ret or async_ else 'block')+';endFill='+('0;' if ret or async_ else '1;')+'strokeColor=#526A89;fontSize=14;')
    msg(0,1,280,'1  创建订单（幂等键）')
    msg(1,2,340,'2  预留库存（订单号）')
    d.box('',55,385,1170,530,'none','rounded=0;strokeColor=#A5B4C7;')
    d.text('alt   库存预留结果',70,395,400,25,14,'#344563',True)
    d.text('[预留成功]',70,430,250,25,14,'#3973D6',True)
    msg(2,1,475,'3  返回预留编号',True)
    box(d,'事务提交\n订单 + Outbox',420,505,190,65,TEAL)
    d.line(390,525,420,525,extra='endArrow=none;dashed=1;')
    msg(1,0,600,'4  返回订单号',True)
    msg(1,3,655,'5  Outbox 投递 OrderCreated',async_=True)
    msg(3,4,715,'6  订阅消费（按事件 ID 去重）',async_=True)
    d.line(55,755,1225,755,extra='dashed=1;')
    d.text('[库存不足]',70,768,250,25,14,'#9B6015',True)
    msg(2,1,815,'3b  预留失败',True)
    msg(1,0,875,'4b  返回库存不足',True)
    for x,t in zip(xs,['客户端','订单服务','库存服务','事件总线','通知服务']):box(d,t,x-80,955,160,40,GRAY)
    note(d,'实线实心箭头：同步调用；虚线开放箭头：返回；实线开放箭头：异步消息。Outbox 重投及通知重试另图展开。',1000,1280)
    d.save()

def lineage():
    d=Diagram('08-lineage','字段血缘 · 从支付与退款到净收款','虚构场景：按支付日归属退款 / 金额同币种，净收款不等同会计收入',width=1440,height=870)
    def table(title,sub,x,y,fields,focus):
        d.group(title,x,y,300,235,GRAY);d.text(sub,x+18,y+47,264,22,12,'#5E6C84')
        out={}
        for i,f in enumerate(fields):out[f]=box(d,f,x+18,y+80+i*44,264,36,BLUE if f in focus else '#FFFFFF')
        return out
    p=table('payments','ODS · 已成功支付',40,205,['payment_id','paid_date','paid_amount'],['paid_amount'])
    r=table('refunds','ODS · 已成功退款',40,500,['payment_id','refund_amount','refund_status'],['refund_amount'])
    rr=table('refund_by_payment','DWD · 按原支付汇总',500,500,['payment_id','refunded_amount','refund_count'],['refunded_amount'])
    net=table('payment_net','DWD · 一笔支付一行',500,205,['payment_id','paid_date','net_amount'],['net_amount'])
    daily=table('daily_net_receipts','DWS · 支付日 × 币种',1100,205,['paid_date','currency','net_receipts'],['net_receipts'])
    def hi(a,b,t='',points=None,extra=''):
        edge(d,a,b,t,'strokeColor=#3973D6;strokeWidth=2;'+extra,points)
    hi(p['paid_amount'],net['net_amount'],'金额',extra='exitX=1;exitY=0.5;entryX=0;entryY=0.5;')
    hi(r['refund_amount'],rr['refunded_amount'],'SUM',extra='exitX=1;exitY=0.5;entryX=0;entryY=0.5;')
    hi(rr['refunded_amount'],net['net_amount'],'按 payment_id 左连接',[(845,642),(845,450),(650,450)],'exitX=1;exitY=0.5;entryX=0.5;entryY=1;')
    hi(net['net_amount'],daily['net_receipts'],'SUM / 支付日 × 币种',extra='exitX=1;exitY=0.5;entryX=0;entryY=0.5;')
    d.group('口径与质量约束',920,500,480,235,TEAL)
    d.text('net_amount = paid_amount − COALESCE(refunded_amount, 0)\n\n退款先聚合，避免一对多连接放大支付额。\n退款回溯到原支付日；日期分区需重算。\n检查：支付键唯一、币种一致、退款不超支付。',940,548,440,165,14)
    note(d,'蓝色：当前关注的金额路径。灰色字段仅作上下文；非焦点依赖省略。币种过滤与日期映射在模型层处理。',780,1440)
    d.save()

def pipeline():
    d=Diagram('11-pipeline','事件流水线 · 订单事件到实时运营指标','虚构场景：近实时处理，分钟级可见 / 展示主链路、质量隔离与重放入口',width=1440,height=850)
    d.group('事件生产',40,200,230,490,BLUE)
    d.group('处理与存储',305,200,800,490,TEAL)
    d.group('消费应用',1140,200,260,490,AMBER)
    a=box(d,'订单服务\nOrderCreated',65,275,180,70,'#FFFFFF')
    b=box(d,'支付服务\nPaymentSucceeded',65,390,180,70,'#FFFFFF')
    c=box(d,'退款服务\nRefundSucceeded',65,505,180,70,'#FFFFFF')
    bus=box(d,'事件总线\n按 order_id 分区',330,390,180,70,'#FFFFFF')
    check=box(d,'校验与去重\nschema / event_id',590,390,180,70,'#FFFFFF')
    agg=box(d,'窗口聚合\n事件时间 · 5 分钟',875,390,200,70,'#FFFFFF')
    raw=box(d,'原始事件归档\n不可变 · 保留 30 天',330,550,180,70,'#FFFFFF')
    dead=box(d,'隔离队列\n无效事件 + 原因',590,550,180,70,RED)
    store=box(d,'指标存储\n幂等更新窗口结果',875,550,200,70,'#FFFFFF')
    dashboard=box(d,'实时运营看板\n订单量 / 成交额',1170,315,200,70,'#FFFFFF')
    alert=box(d,'异常告警\n支付转化率下降',1170,550,200,70,'#FFFFFF')
    for n in [a,b,c]:edge(d,n,bus,extra='exitX=1;exitY=0.5;entryX=0;entryY=0.5;',points=[(285,425)])
    edge(d,bus,check,'订阅');edge(d,check,agg,'有效事件');edge(d,bus,raw,'归档');edge(d,check,dead,'无效');edge(d,agg,store,'窗口结果')
    edge(d,store,dashboard,'查询结果','exitX=1;exitY=0.3;entryX=0;entryY=0.5;',[(1120,571),(1120,350)])
    edge(d,store,alert,'指标输入')
    edge(d,raw,check,'归档事件重放','jumpStyle=arc;jumpSize=8;dashed=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;',[(420,655),(810,655),(810,315),(680,315)])
    d.text('允许迟到：10 分钟\n超过窗口的事件进入离线校正',850,270,240,70,14)
    note(d,'实线：常规数据路径；虚线：运维重放。示例假设至少一次投递，去重与幂等写入共同保证重复消费安全。',735,1440)
    d.save()

if __name__=='__main__':
    for build in [flow,swimlane,sequence,lineage,pipeline]:build()
    print('Generated 5 process gallery diagrams.')
