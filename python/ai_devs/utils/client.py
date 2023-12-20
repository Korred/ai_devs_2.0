from typing import List, Union

import httpx


class AIDevsTask:
    def __init__(self, task_name: str, token: str, data: dict):
        self.task_name = task_name
        self.token = token
        self.data = data


class AIDevsClient:
    BASE_URL = "https://zadania.aidevs.pl/"
    TOKEN_URL = "token/{task_name}"
    TASK_URL = "task/{token}"
    ANSWER_URL = "answer/{token}"

    def __init__(self, api_key: str, base_url: str = BASE_URL):
        self.api_key = api_key
        self.base_url = base_url

    def __repr__(self):
        return f"AIDevsClient(api_key={self.api_key}, base_url={self.base_url})"

    def get_task(self, task_name: str) -> AIDevsTask:
        # TODO: Add some error handling e.g. properly handle reponse code/message

        # To get a task you have the perform the following steps:
        # 1. Get a token for the task
        token_url = self.base_url + self.TOKEN_URL.format(task_name=task_name)
        payload = {"apikey": self.api_key}
        response = httpx.post(token_url, json=payload)
        token = response.json()["token"]

        # 2. Get the task (response) using the token
        task_url = self.base_url + self.TASK_URL.format(token=token)
        response = httpx.get(task_url)

        return AIDevsTask(task_name, token, response.json())

    def post_answer(
        self, task: AIDevsTask, answer: Union[str, dict, List[int], List[float]]
    ):
        # TODO: Add proper typing

        answer_url = self.base_url + self.ANSWER_URL.format(token=task.token)
        payload = {"answer": answer}
        response = httpx.post(answer_url, json=payload)

        return response.json()

    def send_question(self, task: AIDevsTask, data: dict):
        url = self.base_url + self.TASK_URL.format(token=task.token)
        response = httpx.post(url, data=data)

        return response.json()
