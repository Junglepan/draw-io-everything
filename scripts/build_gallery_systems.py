"""Six compact system scenarios; all names and infrastructure are fictional."""
from gallery_base import Diagram, BLUE, TEAL, AMBER, GRAY

LR='exitX=1;exitY=0.5;entryX=0;entryY=0.5;'
TB='exitX=0.5;exitY=1;entryX=0.5;entryY=0;'
DASH='dashed=1;strokeColor=#76859A;'
def card(d,t,x,y,w=190,h=70,fill=BLUE):
    return d.box(t,x,y,w,h,fill,'fontSize=15;')
def note(d,t,y=710): d.text(t,40,y,1040,34,13,'#5E6C84')

def cloud():
    d=Diagram('03-cloud','会员商城 · 双可用区部署','部署视图 / 云边界与可用区明确；实线为请求或数据访问，虚线为异步复制',1120,820)
    client=card(d,'移动端 / Web\n商城用户',40,183,185,65,GRAY)
    cdn=card(d,'CDN + WAF\n缓存静态资源 · 过滤流量',275,183,225,65)
    lb=card(d,'应用负载均衡\n健康检查 · 跨区路由',570,183,250,65)
    d.edge(client,cdn,'HTTPS',LR);d.edge(cdn,lb,'动态请求',LR)
    d.group('生产 VPC · 10.24.0.0/16',40,290,1040,410,GRAY)
    d.group('可用区 A · 私有子网',65,340,475,330,BLUE)
    d.group('可用区 B · 私有子网',565,340,490,330,TEAL)
    a=card(d,'商城 API A\n订单 / 会员接口',90,395,200,70,'#FFFFFF')
    b=card(d,'商城 API B\n订单 / 会员接口',590,395,200,70,'#FFFFFF')
    wa=card(d,'任务 Worker A\n履约事件处理',315,395,200,70,'#FFFFFF')
    wb=card(d,'任务 Worker B\n履约事件处理',815,395,215,70,'#FFFFFF')
    da=card(d,'订单数据库 · 主库\n事务写入',90,575,200,70,'#FFFFFF')
    db=card(d,'订单数据库 · 备用\n跨区故障接管',590,575,200,70,'#FFFFFF')
    qa=card(d,'消息代理 A\n持久化事件',315,575,200,70,'#FFFFFF')
    qb=card(d,'消息代理 B\n副本',815,575,215,70,'#FFFFFF')
    d.edge(lb,a,'路由 A', 'exitX=0.2;exitY=1;entryX=0;entryY=0.5;',[(620,270),(55,270),(55,430)])
    d.edge(lb,b,'路由 B','exitX=0.8;exitY=1;entryX=0;entryY=0.5;',[(770,280),(550,280),(550,430)])
    d.edge(a,da,'读写',TB); d.edge(b,da,'主库访问','exitX=0.2;exitY=1;entryX=1;entryY=0.25;',[(630,500),(290,500)])
    d.root[-1].find('mxGeometry').set('x','-0.55')
    d.edge(qa,wa,'消费', 'exitX=0.5;exitY=0;entryX=0.5;entryY=1;')
    d.edge(qb,wb,'消费', 'exitX=0.5;exitY=0;entryX=0.5;entryY=1;')
    d.edge(da,db,'复制',LR+DASH,[(300,680),(570,680)])
    d.edge(qa,qb,'集群复制','exitX=0.8;exitY=1;entryX=0.8;entryY=1;'+DASH,[(475,690),(987,690)])
    note(d,'范围：简化部署拓扑。应用经事务 Outbox 发布事件；发布链路及运维组件在此视图省略。',725); d.save()

