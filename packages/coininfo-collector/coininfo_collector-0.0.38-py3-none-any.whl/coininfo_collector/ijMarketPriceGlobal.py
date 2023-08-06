# -*- coding: utf-8 -*-
# ijMarketPriceGlobal
import logging
import requests
import ujson
from .coinSummary import CoinSummary
from .web_requests_async import async_post, async_put

log = logging.getLogger('coininfo_collector')

class IJMarketPriceGlobal:
    reportURL_exchange_coins = ''
    reportURL_sparkline = ''
    requestURL_getCoinInfo = ''

    def __init__(self, *args, **kwargs):
        pass
    

    @staticmethod
    def setURL(
        urlExchangeCoins,
        urlSparklinePrefix,
        requestGetCoinInfoURL,
    ):
        IJMarketPriceGlobal.reportURL_exchange_coins = urlExchangeCoins
        IJMarketPriceGlobal.reportURL_sparkline = urlSparklinePrefix + '/updateSparkline'
        IJMarketPriceGlobal.requestURL_getCoinInfo = requestGetCoinInfoURL

    @staticmethod
    async def getCoinInfo(coinId):
        try:
            respJson = await async_post(
                log,
                IJMarketPriceGlobal.requestURL_getCoinInfo,
                data={
                    'coin_id':coinId,
                },
                retJson=True
            )
            if respJson is None:
                log.error('failed getCoinInfo. url:{}'.format(
                    IJMarketPriceGlobal.requestURL_getCoinInfo
                ))
                return None

        except Exception as inst:
            log.error('exception in getCoinPriceGlobal-getCoinInfo. msg:{}'.format(inst.args))
            return None

        return respJson


    @staticmethod
    async def reportCoinPriceGlobal(jobName, data):
        output = {}
        output['market_name'] = '_global'
        output['data'] = list()

        rank = 0
        geckoIdList = list()

        for coin in data:
            coinObjWrap = await IJMarketPriceGlobal.getCoinInfo(coin['id'])
            if coinObjWrap is None or coinObjWrap['coinObj'] is None:
                log.error('none of coininfo. coindID:{}'.format(coin['id']))
                continue

            coinObj = coinObjWrap['coinObj']

            output['data'].append(
                {
                    'rank':rank,
                    'id':coinObj['coin_id'],
                    'name_en':coinObj['name_en'],
                    'name_ko':coinObj['name_ko'],
                    'current_price':float(coin['current_price']),
                    'price_change_percentage_24h':float(coin['price_change_percentage_24h']),
                    'symbol':coinObj['symbol'],
                    'total_volume':float(coin['total_volume']),
                    'img_num': int(coinObj['gecko_id']),
                    'trade_url': coinObj['trade_url'],
                    'image_thumb' : coinObj['image_thumb'],
                    'image_small' : coinObj['image_small'],
                    'image_large' : coinObj['image_large'],
                }
            )

            # for sparkline
            geckoIdList.append(int(coinObj['gecko_id']))

            rank += 1
            if rank >= 10:
                break

        # report to data-svc
        await IJMarketPriceGlobal._report_retry(
            3,
            'getCoinPriceGlobal',
            IJMarketPriceGlobal.reportURL_exchange_coins,# self._urls['urls']['coinPriceReportURL'],
            output
        )

        # update Sparkline
        try:
            # report to scheduler
            resp = await async_post(
                log,
                IJMarketPriceGlobal.reportURL_sparkline,
                data={
                    'geckoIdList':geckoIdList,
                }
            )
            if resp is None:
                log.error('failed report. url:{}'.format(
                    IJMarketPriceGlobal.reportURL_sparkline,
                ))
        except Exception as inst:
            log.error('exception in getCoinPriceGlobal-sparkline. msg:{}'.format(inst.args))



    @staticmethod
    async def _report_retry(retyCnt, name, url, output):
        for i in range(retyCnt):
            resp = await async_put(
                log,
                url,
                data=output
            )
            if resp is None:
                log.error('failed {}'.format(name))
            else:
                log.debug('reported {}. url:{}'.format(name, url))