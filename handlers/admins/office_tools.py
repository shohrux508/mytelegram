from urllib.parse import parse_qs

import requests as rr

from data.database import host


class myNotes():
    def get(self, pk):
        response = rr.get(url=f'{host}/myserver/notes/{pk}')
        if response.status_code != 200:
            return False, response.json(), response.status_code
        text = (f'Заметка номер: {response.json()["title"]}\n\n'
                f'{response.json()["text"]}')
        return True, text, response.json()

    def list(self, page=1):
        response = rr.get(url=f'{host}/myserver/notes/?page={page}')
        if response.status_code != 200:
            return None, response.json()
        return response.json()

    def create(self, title, text):
        response = rr.post(url=f'{host}/myserver/notes/new/', data={'title': title, 'text': text})
        return response.json(), response.status_code

    def update(self, pk, title=None, text=None):
        response = rr.get(url=f'{host}/myserver/notes/{pk}')
        if response.status_code != 200:
            return False, response.json(), response.status_code
        note_data = response.json()['results']
        if title:
            note_data['title'] = title
        if text:
            note_data['text'] = text
        response2 = rr.put(url=f'{host}/myserver/notes/{pk}', data=note_data)
        if response2.status_code == 200:
            return True, response.json()
        return False, response.json(), response.status_code

    def delete(self, pk):
        response = rr.delete(url=f'{host}/myserver/notes/{pk}')
        return response


class myPlans():

    def get(self, pk):
        response = rr.get(url=f'{host}/myserver/plans/{pk}')
        return response

    def list(self, page=None):
        # page = 'page=1&status=False'
        if page:
            if '&' in page:
                url = f'{host}/myserver/plans/filter/?{page}'
            else:
                url = f'{host}/myserver/plans/?{page}'
        else:
            url = f'{host}/myserver/plans/?page=1'
        response = rr.get(url=url)
        if response.status_code == 200:
            return True, response.json()
        return False, response.json()

    def create(self, title, text, type=None, deadline=None):
        response = rr.get(url=f'{host}/myserver/plans/new/',
                          data={'title': title, 'text': text, 'type': type, 'deadline': deadline})
        return response

    def update(self, pk, title=None, text=None, type=None, deadline=None, status=None):
        response = rr.get(url=f'{host}/myserver/plans/{pk}')
        if response.status_code == 200:
            data = response.json()['results']
            data.update({k: v for k, v in
                         {'title': title, 'text': text, 'type': type, 'deadline': deadline, 'status': status}.items() if
                         v})
            response2 = rr.put(url=f'{host}/myserver/plans/{pk}', data=data)

            return response2
        else:
            return None

    def delete(self, pk):
        response = rr.delete(url=f'{host}/myserver/plans/{pk}')
        return response.json()

    def put(self, pk, type=None, text=None, status=None):
        response = rr.get(url=f'{host}/myserver/plans/{pk}')
        if response.status_code == 200:
            data = response.json()
            if type:
                data['type'] = type
            if text:
                data['text'] = text
            if status:
                data['status'] = status
            response2 = rr.put(url=f'{host}/myserver/plans/{pk}/', data=data)
            return response2
        return None

    def types_list(self):
        response = rr.get(url=f'{host}/myserver/plans/types/').json()['types']
        return response


def jsonNote_to_message(json):
    textList = []
    for i in json:
        text = (f'Заметка номер: {i["title"]}\n'
                f'{i["text"]}\n------')
        textList.append(text)
    message = '\n'.join(textList)
    return message


def filterPlansJson(page):
    status, response = myPlans().list(page=page)
    if 'type' in page:
        text = 'Сортировка по типу планов'
    elif 'status' in page:
        text = 'Сортировка по статусу планов'
    else:
        text = 'Ваши планы'
    if status:
        return response['results'], text, status
    return response, text, status


def switchPage_datas(current_page, next=None, previous=None):
    query_params = parse_qs(current_page)
    current_page_int = int(query_params.get('page', [1])[0])
    next_page_int = current_page_int + 1
    pre_page_int = current_page_int - 1
    nextPage = current_page.replace(f'{str(current_page_int)}', f'{str(next_page_int)}')
    previousPage = current_page.replace(f'{str(current_page_int)}', f'{str(pre_page_int)}')
    if next:
        return nextPage
    elif previous:
        return previousPage
    return current_page



def getPlanText(pk):
    response = myPlans().get(pk=pk)
    if response.status_code != 200:
        return None
    data = response.json()
    title = data['title']
    text = data['text']
    type = data['type']
    status = data['status']
    deadline = data['deadline']
    if status:
        statusAsText = 'Выполнено'
    else:
        statusAsText = 'Не выполнено'
    message = (f'{title}.\n\n'
               f'{text}\n\n'
               f'Статус: {statusAsText}\n')
    return message, status