def cluster():
    d=Diagram('04-cluster','推荐服务 · Kubernetes 组件关系','控制关系视图 / 蓝色表示控制面，绿色表示工作节点；虚线为观察与协调，非业务请求路径',1120,820)
    d.group('控制平面',40,185,340,500,BLUE)
    api=card(d,'API Server\n统一集群 API',75,245,270,70,'#FFFFFF')
    etcd=card(d,'etcd\n集群状态存储',75,355,270,65,'#FFFFFF')
    sch=card(d,'Scheduler\n为待调度 Pod 选择节点',75,465,270,65,'#FFFFFF')
    ctrl=card(d,'Controller Manager\n期望状态协调',75,575,270,65,'#FFFFFF')
    d.edge(api,etcd,'持久化',TB)
    d.edge(sch,api,'watch / bind','exitX=0;exitY=0.5;entryX=0;entryY=0.5;'+DASH,[(55,497),(55,280)])
    d.edge(ctrl,api,'watch / update','exitX=1;exitY=0.5;entryX=1;entryY=0.8;'+DASH,[(365,607),(365,301)])
    for x,name in [(460,'工作节点 A'),(790,'工作节点 B')]:
        d.group(name,x,185,290,500,TEAL)
        k=card(d,'kubelet\n观察 PodSpec · 汇报状态',x+25,245,240,70,'#FFFFFF')
        r=card(d,'容器运行时\n启动 / 停止容器',x+25,375,240,70,'#FFFFFF')
        p=card(d,'推荐服务 Pod\n应用容器 + 指标端点',x+25,515,240,100,'#FFFFFF')
        d.edge(k,api,'API 协调','exitX=0.5;exitY=0;entryX='+('0.5' if x==460 else '0.8')+';entryY=0;'+DASH,[(x+145,165 if x==460 else 180),(210 if x==460 else 291,165 if x==460 else 180)])
        d.edge(k,r,'CRI',TB);d.edge(r,p,'管理生命周期',TB)
    note(d,'业务请求经 Service / Ingress 到达 Pod，另绘流量视图；本图不将控制链路解释为请求转发链路。',725);d.save()

def context():
    d=Diagram('06-context','星桥零售 · 订单协作系统上下文','系统上下文 / 聚焦订单平台与外部参与者，系统内部模块留到下一层展开',1120,830)
    buyer=card(d,'消费者\n[人员]\n提交订单、查看履约进度',40,190,270,100,GRAY)
    ops=card(d,'运营人员\n[人员]\n处理订单异常与售后',810,190,270,100,GRAY)
    d.group('星桥零售 · 自有系统边界',355,305,410,365,BLUE)
    core=card(d,'订单平台\n[软件系统]\n订单生命周期与履约协调',400,355,320,120,'#D7E7FF')
    inventory=card(d,'库存系统\n[软件系统]\n预占、释放与扣减库存',400,545,320,90,'#FFFFFF')
    pay=card(d,'支付网关\n[外部软件系统]\n收款、退款及支付通知',40,365,270,110,AMBER)
    delivery=card(d,'物流平台\n[外部软件系统]\n接单、配送与轨迹通知',810,365,270,110,AMBER)
    crm=card(d,'客户服务系统\n[软件系统]\n工单与订单查询',40,555,270,100,TEAL)
    msg=card(d,'消息服务商\n[外部软件系统]\n短信及订阅消息触达',810,555,270,100,AMBER)
    d.edge(buyer,core,'下单 / 查询','exitX=0.5;exitY=1;entryX=0;entryY=0.2;',[(175,320),(370,320),(370,379)])
    d.edge(ops,core,'异常处置','exitX=0.5;exitY=1;entryX=1;entryY=0.2;',[(945,320),(750,320),(750,379)])
    d.edge(core,pay,'收款 / 退款','exitX=0;exitY=0.5;entryX=1;entryY=0.5;')
    d.edge(core,delivery,'发起配送',LR)
    d.edge(core,inventory,'预占 / 扣减',TB)
    d.edge(crm,core,'查询订单','exitX=1;exitY=0.5;entryX=0;entryY=0.85;',[(335,605),(335,457)])
    d.edge(core,msg,'发送业务通知','exitX=1;exitY=0.85;entryX=0;entryY=0.5;',[(785,457),(785,605)])
    note(d,'箭头表示依赖 / 使用方向，不表示完整时序；浅蓝边界为自有范围，橙色为第三方系统。',720);d.save()

