from requests import post


api = "http://localhost:3000/open-ai"

class OpenAI:
    def opinion(self,news:str):
        return post(api, json={'news': f'Haber : {news}'}).json()