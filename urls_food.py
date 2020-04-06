from bs4 import BeautifulSoup
from selenium import webdriver

urlList = []
driver = webdriver.Firefox()

for i in range(1, 100):
    print(i)
    url = "https://www.food.com/recipe?pn=" + str(i)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html')
    htmlUrls = soup.find_all('h2', {'class': "title"})
    for html in htmlUrls:
        url = html.find('a')['href']
        if '/recipe/' in url:
            urlList.append(url)

# save text list
with open("urlList.txt", 'a') as out:
    for url in urlList:
        out.write(url + '\n')
