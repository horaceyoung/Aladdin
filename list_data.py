""" This file contains the text Aladdin displays on inline keyboards, reply keyboards and other messages Aladdin replies to the user
"""
from Text import *
function_list = [text_button_sell, text_button_buy, text_button_modify_items, text_button_my_shop]

primary_sale_list = [('study materials', 'study materials'), ('electronics', 'electronics'), ('mobile phones & tablets','mobile phones & tablets'), ('motorbikes', 'motorbikes'), ('video gaming', 'video gaming'), ('photography', 'photography')
                     , ('men\'s fashion', 'men\'s fashion'), ('women\'s fashion', 'women\'s fashion'), ('sports gear', 'sports gear'), ('toys & boardgames', 'toys & boardgames'), ('music & other media', 'music & other media')]
secondary_sale_list = {
    'study materials': [('textbooks', 'textbooks'), ('lecture notes', 'lecture notes'), ('past year papers', 'past year papers'),('books', 'books'),('stationary', 'stationary')],
    'electronics':[('laptops', 'laptops'), ('computers', 'computers'), ('computer accessories', 'computer accessories'), ('other gadgets', 'other gadgets'), ('earphones or headphones', 'earphones or headphones')],
    'mobile phones & tablets':[('iphone', 'iphone'), ('android phones', 'android phones'), ('mobile phone accessories'), ('tablets', 'tablets')],
    'motorbikes':[('motorbikes for sale', 'motorbikes for sale'), ('motorbike accessories', 'motorbike accessories')],
    'video gaming':[('video games', 'video games'), ('video game consoles', 'video game consoles'), ('gaming accessories', 'gaming accessories')],
    'photography': [('camera', 'camera'), ('camera accessories', 'camera accessories')],
    'men\'s fashion':[('wallets', 'wallets'), ('footwear', 'footwear'), ('watches', 'watches'), ('clothes', 'clothes')],
    'women\'s fashion':[('wallets', 'wallets'), ('shoes', 'shoes'), ('watches', 'watches'), ('clothes', 'clothes'), ('jewellery', 'jewellery')],
    'sports gear': [('bicycles', 'bicycles'), ('athletic & sports clothing', 'athletic & sports clothing'), ('skateboards', 'skateboards'), ('others', 'others')],
    'toys & boardgames':[('toys', 'toys'), ('boardgames', 'boardgames')],
    'music & other media':[('musical instruments', 'musical instruments'), ('CDs, DVDs and other media', 'CDs, DVDs and other media'), ('music accessories', 'music accessories')],
}

search_list = [(text_button_search_by_type, 'type'), (text_button_search_by_keyword, 'keyword'), (text_button_search_by_shop_name, 'shop name'), (text_button_online_resources, 'internet')]
yes_or_no = [(text_button_yes, 'yes'), (text_button_no, 'no')]
attribute_list = [('price', 'price'), ('description', 'description'), ('delete', 'delete')]

display_attribute_dict = {'price': 'price', 'shop_name': 'shop name', 'item_type_2': 'item type', 'description': 'description', 'item_id': 'item id'}
