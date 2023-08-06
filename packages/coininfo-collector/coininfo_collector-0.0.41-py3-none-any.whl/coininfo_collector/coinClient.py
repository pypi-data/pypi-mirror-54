# -*- coding: utf-8 -*-
import asyncio
import copy
import logging
import queue
import os
import requests
import threading
from time import sleep
import ujson
from utail_base import web_support

from .coinSummary import CoinSummary

# from .coinCommons import CoinCommons as CC
from .ijMarketPriceGlobal import IJMarketPriceGlobal
from .web_requests_async import async_get, async_post, async_put

log = logging.getLogger('coininfo_collector')

api_prefix = 'https://api.coingecko.com/api/v3/'

limitRequestsPerMin = int(os.environ['limitRequestsPerMin']) if 'limitRequestsPerMin' in os.environ else 100
# self._requestDurationForOneRequest = float(limitRequestsPerMin) / 60.0

requestCostTime = float(60) / float(limitRequestsPerMin)


from time import sleep
from timeit import default_timer as timer

def timeDurationAsync(logger, sleepTime = 1.0):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                startTime = timer()

                retValue = await func(*args, **kwargs)

                elapsed = timer() - startTime

                if float(sleepTime) > (elapsed):
                    await asyncio.sleep(float(sleepTime) - float(elapsed))

                return retValue

            except Exception as inst:
                # log the exception
                err = "There was an exception in {}. msg:{}".format(func.__name__, inst.args)
                logger.error(err)
                return None
        return wrapper
    return decorator



class CoinClientBaseClass:
	pass

class CoinClientSingleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(CoinClientSingleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

class CoinClient(CoinClientBaseClass, metaclass=CoinClientSingleton):
    def __init__(
        self,
        loggerName='coininfo_collector', 
        keepJobsInQ = 5,
        aliveURL='http://127.0.0.1:6000/coininfo/coinAlive',
        requestURL='http://127.0.0.1:6000/coininfo/coinJobRequest',
        requestGetCoinInfoURL='http://127.0.0.1:6000/coininfo/get_coin_info',
        reportURL='http://127.0.0.1:6000/coininfo/coinJobReport',
        logURL='http://127.0.0.1:6000/coininfo/coinJobReport',
        schudulerURLPrefix='http://127.0.0.1:6000/coininfo',
        jobCoin=True,
        jobTicker=True,
        cbPostEventLoopBroken=None,
    ):
        self._log = logging.getLogger(loggerName)
        self._keepJobsInQ = keepJobsInQ

        self._aliveURL = aliveURL
        self._requestURL = requestURL
        self._reportURL = reportURL
        self._logURL = logURL

        self._jobCoin = jobCoin
        self._jobTicker = jobTicker

        # 
        self._cbPostEventLoopBroken = cbPostEventLoopBroken


        # job q
        self._jobQ = queue.Queue()
        self._reportQ = queue.Queue()
        self._injectQ = queue.Queue()

        self._requestJobList = list()

        # make Job List.
        self._makeJobList()

        self._tickerPage = 1
        self._coinsMarketPage = 1

        self._tickerList = list()

        # priceGlobal
        IJMarketPriceGlobal.setURL(
            os.environ['url_data_svc'] + '/exchange/coins',
            'http://' + os.environ['schudulerURLPrefix'],
            requestGetCoinInfoURL,
        )

        self._schedulerAlive = False
        self._aliveCheckDurSec = 3.0

        # 작업 쓰레드 시작
        t = threading.Thread(
            target=self._schedule,
            name='coinClient'
        )             
        t.setDaemon(False)
        t.start()

    def __exct_handler(self, loop, data):
        log.error('coinClient Handled exception {0}'.format(data))
        # logging.debug("Handled exception {0}".format(data))

        if loop.is_running() is True:
            loop.stop()

    def _schedule(self):
        while True:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

            asyncio.ensure_future(self._checkingSchuedulerAlive())
            asyncio.ensure_future(self._reportTask())
            asyncio.ensure_future(self._requestTask())
            asyncio.ensure_future(self._runTask())
            asyncio.ensure_future(self._runTaskInjected())

            self._loop.set_exception_handler(self.__exct_handler)

            self._loop.run_forever()

            log.error('broken coinClient Task')

            self._loop.close()

            if self._cbPostEventLoopBroken is not None:
                self._cbPostEventLoopBroken()


    def _makeJobList(self):
        if self._jobCoin is False \
            and self._jobTicker is False:
            web_support.raiseHttpError(log, 0, 'None jobs..')

        if self._jobCoin is True:
            self._requestJobList.append('jobCoin')
        if self._jobTicker is True:
            self._requestJobList.append('jobTicker')


    async def _reportTask(self):
        while True:
            try:
                if self._reportQ.empty() is True:
                    await asyncio.sleep(1)
                    continue

                job, target_id, output = self._reportQ.get()

                # response = requests.post(
                #     self._reportURL,
                #     verify=False,
                #     json={
                #         'job':job,
                #         'id':target_id,
                #         'output':output,
                #     },
                # )

                # if response.status_code != 200:
                #     log.error('failed report. code:{} url:{} msg:{}'.format(
                #         response.status_code, self._reportURL, response.text))

                await async_post(
                    log, self._reportURL,
                    data={
                        'job':job,
                        'id':target_id,
                        'output':output,
                    }
                )

            except Exception as inst:
                log.error('exception in _reportTask. msg:{}'.format(inst.args))

    
    async def _checkingSchuedulerAlive(self):
        while True:
            try:
                if self._schedulerAlive is False:
                    await asyncio.sleep(self._aliveCheckDurSec)
                else:
                    await asyncio.sleep(900)

                result = await async_post(log, self._aliveURL)
                if result is not None:
                    self._schedulerAlive = True
                else:
                    self._schedulerAlive = False
            except Exception as inst:
                log.debug('connecting to coin-scheduler. url:{} msg:{}'.format(self._aliveURL, inst.args))


    async def _requestTask(self):
        while True:
            try:
                if self._schedulerAlive is False:
                    await asyncio.sleep(self._aliveCheckDurSec)
                    continue

                if self._keepJobsInQ <= self._jobQ.qsize():
                    await asyncio.sleep(1)
                    continue

                response = requests.post(
                    self._requestURL,
                    verify=False,
                    json={
                        'jobs':self._requestJobList,
                    },
                )

                jo = await async_post(
                    log, self._requestURL,
                    data={
                        'jobs':self._requestJobList,
                    },
                    retJson=True,
                )
                #print(ujson.dumps(jo, ensure_ascii=False))

                for job in jo['jobs']:
                    self._jobQ.put(job)

                if 0 == len(jo['jobs']):
                    await asyncio.sleep(2)
                    continue

            except Exception as inst:
                log.error('failed _getJobCoinList. msg:{}'.format(inst.args))
                await asyncio.sleep(2)
                continue


    async def _runTask(self):
        while True:
            try:
                if self._jobQ.empty():
                    await asyncio.sleep(1)
                    continue

                job = self._jobQ.get()
                if 'id' not in job:
                    job['id'] = 0

                #print(job)

                endJob = False
                self._tickerPage = 1
                self._coinsMarketPage = 1
                self._coinPriceMarketPage = 1
                output = {}

                while endJob is False:
                    if job['job'] == 'coins_markets':
                        if 'data' not in output:
                            output['data'] = list()
                        endJob = await self._requestCoinsMarkets(output)
                    elif job['job'] == 'market_chart':
                        endJob = await self._requestMarketChart(job['id'], output)
                    elif job['job'] == 'coins':
                        endJob = await self._requestCoins(job['id'], output)
                    elif job['job'] == 'global':
                        endJob = await self._requestGlobal(output)
                    elif job['job'] == 'ticker':
                        if 'tickers' not in output:
                            output['tickers'] = list()
                        endJob = await self._requestTicker(job['id'], output)
                    elif job['job'] == 'bitcoin':
                        endJob = await self._requestBitcoin(output)
                    elif job['job'] == 'coinPriceMarket':
                        if 'data' not in output:
                            output['data'] = list()
                            output['tickers'] = list()

                        endJob = await self._requestCoinPriceMarket(output, job['id'])

                if endJob is True:
                    self._reportQ.put((
                        job['job'],
                        job['id'],
                        output
                    ))

            except Exception as inst:
                log.error('exception in _runTask. job:{} msg:{}'.format(job, inst.args))


    
    async def _runTaskInjected(self):
        while True:
            try:
                if self._injectQ.empty():
                    await asyncio.sleep(1)
                    continue

                job = self._injectQ.get()
                jobName = job['jobName']

                if jobName == 'marketPriceGlobal':
                    # 주요 암호화폐 시세(글로벌)
                    # report to datasvc
                    await IJMarketPriceGlobal.reportCoinPriceGlobal(
                        jobName,
                        job['data'],
                    )

                    # report to scheduler
                    self._reportQ.put((
                        'coins_markets_global', # job name
                        'coins_markets_global', # id. not using in this job
                        job['data']
                    ))

            except Exception as inst:
                log.error('exception in _runTaskInjected. job:{} msg:{}'.format(jobName, inst.args))



    @timeDurationAsync(log, requestCostTime)
    async def _requestCoinsMarkets(self, output):
        perPage = 250
        # order=volume_desc
        # order=market_cap_desc

        jo = await async_get(
            log,
            api_prefix + 'coins/markets?vs_currency=usd&per_page={}&page={}&order=market_cap_desc&price_change_percentage=1h,24h,7d'.format(
                perPage, self._coinsMarketPage
            ),
            headers={'cache-control': 'no-cache'}
        )

        if jo is None:
            return None
        
        if self._coinsMarketPage == 1:

            # 코인 한글이름 찾아넣기
            for coin in jo:
                coinObj = CoinSummary().getCoinInfoByCoinId(coin['id'])
                if coinObj is None:
                    coin['name_ko'] = coin['id']
                else:
                    coin['name_ko'] = coinObj['name_ko']

            # 주요 암호화폐 시세(글로벌)
            self._injectQ.put({
                'jobName':'marketPriceGlobal',
                'data':copy.deepcopy(jo),
            })

        try:
            arraySize = 0
            for ent in jo:
                arraySize += 1
                output['data'].append(ent)

            self._coinsMarketPage += 1

            return perPage > arraySize
            
        except Exception as inst:
            log.error('exception in _requestCoinsMarkets(). msg:{} page:{}'.format(
                inst.args, self._coinsMarketPage
            ))


    @timeDurationAsync(log, requestCostTime)
    async def _requestCoinPriceMarket(self, output, exchange_id):
        jo = await async_get(
            log,
            api_prefix + 'exchanges/{}/tickers?page={}&order=volume_desc'.format(
                exchange_id, self._coinPriceMarketPage),
            headers={'cache-control': 'no-cache'}
        )

        if jo is None:
            return None

        try:
            self._coinPriceMarketPage += 1

            output['tickers'].extend(jo['tickers'])

            # ticker 갯수가 100개 미만일 경우 마지막 페이지임.
            if 100 <= len(jo['tickers']):
                return False

        except Exception as inst:
            log.error('exception in _requestCoinPriceMarket. msg:{}. page:{}'.format(
                    inst.args, self._coinPriceMarketPage))
            return None

        # 거래소 이름
        output['market_name'] = jo['name']

        return True


    @timeDurationAsync(log, requestCostTime)
    async def _requestMarketChart(self, target_id, output):
        jo = await async_get(
            log,
            api_prefix + 'coins/{}/market_chart?vs_currency=usd&days=1'.format(
                target_id,
            ),
            headers={'cache-control': 'no-cache'}
        )
        if jo is None:
            return None
        
        jo['cid'] = str(target_id)
        jo['days'] = 1

        output['data'] = jo
        return True

    @timeDurationAsync(log, requestCostTime)
    async def _requestCoins(self, target_id, output):
        jo = await async_get(
            log,
            api_prefix + 'coins/{}?tickers=true&market_data=true&community_data=true&developer_data=true&sparkline=true'.format(target_id),
            headers={'cache-control': 'no-cache'}
        )
        if jo is None:
            return None
        
        output['data'] = jo
        return True

    @timeDurationAsync(log, requestCostTime)
    async def _requestGlobal(self, output):
        jo = await async_get(
            log,
            api_prefix + 'global',
            headers={'cache-control': 'no-cache'}
        )
        if jo is None:
            return None

        output['data'] = jo
        return True

    
    async def _requestBitcoin(self, output):
        exchange_ids_bitcoin = ['binance', 'bitfinex', 'upbit']

        for exchange_id in exchange_ids_bitcoin:

            jo = await async_get(
                log,
                api_prefix + 'coins/bitcoin/tickers?exchange_ids={}&page=1'.format(exchange_id),
                headers={'cache-control': 'no-cache'}
            )
            if jo is None:
                log.error('failed _requestBitcoin. exchangeID:{}'.format(
                    exchange_id
                ))
                continue

            jo['id'] = 'bitcoin'

            resp = await async_put(
                log,
                os.environ['url_data_svc'] + '/coin/tickers',
                data=jo
            )
            if resp is not None:
                log.debug('reported. _requestBitcoin exchange_id: {}'.format(exchange_id))
            else:
                log.error('report failed _requestBitcoin. exchange_id:{}'.format(exchange_id))

        
        return True



    @timeDurationAsync(log, requestCostTime )
    async def _requestTicker(self, target_id, output):
        jo = await async_get(
            log,
            api_prefix + 'exchanges/{}/tickers?page={}&order=volume_desc'.format(
                target_id, self._tickerPage
            ),
            headers={'cache-control': 'no-cache'}
        )
        if jo is None:
            return None

        self._tickerPage += 1

        try:
            output['tickers'].extend(jo['tickers'])
        except Exception as inst:
            log.error('_requestTicker. no tickers. msg:{}. target_id:{}'.format(
                inst.args, target_id
            ))
            return None

        if len(output['tickers']) == 0:
            log.error('_requestTicker. no tickers. (not error). exchange:{}'.format(
                target_id
            ))
            return None

        # ticker 갯수가 100개 미만일 경우 마지막 페이지 입니다.
        return 100 > len(jo['tickers'])
