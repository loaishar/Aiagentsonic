import asyncio
import logging
from typing import Optional

from browser_use import Browser as BrowserUseBrowser
from browser_use import BrowserConfig

from app.config import config

logger = logging.getLogger(__name__)


class BrowserPool:
    """
    A class to manage a pool of browser instances.
    """

    def __init__(self, max_size: int = 5):
        self.max_size = max_size
        self._pool: asyncio.Queue[BrowserUseBrowser] = asyncio.Queue(maxsize=max_size)
        self._lock = asyncio.Lock()
        self._browser_config = self._get_browser_config()
        self._initialized = False

    async def initialize(self):
        """
        Initialize the browser pool by creating the initial browser instances.
        """
        if self._initialized:
            return

        logger.info(f"Initializing browser pool with {self.max_size} browsers...")
        for _ in range(self.max_size):
            browser = await self._create_browser()
            await self._pool.put(browser)
        self._initialized = True
        logger.info("Browser pool initialized.")

    async def acquire(self) -> BrowserUseBrowser:
        """
        Acquire a browser instance from the pool.
        """
        await self.initialize()
        logger.debug("Acquiring browser from pool...")
        browser = await self._pool.get()
        logger.debug("Browser acquired from pool.")
        return browser

    async def release(self, browser: BrowserUseBrowser):
        """
        Release a browser instance back to the pool.
        """
        logger.debug("Releasing browser back to pool...")
        await self._pool.put(browser)
        logger.debug("Browser released back to pool.")

    async def close(self):
        """
        Close all browser instances in the pool.
        """
        logger.info("Closing all browsers in the pool...")
        while not self._pool.empty():
            browser = await self._pool.get()
            await browser.close()
        logger.info("All browsers closed.")

    def _get_browser_config(self) -> BrowserConfig:
        """
        Get the browser configuration from the app config.
        """
        browser_config_kwargs = {"headless": False, "disable_security": True}

        if config.browser_config:
            from browser_use.browser.browser import ProxySettings

            # handle proxy settings.
            if config.browser_config.proxy and config.browser_config.proxy.server:
                browser_config_kwargs["proxy"] = ProxySettings(
                    server=config.browser_config.proxy.server,
                    username=config.browser_config.proxy.username,
                    password=config.browser_config.proxy.password,
                )

            browser_attrs = [
                "headless",
                "disable_security",
                "extra_chromium_args",
                "chrome_instance_path",
                "wss_url",
                "cdp_url",
            ]

            for attr in browser_attrs:
                value = getattr(config.browser_config, attr, None)
                if value is not None:
                    if not isinstance(value, list) or value:
                        browser_config_kwargs[attr] = value

        return BrowserConfig(**browser_config_kwargs)

    async def _create_browser(self) -> BrowserUseBrowser:
        """
        Create a new browser instance.
        """
        logger.debug("Creating a new browser instance...")
        browser = BrowserUseBrowser(self._browser_config)
        logger.debug("New browser instance created.")
        return browser


# Global browser pool instance
browser_pool = BrowserPool(max_size=5)  # You can adjust the pool size as needed
