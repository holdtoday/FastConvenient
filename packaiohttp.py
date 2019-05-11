import aiohttp as web
from lxml import etree
import asyncio
import json


result_list = []
loop = asyncio.get_event_loop()


async def main(url, method, params=None, data=None, json=None, headers=None, cookies=None, proxy=None, timeout=None):
    async with web.ClientSession() as session:
        try:
            async with session.request(url=url, method=method, params=params, data=data, json=json, headers=headers,
                                       cookies=cookies, proxy=proxy, timeout=timeout) as resp:
                result_list.append(GetResponse(await resp.read(), resp))
        except:
            pass


def get(url, params=None, data=None, json=None, headers=None, cookies=None, proxy=None, timeout=None):
    loop.run_until_complete(
        main(url=url, method='GET', params=params, data=data, json=json, headers=headers, cookies=cookies, proxy=proxy,
             timeout=timeout))
    return result_list[-1]


def post(url, params=None, data=None, json=None, headers=None, cookies=None, proxy=None, timeout=None):
    loop.run_until_complete(
        main(url=url, method='POST', params=params, data=data, json=json, headers=headers, cookies=cookies, proxy=proxy,
             timeout=timeout))
    return result_list[-1]


def gets(urls, params=None, data=None, json=None, headers=None, cookies=None, proxy=None, timeout=None):
    task = []
    for url in urls:
        task.append(asyncio.ensure_future(
            main(url=url, method='GET', params=params, data=data, json=json, headers=headers, cookies=cookies,
                 proxy=proxy, timeout=timeout)))
        loop.run_until_complete(asyncio.wait(task))
    return result_list


def get_headers(str):
    headers = {}
    for i in str.split('\n'):
        s2 = i.strip()
        if s2:
            resultList = s2.split(':')
            if len(resultList) == 2:
                headers[resultList[0].strip()] = resultList[1].strip()
            else:
                headers[resultList[0].strip()] = resultList[1].strip() + resultList[2].strip()
    return headers


def get_cookies(str):
    cookies = {}
    for i in str.split(';'):
        s2 = i.strip()
        if s2:
            resultList = s2.split('=')
            cookies[resultList[0].strip()] = resultList[1].strip()
    return cookies


class GetResponse():
    def __init__(self, content, resp):
        self.content = content
        self.resp = resp
        print(self.resp.url)

    @property
    def status(self):
        return self.resp.status

    @property
    def url(self):
        return self.resp.url

    @property
    def headers(self):
        return self.resp.headers

    @property
    def cookies(self):
        return self.resp.cookies

    @property
    def method(self):
        return self.resp.method

    @property
    def text(self, encode='utf-8'):
        return self.content.decode(encoding=encode)

    @property
    def json(self):
        return json.loads(self.text)

    def info_by_xpath(self, str):
        return etree.HTML(self.content).xpath(str)

    def info_from_json(self, key):
        json_result = []
        return info_by_key(self.json, json_result, key)


def info_by_key(info, json_result, key):
    key_value = ''
    if isinstance(info, dict):
        for i in info.values():
            if key in json_result.keys():
                key_value = json_result.get(key)
            else:
                info_by_key(i, json_result, key)
    elif isinstance(info, list):
        for j in info:
            info_by_key(j, json_result, key)
    if not key_value:
        json_result.append(key_value)
    return json_result
