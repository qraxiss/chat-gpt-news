import flet as ft
from threading import Thread
from controller.api import OpenAI
from json import loads

img_path = "/Users/qraxiss/Documents/GitHub/node/frontend/img"

print("a"*0)

def thread(func):
    def inner(*args, **kwargs):
        obj = Thread(target=func,args=args,kwargs=kwargs)
        obj.start()
        return obj
    return inner

class Page:
    components = {
        'gptlogo': ft.Image(f'{img_path}/logo.png',
                            width=65,
                            height=65,
                            fit=ft.ImageFit.CONTAIN),
        'textfield': None,
        'newsbutton': None,
        'datatable': ft.DataTable(columns=[ft.DataColumn(ft.Text(col)) for col in ["Haber", "Yorum", "Etki"]]
                                  ,expand=True)
    }

    def __init__(self):
        self.openai = OpenAI()

    def __call__(self, page: ft.Page):
        self.page: ft.Page = page
        self.page_config()

    def page_config(self):
        self.page.title = "chatgpt based news evaluator"
        self.page.vertical_alignment = ft.alignment.center
        self.page.scroll = "always"
        self.page.add(*self.template())
        self.page.update()


    def news(self, e):
        res = loads((self.openai.opinion(self.textfield.value))["content"])
        ai_msg = res["ai_opinion"].replace('\n', '')
        news = self.textfield.value

        if res['yon'].lower() == 'pozitif':
            puan, color = "🟩" * res['puan'], "#50C878" 
        elif res['yon'].lower() == 'negatif':
            puan, color = "🟥" * res['puan'], "#EE4B2B"
        else:
            puan, color = "⬜️" * res['puan'], None

        self.components['datatable'].rows.insert(0,
            ft.DataRow(cells=[
                ft.DataCell(ft.TextButton(news[:25]+'...', on_click=lambda e, msg = news: self.snack(msg))),
                ft.DataCell(ft.TextButton(ai_msg[:25]+'...', on_click=lambda e, msg = ai_msg: self.snack(msg))),
                ft.DataCell(ft.Text(puan, color=color))
            ])
        )
        self.textfield.value = ""
        self.page.update()

    @property
    def newsbutton(self):
        component = self.components['newsbutton']
        if component is not None:
            return component

        self.components['newsbutton'] = ft.IconButton(
            ft.icons.NEWSPAPER, on_click=self.news)

        return self.newsbutton

    @property
    def textfield(self):
        component = self.components['textfield']
        if component is not None:
            return component

        self.components['textfield'] = ft.TextField(
            multiline=True,
            min_lines=8,
            prefix_text="Haber:  ",
            text_size=13
        )

        return self.textfield

    def template(self):
        return [
            ft.Row([
                self.components['gptlogo'],
            ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row([
                self.newsbutton,
            ],
                alignment=ft.MainAxisAlignment.CENTER
            ),


            ft.ResponsiveRow([
                self.textfield
            ],
            ),

            ft.Row([self.components['datatable']], alignment=ft.MainAxisAlignment.CENTER,)
        ]

    def snack(self,msg):
        self.page.snack_bar = ft.SnackBar(ft.Text(msg), action="Ok")
        self.page.snack_bar.open = True
        self.page.update()

ft.app(Page())