# -*- coding: utf-8 -*-

import re
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

fn_input = 'sample_table.last.json'
fn_output = 'result.last.json'

# province = '\u7701'
# city = '\u5e02'
# area = '\u533a'
# county = '\u53bf'

# 匹配{省&市(县|区|市)} 如 浙江省杭州市江干区
p_province_city_area_county = u'(.*?\u7701)(.*?\u5e02)(.*[\u53bf|\u533a|\u5e02])'

# 匹配{省&市} 如 广东省中山市
p_province_city = u'(.*?\u7701)(.*\u5e02)'

# 匹配{市(县|区)} 如 天津市宁河县
p_city_area_county = u'(.*?\u5e02)(.*?[\u53bf|\u533a|\u5e02])'

# 匹配{省&地区&(县|区|市)} 如 四川省资阳地区仁寿县
# 如果匹配,需要将(地区)换成(市)
p_province_region_area_county = u'(.*?\u7701)(.*?\u5730\u533a)(.*[\u53bf|\u533a|\u5e02])'

# 匹配{省&地区} 如 江西省赣州地区
# 如果匹配,需要将(地区)换成(市)
p_province_region = u'(.*?\u7701)(.*?\u5730\u533a)'

# 匹配{省&自治州&(县|区|市)} 如 云南省楚雄彝族自治州元谋县
p_province_prefecture_area_county = u'(.*?\u7701)(.*\u81ea\u6cbb\u5dde)(.*[\u53bf|\u533a|\u5e02]?)'

# 匹配{自治区&(市|盟)&(县|区|市)} 如 宁夏回族自治区吴忠市中卫县 内蒙古自治区哲里木盟通辽县
p_prefecture_city_county = u'(.*?\u81ea\u6cbb\u533a)(.*?[\u5e02|\u76df])(.*[\u53bf|\u533a|\u5e02])'

# 匹配{自治区&盟&(*)} 如 内蒙古自治区哲里木盟库伦旗
p_prefecture_city = u'(.*?\u81ea\u6cbb\u533a)(.*?[\u5e02|\u76df])(.*)'

# 匹配{自治区&自治州&(县|区|市)} 如 新疆维吾尔自治区巴音郭楞蒙古自治州和静县
p_prefecture_prefecture_county = u'(.*?\u81ea\u6cbb\u533a)(.*\u81ea\u6cbb\u5dde)(.*[\u53bf|\u533a|\u5e02])'

# 匹配{自治区&地区&(县|区|市)} 如 广西壮族自治区南宁地区宾阳县
# 如果匹配,需要将(地区)换成(市)
p_prefecture_region_county = u'(.*?\u81ea\u6cbb\u533a)(.*?\u5730\u533a)(.*[\u53bf|\u533a|\u5e02])'

# 匹配{省&县} 如 福建省同安县
p_province_county = u'(.*?\u7701)(.*\u53bf)'

eol = b'\n'

f_input = open(fn_input, 'r')
f_output = open(fn_output, 'wr+')


def write_record(fp, record):
    # del record['native_place']
    fp.write(json.dumps(record, ensure_ascii=False) + eol)


def update_record(record, province=None, city=None, county=None):
    tmp = dict(record)
    tmp.update({
        'province': province,
        'city': city,
        'county': county
    })
    return tmp


# ind = 0
for line in f_input.readlines():
    # ind += 1
    # if ind > 2000:
    #     break

    line = line.strip()
    record = json.loads(line)
    record['native_place'] = unicode(str(record['native_place']))

    record['number_of_fetus'] = record['number_of_fetus'] not in ['null', ''] and int(record['number_of_fetus']) or None
    record['age'] = record['age'] not in ['null', ''] and int(record['age']) or None
    record['fetus_gender'] = record['fetus_gender'] not in ['null', ''] and int(record['fetus_gender']) or None
    record['pregnancy_week'] = record['pregnancy_week'] not in ['null', ''] and int(record['pregnancy_week']) or None
    record['gestational_week'] = record['gestational_week'] not in ['null', ''] and int(record['gestational_week']) or None
    record['ivf_symbol'] = record['ivf_symbol'] not in ['null', ''] and int(record['ivf_symbol']) or None
    record['ethnicity'] = record['ethnicity'] not in ['null', ''] and record['ethnicity'] or None

    # 新疆维吾尔自治区巴音郭楞蒙古自治州和静县
    matches = re.match(p_prefecture_prefecture_county, record['native_place'])
    if matches:
        record = update_record(record, province=matches.groups()[0], city=matches.groups()[1].replace('省直辖行政单位', ''), county=matches.groups()[2])
        write_record(f_output, record)
        continue

    # 云南省楚雄彝族自治州元谋县
    matches = re.match(p_province_prefecture_area_county, record['native_place'])
    if matches:
        record = update_record(record, province=matches.groups()[0], city=matches.groups()[1].replace('省直辖行政单位', ''), county=matches.groups()[2])
        write_record(f_output, record)
        continue

    # 广西壮族自治区南宁地区宾阳县
    matches = re.match(p_prefecture_region_county, record['native_place'])
    if matches:
        record = update_record(record, province=matches.groups()[0], city=matches.groups()[1].replace('地区', '市'),
                               county=matches.groups()[2])
        write_record(f_output, record)
        continue

    # 宁夏回族自治区吴忠市中卫县 内蒙古自治区哲里木盟通辽县
    matches = re.match(p_prefecture_city_county, record['native_place'])
    if matches:
        record = update_record(record, province=matches.groups()[0], city=matches.groups()[1].replace('省直辖行政单位', ''),
                               county=matches.groups()[2])
        write_record(f_output, record)
        continue

    # 内蒙古自治区哲里木盟库伦旗
    matches = re.match(p_prefecture_city, record['native_place'])
    if matches:
        record = update_record(record, province=matches.groups()[0], city=matches.groups()[1].replace('省直辖行政单位', ''),
                               county=matches.groups()[2])
        write_record(f_output, record)
        continue

    # 四川省资阳地区仁寿县
    matches = re.match(p_province_region_area_county, record['native_place'])
    if matches:
        record = update_record(record, province=matches.groups()[0], city=matches.groups()[1].replace('地区', '市'),
                               county=matches.groups()[2])
        write_record(f_output, record)
        continue

    # 江西省赣州地区
    matches = re.match(p_province_region, record['native_place'])
    if matches:
        record = update_record(record, province=matches.groups()[0], city=matches.groups()[1].replace('地区', '市'))
        write_record(f_output, record)
        continue

    # 浙江省杭州市江干区
    matches = re.match(p_province_city_area_county, record['native_place'])
    if matches:
        record = update_record(record, province=matches.groups()[0], city=matches.groups()[1], county=matches.groups()[2])
        write_record(f_output, record)
        continue

    # 广东省中山市
    matches = re.match(p_province_city, record['native_place'])
    if matches:
        record = update_record(record, province=matches.groups()[0], city=matches.groups()[1].replace('省直辖行政单位', ''))
        write_record(f_output, record)
        continue

    # 天津市宁河县
    matches = re.match(p_city_area_county, record['native_place'])
    if matches:
        record = update_record(record, city=matches.groups()[0], county=matches.groups()[1])
        write_record(f_output, record)
        continue

    # 福建省同安县
    matches = re.match(p_province_county, record['native_place'])
    if matches:
        record = update_record(record, province=matches.groups()[0], county=matches.groups()[1])
        write_record(f_output, record)
        continue

    write_record(f_output, record)


f_output.close()
f_input.close()


