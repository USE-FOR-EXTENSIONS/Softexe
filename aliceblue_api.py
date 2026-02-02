import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, List
import requests
from requests.auth import HTTPBasicAuth
import asyncio
from aiohttp import ClientSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AliceBlueAPIClient:
    """
    AliceBlue Online API Client for Trade Mirroring System
    Handles all API communication with AliceBlue platform
    """

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://aliceblueonline.com/api/"
        self.session = None
        self.access_token = None

    async def initialize(self):
        """Initialize async session"""
        self.session = ClientSession()

    async def close(self):
        """Close async session"""
        if self.session:
            await self.session.close()

    def authenticate(self) -> bool:
        """
        Authenticate with AliceBlue API
        Returns: bool - True if authentication successful
        """
        try:
            auth_url = f"{self.base_url}authenticate"
            payload = {
                "apikey": self.api_key,
                "apisecret": self.api_secret
            }
            response = requests.post(auth_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token', data.get('token'))
                logger.info("✓ Authentication successful")
                return True
            else:
                logger.error(f"✗ Authentication failed: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False

    def get_account_details(self, account_id: str) -> Optional[Dict]:
        """Get master account details"""
        try:
            url = f"{self.base_url}account/{account_id}"
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get account details: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error getting account details: {str(e)}")
            return None

    def get_positions(self, account_id: str) -> List[Dict]:
        """Get current positions for master account"""
        try:
            url = f"{self.base_url}positions/{account_id}"
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.json().get('positions', [])
            else:
                logger.error(f"Failed to get positions: {response.text}")
                return []
        except Exception as e:
            logger.error(f"Error getting positions: {str(e)}")
            return []

    def get_orders(self, account_id: str, status: str = "all") -> List[Dict]:
        """Get orders history"""
        try:
            url = f"{self.base_url}orders/{account_id}?status={status}"
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.json().get('orders', [])
            else:
                logger.error(f"Failed to get orders: {response.text}")
                return []
        except Exception as e:
            logger.error(f"Error getting orders: {str(e)}")
            return []

    def place_order(self, account_id: str, order_params: Dict) -> Optional[Dict]:
        """
        Place an order on follower account
        
        Args:
            account_id: Follower account ID
            order_params: Order parameters {symbol, side, quantity, price, order_type, etc}
        """
        try:
            url = f"{self.base_url}orders/place"
            headers = self._get_headers()
            payload = {
                "account_id": account_id,
                **order_params
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code in [200, 201]:
                logger.info(f"✓ Order placed: {order_params['symbol']}")
                return response.json()
            else:
                logger.error(f"Failed to place order: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error placing order: {str(e)}")
            return None

    def modify_order(self, account_id: str, order_id: str, modifications: Dict) -> Optional[Dict]:
        """Modify existing order"""
        try:
            url = f"{self.base_url}orders/{order_id}/modify"
            headers = self._get_headers()
            payload = {
                "account_id": account_id,
                **modifications
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code in [200, 201]:
                logger.info(f"✓ Order modified: {order_id}")
                return response.json()
            else:
                logger.error(f"Failed to modify order: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error modifying order: {str(e)}")
            return None

    def cancel_order(self, account_id: str, order_id: str) -> bool:
        """Cancel an order"""
        try:
            url = f"{self.base_url}orders/{order_id}/cancel"
            headers = self._get_headers()
            payload = {"account_id": account_id}
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code in [200, 201]:
                logger.info(f"✓ Order cancelled: {order_id}")
                return True
            else:
                logger.error(f"Failed to cancel order: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error cancelling order: {str(e)}")
            return False

    def get_holdings(self, account_id: str) -> List[Dict]:
        """Get account holdings/portfolio"""
        try:
            url = f"{self.base_url}holdings/{account_id}"
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.json().get('holdings', [])
            else:
                logger.error(f"Failed to get holdings: {response.text}")
                return []
        except Exception as e:
            logger.error(f"Error getting holdings: {str(e)}")
            return []

    def _get_headers(self) -> Dict:
        """Get headers with authentication token"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
