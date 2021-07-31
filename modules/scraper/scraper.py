import requests
from bs4 import BeautifulSoup


class StudiumScraper:

    def __init__(self, text_list=[], url_list=[]):
        self.text_list = text_list
        self.url_list = url_list

    def __get_main_page(self) -> str:
        """get the redirect main page

        Returns:
            str: url of main page
        """
        page = requests.get('https://studium.unict.it/dokeos')
        soup = BeautifulSoup(page.content, 'html.parser')
        soup_meta = soup.find_all('meta', attrs={'http-equiv': 'REFRESH'})
        meta_content: str = soup_meta[0]['content']
        url = meta_content[meta_content.find('URL=') + 4:]
        return url

    @classmethod
    def get_years(cls):
        """get academic year list

        """
        page = requests.get(cls.__get_main_page(cls))
        soup = BeautifulSoup(page.content, 'html.parser')

        text_list = []
        url_list = []
        year_all_soup = soup.find_all('option')

        for year_soup in year_all_soup:
            # this check because on old years the bug has been fixed
            if year_soup['value'].find('/studium.unict.it') != -1 or year_soup['value'].startswith('/'):
                text_list.append(year_soup.get_text())
                url_list.append(year_soup['value'])

        return cls(text_list, url_list)

    @classmethod
    def get_cats(cls, url: str):
        """get categories (degree courses)

        Args:
            url (str): url to scrape categories

        """
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        catlist_soup = soup.find('div', attrs={'class': 'home_cats'})
        text_list = []
        url_list = []
        catlist_all_soup = catlist_soup.find_all('a')

        for cat_soup in catlist_all_soup:
            if cat_soup['href'].find('syllabus') != -1:
                continue

            text_list.append(cat_soup.get_text())
            url_list.append(cat_soup['href'])

        return cls(text_list, url_list)

    @classmethod
    def get_files_list(cls, url: str):
        """
        get list of files on current url

        Args:
            url (str): url of current folder

        """
        doc_path = 'document/' if url.find('/document') == - \
            1 and not url.startswith('/') else ''
        url = url + doc_path
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup_fs = soup.find_all('a')

        text_list = []
        url_list = []
        for fs_el in soup_fs:
            if fs_el['href'].startswith('?'):
                continue
            text_list.append(cls.get_safe_text(fs_el.get_text()))
            url_list.append(cls.get_safe_path(fs_el['href'], doc_path))
        return cls(text_list, url_list)

    @staticmethod
    def get_safe_path(path: str, doc_path: str) -> str:
        """get safe studium path for bot

        Args:
            path (str): current path scraped
            doc_path (str): parent folder

        Returns:
            str: safe path
        """
        courses_path_index = path.find('/courses/')
        document_path_index = path.find('/document/')

        if courses_path_index != -1 and document_path_index == -1:
            path = path[:courses_path_index]
            doc_path = ''

        return doc_path + path

    @staticmethod
    def get_safe_text(text: str) -> str:
        """get better text for button

        Args:
            text (str): current text to optimize

        Returns:
            str: optimized text
        """
        if text.endswith('/'):
            text = '📂 ' + text[:-1]
        return text
