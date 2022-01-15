from bs4 import BeautifulSoup
import requests

from multiprocessing.dummy import Pool as ThreadPool

data : list = []
search_ = ""

def Search(search_keyword):
    global search_
    search_ = search_keyword
    global data 
    data = []
    # Make the Pool of workers
    pool = ThreadPool(3)

    pool.map(searchResults, [1,2,3])


    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()

    # print(data)
    return data
  



def searchResults(i):
    global search_
    global data
    URL = "https://www.pdfdrive.com/search?q="+search_+"&pagecount=&pubyear=&searchin=&page="+str(i)
    result = requests.get(URL)
    soup = BeautifulSoup(result.content,'html.parser')
    result = soup.find_all("div", {"class":"file-left"})
    pool = ThreadPool(4)

    pool.map(booksInfo, result)


    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()
    

def booksInfo(result):
        global data
        Links = result.find('a', href=True)
        title = result.find('img',title=True)
        ImageUrl = result.find('img',src=True)
        # print(ImageUrl['src'])
        URL = ImageUrl['src']
        page = requests.get(URL)
        id = "id"+Links['href']
        

        if title and page.url != "https://cdn.asaha.com/assets/img/nocover.jpg":
                temp = {"id": id, "link": Links['href'],"imageURL": 
                page.url, "title":
                title['title']}
                data.append(temp)