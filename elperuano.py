from source import RawSource, SourceDescription
from bs4 import BeautifulSoup
import requests
from os import path
from datetime import datetime as dt
import locale


class Source(RawSource):
    def __init__(self):
        super().__init__()
        self.base_url = "https://elperuano.pe/busqueda.aspx"
        self.state_params = {
            "__EVENTTARGET": "",
            "__VIEWSTATE": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATEGENERATOR": "",
            "__EVENTVALIDATION": "",
            "ctl00$ucCabecera1$search": "",
            "ctl00$ContentPlaceHolder1$txtBusqueda": "",
            "ctl00$ContentPlaceHolder1$ddlSecciones": ""
        }
        self.raw_dataset: list = []

    def describe(self):
        return SourceDescription(name="el peruano", version='0.0.1')

    @staticmethod
    def page(page: int = 0) -> str:
        p = "0{}".format(str(page)) if page < 10 else str(page)
        return "ctl00$ContentPlaceHolder1$rptPaginado$ctl{}$lnkbtnPaging".format(p)

    @staticmethod
    def trim(s: str) -> str:
        return s.replace("'", "").replace("\\", "")

    def load_info_person(self, person_name: str):
        self.state_params["ctl00$ContentPlaceHolder1$txtBusqueda"] = person_name
        self.state_params["ctl00$ContentPlaceHolder1$ddlSecciones"] = "1"

        url = "{}?claves={}".format(self.base_url, person_name.replace(" ", "+"))

        # first load to fetch state params
        res = requests.post(url)

        if res.status_code != 200:
            raise Exception("invalid index page response")

        soup = BeautifulSoup(res.content.decode('utf-8', 'ignore'), 'html.parser')

        v_state = soup.find(id="__VIEWSTATE")
        v_gen = soup.find(id="__VIEWSTATEGENERATOR")
        e_val = soup.find(id="__EVENTVALIDATION")

        self.state_params["__VIEWSTATE"] = v_state.get('value')
        self.state_params["__VIEWSTATEGENERATOR"] = v_gen.get('value')
        self.state_params["__EVENTVALIDATION"] = e_val.get('value')

        news: list = []

        last, diff, i = 0, 0, 0
        last_head, head = "", ""

        while diff == 0 or i < 2:
            self.state_params["__EVENTTARGET"] = self.page(i)
            print(self.page(i))
            res = requests.post(url, data=self.state_params)

            soup = BeautifulSoup(res.content.decode('utf-8'), "html.parser")

            ul = soup.find("ul", "buscador")
            lis = ul.find_all("li")

            if len(lis) is 0:
                break

            for j, li in enumerate(lis):
                title = li.find("b").find("a")

                if title is None:
                    raise Exception("holmes couldn't fetch the title of the 'el peruano' news")
                if j == 0:
                    head = title.get_text()
                    if i < 1:
                        last_head = head

                t = title.text

                ps = li.find_all("p")
                if len(ps) != 2:
                    raise Exception("holmes couldn't fetch the title of the 'el peruano' news")

                launch_time = ps[0]
                launch_time = launch_time.text

                p = ps[1]
                body = p.text

                a = li.find("a")
                a = a if a is not None else {"href": "/"}

                img = li.find("img")
                img = img if img is not None else {"src": ""}
                chunks = launch_time.split(",")
                time = chunks[1] if len(chunks) > 1 else ""
                time = time.strip()

                # time = dt.strptime(time, "%d de %B de %Y")
                news.append({
                    "title": t,
                    "time": time,
                    "body": body,
                    "link": path.join(self.base_url, self.trim(a['href'])),
                    "image": self.trim(img["src"])
                })

            if last_head == head and i > 1:
                break

            diff = last - len(lis)
            last = len(lis)
            i += 1

        self.raw_dataset = news
