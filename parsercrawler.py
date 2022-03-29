import bs4
from bs4 import BeautifulSoup


class JobsoffersParser:
    def __init__(self):
        self.soup = None

    @property
    def remote_tag(self):
        salary_tag = self.soup.find('p', attrs={'class': 'chakra-text css-0'})

        if salary_tag:
            return salary_tag.text.replace('\u200c', ' ')


    @property
    def company_name(self):
        remote_tag = self.soup.find('a', attrs={"class": "chakra-link css-f4h6uy"})
        if remote_tag:
            return remote_tag.text

    @property
    def location_tag(self):
        loc_tage = self.soup.find('div', attrs={'class': "chakra-stack css-84zodg"})
        if loc_tage:
            return loc_tage.text

    @property
    def skil_tage(self):
        skiltage = self.soup.find('div', attrs={'title': "تکنولوژی اصلی"})
        if skiltage:
            return skiltage.text

    def parser(self, html_doc):
        self.soup = BeautifulSoup(html_doc, 'html.parser')
        data = dict(
            is_fulltime=self.remote_tag, company=self.company_name,
            Location=self.location_tag, Essential_skill=self.skil_tage
        )


        return data


