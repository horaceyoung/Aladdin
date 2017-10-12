import time
import json
import telepot
from pprint import pprint
from Text import *
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from searchXXXX import search_info
from search_price_taobao_updated import search_taobao
from list_data import function_list, primary_sale_list, secondary_sale_list, search_list, yes_or_no, attribute_list, display_attribute_dict

# This class is to store item information and shop information

class add_item(object):

    def __init__(self):
        self.new_item = {}
        self.shop_info = {}
        self.user_info = {}

    def add_attribute(self, attribute_name, info):
        self.new_item[attribute_name] = info

    def add_shop(self, attribute_name, info):
        self.shop_info[attribute_name] = info

    def add_user(self, attribute_name, info):
        self.user_info[attribute_name] = info

# This is our class, Aladdin
class Aladdin(telepot.helper.ChatHandler):

    # This function is to initialize Aladdin
    def __init__(self, *args, **kwargs):
        super(Aladdin, self).__init__(include_callback_query=True, *args, **kwargs)
        self.indicator = 'choose_function'
        self.store = add_item()

    # This function is what Aladdin does when the user first send a message
    def open(self, initial_msg, seed):
        content_type, chat_type, chat_id = telepot.glance(initial_msg)
        if chat_type == 'group' and initial_msg['text'] == '@aladdin_of_teletubbies_bot  Answer my summoning!':
            bot.sendMessage(chat_id, text_helping_message, parse_mode='Markdown')
            self.close()
        if chat_type == "private":
            search_result = self.search_data('user_info.json', 'chat_id', chat_id)
            if not search_result:
                bot.sendMessage(chat_id, text_helping_message, parse_mode='Markdown')
                self.store.add_user('chat_id', chat_id)
                self.store.add_user('first_name', initial_msg['chat']['first_name'])
                if 'last_name' in initial_msg['chat']:
                    self.store.add_user('last_name', initial_msg['chat']['last_name'])
                if 'username' in initial_msg['chat']:
                    self.store.add_user('username', initial_msg['chat']['username'])
                with open('user_info.json', 'a') as handle:
                    json.dump(self.store.user_info, handle)
                    handle.write("\n")
                handle.close()
            self.send_list_keyboard(chat_id, text_welcome_message, function_list)
            bot.sendAudio(chat_id, gif_welcome)
        return True

    # This function is to send a custom inline keyboard to the user
    def send_custom_inline_keyboard(self, chat_id, text_info, send_tuple_list):
        kb = []
        for t in send_tuple_list:
            kb.append([InlineKeyboardButton(text=t[0], callback_data=t[1])])
        mark_up = InlineKeyboardMarkup(inline_keyboard=kb)
        bot.sendMessage(chat_id, text=text_info, reply_markup=mark_up, parse_mode='Markdown')

    # This function is to add information to the item, send a message to the user, and change indicator
    def add_attribute_info(self, attribute_name, read_message, send_message, change_indicator):
        self.store.add_attribute(attribute_name, read_message)
        self.sender.sendMessage(send_message, parse_mode='Markdown')
        self.indicator = change_indicator

    # This function is to send a custom reply keyboard to the user
    # (the messages displayed on the keyboards are passed to the function as strings)
    def send_custom_keyboard(self, chat_id, text_info, *args):
        kb = []
        kb_2 = []
        for arg in args:
            kb.append(KeyboardButton(text=arg))
        kb_2.append(kb)
        mark_up = ReplyKeyboardMarkup(keyboard=kb_2, resize_keyboard = True, one_time_keyboard = True )
        bot.sendMessage(chat_id, text=text_info, reply_markup=mark_up)

    # This function is also to send a custom reply keyboard to the user
    # (the messages displayed on the keyboards are passed to the function as a list of strings)
    def send_list_keyboard(self, chat_id, text_info, lst):
        kb = []
        kb_2 = []
        for item in lst:
            kb.append(item)
            kb_2.append(kb)
            kb = []
        mark_up = ReplyKeyboardMarkup(keyboard=kb_2, one_time_keyboard = True)
        bot.sendMessage(chat_id, text=text_info, reply_markup=mark_up)

    # This function is to search data (a key-value pair) from the database
    def search_data(self, file, search_key, search_value):
        with open(file, 'r') as handle:
            user_sale_data = [json.loads(line) for line in handle]

            # when the database is empty, return an empty list
            if not user_sale_data:
                handle.close()
                return []

            # when the database is not empty, search through the database and return the search result
            else:
                return_list = []
                for data in user_sale_data:
                    if data[search_key] == search_value:
                        return_list.append(data)
                handle.close()
                return return_list

    # This function is to search whether the keyword (search_value in the function)
    # is part of the value which corresponds to the key
    def search_keyword(self, search_key, search_value):
        with open('item.json', 'r') as handle:
            user_sale_data = [json.loads(line) for line in handle]

            # when the database is empty
            if not user_sale_data:
                handle.close()
                return []

            # when the database is not empty
            else:
                return_list = []
                for data in user_sale_data:
                    if search_value in data[search_key]:
                        return_list.append(data)
                handle.close()
                return return_list

    # This function is to format and send the key information of the item(s) and send to the user
    def we_have_found(self, found_list, user_id):
        result = text_have_found+'\n'
        result_2 = ''

        # if the item list is not empty
        if found_list:
            for data in found_list:
                for attribute in ['item_id', 'item_type_2', 'price']:
                    if attribute == 'item_id':
                        result_2 += '/' + str(data[attribute]) + '\t'
                    elif attribute == 'price':
                        result_2 += '$' + str(data[attribute]) + '\t'
                    else:
                        result_2 += str(data[attribute]) + ' \t'
                result_2 += '\n'

        # send the result to the user
        if result_2:
            result += result_2
            bot.sendMessage(user_id, result)

        # if the item list is empty, inform the user about this and end the service
        else:
            bot.sendMessage(user_id, text_sorry)
            self.send_list_keyboard(user_id, text_thank_you, [text_button_main])
            self.close()

    # This function is to send the detailed information of an item to the user
    def display_info(self, info, user_id, attribute_list):
        result = text_display_detail
        result_2 = ''

        # if info is not empty, generate the formatted message
        if info:
            for attribute in attribute_list:
                if attribute == 'item_id':
                    result_2 += '/' + str(info[attribute]) + '\n'
                elif attribute == 'price':
                    result_2 += 'price: $' + str(info[attribute]) + '\n'
                else:
                    result_2 += display_attribute_dict[attribute] + ': ' + str(info[attribute]) + '\n'
        # send the formatted message to the user
        if result_2:
            result += result_2
            bot.sendMessage(user_id, result)
        # if info is empty, it means that the user has input an invalid item id
        # in this case, remind the user to choose from the item list Aladdin provided
        else:
            bot.sendMessage(user_id, text_choose_from_list)

    # This funciton is to respond to the user's callback query
    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        # Close inline keyboard
        inline_message_id = msg['message']['chat']['id'], msg['message']['message_id']
        bot.editMessageReplyMarkup(inline_message_id, reply_markup=None)

        # --------------- SELL ---------------
        if self.indicator == 'choose_item_type':
            bot.sendMessage(from_id, text_chosen_type+' %s!' % query_data)
            self.store.add_attribute("item_type_1", query_data)

            self.send_custom_inline_keyboard(from_id, text_choose_type2, secondary_sale_list[query_data])
            self.indicator = 'choose_item_type_2'

        elif self.indicator == 'choose_item_type_2':
            bot.sendMessage(from_id, text_chosen_type+'%s!' % query_data)
            self.store.add_attribute("item_type_2", query_data)
            bot.sendMessage(from_id, text_input_price, parse_mode='Markdown')
            self.indicator = 'input_price'

        elif self.indicator == 'choose_input_image':
            if query_data == 'yes':
                bot.sendMessage(from_id, text_send_photo)
                self.indicator = 'input_image'
            elif query_data == 'no':
                self.store.add_attribute('photo_id', '')
                self.send_list_keyboard(from_id, text_successfully_add, [text_button_main])

                # at this point, since the user chose to not add a photo of the item, he/she has completed inputting
                # all the necessary information
                # we can now store information to the database

                # read from database
                with open('item.json', 'r') as handle:
                    user_sale_data = [json.loads(line) for line in handle]
                    individual_sale_data = []

                    for data in user_sale_data:
                        if data['chat_id'] == from_id:
                            individual_sale_data.append(data)

                    # create item id from user id
                    # the first part of item id is the user id
                    # the last three digits of the item id indicate the index of the item in a user's item list
                    if not individual_sale_data:
                        self.store.new_item['item_id'] = from_id * 1000 + 1
                    else:
                        self.store.new_item['item_id'] = from_id * 1000 + len(individual_sale_data) + 1
                    handle.close()

                # write to database
                with open('item.json', 'a') as handle:
                    json.dump(self.store.new_item, handle)
                    handle.write("\n")
                handle.close()
                self.close()

        # --------------- BUY ---------------
        elif self.indicator == 'how_to_search':
            if query_data == 'type':
                self.store.add_attribute('search_type', query_data)
                self.send_custom_inline_keyboard(from_id, text_search_type1, primary_sale_list)
                self.indicator = 'type_search'

            elif query_data == 'keyword':
                self.add_attribute_info('search_type', query_data, text_keyword, "keyword_search")

            elif query_data == 'shop name':
                self.add_attribute_info('search_type', query_data, text_shop_name, "shop_name_search")

            elif query_data == 'internet':
                bot.sendMessage(from_id, text_online_keyword)
                self.indicator = 'give_internet_search_result'

        elif self.indicator == 'type_search':
            bot.sendMessage(from_id, 'Okay, %s!' % query_data)
            self.store.add_attribute('item_type_1', query_data)
            self.send_custom_inline_keyboard(from_id, text_search_type2, secondary_sale_list[query_data])
            self.indicator = 'find'

        elif self.indicator == 'find':
            bot.sendMessage(from_id, text_searched_type+' %s!' % query_data)
            self.add_attribute_info('item_type_2', query_data, text_searching, "not decided")
            bot.sendAudio(from_id, gif_searching)

            search_result = self.search_data('item.json', 'item_type_2', self.store.new_item['item_type_2'])
            self.we_have_found(search_result, from_id)
            bot.sendMessage(from_id, text_choose_item, parse_mode='Markdown')
            self.indicator = 'choose_item'

        elif self.indicator == 'want_contact_or_not':
            if query_data == 'yes':
                item_owner = int(self.store.shop_info['temp_item']/1000)
                with open('shop_info.json', 'r') as handle:
                    contact_data = [json.loads(line) for line in handle]
                    for data in contact_data:
                        if data['contact']['contact']['user_id'] == item_owner:
                            contact_send = data
                bot.sendContact(from_id, contact_send['contact']['contact']['phone_number'], contact_send['contact']['contact']['first_name'], contact_send['contact']['contact']['last_name'])
            self.send_custom_inline_keyboard(from_id, text_check_another, yes_or_no)
            self.indicator = 'next_item'

        elif self.indicator == 'next_item':
            if query_data == 'yes':
                self.indicator = 'choose_item'
            elif query_data == 'no':
                self.send_list_keyboard(from_id, text_thank_you, [text_button_main])
                self.close()

        # --------------- CHANGE ---------------
        elif self.indicator == 'change_attribute':
            if query_data == 'delete':
                with open('item.json', 'r') as handle:
                    user_sale_data = [json.loads(line) for line in handle]
                    for data in user_sale_data:
                        if str(data['item_id']) == str(self.store.new_item['item_id']):
                            user_sale_data.remove(data)
                            self.store.new_item['original_data'] = data
                    handle.close()
                with open('item.json', 'w') as handle:
                    for data in user_sale_data:
                        json.dump(data, handle)
                        handle.write("\n")
                    handle.close()
                bot.sendMessage(from_id, text_successfully_delete)
                self.send_list_keyboard(from_id, text_thank_you, [text_button_main])
                self.close()
            else:
                bot.sendMessage(from_id, text_new_info)
                self.store.new_item['to_change_attribute'] = query_data
                self.indicator = 'new_info'

        elif self.indicator == 'check_another':
            if query_data == 'yes':
                self.indicator = 'choose_my_item'
            else:
                self.send_list_keyboard(from_id, text_thank_you, [text_button_main])
                self.close()

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        # To allow the user cancel the action at any time and return to the main menu
        if ('text' in msg) and (msg['text'] == text_button_cancel):
            bot.sendMessage(chat_id, text_cancel)
            self.send_list_keyboard(chat_id, text_welcome_message, function_list)
            self.indicator = 'choose_function'

        if ('text' in msg) and (msg['text'] == '/help'):
            bot.sendMessage(chat_id, text_helping_message)
            self.close()

        if ('text' in msg) and (msg['text'] == '/sell'):
            self.send_custom_keyboard(chat_id, text_welcome_seller, text_button_cancel)
            search_result = self.search_data('shop_info.json', 'chat_id', chat_id)
            if not search_result:
                bot.sendMessage(chat_id, text_name_shop, parse_mode='MarkDown')
                self.store.add_shop('chat_id', chat_id)
                self.indicator = 'add_shop_name'
            else:
                bot.sendMessage(chat_id, text_own_shop + search_result[0]['shop_name'])
                self.send_custom_inline_keyboard(chat_id, text_choose_type1, primary_sale_list)
                self.indicator = 'choose_item_type'

        if ('text' in msg) and (msg['text'] == '/buy'):
            self.send_custom_keyboard(chat_id, text_welcome_buyer, text_button_cancel)
            self.send_custom_inline_keyboard(chat_id, text_choose_search_type, search_list)
            self.indicator = 'how_to_search'

        if ('text' in msg) and (msg['text'] == '/credit'):
            bot.sendMessage(chat_id, text_credit)
            bot.sendAudio(chat_id, gif_credit)
            self.close()



        if self.indicator == 'choose_function':
            self.store.new_item['chat_id'] = msg['chat']['id']

            # --------------- SELL ---------------
            if ('text' in msg) and (msg['text'] == text_button_sell):
                self.send_custom_keyboard(chat_id, text_welcome_seller, text_button_cancel)
                with open('shop_info.json', 'r') as handle:
                    contact_data = [json.loads(line) for line in handle]
                    result_list = []
                    for data in contact_data:
                        if data['contact']['contact']['user_id'] == chat_id:
                            result_list.append(data)
                    handle.close()
                    if not result_list:
                        # If chat id is not found in the shop_info file, the user is a new seller
                        # So Aladdin should ask the user to name the shop and store the shop data
                        bot.sendMessage(chat_id, text_name_shop, parse_mode='MarkDown')
                        self.store.add_shop('chat_id', chat_id)
                        self.indicator = 'add_shop_name'
                    # If chat id is found in the shop_info file, the user is not new seller
                    # So Aladdin should give the user the shop name and proceed
                    else:
                        self.send_custom_inline_keyboard(chat_id, text_choose_type1, primary_sale_list)
                        self.indicator = 'choose_item_type'
                    handle.close()

            # --------------- BUY ---------------
            elif ('text' in msg) and (msg['text'] == text_button_buy):
                self.send_custom_keyboard(chat_id, text_welcome_buyer, text_button_cancel)
                self.send_custom_inline_keyboard(chat_id, text_choose_search_type, search_list)
                self.indicator = 'how_to_search'

            # --------------- CHANGE ---------------
            elif ('text' in msg) and (msg['text'] == text_button_modify_items):
                self.send_custom_keyboard(chat_id, text_searching, text_button_cancel)
                search_result = self.search_data('item.json', 'chat_id', chat_id)
                # if the user does not have anything on sale
                if not search_result:
                    bot.sendMessage(chat_id, text_nothing_on_sale)
                    self.send_list_keyboard(chat_id, text_thank_you, [text_button_main])
                    self.close()

                # if the user's shop is not empty
                else:
                    bot.sendMessage(chat_id, text_all)
                    self.we_have_found(search_result, chat_id)
                    self.indicator = 'choose_item_modify'

            # --------------- CHECK ---------------
            elif ('text' in msg) and (msg['text'] == text_button_my_shop):
                self.send_custom_keyboard(chat_id, text_my, text_button_cancel)
                search_result = self.search_data('item.json', 'chat_id', chat_id)
                self.we_have_found(search_result, chat_id)
                self.indicator = 'choose_my_item'

        # --------------- SELL ---------------
        elif self.indicator == 'add_shop_name':
            try:
                self.store.add_shop('shop_name', msg['text'])
                bot.sendMessage(chat_id, text_get_contact_info, parse_mode='MarkDown', reply_markup=ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text='Yes', request_contact = True)]], one_time_keyboard = True))
                self.indicator = 'add_contact'
            except KeyError:
                bot.sendMessage(chat_id, text_type_shop_name)

        elif self.indicator == 'add_contact':
            self.store.shop_info['contact'] = msg
            try:
                with open('shop_info.json', 'a') as handle:
                    json.dump(self.store.shop_info, handle)
                    handle.write("\n")
                self.send_custom_inline_keyboard(chat_id, text_choose_type1, primary_sale_list)
                self.indicator = 'choose_item_type'
            except KeyError:
                bot.sendMessage(chat_id, text_type_contact_info)

        elif self.indicator == 'input_price':
            try:
                price_int = int(msg['text'])
                self.add_attribute_info('price', price_int, text_input_description,
                                        "input_description")
            except ValueError:
                bot.sendMessage(chat_id, text_only_number)
            except KeyError:
                bot.sendMessage(chat_id, text_only_number)

        elif self.indicator == "input_description":
            try:
                self.store.add_attribute('description', msg['text'])
                self.send_custom_inline_keyboard(chat_id, text_add_photo, yes_or_no)
                self.indicator = 'choose_input_image'
            except KeyError:
                bot.sendMessage(chat_id, text_type_description)

        elif self.indicator == 'input_image':
            try:
                self.store.add_attribute('photo_id', msg['photo'][0]['file_id'])
                self.send_list_keyboard(chat_id, text_successfully_add,
                                        [text_button_main])
            except KeyError:
                bot.sendMessage(chat_id, text_send_photo)

            # read from database
            with open('item.json', 'r') as handle:
                user_sale_data = [json.loads(line) for line in handle]
                individual_sale_data = []

                for data in user_sale_data:
                    if data['chat_id'] == chat_id:
                        individual_sale_data.append(data)

                if not individual_sale_data:
                    self.store.new_item['item_id'] = chat_id * 1000 + 1
                else:
                    self.store.new_item['item_id'] = chat_id * 1000 + len(individual_sale_data) + 1
                handle.close()

            # write to database
            with open('item.json', 'a') as handle:
                json.dump(self.store.new_item, handle)
                handle.write("\n")
            handle.close()
            self.close()

        # --------------- BUY ---------------
        elif self.indicator == 'choose_item_type':
            bot.sendMessage(chat_id, text_search_type1)

        elif self.indicator == 'choose_item_type_2':
            bot.sendMessage(chat_id, text_search_type2)

        elif self.indicator == 'how_to_search':
            bot.sendMessage(chat_id, text_choose_search_type)

        elif self.indicator == 'type_search':
            bot.sendMessage(chat_id, text_search_type1)

        elif self.indicator == 'find':
            bot.sendMessage(chat_id, text_search_type2)

        elif self.indicator == 'keyword_search':
            try:
                search_result = self.search_keyword('description', msg['text'])
                self.we_have_found(search_result, chat_id)
                bot.sendMessage(chat_id, text_choose_item, parse_mode='MarkDown')
                self.indicator = 'choose_item'
            except KeyError:
                bot.sendMessage(chat_id, text_type_keyword)

        elif self.indicator == 'shop_name_search':
            try:
                shop_result = self.search_data('shop_info.json', 'shop_name', msg['text'])
                search_result = self.search_data('item.json', 'chat_id', shop_result[0]['chat_id'])
                self.we_have_found(search_result, chat_id)
                bot.sendMessage(chat_id, text_choose_item, parse_mode='MarkDown')
                self.indicator = 'choose_item'
            except IndexError:
                self.send_list_keyboard(chat_id, text_sorry_shop, [text_button_main])
                self.close()
            except KeyError:
                bot.sendMessage(chat_id, text_type_shop_name)

        elif self.indicator == 'give_internet_search_result':
            if 'text' in msg:
                reply_amazon = search_info(msg)
                reply_taobao = search_taobao(msg)
                bot.sendMessage(chat_id, reply_amazon, parse_mode='Markdown')
                bot.sendMessage(chat_id, reply_taobao)
                self.send_list_keyboard(chat_id, text_thank_you, [text_button_main])
                self.close()
            else:
                bot.sendMessage(chat_id, text_type_keyword)

        elif self.indicator == 'choose_item':
            try:
                id_int = int(msg['text'][1:])
                self.store.add_shop('temp_item', id_int)
                try:
                    item_info = self.search_data('item.json', 'item_id', id_int)
                    self.display_info(item_info[0], chat_id, ['item_id', 'item_type_2', 'description', 'price'])
                    if not item_info[0]['photo_id']:
                        pass
                    else:
                        bot.sendMessage(chat_id, text_display_photo)
                        bot.sendPhoto(chat_id, item_info[0]['photo_id'])
                    self.send_custom_inline_keyboard(chat_id, text_want_contact, yes_or_no)
                    self.indicator = 'want_contact_or_not'
                except IndexError:
                    bot.sendMessage(chat_id, text_choose_from_list)

            except ValueError:
                bot.sendMessage(chat_id, text_choose_from_list)
            except KeyError:
                bot.sendMessage(chat_id, text_choose_from_list)

        # --------------- CHECK ---------------
        elif self.indicator == 'choose_my_item':
            try:
                id_int = int(msg['text'][1:])
                item_info = self.search_data('item.json', 'item_id', id_int)
                self.display_info(item_info[0], chat_id, ['item_id', 'item_type_2', 'description', 'price'])
                self.indicator = 'check_another'
                self.send_custom_inline_keyboard(chat_id, text_check_another, yes_or_no)

            except ValueError:
                bot.sendMessage(chat_id, text_choose_from_list)

            except KeyError:
                bot.sendMessage(chat_id, text_choose_from_list)

        # --------------- CHANGE ---------------
        elif self.indicator == 'choose_item_modify':
            try:
                self.store.new_item['item_id'] = msg['text'][1:]
                self.send_custom_inline_keyboard(chat_id, text_modify_method, attribute_list)
                self.indicator = 'change_attribute'
            except KeyError:
                bot.sendMessage(chat_id, text_choose_from_list)

        elif self.indicator == 'change_attribute':
            bot.sendMessage(chat_id, text_new_info)

        elif self.indicator == 'new_info':
            # extract data from the original file
            with open('item.json', 'r') as handle:
                user_sale_data = [json.loads(line) for line in handle]
                # remove the info of the item to be modified from database
                for data in user_sale_data:
                    if str(data['item_id']) == str(self.store.new_item['item_id']):
                        user_sale_data.remove(data)
                        self.store.new_item['original_data'] = data
                handle.close()

            # write the modified data to the file
            with open('item.json', 'w') as handle:
                for data in user_sale_data:
                    json.dump(data, handle)
                    handle.write("\n")
                handle.close()

            # modify the item info and append to the file
            try:
                if self.store.new_item['to_change_attribute'] != 'price':
                    self.store.new_item['original_data'][self.store.new_item['to_change_attribute']] = msg['text']
                elif self.store.new_item['to_change_attribute'] == 'price':
                    try:
                        price_int = int(msg['text'])
                        self.store.new_item['original_data'][self.store.new_item['to_change_attribute']] = price_int
                    except ValueError:
                        bot.sendMessage(chat_id, text_only_number)
                        self.send_list_keyboard(chat_id, text_thank_you, [''])
                        self.close()

                with open('item.json', 'a') as handle:
                    json.dump(self.store.new_item['original_data'], handle)
                    handle.write("\n")
                    handle.close()
                bot.sendMessage(chat_id, text_successfully_change)
            except KeyError:
                bot.sendMessage(chat_id, text_choose_from_list)
            self.close()

TOKEN = '*****************'


bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Aladdin, timeout=3600000),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(200)
