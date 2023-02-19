from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from mylist import *
import sqlite3

with sqlite3.connect('db-11.db') as db:
    sql = db.cursor()


class MyRoot(BoxLayout):

    MY_DICT: dict = {'steel': '201', 'thicken': '0,5', 'diam': 'd150/220', 'item': None, 'num': '1', 'price': None}
    MY_SUM: list = []
    MY_STR: str = ''
    d_sndv: list = d_sndv
    d_gola: list = d_gola
    zkn_sndv: list = zkn_sndv
    zkn_gola: list = zkn_gola
    trnk_sndv: list = trnk_sndv
    trnk_gola: list = trnk_gola
    kln_sndv: list = kln_sndv
    kln_gola: list = kln_gola
    tube_sndv: list = tube_sndv
    tube_gola: list = tube_gola
    conf_g_s: dict = conf_g_s
    conf_s_g: dict = conf_s_g

    @staticmethod
    def make_list(keys) -> list:
        """Returns a list of values from the database to Spinner button inshSp and krplSp"""
        return [x[0] for x in sql.execute('SELECT name FROM button WHERE button == ? AND type == ?', keys).fetchall()]

    def spinner_values(self, instance):
        """Change values in Spinner button"""
        if instance.text == 'Сендвіч':
            self.ids.diamValSp.text = self.conf_g_s[self.MY_DICT['diam']]
            self.ids.diamValSp.values = self.d_sndv
            self.ids.trnkSp.values = self.trnk_sndv
            self.ids.tubeSp.values = self.tube_sndv
            self.ids.kolnSp.values = self.kln_sndv
            self.ids.zknSp.values = self.zkn_sndv
        if instance.text == 'Гола':
            self.ids.diamValSp.text = self.conf_s_g[self.MY_DICT['diam']]
            self.ids.diamValSp.values = self.d_gola
            self.ids.trnkSp.values = self.trnk_gola
            self.ids.tubeSp.values = self.tube_gola
            self.ids.kolnSp.values = self.kln_gola
            self.ids.zknSp.values = self.zkn_gola

    def calculate(self):
        """Finds the value in the database according to the query"""
        try:
            if self.MY_DICT['item'] in ('Кронштейн_500', 'Кронштейн_1000'):
                query: str = 'SELECT price FROM price_t WHERE category == ?'
                values: tuple = (self.MY_DICT['item'],)
                res: tuple = sql.execute(query, values).fetchone()
                self.MY_DICT['price']: int = res[0]
                output = f"{self.MY_DICT['item']}     {self.MY_DICT['num']}  *  {self.MY_DICT['price']}"
                self.ids.top_str_l.text = output
            elif self.MY_DICT['item'] in ('Лійка', 'Окапник', 'Скоба', 'Хомут_під_розт', 'Хомут_обж', 'Розв_платформа'):
                query: str = 'SELECT price FROM price_t WHERE diameter == ? AND category == ?'
                values: tuple = (self.MY_DICT['diam'], self.MY_DICT['item'])
                res: tuple = sql.execute(query, values).fetchone()
                self.MY_DICT['price']: int = res[0]
                output: str = f"{self.MY_DICT['item']} {self.MY_DICT['diam']}" \
                              f"     {self.MY_DICT['num']}  *  {self.MY_DICT['price']}"
                self.ids.top_str_l.text = output
            else:
                query: str = 'SELECT price FROM price_t WHERE steel == ? AND thickness == ? AND diameter == ?' \
                             ' AND category == ?'
                values: tuple = (self.MY_DICT['steel'], self.MY_DICT['thicken'],
                                 self.MY_DICT['diam'], self.MY_DICT['item'])
                res: tuple = sql.execute(query, values).fetchone()
                self.MY_DICT['price']: int = res[0]
                output: str = f"{self.MY_DICT['item']} {self.MY_DICT['diam']} {self.MY_DICT['thicken']}" \
                              f" {self.MY_DICT['steel']}    {self.MY_DICT['num']}  *  {self.MY_DICT['price']}"
                self.ids.top_str_l.text = output
        except:
            self.ids.top_str_l.text = f"{self.MY_DICT['item']} {self.MY_DICT['diam']} No result"

    def change_dict(self, instance):
        """Change query and try to find value in database"""
        self.MY_DICT[instance.name] = instance.text
        self.calculate()

    def ok(self):
        """Add string to result and sum values"""
        sum_row: int = int(self.MY_DICT['num'])*int(self.MY_DICT['price'])
        self.MY_SUM.append(sum_row)
        self.MY_STR: str = f"{self.MY_STR}\n{self.ids.top_str_l.text}  = {sum_row}"
        self.MY_DICT['num']: str = '1'
        self.ids.result_l.text: str = self.MY_STR
        self.ids.sum_l.text: str = f"SUM:___{sum(self.MY_SUM)}___"
        self.ids.top_str_l.text = self.ids.top_str_l.init_text

    def clear(self):
        """Clear result"""
        self.MY_STR = ''
        self.MY_SUM = []
        self.ids.top_str_l.text = self.ids.top_str_l.init_text
        self.ids.result_l.text = self.ids.result_l.init_text
        self.ids.sum_l.text = self.ids.sum_l.init_text


class MyApp(App, MyRoot):
    def build(self):
        return MyRoot()


if __name__ == "__main__":
    MyApp().run()
