import bs4
import requests

# This function is to grab information from the Internet and return the formatted search result
def search_info(msg):
    item_name = str(msg['text'])
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'}
    url = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords='+item_name
    response = requests.get(url, headers=headers)    
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    # Use a loop  in case BS4 cannot grab the information correctly
    # And set a coefficient to prevent 'death loop'
    count = 5
    while count >= 0:
        if not soup.find_all('h2', class_="a-size-medium s-inline s-access-title a-text-normal")  :
            response = requests.get(url, headers=headers)    
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            count =count - 1
            continue
        else:        
            # the first three items' names
                name1 = soup.find_all('h2', class_="a-size-medium s-inline s-access-title a-text-normal")[0].string
                name2 = soup.find_all('h2', class_="a-size-medium s-inline s-access-title a-text-normal")[1].string
                name3 = soup.find_all('h2', class_="a-size-medium s-inline s-access-title a-text-normal")[2].string

            # the first three items' price
                price1 = '*$' + soup.find_all('span', class_='sx-price-whole', limit=3)[0].string + '.' + \
                     soup.find_all('span', class_='sx-price-whole', limit=3)[0].next_sibling.next_sibling.string+'*'
                price2 = '*$' + soup.find_all('span', class_='sx-price-whole', limit=3)[1].string + '.' + \
                     soup.find_all('span', class_='sx-price-whole', limit=3)[1].next_sibling.next_sibling.string+'*'
                price3 = '*$' + soup.find_all('span', class_='sx-price-whole', limit=3)[2].string + '.' + \
                     soup.find_all('span', class_='sx-price-whole', limit=3)[2].next_sibling.next_sibling.string+'*'

            # To send the result to users
                return('The first three results of ' + item_name + ' in amazon are listed below: ''\n\n' + name1 + '  ' + price1 + '\n\n' + name2 + '  ' + price2 + '\n\n' + name3 + '  ' + price3
                                 + "\n\n*Here you go the links* \U000026C4: \n" +
                                 soup.find_all('span', class_='sx-price-whole', limit=3)[0].find_all_previous("a",
                                                                                                              class_="a-link-normal a-text-normal")[
                                     0]['href']
                                 + '\n\n' +
                                 soup.find_all('span', class_='sx-price-whole', limit=3)[1].find_all_previous("a",
                                                                                                              class_="a-link-normal a-text-normal")[
                                     0]['href']
                                 + '\n\n' +
                                 soup.find_all('span', class_='sx-price-whole', limit=3)[2].find_all_previous("a",
                                                                                                              class_="a-link-normal a-text-normal")[
                                     0]['href']
                                +" \n\n You need to add 'https://www.amazon.com' in front of the link if it does not generate automatically \n"
                                +"\U0001F648 Sorry for the inconvenience \U0001F648 "                                                  
                            )
                break
                
        
    else :
        return("\U0001F614 Sorry , the Amazon server is too *busy*,"+
               " maybe you can try to search another item name .")

