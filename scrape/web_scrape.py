import mechanicalsoup

browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'lxml'},
    raise_on_404=True,
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74'
)

url = "https://us.nicebooks.com"
search_page = browser.get(url)
search_html = search_page.soup

form = search_html.select("form")[0]
form.select("input")[0]["value"] = "zeus"

result_page = browser.submit(form, search_page.url)

print(result_page.soup)

pass
