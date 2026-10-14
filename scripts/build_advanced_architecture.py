"""Original fictional system landscape and field lineage; only Python stdlib.
Run from any directory: python3 scripts/build_advanced_architecture.py
Render each generated file with draw.io Desktop. These are not an auto-layout engine.
"""
from pathlib import Path
import xml.etree.ElementTree as E
OUT=Path(__file__).resolve().parents[1]/'examples'/'advanced'
class Diagram:
    def __init__(self,name,title,sub,w=1840,h=1240):
        self.name=name; self.n=0
        self.doc=E.Element('mxfile',host='drawio-everything')
        p=E.SubElement(self.doc,'diagram',id=name,name=title)
        m=E.SubElement(p,'mxGraphModel',page='1',pageWidth=str(w),pageHeight=str(h),grid='1',gridSize='10')
        self.r=E.SubElement(m,'root');E.SubElement(self.r,'mxCell',id='0');E.SubElement(self.r,'mxCell',id='1',parent='0')
        self.box('',0,0,w,h,'fillColor=#FFFFFF;strokeColor=none;')
        self.text('DRAWIO EVERYTHING   /   FIELD NOTES',40,25,w-80,25,14,'#627088',True)
        self.text(title,40,66,w-80,50,34,'#142D48',True)
        self.text(sub,40,124,w-80,32,17,'#59677A')
    def box(self,v,x,y,w,h,s=''):
        self.n+=1; i='n'+str(self.n)
        c=E.SubElement(self.r,'mxCell',id=i,value=v,style='html=1;whiteSpace=wrap;fontFamily=Arial;fontSize=17;fontColor=#263A50;spacing=12;'+s,vertex='1',parent='1')
        E.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
        return i
    def text(self,v,x,y,w,h,size=17,color='#263A50',bold=False):
        return self.box(v,x,y,w,h,f'fillColor=none;strokeColor=none;align=left;spacing=0;fontSize={size};fontColor={color};fontStyle={int(bold)};')
    def edge(self,a,b,label='',points=(),s=''):
        self.n+=1
        c=E.SubElement(self.r,'mxCell',id='e'+str(self.n),value=label,source=a,target=b,parent='1',edge='1',style='html=1;edgeStyle=none;rounded=0;endArrow=block;endSize=9;strokeWidth=1.7;strokeColor=#687C92;fontSize=15;fontColor=#40546A;fontFamily=Arial;labelBackgroundColor=#FFFFFF;'+s)
        g=E.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
        if points:
            arr=E.SubElement(g,'Array',attrib={'as':'points'})
            for x,y in points:E.SubElement(arr,'mxPoint',x=str(x),y=str(y))
    def save(self):
        OUT.mkdir(parents=True,exist_ok=True);E.indent(self.doc)
        E.ElementTree(self.doc).write(OUT/(self.name+'.drawio'),encoding='utf-8',xml_declaration=True)

