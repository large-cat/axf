# -*- coding:utf-8 -*-

import json

def readJsonFile(path):
    with open(path, "rb") as f:
        data = json.load(f)

    return data

a = readJsonFile("flash.json")
data = a["data"]["products"]
list = []
for k,v in data.items():
    # if k == "104749":
    #     continue
    for item in v:
        str = "insert into axf_goods(productid,productimg,productname,productlongname,isxf,pmdesc,specifics,price,marketprice,categoryid,childcid,childcidname,dealerid,storenums,productnum) values("
        str += "\"" + item["product_id"] + "\","
        str += "\"" + item["img"] + "\","
        str += "\"" + item["keywords"] + "\","
        str += "\"" + item["long_name"] + "\","
        a = "%d"%item["is_xf"]
        str +=  a + ","
        z = item["pm_desc"]
        # if z == "":
        #     z = ""
        # else:
        #     z = 1
        # z = "%d"%z
        str += "\"" + z + "\","
        str += "\"" + item["specifics"] + "\","
        b = 0
        try:
            b = "%.2f"%item["price"]
        except:
            b = item["price"]
        str += b + ","
        e = "%.2f"%item["market_price"]
        str += e + ","
        f = 0
        try:
            f = "%d" % item["category_id"]
        except:
            f = item["category_id"]

        str += f + ","
        try:
            g = "%d"%item["child_cid"]
        except:
            g = item["child_cid"]
        str += g + ","
        try:
            str += "\"" + item["cids"][g] + "\","
            str += "\"" + item["dealer_id"] + "\","
        except:
            continue
        c = "%d" % item["store_nums"]
        str += c + ","
        d = 0
        try:
            d = "%d" % item["product_num"]
        except:
            d = item["product_num"]
        str += d + ");"
        print(str)
        list.append(str)