def application():
    d=Diagram('07-application','零售应用组合 · 生命周期资产地图','资产视图 / 以业务域归类，颜色仅编码生命周期；无连线表示本图不展示系统依赖',1120,810)
    states=[('稳定','#E6F5F0'),('演进','#EAF2FF'),('退役','#FFF3DA')]
    domains=[('交易与履约',[('订单中心','稳定'),('库存中心','稳定'),('履约编排','演进'),('旧订单后台','退役')]),('客户与增长',[('会员中心','稳定'),('优惠券平台','稳定'),('触达编排','演进'),('旧积分门户','退役')]),('经营与支撑',[('商品中心','稳定'),('结算中心','演进'),('经营分析','演进'),('报表工作台','退役')])]
    fills=dict(states)
    for col,(domain,apps) in enumerate(domains):
        x=40+col*355;d.group(domain,x,190,330,465,GRAY)
        for row,(title,status) in enumerate(apps):
            card(d,f'{title}\n生命周期：{status}',x+20,250+row*95,290,75,fills[status])
    for i,(s,c) in enumerate(states):card(d,f'{s}  /  '+{'稳定':'持续运营','演进':'能力建设','退役':'迁移收敛'}[s],40+i*355,685,330,50,c)
    d.save()

def network():
    d=Diagram('09-network','制造园区 · 生产网络分区','逻辑网络视图 / 上层为共享骨干，下层按区域分组；连线表示网络连接，非报文方向',1120,820)
    wan=card(d,'企业 WAN\n总部专线',40,195,210,70,GRAY)
    fw=card(d,'园区防火墙\nWAN 边界访问策略',335,195,230,70,AMBER)
    core=card(d,'核心交换机组\n园区汇聚骨干',650,195,280,70,BLUE)
    d.edge(wan,fw,'专线',LR+'endArrow=none;');d.edge(fw,core,'受控互联',LR+'endArrow=none;')
    for i,(title,n1,n2) in enumerate([('办公区 · VLAN 10','办公终端组','协作服务器'),('生产区 · VLAN 20','产线 PLC 组','工业 HMI 组'),('运维区 · VLAN 30','跳板机','监控采集器')]):
        x=40+i*355;d.group(title,x,355,330,320,[BLUE,TEAL,AMBER][i])
        sw=card(d,'区域接入交换机',x+40,415,250,65,'#FFFFFF')
        a=card(d,n1,x+20,565,140,65,'#FFFFFF');b=card(d,n2,x+175,565,135,65,'#FFFFFF')
        d.edge(core,sw,'区域上联','exitX='+str([0.2,0.5,0.8][i])+';exitY=1;entryX=0.9;entryY=0;endArrow=none;',[(706+i*84,300+i*15),(x+265,300+i*15)])
        d.edge(sw,a,'','exitX=0.25;exitY=1;entryX=0.5;entryY=0;endArrow=none;',[(x+102,525),(x+90,525)])
        d.edge(sw,b,'','exitX=0.75;exitY=1;entryX=0.5;entryY=0;endArrow=none;',[(x+227,525),(x+242,525)])
    note(d,'示意范围：区域级互联；防火墙控制 WAN 边界访问，区域间策略、设备冗余及地址细节另图展开。',725);d.save()

def capability():
    d=Diagram('10-capability','连锁零售 · 业务能力地图','能力视图 / 各列为业务域，卡片表达业务能够做什么；颜色仅帮助识别业务归属',1120,810)
    domains=[('客户经营',BLUE,['客户识别','会员权益','客户分群','客户服务']),('商品经营',TEAL,['商品规划','定价管理','促销管理','库存管理']),('交易履约',AMBER,['订单管理','支付结算','配送管理','退换管理'])]
    for i,(title,color,items) in enumerate(domains):
        x=40+i*355;d.group(title,x,190,330,400,color)
        for j,t in enumerate(items):card(d,t,x+20,250+j*78,290,58,'#FFFFFF')
    d.group('共享支撑能力 · 跨业务域复用',40,615,1040,115,GRAY)
    for i,t in enumerate(['身份与权限','数据治理','风险管理','运营监控']):card(d,t,60+i*255,665,235,45,'#FFFFFF')
    d.save()

if __name__=='__main__':
    for build in [cloud,cluster,context,application,network,capability]:build()