def landscape():
    d=Diagram('retail-landscape','北辰零售 · 全渠道业务系统全景','虚构场景  /  人员与软件系统粒度  /  展示关键业务依赖与组织责任，省略内部服务及部署拓扑')
    d.box('',40,365,1270,760,'rounded=0;fillColor=#F8FAFC;strokeColor=#7F94A9;dashed=1;dashPattern=3 4;strokeWidth=2;')
    d.text('北辰零售集团  ·  自有软件系统',60,1070,600,30,18,'#41576D',True)
    d.box('',1400,365,400,760,'rounded=0;fillColor=#FFFCF6;strokeColor=#C2A76C;dashed=1;dashPattern=3 4;strokeWidth=2;')
    d.text('外部合作方  ·  独立运营责任',1420,380,360,30,18,'#816733',True)
    def person(name,desc,x):
        d.box('',x+110,181,54,54,'shape=ellipse;strokeColor=#187E78;strokeWidth=2;fillColor=#FFFFFF;')
        return d.box(f'<b>{name}</b><br><font style="font-size:13px">[人员]</font><br>{desc}',x,235,275,92,'rounded=1;arcSize=24;fillColor=#F2FBF8;strokeColor=#187E78;strokeWidth=2;fontColor=#176B66;')
    customer=person('会员顾客','购买商品、查询订单与积分',90)
    operator=person('履约运营','监控订单与处理履约异常',510)
    analyst=person('财务分析师','对账、关账与收入分析',930)
    def system(name,desc,x,y,external=False):
        color='#A67B2B' if external else '#28629B'
        return d.box(f'<b>{name}</b><br><font style="font-size:13px">[软件系统]</font><br><br>{desc}',x,y,275,150,f'rounded=1;arcSize=9;fillColor=#FFFFFF;strokeColor={color};strokeWidth=2;fontColor={color};')
    digital=system('全渠道交易门户','承接 App、网页及门店订单<br>统一顾客交易入口',90,460)
    oms=system('订单管理系统','管理订单生命周期<br>编排支付与履约请求',510,460)
    fin=system('财务结算系统','归集收款与退款<br>核对订单并生成结算凭证',930,460)
    member=system('会员与权益平台','统一会员身份<br>管理积分和权益账户',90,850)
    wms=system('仓储履约系统','分配库存、拣货出库<br>跟踪包裹与签收状态',510,850)
    data=system('经营分析平台','汇聚交易与履约事实<br>提供经营指标和异常监测',930,850)
    pay=system('聚合支付平台','处理支付与原路退款<br>提供支付结果和账单',1460,460,True)
    courier=system('物流协同平台','承运揽收与配送<br>提供运单和物流轨迹',1460,730,True)
    erp=system('第三方财务托管平台','接收结算凭证<br>提供总账与财务报表服务',1460,960,True)
    for p,t,l in [(customer,digital,'浏览、下单、售后'),(operator,oms,'监控与人工处置'),(analyst,fin,'对账与结算审核')]:
        d.edge(p,t,l,s='exitX=0.5;exitY=1;entryX=0.5;entryY=0;')
    d.edge(digital,oms,'创建 / 查询订单',s='exitX=1;exitY=0.5;entryX=0;entryY=0.5;')
    d.edge(oms,fin,'提供交易 /<br>退款事实',s='exitX=1;exitY=0.5;entryX=0;entryY=0.5;')
    d.edge(fin,pay,'核对收款 / 退款账单',s='exitX=1;exitY=0.5;entryX=0;entryY=0.5;')
    d.edge(digital,member,'校验会员 / 使用权益',s='exitX=0.5;exitY=1;entryX=0.5;entryY=0;')
    d.edge(oms,wms,'',s='exitX=0.38;exitY=1;entryX=0.38;entryY=0;')
    d.edge(wms,oms,'',s='exitX=0.78;exitY=0;entryX=0.78;entryY=1;')
    d.edge(fin,data,'发布结算事实',s='exitX=0.5;exitY=1;entryX=0.5;entryY=0;')
    d.edge(wms,data,'提供履约事实',s='exitX=1;exitY=0.5;entryX=0;entryY=0.5;')
    d.edge(wms,courier,'创建运单 / 查询轨迹',[(820,800),(1370,800)],'exitX=1;exitY=0.12;entryX=0;entryY=0.5;')
    d.edge(fin,erp,'',[(1335,580),(1335,1035)],'exitX=1;exitY=0.8;entryX=0;entryY=0.5;')
    d.edge(oms,pay,'发起支付 / 退款',[(740,680),(1370,680),(1370,580)],'exitX=0.84;exitY=1;entryX=0;entryY=0.8;')
    d.box('下发履约请求',535,645,145,26,'fillColor=#F8FAFC;strokeColor=none;fontSize=15;spacing=0;')
    d.box('反馈库存 / 出库状态',650,765,170,26,'fillColor=#F8FAFC;strokeColor=none;fontSize=15;spacing=0;')
    d.box('提交审核后的<br>会计凭证',1240,920,155,50,'fillColor=#FFFFFF;strokeColor=none;fontSize=15;spacing=0;')
    d.text('图例   绿色轮廓：人员   ·   蓝色轮廓：自有系统   ·   金色轮廓：外部系统   ·   虚线框：组织责任边界',40,1150,1760,28,16)
    d.text('箭头：发起方 → 被使用系统；关系文字描述使用目的。不是时序图，箭头不表示唯一的数据流向。  |  原创虚构示例',40,1190,1760,24,14,'#68788B')
    d.save()

