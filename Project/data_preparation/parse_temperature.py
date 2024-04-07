from bs4 import BeautifulSoup


def parse_temperature():
    html = 'data/wiki_temperature.html'
    with open(html, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser', from_encoding='utf-8')
        table = soup.find('table')
        rows = table.find_all('tr')
        temperatures = {}
        for row in rows[1:]:
            columns = row.find_all('td')
            country = columns[0].text.strip()
            temperature = columns[1].text.split('\xa0')[0].strip()
            temperatures[country] = temperature
        return temperatures


if __name__ == '__main__':
    # print(parse_temperature())
    temperatures = parse_temperature()
    with open('data/mean_temperature.csv', 'w', encoding='utf-8') as f:
        f.write('Country,Mean temperature\n')
        for country, temperature in temperatures.items():
            f.write(f'{country},{temperature}\n')