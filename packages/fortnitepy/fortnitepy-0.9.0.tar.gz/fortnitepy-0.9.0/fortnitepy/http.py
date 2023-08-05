# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2019 Terbau

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import aiohttp
import asyncio
import logging
import json

from .errors import HTTPException

log = logging.getLogger(__name__)


class HTTPClient:
    def __init__(self, client, connector=None):
        self.client = client
        self.connector = connector
        self._jar = aiohttp.CookieJar()
        self.headers = {}

        self.create_connection()
    
    @classmethod
    async def json_or_text(cls, response):
        text = await response.text(encoding='utf-8')
        if response.headers.get('content-type') == 'application/json':
            return json.loads(text)
        return text

    @property
    def user_agent(self):
        return 'EpicGamesLauncher/{0.client.build} {0.client.os}'.format(self)

    def get_auth(self, auth):
        s = 'basic '
        if auth.upper() == 'FORTNITE':
            s += self.client.fortnite_token
        elif auth.upper() == 'LAUNCHER':
            s += self.client.launcher_token
        else:
            s = auth
        
        return s

    def add_header(self, key, val):
        self.headers[key] = val

    def remove_header(self, key):
        return self.headers.pop(key)

    async def close(self):
        self._jar.clear()
        if self.__session and not self.__session.closed:
            await self.__session.close()

    def create_connection(self):
        self.__session = aiohttp.ClientSession(
            connector=self.connector,
            loop=self.client.loop,
            cookie_jar=self._jar
        )

    @property
    def session(self):
        return self.__session

    async def request(self, method, url, is_json=False, **kwargs):
        headers = {**kwargs.get('headers', {}), **self.headers}

        if is_json:
            try:
                kwargs['data'] = json.dumps(kwargs['data'])
            except KeyError:
                pass
            headers['content-type'] = 'application/json'

        if headers != {}:
            kwargs['headers'] = headers

        raw = False
        try:
            raw = kwargs.pop('raw')
        except KeyError:
            pass

        async with self.__session.request(method, url, **kwargs) as r:
            log.debug(f'{method} {url} has returned {r.status}')
            if raw:
                return r

            data = await self.json_or_text(r)
            try:
                _data = json.loads(data)
                if 'errorCode' in _data.keys():
                    raise HTTPException(r, _data)
            except (KeyError, TypeError, json.decoder.JSONDecodeError):
                pass
            return data

    async def fn_request(self, method, url, auth, **kwargs):
        headers = kwargs.get('headers', {})
        headers['User-Agent'] = self.user_agent
        if auth is not None:
            headers['Authorization'] = self.get_auth(auth)
        kwargs['headers'] = headers
        
        return await self.request(method, url, **kwargs)

    async def get(self, url, auth, **kwargs):
        return await self.fn_request('GET', url, auth, **kwargs)

    async def post(self, url, auth, **kwargs):
        return await self.fn_request('POST', url, auth, **kwargs)

    async def delete(self, url, auth, **kwargs):
        return await self.fn_request('DELETE', url, auth, **kwargs)

    async def patch(self, url, auth, **kwargs):
        return await self.fn_request('PATCH', url, auth, **kwargs)

    async def get_launcher_entitlements(self):
        return await self.get(
            'https://entitlement-public-service-prod08.ol.epicgames.com/entitlement/' \
            'api/account/{0.client.user.id}/entitlements?start=0&count=5000'.format(self),
            self.client.auth.launcher_authorization
        )

    async def launcher_quickpurchase_fortnite(self):
        return await self.post(
            'https://orderprocessor-public-service-ecomprod01.ol.epicgames.com/orderprocessor/'
            'api/shared/accounts/{0.client.user.id}/orders/quickPurchase'.format(self),
            self.client.auth.launcher_authorization,
            json={
                'salesChannel': 'Launcher-purchase-client',
                'entitlementSource': 'Launcher-purchase-client',
                'returnSplitPaymentItems': False,
                'lineOffers': [
                    {
                        'offerId': '09176f4ff7564bbbb499bbe20bd6348f',
                        'quantity': 1,
                        'namespace': 'fn'
                    }
                ]
            }
        )

    async def launcher_purchase_fortnite(self):
        return await self.get(
            'https://launcher-website-prod07.ol.epicgames.com/purchase' \
            '?showNavigation=true&namespace=fn&offers=09176f4ff7564bbbb499bbe20bd6348f',
            None
        )

    async def launcher_purchase_preview(self, token):
        return await self.post(
            'https://payment-website-pci.ol.epicgames.com/purchase/order-preview',
            self.client.auth.launcher_authorization,
            headers={
                'x-requested-with': token
            },
            data={
                'useDefault': True,
                'setDefault': False,
                'namespace': 'fn',
                'country': None,
                'countryName': None,
                'orderComplete': None,
                'orderId': None,
                'orderError': None,
                'orderPending': None,
                'offers': [
                    '09176f4ff7564bbbb499bbe20bd6348f'
                ],
                'offerPrice': ''
            }
        )

    async def launcher_purchase_confirm(self, token, order):
        return await self.post(
            'https://payment-website-pci.ol.epicgames.com/purchase/confirm-order',
            self.client.auth.launcher_authorization,
            headers={
                'x-requested-with': token
            },
            data={
                'useDefault': True,
                'setDefault': False,
                'namespace': order['namespace'],
                'country': order['country'],
                'countryName': order['countryName'],
                'orderId': None,
                'orderComplete': None,
                'orderError': None,
                'orderPending': None,
                'offers': order['offers'],
                'includeAccountBalance': False,
                'totalAmount': order['orderResponse']['totalPrice'],
                'affiliateId': '',
                'creatorSource': '',
                'syncToken': order['syncToken']
            }
        )

    async def get_profile_by_display_name(self, display_name):
        return await self.get(
            'https://account-public-service-prod03.ol.epicgames.com/account/api/' \
            'public/account/displayName/{0}'.format(display_name),
            self.client.auth.authorization
        )

    async def get_profile(self, user_id):
        return await self.get(
            'https://account-public-service-prod03.ol.epicgames.com/account/api/' \
            'public/account/{0}'.format(user_id),
            self.client.auth.authorization
        )

    async def get_profiles(self, user_ids):
        accounts = ['&accountId={}'.format(user_id) for user_id in user_ids]
        return await self.get(
            'https://account-public-service-prod03.ol.epicgames.com/account/api/' \
            'public/account?{0}'.format(''.join(accounts)),
            self.client.auth.authorization
        )
    
    async def get_friends(self, *, include_pending=False):
        _incl = True if include_pending else False
        return await self.get(
            'https://friends-public-service-prod06.ol.epicgames.com/friends/api/' \
            'public/friends/{0.client.user.id}?includePending={1}'.format(self, _incl),
            self.client.auth.authorization
        )

    async def add_friend(self, user_id):
        return await self.post(
            'https://friends-public-service-prod06.ol.epicgames.com/friends/api/' \
            'public/friends/{0.client.user.id}/{1}'.format(self, user_id),
            self.client.auth.authorization
        )

    async def remove_friend(self, user_id):
        return await self.delete(
            'https://friends-public-service-prod06.ol.epicgames.com/friends/api/' \
            'public/friends/{0.client.user.id}/{1}'.format(self, user_id),
            self.client.auth.authorization
        )

    async def get_friends_blocklist(self):
        return await self.get(
            'https://friends-public-service-prod06.ol.epicgames.com/friends/api/' \
            'public/blocklist/{0.client.user.id}'.format(self),
            self.client.auth.authorization
        )

    async def block_user(self, user_id):
        return await self.post(
            'https://friends-public-service-prod06.ol.epicgames.com/friends/api/' \
            'public/blocklist/{0.client.user.id}/{1}'.format(self, user_id),
            self.client.auth.authorization
        )

    async def unblock_user(self, user_id):
        return await self.delete(
            'https://friends-public-service-prod06.ol.epicgames.com/friends/api/' \
            'public/blocklist/{0.client.user.id}/{1}'.format(self, user_id),
            self.client.auth.authorization
        )

    async def get_br_stats_v1(self, user_id):
        return await self.get(
            'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/' \
            'stats/{0}'.format(user_id),
            self.client.auth.authorization
        )

    async def get_br_stats_v2(self, user_id, *, start_time=None, end_time=None):
        query_parameters = ''
        if start_time:
            query_parameters += '&startTime={}'.format(start_time)
        if end_time:
            query_parameters += '&endTime={}'.format(end_time)

        return await self.get(
            'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/' \
            'statsv2/account/{0}{1}'.format(user_id, query_parameters),
            self.client.auth.authorization
        )

    async def get_multiple_br_stats_v2(self, ids, stats, *, start_time=None, end_time=None):
        params = {}
        if start_time:
            params['startTime'] = start_time
        if end_time:
            params['endTime'] = end_time

        return await self.post(
            'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/statsv2/query',
            self.client.auth.authorization,
            data={
                'owners': ids,
                'stats': stats
            },
            is_json=True,
            params=params
        )

    async def get_br_leaderboard(self, stat, platform, mode, window, *, page=0, items_per_page=50):
        return await self.post(
            'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/' \
            'leaderboards/type/global/stat/br_{0}_{1}_m0_{2}/window/{3}?ownertype=1'.format(
                stat,
                platform.value,
                mode.value,
                window.value
            ),
            self.client.auth.authorization,
            is_json=True,
            params={
                'pageNumber': page,
                'itemsPerPage': items_per_page
            }
        )

    async def get_br_leaderboard_v2(self, stat):
        return await self.get(
            'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/' \
            'statsv2/leaderboards/{0}'.format(stat),
            self.client.auth.authorization
        )

    async def get_lightswitch_status(self, service_id=None):
        return await self.get(
            'https://lightswitch-public-service-prod06.ol.epicgames.com/lightswitch/api/' \
            'service/bulk/status',
            self.client.auth.authorization,
            params={'serviceId': service_id} if service_id else None
        )

    async def get_store_catalog(self):
        return await self.get(
            'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/storefront/v2/catalog',
            self.client.auth.authorization
        )

    async def get_fortnite_news(self):
        return await self.get(
            'https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game',
            self.client.auth.authorization
        )

    async def get_fortnite_content(self):
        data = await self.get(
            'https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game',
            self.client.auth.authorization
        )
        return json.loads(data)

    async def get_fortnite_timeline(self):
        return await self.get(
            'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/calendar/v1/timeline',
            self.client.auth.authorization
        )

    ########################################
    # Party
    ########################################

    async def party_send_invite(self, party_id, user_id):
        return await self.post(
            'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/' \
            'parties/{0}/invites/{1}'.format(party_id, user_id),
            self.client.auth.authorization,
            json={
                'urn:epic:cfg:build-id_s': self.client.party_build_id,
                'urn:epic:conn:platform_s': self.client.platform.value,
                'urn:epic:conn:type_s': 'game',
                'urn:epic:invite:platformdata_s': '',
                'urn:epic:member:dn_s': self.client.user.display_name,
            }
        )

    async def party_send_ping(self, user_id):
        return await self.post(
            'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/' \
            'user/{0}/pings/{1.client.user.id}'.format(user_id, self),
            self.client.auth.authorization,
            is_json=True
        )

    # partyinvite decline
    async def party_decline_invite(self, party_id):
        return await self.post(
            'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/' \
            'parties/{0}/invites/{1.client.user.id}/decline'.format(party_id, self),
            self.client.auth.authorization,
            is_json=True
        )

    async def party_member_confirm(self, party_id, user_id):
        return await self.post(
            'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/' \
            'parties/{0}/members/{1}/confirm'.format(party_id, user_id),
            self.client.auth.authorization,
            is_json=True
        )
    
    async def party_member_reject(self, party_id, user_id):
        return await self.post(
            'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/' \
            'parties/{0}/members/{1}/reject'.format(party_id, user_id),
            self.client.auth.authorization,
            is_json=True
        )

    async def party_promote_member(self, party_id, user_id):
        return await self.post(
            'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/' \
            'parties/{0}/members/{1}/promote'.format(party_id, user_id),
            self.client.auth.authorization,
            is_json=True
        )

    async def party_kick_member(self, party_id, user_id):
        return await self.delete(
            'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/' \
            'parties/{0}/members/{1}'.format(party_id, user_id),
            self.client.auth.authorization,
        )

    async def party_leave(self, party_id):
        data = {
            'connection': {
                'id': self.client.user.jid,
                'meta': {
                    'urn:epic:conn:platform_s': self.client.platform.value,
                    'urn:epic:conn:type_s': 'game'
                }
            },
            'meta': {
                'urn:epic:member:dn_s': self.client.user.display_name,
                'urn:epic:member:type_s': 'game',
                'urn:epic:member:platform_s': self.client.platform.value,
                'urn:epic:member:joinrequest_j': '{"CrossplayPreference_i":"1"}',
            }
        }

        return await self.delete(
            'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/' \
            'parties/{0}/members/{1.client.user.id}'.format(party_id, self),
            self.client.auth.authorization,
            data=data,
            is_json=True
        )

    async def party_join_request(self, party_id):
        data = {
            'connection': {
                'id': str(self.client.xmpp.xmpp_client.local_jid),
                'meta': {
                    'urn:epic:conn:platform_s': self.client.platform.value,
                    'urn:epic:conn:type_s': 'game',
                },
            },
            'meta': {
                'urn:epic:member:dn_s': self.client.user.display_name,
                'urn:epic:member:type_s': 'game',
                'urn:epic:member:platform_s': self.client.platform.value,
                'urn:epic:member:joinrequest_j': '{"CrossplayPreference_i":"1","SubGame_u":"1"}',
            },
        }

        return await self.post(
            'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/' \
            'parties/{0}/members/{1.client.user.id}/join'.format(party_id, self),
            self.client.auth.authorization,
            data=data,
            is_json=True
        )
    
    async def party_lookup(self, party_id):
        return await self.get(
            'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/' \
            'parties/{0}'.format(party_id),
            self.client.auth.authorization
        )
    
    async def party_lookup_user(self, user_id):
        return await self.get(
            'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/' \
            'user/{0}'.format(user_id),
            self.client.auth.authorization
        )

    async def party_lookup_ping(self, user_id):
        return await self.get(
            'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/' \
            '{0.client.user.id}/pings/{1}/parties'.format(self, user_id),
            self.client.auth.authorization
        )

    async def party_create(self, config):
        data = {
            'config': {
                'join_confirmation': config['join_confirmation'],
                'joinability': config['joinability'],
                'max_size': config['max_size']
            },
            'join_info': {
                'connection': {
                    'id': str(self.client.xmpp.xmpp_client.local_jid),
                    'meta': {
                        'urn:epic:conn:platform_s': self.client.platform.value,
                        'urn:epic:conn:type_s': 'game'
                    }
                }
            },
            'meta': {
                'urn:epic:cfg:party-type-id_s': 'default',
                'urn:epic:cfg:build-id_s': str(self.client.party_build_id),
                'urn:epic:cfg:join-request-action_s': 'Manual',
                'urn:epic:cfg:chat-enabled_b': str(config['chat_enabled']).lower()
            }
        }

        return await self.post(
            'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/' \
            'parties',
            self.client.auth.authorization,
            data=data,
            is_json=True
        )

    async def party_update_member_meta(self, party_id, user_id, meta, revision):
        data = {
            'delete': [],
            'revision': revision,
            'update': meta
        }

        await self.patch(
            'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/' \
            'parties/{0}/members/{1}/meta'.format(party_id, user_id),
            self.client.auth.authorization,
            data=data,
            is_json=True
        )

    async def party_update_meta(self, party_id, updated_meta, deleted_meta, config, revision):
        data = {
            'config': {
                'join_confirmation': config['join_confirmation'],
                'joinability': config['joinability'],
                'max_size': config['max_size']
            },
            'meta': {
                'delete': deleted_meta,
                'update': updated_meta
            },
            'party_state_overridden': {},
            'party_privacy_type': config['joinability'],
            'party_type': config['type'],
            'party_sub_type': config['sub_type'],
            'max_number_of_members': config['max_size'],
            'invite_ttl_seconds': config['invite_ttl_seconds'],
            'revision': revision
        }

        return await self.patch(
            'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/' \
            'parties/{0}'.format(party_id),
            self.client.auth.authorization,
            data=data,
            is_json=True
        )
