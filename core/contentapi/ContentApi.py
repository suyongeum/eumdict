import requests
from django.conf import settings

class ContentApi:

    def get_number_of_lines(self, content_id):
        url = settings.GET_CONTENT_INFO
        # which = 1 - number of sentences within the content
        # which = 2 - whole sentences within the content
        data = {"content_id": content_id, "which": 1}
        r = requests.post(url, params=data)
        r.connection.close()
        lines_amount = int(r.text)
        return lines_amount

    def get_content_script(self, content_id):
        url = settings.GET_CONTENT_INFO
        # which = 1 - number of sentences within the content
        # which = 2 - whole sentences within the content
        data = {"content_id": content_id, "which": 2}
        r = requests.post(url, params=data)
        r.connection.close()
        lines = r.text.split('\n')
        return lines

    def get_line(self, content_id, line_id):
        url = settings.GET_LINE_INFO
        # which = 1 - sentence:difficulty
        # which = 2 - sentence
        # which = 3 - difficulty
        # which = 4 - lemm_sentence
        data = {"content_id": content_id, "line_id": line_id, "which": 2}
        r = requests.post(url, params=data)
        r.connection.close()
        return r.text

    def get_lemm_line(self, content_id, line_id):
        url = settings.GET_LINE_INFO
        # which = 1 - sentence:difficulty
        # which = 2 - sentence
        # which = 3 - difficulty
        # which = 4 - lemm_sentence
        data = {"content_id": content_id, "line_id": line_id, "which": 4}
        r = requests.post(url, params=data)
        r.connection.close()
        return r.text

    def get_amount_of_words_in_line(self, content_id, line_id):
        line = self.get_line(content_id, line_id)
        words = line.split(' ')
        return len(words)

    def get_line_difficulty(self, content_id, line_id):
        url = settings.GET_LINE_INFO
        # which = 1 - sentence:difficulty
        # which = 2 - sentence
        # which = 3 - difficulty
        # which = 4 - lemm_sentence
        data = {"content_id": content_id, "line_id": line_id, "which": 3}
        r = requests.post(url, params=data)
        r.connection.close()
        difficulty = float(r.text)
        return difficulty

    def verify_line(self, content_id, line_id, input):
        url = settings.GET_VERIFY
        data = {"content_id": content_id, "line_id": line_id, "input": input}
        r = requests.post(url, params=data)
        r.connection.close()
        return r.text
