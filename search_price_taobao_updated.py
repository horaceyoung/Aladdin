import json
import requests
import telepot
import re



def search_taobao(msg):
    
    item_name = msg['text']
    response = requests.get('https://s.taobao.com/search?q='+item_name)    
    html = response.text
    regex =  r'g_page_config =(.+)'
    items = re.findall(regex, html)
    items = items.pop().strip()
    items = items[0:-1]
    items = json.loads(items)
    item_list= items['mods']['itemlist']['data']['auctions']
    #raw name
    try:        
        name1 = item_list[0]['raw_title'] 
        name2 = item_list[1]['raw_title']
        name3 = item_list[2]['raw_title']
    #prices
        price1 = '¥'+ item_list[0]['view_price'] 
        price2 = '¥'+ item_list[1]['view_price'] 
        price3 = '¥'+ item_list[2]['view_price'] 
      # To send the result to users
    
        return('The first three results of '+item_name+' in Taobao are listed below: ''\n\n'+ name1 +'  '+ price1+'\n\n'+ name2 +'  ' + price2+'\n\n'+ name3 + '  ' + price3
                        +'\n\nHere you go the links\U000026C4: \n'+ item_list[0]['detail_url']
                        +'\n\n'+ item_list[1]['detail_url']
                        +'\n\n'+ item_list[2]['detail_url'])
    except IndexError:
        return("\U0001F614 Sorry , the Taobao server is too busy,"+
               " maybe you can try to search another item name .")
                       

