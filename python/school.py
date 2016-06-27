#!/bin/python3
import requests
from lxml import etree

html = '''
<div class="area_select">   学校所在地： <select onchange="change_state(this)" id="state_select" name="select">     <option value="0">中国</option>     <option value="840">美国</option>       <option value="124">加拿大</option>     <option value="826">英国</option>       <option value="36">澳大利亚</option>        <option value="554">新西兰</option>     <option value="702">新加坡</option>     <option value="372">爱尔兰</option>     <option value="528">荷兰</option>       <option value="458">马来西亚</option>       <option value="764">泰国</option>       <option value="710">南非</option>       <option value="578">挪威</option>       <option value="208">丹麦</option>       <option value="608">菲律宾</option>     <option value="9999">其他</option>  </select>　<select onchange="select_city(this)" id="_province" style="width: 105px;">       <option value="0">请选择省(市)...</option>      <option value="11">北京</option>        <option value="12">天津</option>        <option value="13">河北</option>        <option value="14">山西</option>        <option value="15">内蒙古</option>      <option value="21">辽宁</option>        <option value="22">吉林</option>        <option value="23">黑龙江</option>      <option value="31">上海</option>        <option value="32">江苏</option>        <option value="33">浙江</option>        <option value="34">安徽</option>        <option value="35">福建</option>        <option value="36">江西</option>        <option value="37">山东</option>        <option value="41">河南</option>        <option value="42">湖北</option>        <option value="43">湖南</option>        <option value="44">广东</option>        <option value="45">广西</option>        <option value="46">海南</option>       <option value="50">重庆</option>        <option value="51">四川</option>        <option value="52">贵州</option>        <option value="53">云南</option>        <option value="54">西藏</option>        <option value="61">陕西</option>        <option value="62">甘肃</option>        <option value="63">青海</option>        <option value="64">宁夏</option>        <option value="65">新疆</option>        <option value="71">台湾</option>        <option value="81">香港</option>        <option value="82">澳门</option>    </select></div>
'''
xml = etree.fromstring(html)
state=xml.xpath('//select[@id="state_select"]/option')
city=xml.xpath('//select[@id="_province"]/option')
file_root='http://cdn.tencentgroup.qq.com/join_static/'

for s in state :
    root = etree.Element(s.text)
    if s.values()[0] == '0' :
        for c in city :
            if(c.values()[0] != '0') :
                child = etree.Element(c.text)
                url = file_root + 'school/'+ c.values()[0] + '_1.htm'
                req = requests.get(url)
                text = req.text.encode(req.encoding).decode()
                unixml = etree.fromstring(text)
                unis = unixml.xpath('//a')
                for uni in unis :
                    cd = etree.Element('school')
                    cd.text = uni.text
                    child.append(cd)
                root.append(child)
    else:
        url = file_root + 'school/f'+ s.values()[0] + '_1.htm'
        req = requests.get(url)
        text = req.text.encode(req.encoding).decode()
        unixml = etree.HTML(text)
        unis = unixml.xpath('//a')
        for uni in unis :
            cd = etree.Element('school')
            cd.text = uni.text
            root.append(cd)
    print(etree.tostring(root, encoding='utf8').decode())
