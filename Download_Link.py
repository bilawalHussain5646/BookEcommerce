from bs4 import BeautifulSoup
import requests

def FetchDownloadLink(link):

  
    
    id_starting = link.rfind('-') + 2
    id = link[id_starting:-5]
    print(id)
    # Finding Id of the book

    URL = "https://www.pdfdrive.com"+link
    # print("This is URL: ",URL)
    result = requests.get(URL)
    soup = BeautifulSoup(result.content,'html.parser')
    
    res = soup.find_all('script')[6].string
    # print(res)

    # Find the script
 
    position_session = res.find('session:')
    # Find position of session

    res= res.strip()[position_session:]
    # print(res)
    # print("Total Length: ",totalLength)
    totalLength = len(res)
    # New Updated string starting from session

    # Remove from end now where ,r:"

    # print(res.find(',r:\''))
    position_session_ending= res.find(',r:\'')
    totalLength = position_session_ending-totalLength
    # print(res)
    # Find position of the end


    session_id= res.strip()[:totalLength]
    # Enter Last Location in the strip
    
    session_id = session_id[9:-1]
    #This is session id

    # This is id of book 

    Url_For_PdfDrive = "https://www.pdfdrive.com/ebook/broken?id="+id + "&session="+session_id
    # print(session_id)
    # print(Url_For_PdfDrive)
    result = requests.get(Url_For_PdfDrive)
    soup = BeautifulSoup(result.content,'html.parser')
    
    downloadLink =  soup.find("a")
    downloadLink = downloadLink['href']
    if downloadLink[0] == "/":
        downloadLink = "https://www.pdfdrive.com" + downloadLink
    # print(downloadLink)   
    return downloadLink  

# FetchDownloadLink('/i-am-malala-full-text-d34776467.html')
