< - Description of the Funtions for Bot Project Aladdin --- Created by Goup Teletubbies - > 

#Part 1 Python files

1> Bot.py
     The file contains all the main functions for the bot. The functions can be classified as following:
     **For sellers:
        -By clicking on the button 'Sell item', the seller'll start the procedure of adding an item to sell. 
         
         If the seller's personal information hasn'e been identifies, he/she'll be asked to create a shop by giving a name to the shop and leaving personal contact info.
        
        -Then the seller with follow a procedure of choosing the type, adding the price and inputting the description for the item.

        -Additionally the seller can send a photo of the item. Finally the item will be recored and givinga unique item ID and put on sale.

        -The seller can change the information of any item or remove it from sale by clicking on the button 'Modify items' and check the items that one sell by clicking on the button 'My shop'
    **For buyers:
        --Four kinds of searching methods are provided to the buyer. They are: 

         * --By Item type
         * --By Keyword
         * --By Shop name
         * --Online resources

        - After searching the customer can check out for more information by clicking on the item ID shown
 
        - Customer can choose whether to get the contact info of the seller. If so, the seller will receive a messages informing his item is checked.

2> list_data.py
     The file contains the data for:
     
     1. Specifying the type of an item by choosing the type of the item;

     2. Search methods;

     3. Attributes of an item; 
 
     4. Funtions buttons;

     The lists in this file are passed to the Bot.py as a parameter in a built-in function called *send_list_keyboard* to send custom keyboards or inline keyboards to the user.

3> SearchXXXX.py

4> Text.py
     This file contains the data of:
    
     1. Conversations Aladdin will have with users;

     2. Emojis that are involved;

     3. GIFs that are involved;
     
     If we want to modify text/GIFs/emojis that Aladdin sends to the customer, we can directly modify the corresponding variables in this file without searching the text/GIFs/emojsi in Bot.py



# Part2 JSON files --> JSON files are files containing multiple dictionaries. We use JSON files as our database

1> item.json
    
    Contains the data for all the items on sale, each item has the following attributes:
   
    1. Primary item type
    2. Secondary item type
    3. Item ID
    4. Price
    5. Photo ID  (optional)
    6. Chat ID (of the seller)
    7. Desprition of the item

2> shop_info.json
    
    Contains the data for all the existing shops, each shop has the following attributes:
   
    1. Shop name
    2. Chat ID
    3. Contact info

3>user_info.json

    Contains the data for all the existing shops, each shop has the following attributes:
   
    1. Username
    2. Chat ID
    3. User's first name (Optional)
    4. User's last name (Optional)
