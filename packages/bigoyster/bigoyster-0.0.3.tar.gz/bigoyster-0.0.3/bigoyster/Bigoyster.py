import requests
import logging
import json

_logger = logging.getLogger(__name__)


class Bigoyster:
    token = False

    def __init__(self, base_url='https://api.bigoyster.com/', token=False, username=False, password=False):
        self.base_url = base_url
        if token:
            self.token = token
        else:
            self.token = self.get_token(username, password)

    def get_token(self, username, password):
        url = self.base_url + "api-token-auth/"

        payload = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return json.loads(response.text)['token']
        else:
            print('GET TOKEN FAILED')
            return False

    def get_headers(self):
        headers = {
            'Authorization': "Token " + self.token,
        }
        return headers

    def call_create_api(self, object, values):
        baseurl = self.base_url
        url = baseurl + object + '/create/'

        response = requests.post(url, json=values, headers=self.get_headers(), timeout=5)
        print(response.elapsed)
        if response.status_code == 201:
            result = json.loads(response.text)
            return result
        elif response.status_code == 401:
            print('NOT AUTHORIZED')
            if self.get_token():
                print('RETRY')
                return self.call_create_api(object, values)
        elif response.status_code >= 400:
            print('400s BAD REQUEST')

        else:
            print('UNHANDLED STATUS CODE')
        return False, response

    def call_get_api(self, object, params):
        baseurl = self.base_url
        url = baseurl + object + '/get/'

        response = requests.get(url, params=params, headers=self.get_headers(), timeout=5)
        print(response.elapsed)
        if response.status_code == 200:
            result = json.loads(response.text)
            return result
        elif response.status_code == 401:
            print('NOT AUTHORIZED')
            if self.get_token():
                print('RETRY')
                return self.call_get_api(object, params)
        elif response.status_code == 404:
            print('NOT FOUND')
            return False
        elif response.status_code >= 400:
            print('400s BAD REQUEST')

        else:
            print('UNHANDLED STATUS CODE')
        return False, response

    def call_list_api(self, object, params):
        baseurl = self.base_url
        url = baseurl + object + '/list/'

        response = requests.get(url, params=params, headers=self.get_headers(), timeout=5)
        print(response.elapsed)
        if response.status_code == 200:
            result = json.loads(response.text)
            return result
        elif response.status_code == 401:
            print('NOT AUTHORIZED')
            if self.get_token():
                print('RETRY')
                return self.call_get_api(object, params)
        elif response.status_code == 404:
            print('NOT FOUND')
            return False
        elif response.status_code >= 400:
            print('400s BAD REQUEST')

        else:
            print('UNHANDLED STATUS CODE')
        return False, response

    # HELPER FUNCTIONS BELOW
    def get_consumer_by_phone(self, phone):
        return self.call_get_api('consumer', {'phone': phone})

    def get_consumer_coupons(self, device_id, consumer_id, upcs='', qtys='', prices='', txn_line_refs=''):
        """
        Get all consumer coupons with optional parameters
        :param consumer_id: UUID
        :param upcs: comma separated string
        :param qtys: comma separated string
        :param prices: comma separated string
        :return:
        """
        params = {
            "consumer": consumer_id,
            "status": "active",
            "upcs": upcs,
            "qtys": qtys,
            "prices": prices
        }
        products = upcs.split(',')
        quantities = [int(v) for v in qtys.split(',')]
        txn_lines = txn_line_refs.split(',')
        result = self.call_list_api('coupon', params=params)
        print(result)
        valid = []
        for coupon in result:
            common = list(set(products) & set(coupon.get('upcs')))
            if len(common) > 0:
                index = products.index(common[0])
                purchased_qty = int(quantities[index])
                coupon_limit = int(coupon.get('per_customer_limit'))
                if purchased_qty <= coupon_limit:
                    qty_captured = purchased_qty
                else:
                    qty_captured = coupon_limit

                valid.append({
                    'id': coupon.get('id'),
                    'upc': common[0],
                    'each_currency_off': coupon.get('discount_amount', 0),
                    'discount_type': coupon.get('discount_type'),
                    'description':  coupon.get('description', 'MISSING DESCRIPTION'),
                    'qty_captured': qty_captured,
                    'txn_line_ref': txn_lines[index]
                })

                if purchased_qty == coupon_limit:
                    del quantities[index]
                    del products[index]
                else:
                    quantities[index] = quantities[index] - 1
        print(products)
        print(quantities)
        auth_code = 'kdCjdhsUi4H'
        return {'auth_code': auth_code, 'coupons': valid}

    def redeem_coupons(self, device_id, coupon_ids, redemption_values):
        # todo put this in redis
        # todo for each upc send to petzmobile for stats
        # todo calculate total based on passed values and previous total
        total = 123.0
        receipt_lines = "You're total saving with \n Petzmobile: %s" % total
        return {'success': 'True', 'receipt_lines': receipt_lines}

    def get_campaign_upcs(self, device_id):
        params = {
            "view": "criteria",
            "status": "active"
        }
        result = self.call_list_api('campaign', params=params).get('results')
        upcs = []
        for c in result:
            for upc in c.get('criteria', {}).get('valid_products', []):
                if upc not in upcs:
                    upcs.append(upc)
        return upcs

    def create_retail_coupon(self, device_id):
        return {'success': 'True'}

    def create_retail_settlement(self, device_id):
        return {'success': 'True'}
