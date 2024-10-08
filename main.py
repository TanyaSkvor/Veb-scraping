import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers

# Входные данные
url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
keywords = ['Django', 'Flask']

def get_fake_headers():
    return Headers(browser='chrome', os='win').generate()

# Запрос
response = requests.get(url, headers=get_fake_headers())

# Обработка запроса
results = []
if response.status_code == 200:
    soup = BeautifulSoup(response.text, features='lxml')
    vacancies = soup.find_all(class_ = "vacancy-info--umZA61PpMY07JVJtomBA")
    for vacancy in vacancies:
        link = vacancy.find('a', class_ = 'magritte-link___b4rEM_4-3-2 magritte-link_style_neutral___iqoW0_4-3-2 magritte-link_enable-visited___Biyib_4-3-2')['href']
        company = vacancy.find('span',{'data-qa':'vacancy-serp__vacancy-employer-text'}).text
        city = vacancy.find('span',{'data-qa':'vacancy-serp__vacancy-address'}).text
        salary = vacancy.find('span', class_ ='magritte-text___pbpft_3-0-15 magritte-text_style-primary___AQ7MW_3-0-15 magritte-text_typography-label-1-regular___pi3R-_3-0-15')
        if salary:
            salary = salary.text.strip()
        else:
            salary = 'Заработная плата не указана'
        response_link = requests.get(link, headers=get_fake_headers())
        soup_link = BeautifulSoup(response_link.text, features='lxml')
        description = soup_link.find('div', class_ = 'vacancy-branded-user-content')
        if description:
            description = description.text
        else:
            description = 'Нет описания'
        if all(keyword.lower() in description.lower() for keyword in keywords):
            vacancy_info = {
                'link': link,
                'company': company,
                'city': city,
                'salary': salary
            }
            results.append(vacancy_info)

    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

    print('Код выполненю Результаты поиска сохранены в файле vacancies.json.')
else:
    print('Ошибка при выполнении запроса. Попробуйте снова.')