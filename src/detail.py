
import time
import requests
from lxml import etree
import re
import json
#  //*[@id="js-size-selector"]  大小选择


def requ_repeat(link,err_txt,par=None,hes = None):
    """ 用于多次重试

    Args:
        link (_type_): _description_
        err_txt (_type_): _description_

    Returns:
        _type_: _description_
    """
    keep = True
    maxtimes = 3
    count = 0
    while keep and count < maxtimes:
        try:
            # if hes == None:
            #     hes = {
            #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
            #     }
            response = requests.request("GET",link,timeout=5,params=par,headers=hes)
            if response.status_code == 200:
                keep = False
                return response
            else:
                count = count + 1
                print(err_txt+'  获取重试' + str(count))
                pass
        except Exception as e:
            # print(e)
            count = count + 1
            print(err_txt+'  获取重试' + str(count))
        
    return False


def get_html(pdd):
    # https://www.prada.com/fr/fr/men/bags/messenger_bags/products.nux.getProductsByPartNumbers.json?partNumbers=2VH069_2FKL_F0807_V_MOF
    url = pdd
    try:
        response = requ_repeat(link=url,err_txt='商品详情页 html ')
        if response == False:
            return '0'
        p_html = etree.HTML(response.text)
        
        return p_html
    except Exception as e:
        print(url,'请求失败')
        return '0'

    

def get_name(p):
    try:
        name = p.xpath('//h1[@class="product-name"]/text()')[0]
        return name   #  name  中 会不会有  换行符
    except:
        print('name 提取出错')
        return 'err'


def get_pr(p):
    try:
        pr = p.xpath('//div[@class="product-main-content-inner"]/div[@class="product-price"]/span/text()')[0]
        pr = pr[:-2]
        return pr
    except:
        # print('价格  采集失败')
        return 'err'


def get_imu(p):
    imgs = p.xpath('//div[@class="product-block-images"]/ul/li')
    itt = ''
    for img in imgs:
        imo = img.xpath('.//img/@srcset')
        if len(imo) == 0:
            imo= img.xpath('.//img/@data-srcset')
        if imo == []:
            continue
        imo = imo[0]
        imt = imo.split(',')[0]
        im = imt.split(' ')[0]
        itt = itt +im + ','
    return itt




def l3(st_jsons):
    t = 0
    for s in st_jsons:
        n = s
        if n == 'Louis Vuitton Paris Galeries Lafayette':
            t = 1
    return t


def get_l4(ns):
    """
    第四行货量
    """
    pgns = []
    tp = 0
    tg = 0 
    p = True
    g = True
    for n in ns:
        n_u = n.upper()
        if 'PRINTEMPS' in n_u:
            pgns.append(n)
            if p:
                tp = tp+1
                p = False
        if 'GALERIES' in n_u:
            pgns.append(n)
            if g:
                tg = tg + 1
                g = False
    
    
    for pgst in pgns:
        ns.remove(pgst)
    
    t = tp + tg + len(ns)
                
    return t



def get_sts(vstids):
    sts = []
    for vstid in vstids:
        stid = vstid[1]
        if stid == None:
            continue
        v = vstid[0]
        l3 = vstid[2]
        url = 'https://www.givenchy.com/on/demandware.store/Sites-GIV_FR-Site/fr/FindInStore-Find?pid='+stid+'&filter_country=fr&show_name=true'
        response = requ_repeat(link=url,err_txt='商品店铺 html ')
        if response == False:
            print('获取商店失败')
            st = [v,'err','err']
            sts.append(st)
            continue
        p = etree.HTML(response.text)
        sts_lis = p.xpath('//ul[@class="store-list"]/li[@class="store instock"]')
        ns = []
        for st_li in sts_lis:
            try:
                n = st_li.xpath('./section/h3//span/text()')[0]
                ns.append(n)
            except:
                continue
        l4 = get_l4(ns)
        
        sts.append([v,l3,l4])
        

    return sts

def get_id(p):
    ps = p.split('/')
    id = ps[-1][:-5]
    return id

def get_sz(p):
    try:
        ts = p.xpath('//div[@class="size-list js-size-list"]/div')
        szs =[]
        for t in ts:
            try:
                v = t.xpath('.//input/@value')[0]
                u = t.xpath('.//input/@data-url')[0]
                if t.xpath('./label[@class="dropdown-option__label unavailable-size"]') == []:
                    l3 = 1 
                else:
                    l3 = 0
                szs.append([v,u,l3])
            except:
                continue
        return szs 
    except:
        return []
    
def u_sid(szs):
    for sz in szs:
        url = sz[1]
        response = requ_repeat(link=url,err_txt='szid html ')
        if response == False:
            print('获取szid失败')
            sz[1] = None
            continue
        p = etree.HTML(response.text)
        stid = p.xpath('//div[@class="inventory"]/input/@value')[0]
        sz[1] = stid
    
    return szs

