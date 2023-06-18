import bestprice


coop_test = '35230257508426004599590005671911425513149074'
sr_test = '35221245495694001276590008047580969276482206'

access_key = coop_test

def scrap_data_test(cfe_key:str)-> str:
     with open('test_data.txt', 'r') as file:
        return file.read().rstrip()

header_data, item_data = scrap_data_test(access_key)

cfe_header_data = bestprice.get_cfe_header_data(header_data, access_key)
cfe_item_data = bestprice.get_cfe_item_data(item_data)

header_data_adjusted = bestprice.adjust_cfe_header_data(cfe_header_data)
item_data_adjusted = bestprice.adjust_cfe_item_data(cfe_item_data)

print(header_data_adjusted)
print(50*'-')
print(item_data_adjusted)