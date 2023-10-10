from bs4 import BeautifulSoup

with open('data/sec-edgar-filings/AAPL/10-K/0000320193-22-000108/full-submission.txt', 'r', encoding='utf-8') as file:
    content = file.read()

soup = BeautifulSoup(content, 'html.parser')
cleaned_text = soup.get_text()


with open('cleaned_file.txt', 'w', encoding='utf-8') as file:
    file.write(cleaned_text)

print(cleaned_text)