def get_zu(p):
    try:
        zu = p.xpath('//option[@data-dispatcher-countrycode="CN"]/@value')[0]
        return zu
    except:
        return False

def get_zh(url_zh):
    response = requ_repeat(link=url_zh,err_txt='商品详情页zh html ')
    if response == False:
        return False
    p_html = etree.HTML(response.text)
    '''
    try:  #  script type="application/ld+json"
        jss = p_html.xpath('//script[@type="application/ld+json"]/text()')
        if len(jss) == 1:
            js = jss[0]
            js_json = json.loads(js)
        else:
            js = jss[1]
            js_json = json.loads(js)
        try:
            matps = p_html.xpath('//div[@class="product-dl-item"]')
            for matp in matps:
                jt = matp.xpath('./dt/text()')[0]
                if '材质' in jt:
                    mats = matp.xpath('./dd//text()')
                    for mat in mats:
                        mt = mat.replace('\n','')
                        mt = mt.replace(' ','')
                        mt = mt.replace('\t','')
                        mt = mt.replace('\r','')
                        if mt != '':
                            js_json['material'] = mt
                        else:
                            continue
                    break
        except:
            js_json['material'] = ''
    '''
    return p_html
    # except:
    #     return False

def get_pds_fr(p):
    pds = {
        'name': '',
        'material': '',
        'color': '',
        'st': '',
        'description': ''
    }
    return pds

def get_pds_zh(p):
    pds = {
        'name': '',
        'material': '',
        'color': '',
        'st': '',
        'description': ''
    }
    try:#h1 class="product-name"
        name = p.xpath('//h1[@class="product-name"]/@k-productname')[0]
        pds['name'] = name
    except:
        pass
    try:
        pt = p.xpath('//dl[@class="table-brand"]/div[2]/dd')[0]
        materials = pt.xpath('.//text()')
        mat = ''
        for t in materials:
            t = t.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
            if t == '':
                continue
            else:
                mat = t.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
        if mat == '':
            print('/')
            pass
        pds['material'] = mat
    except:
        pass
    try:
        color = p.xpath('//dl[@class="table-brand"]/div[1]/dd/text()')[0].replace(' ','').replace('\t','').replace('\r','').replace('\n','')
        pds['color'] = color
    except:
        pass
    # try:
    #     st = p['st']
    #     pds['st'] = st
    # except:
    #     pass
    try:
        descriptions = p.xpath('//div[@class="short-description"]/ul/li')
        description = ''
        for des in descriptions:
            if des.xpath('./text()') == []:
                continue
            if des.xpath('./text()')[0] in description:
                break
            else:
                description = description + des.xpath('./text()')[0] + ','
        pds['description'] = description
    except:
        pass
    return pds


def deal(id,p):
    name= get_name(p)
    pr = get_pr(p)
    imu = get_imu(p)
    sz  = get_sz(p)
    
    if len(sz) == 0:
        v = 'os'
        stid = p.xpath('//div[@class="inventory"]/input/@value')[0]
        if p.xpath('//button[@id="add-to-cart"]/span[@class="btn__label"]/text()') == []:
            l3 = 0
        elif p.xpath('//button[@id="add-to-cart"]/span[@class="btn__label"]/text()')[0] == 'Ajouter au panier':
            l3 = 1
        else:
            l3 =0   
        sts = get_sts([[v,stid,l3]])
        pass
    else:
        szid = u_sid(sz)
        sts = get_sts(szid)
        pass
    # 增加  中文名称 材料  颜色 尺码标准 描述
    url_zh  = get_zu(p)
    if '?' in url_zh:
        url_zh = url_zh.split('?')[0]
    pds = {
        'name':name,
        'material':'',
        'color':'',
        'st':'',
        'description':''
    }
    if url_zh == False or url_zh == None:
        pds = pds
        pass
    else:
        zh_json = get_zh(url_zh)
        if zh_json == False or zh_json.xpath('//h1[@class="product-name"]/@k-productname') == []:
            pds = get_pds_zh(p)
        else:
            pds = get_pds_zh(zh_json)

    des = []
    for st in sts:
        de = [id,pr]+st+[pds['name'],pds['material'],pds['color'],pds['st'],pds['description'],imu]
        des.append(de)
    return des


def main(pdd):
    id = get_id(pdd)
    p = get_html(pdd)
    
    if type(p) == str:
        return [[id,'','OS','','','','','','','','']]
    else:
        dts = deal(id,p)
        return dts
    
def out(pdd):
    return main(pdd)

if __name__ == '__main__':
    pdd = 'https://www.givenchy.com/fr/fr/veste-en-laine-a-detail-plisse/BW30DW1497-001.html'
    out(pdd) 