def lineage():
    d=Diagram('revenue-lineage','收入指标 · 从订单明细到管理报表的字段血缘','虚构场景  /  关注字段：net_revenue_cny  /  本期已履约商品金额 − 本期已完成退款金额；不含运费与税费',1900,1200)
    for x,w,n in [(40,320,'01  业务来源'),(500,320,'02  清洗与聚合'),(960,340,'03  统一事实'),(1460,390,'04  下游消费')]:
        d.text(n,x,190,w,28,19,'#263A50',True)
        d.box('',x,230,w,3,'strokeColor=none;fillColor=#D9DFEA;')
    def table(x,y,w,title,meta,fields,selected=(),badge=None):
        h=80+38*len(fields)
        d.box('',x,y,w,h,'rounded=1;arcSize=4;strokeColor=#C9D1E0;fillColor=#FFFFFF;strokeWidth=1.4;')
        d.box('',x,y,w,76,'rounded=0;strokeColor=none;fillColor=#F2F5FA;')
        d.text(meta,x+15,y+10,w-30,20,12,'#64748B')
        d.text(title,x+15,y+35,w-30,27,19,'#253C59',True)
        ids={}
        for j,f in enumerate(fields):
            active=f in selected
            ids[f]=d.box(f,x+8,y+80+j*38,w-16,34,f'align=left;spacingLeft=10;fontSize=16;rounded=1;arcSize=8;fillColor={"#EEEAFE" if active else "#FFFFFF"};strokeColor={"#8E78E9" if active else "none"};fontColor={"#583DB0" if active else "#65758A"};fontStyle={int(active)};')
        return ids
    orders=table(40,280,320,'order_items','OLTP  /  commerce  /  CDC ≤ 5 min',['order_item_id · PK','order_id · FK','fulfilled_at','item_net_cny'],['item_net_cny'])
    refunds=table(40,590,320,'refund_items','OLTP  /  aftersales  /  CDC ≤ 5 min',['refund_item_id · PK','order_item_id · FK','completed_at','refund_net_cny'],['refund_net_cny'])
    stores=table(40,900,320,'stores','MASTER  /  organization  /  daily',['store_id · PK','region_code'])
    clean=table(500,280,320,'stg_fulfilled_items','SQL MODEL  /  item grain',['order_item_id · PK','store_id','business_date','item_net_cny'],['item_net_cny'])
    refund=table(500,650,320,'int_refunds_daily','SQL MODEL  /  item × refund date',['order_item_id','business_date','refund_net_cny'],['refund_net_cny'])
    fact=table(960,420,340,'fct_revenue_daily','WAREHOUSE  /  date × store',['business_date · PK¹','store_id · PK¹','fulfilled_item_cny','completed_refund_cny','net_revenue_cny','region_code'],['fulfilled_item_cny','completed_refund_cny','net_revenue_cny'])
    metric=table(1460,280,390,'营业收入看板','BI DATASET  /  finance_daily',['business_date','net_revenue_cny','region_code'],['net_revenue_cny'])
    close=table(1460,580,390,'月度经营分析','SEMANTIC VIEW  /  monthly_revenue',['month × region','SUM(net_revenue_cny)'],['SUM(net_revenue_cny)'])
    alert=table(1460,850,390,'收入波动监测','RULE INPUT  /  revenue_monitor',['store_id × business_date','net_revenue_cny','7d_baseline'],['net_revenue_cny'])
    purple='strokeColor=#7958D6;strokeWidth=2.5;fontColor=#6549AD;curved=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;'
    muted='strokeColor=#B6C0CF;strokeWidth=1.3;curved=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;'
    def link(a,b,label='',pts=(),focus=True): d.edge(a,b,label,pts,purple if focus else muted)
    link(orders['order_item_id · PK'],clean['order_item_id · PK'],focus=False)
    link(orders['fulfilled_at'],clean['business_date'],focus=False)
    link(orders['item_net_cny'],clean['item_net_cny'],'已履约过滤')
    link(refunds['refund_net_cny'],refund['refund_net_cny'],'完成退款聚合')
    link(refunds['completed_at'],refund['business_date'],focus=False)
    link(clean['item_net_cny'],fact['fulfilled_item_cny'],'Σ 按日 / 门店',[(890,490)])
    link(refund['refund_net_cny'],fact['completed_refund_cny'],'Σ 按日 / 门店',[(890,785),(910,640)])
    link(stores['region_code'],fact['region_code'],'归属维度',[(880,1015),(915,715)],False)
    # The contract below defines intra-table calculation; cross-asset edges stay uncluttered.
    link(fact['net_revenue_cny'],metric['net_revenue_cny'],'',[(1400,650),(1410,415)])
    link(fact['net_revenue_cny'],close['SUM(net_revenue_cny)'],'',[(1390,680)])
    link(fact['net_revenue_cny'],alert['net_revenue_cny'],'',[(1400,730),(1410,985)])
    d.box('',940,820,380,210,'rounded=1;arcSize=6;fillColor=#F6F3FE;strokeColor=#DDD5F3;')
    d.text('指标契约 / BUSINESS CONTRACT',960,838,340,25,15,'#6549AD',True)
    d.text('净收入 = 已履约商品金额 − 已完成退款\n业务日：Asia/Shanghai 自然日\n货币：CNY；允许负净收入\n¹ 复合主键：业务日 + 门店\n退款按完成日入账，不回写原订单日',960,877,340,130,16,'#4B4560')
    d.text('紫色字段与实线：当前收入指标依赖路径    ·    灰色字段与线：上下文依赖    ·    箭头：源字段 → 派生字段',40,1100,1800,27,16)
    d.text('展示相关字段而非全量 Schema；省略非焦点主键传递与维表连接。所有资产、字段与口径均为虚构演示，非会计准则建议。',40,1140,1800,27,14,'#68788B')
    d.save()
if __name__=='__main__': landscape();lineage()
