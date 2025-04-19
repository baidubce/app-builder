import asyncio
import json
import logging
from typing import Any, Dict, Optional, Union, List, Tuple

import aiohttp
from aiohttp import ClientTimeout

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HTTPClient:
    """
    HTTP client with retry mechanism, timeout handling, and error reporting.
    Supports exponential backoff for retries.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        default_timeout: int = 30,
        max_retries: int = 3,
    ):
        """
        Initialize the HTTP client.

        Args:
            base_url: Base URL for all requests
            headers: Default headers to include in all requests
            default_timeout: Default timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url
        self.headers = headers or {}
        self.default_timeout = default_timeout
        self.max_retries = max_retries
        self.session: Optional[aiohttp.ClientSession] = None

    async def _ensure_session(self) -> None:
        """Ensure aiohttp session exists and is open"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=ClientTimeout(total=self.default_timeout),
                headers=self.headers
            )

    async def close(self) -> None:
        """Close the HTTP session"""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

    async def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        data: Optional[str] = None,
        json_data: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request with retry mechanism.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            url: URL path (will be joined with base_url if provided)
            params: Query parameters
            headers: Additional headers (will be merged with default headers)
            data: Request body as string
            json_data: Request body as JSON (will be serialized)
            timeout: Request timeout in seconds (overrides default_timeout)
            max_retries: Maximum retry attempts (overrides default max_retries)

        Returns:
            Dictionary with response data or error information
        """
        # Use provided values or fall back to defaults
        timeout = timeout or self.default_timeout
        max_retries = max_retries if max_retries is not None else self.max_retries
        
        # Merge headers
        merged_headers = dict(self.headers)
        if headers:
            merged_headers.update(headers)
            
        # Handle JSON data
        if json_data:
            data = json.dumps(json_data)
            merged_headers['Content-Type'] = 'application/json'
            
        # Construct full URL
        from urllib.parse import urljoin
        full_url = urljoin(self.base_url, url) if self.base_url else url
        
        await self._ensure_session()
        
        # Implement retry logic
        retries = 0
        while retries <= max_retries:
            try:
                logger.info(f"Making {method} request to {full_url} (Attempt {retries+1}/{max_retries+1})")
                
                async with self.session.request(
                    method=method.upper(),
                    url=full_url,
                    params=params,
                    headers=merged_headers,
                    data=data,
                    timeout=ClientTimeout(total=timeout)
                ) as response:
                    response.raise_for_status()
                    
                    # Handle different response content types
                    content_type = response.headers.get('content-type', '')
                    
                    if 'application/json' in content_type:
                        result = await response.json()
                    else:
                        result = await response.text()
                        
                    return {
                        'success': True,
                        'status_code': response.status,
                        'content_type': content_type,
                        'data': result
                    }
                    
            except (aiohttp.ClientResponseError, aiohttp.ClientConnectorError) as e:
                error_message = str(e)
                error_body = None
                
                if isinstance(e, aiohttp.ClientResponseError):
                    try:
                        error_body = await response.json()
                    except:
                        try:
                            error_body = await response.text()
                        except:
                            error_body = "Could not read response body"
                    
                    error_message = f"{error_message} - {error_body}"
                
                retries += 1
                if retries <= max_retries:
                    wait_time = 2 ** retries  # Exponential backoff
                    logger.warning(f"Request failed: {error_message}. Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Request failed after {max_retries+1} attempts: {error_message}")
                    return {
                        'success': False,
                        'error': {
                            'type': 'http_error' if isinstance(e, aiohttp.ClientResponseError) else 'network_error',
                            'status_code': e.status if isinstance(e, aiohttp.ClientResponseError) else None,
                            'detail': error_message
                        }
                    }
            except aiohttp.ClientError as e:
                logger.error(f"Client error: {str(e)}")
                return {
                    'success': False,
                    'error': {
                        'type': 'network_error',
                        'detail': str(e)
                    }
                }
            except asyncio.TimeoutError:
                retries += 1
                if retries <= max_retries:
                    wait_time = 2 ** retries  # Exponential backoff
                    logger.warning(f"Request timed out after {timeout} seconds. Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Request timed out after {max_retries+1} attempts")
                    return {
                        'success': False,
                        'error': {
                            'type': 'timeout_error',
                            'detail': f"Request timed out after {timeout} seconds"
                        }
                    }
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                return {
                    'success': False,
                    'error': {
                        'type': 'unexpected_error',
                        'detail': str(e)
                    }
                }
                
    async def get(self, url: str, **kwargs) -> Dict[str, Any]:
        """Convenience method for GET requests"""
        return await self.request("GET", url, **kwargs)
        
    async def post(self, url: str, **kwargs) -> Dict[str, Any]:
        """Convenience method for POST requests"""
        return await self.request("POST", url, **kwargs)
        
    async def put(self, url: str, **kwargs) -> Dict[str, Any]:
        """Convenience method for PUT requests"""
        return await self.request("PUT", url, **kwargs)
        
    async def patch(self, url: str, **kwargs) -> Dict[str, Any]:
        """Convenience method for PATCH requests"""
        return await self.request("PATCH", url, **kwargs)
        
    async def delete(self, url: str, **kwargs) -> Dict[str, Any]:
        """Convenience method for DELETE requests"""
        return await self.request("DELETE", url, **kwargs)
