from bs4 import BeautifulSoup
import requests, openpyxl
import re
import _thread


def find_all_range(start,end):
    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = 'tiêu đề'
    sheet.append(['cột 1','cột 2','cột 3','cột 4','published_time','modified_time'])
    try:
        link_base = 'https://amis.misa.vn'
        #duyệt toàn bộ chữ cái và thêm toàn bộ chỗ cái vào
        # for one in range(97,123):
        #     item = link_base + chr(one)
        #     list_link.append(item)
        #funtion tìm và duyệt link 
        
            #/66950/
        for one in range(start,end):
            item = link_base +'/'+ str(one) + '/'
            #duyệt vào các link và lấy data
            link = item
            #truy cập
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            
            source = requests.get(link,headers=headers)

            #kiểm tra url 
            # txt = "https://amis.misa.vn/wp-content/uploads/2019/05/AMIS_top_banner_09.png"
            x = re.search("/wp-content/", source.url)
            if x:
                print("Lỗi, bỏ qua")
            else:
                #kiểm tra trạng thái 
                source.raise_for_status()
                soup = BeautifulSoup(source.text, 'html.parser')
                # author = soup.find_all('meta', {'name': 'author'})[1]["content"]
                url_page = soup.find("meta",  {"property":"og:url"})["content"]
                #kiểm tra 404
                if url_page != "/404-page/":
                    author = soup.find_all('meta', {'itemprop': 'name'})[0]["content"]
                    title = soup.find('title').text
                    published_time = soup.find_all('meta', {'property': 'article:published_time'})[0]["content"]
                    modified_time = soup.find_all('meta', {'property': 'article:modified_time'})[0]["content"]
                    # print(url_page)
                    # print(author)
                    # print(title)
                    print('done:', link)
                    sheet.append(['cột 1',author,url_page,title,published_time,modified_time] )
                else:
                    print('404 nhé !', link)
    except Exception as e:
        print('lỗi ', e)
    excel.save('author_file.xlsx')

# find_all_range(1000,2000)
# Tao hai luong song song va thuc thi chung chạy 5 luồng
def tao_luong(luong):
    try:
        _thread.start_new_thread(find_all_range,(luong, luong + 1000))
        _thread.start_new_thread(find_all_range,(luong+ 1000, luong + 2000))
        _thread.start_new_thread(find_all_range,(luong+ 2000, luong + 3000))
        _thread.start_new_thread(find_all_range,(luong+ 3000, luong + 4000))
        _thread.start_new_thread(find_all_range,(luong+ 4000, luong + 5000))
    except:
        print ("Loi: Khong the bat dau luong moi")
    while 1:
        pass


tao_luong(1000)