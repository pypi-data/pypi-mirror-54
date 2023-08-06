# -*- coding: utf-8 -*-
import aiohttp
import ujson

async def async_get(log, url, headers=None):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                text = await resp.text()
                if resp.status is not 200:
                    log.error('GET {} failed with status {} - {}'.format(url, resp.status, text))
                    return None
                return await resp.json()
    except Exception as inst:
        log.error('exception in fetch. url:{} msg:{}'.format(url, inst.args))
        return None


async def async_post(log, url, data=None, retJson=None):
    try:
        if data is not None:
            headers = {
                "content-type":"application/json"
            }
            dataSerial = ujson.dumps(data, ensure_ascii=False)
        else:
            headers = None
            dataSerial = None

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=dataSerial) as resp:
                text = await resp.text()
                if resp.status is not 200:
                    log.error('POST {} failed with status {} - {}'.format(url, resp.status, text))
                    return None
                if retJson is not None and retJson is True:
                    return await resp.json()
                else:
                    return resp
                    
    except Exception as inst:
        log.error('exception in fetch. url:{} msg:{}'.format(url, inst.args))
        return None


async def async_put(log, url, data=None, retJson=None):
    try:
        if data is not None:
            headers = {
                "content-type":"application/json"
            }
            dataSerial = ujson.dumps(data, ensure_ascii=False)
        else:
            headers = None
            dataSerial = None

        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, data=dataSerial) as resp:
                text = await resp.text()
                if resp.status is not 200:
                    log.error('POST {} failed with status {} - {}'.format(url, resp.status, text))
                    return None
                if retJson is not None and retJson is True:
                    return await resp.json()
                else:
                    return resp
                    
    except Exception as inst:
        log.error('exception in fetch. url:{} msg:{}'.format(url, inst.args))
        return None