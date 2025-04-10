from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import os
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BasePage:
    """
    Base Page class that all page objects will inherit from.
    
    This class provides common methods for page interactions such as
    navigation, element finding, clicking, and data input.
    """
    
    def __init__(self, driver, base_url=None):
        """
        Initialize the BasePage with WebDriver instance.
        
        Args:
            driver: WebDriver instance
            base_url: Base URL for the website
        """
        self.driver = driver
        self.base_url = base_url or "https://coinmarketcap.com"
        self.timeout = 10
    
    def navigate_to(self, url_path=""):
        """
        Navigate to the specified URL path.
        
        Args:
            url_path: Path to append to the base URL
            
        Returns:
            Self for method chaining
        """
        url = f"{self.base_url}/{url_path}"
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)
        return self
    
    def find_element(self, locator, timeout=None):
        """
        Find an element on the page with explicit wait.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            timeout: Wait timeout in seconds
            
        Returns:
            WebElement if found
            
        Raises:
            TimeoutException if element not found within timeout
        """
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element not found with locator: {locator}")
            raise
    
    def find_elements(self, locator, timeout=None):
        """
        Find multiple elements on the page with explicit wait.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            timeout: Wait timeout in seconds
            
        Returns:
            List of WebElements if found
            
        Raises:
            TimeoutException if no elements found within timeout
        """
        timeout = timeout or self.timeout
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            logger.error(f"Elements not found with locator: {locator}")
            raise
    
    def click(self, locator, timeout=None):
        """
        Click on an element.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            timeout: Wait timeout in seconds
            
        Returns:
            Self for method chaining
        """
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            return self
        except TimeoutException:
            logger.error(f"Element not clickable with locator: {locator}")
            raise
    
    def input_text(self, locator, text, timeout=None):
        """
        Input text into an element.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            text: Text to input
            timeout: Wait timeout in seconds
            
        Returns:
            Self for method chaining
        """
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.clear()
            element.send_keys(text)
            return self
        except TimeoutException:
            logger.error(f"Element not interactable with locator: {locator}")
            raise
    
    def get_text(self, locator, timeout=None):
        """
        Get text from an element.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            timeout: Wait timeout in seconds
            
        Returns:
            Text content of the element
        """
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.text
        except TimeoutException:
            logger.error(f"Element not visible with locator: {locator}")
            raise
    
    def is_element_present(self, locator, timeout=None):
        """
        Check if an element is present on the page.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            timeout: Wait timeout in seconds
            
        Returns:
            True if element is present, False otherwise
        """
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_visible(self, locator, timeout=None):
        """
        Wait for an element to be visible.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            timeout: Wait timeout in seconds
            
        Returns:
            WebElement if visible
            
        Raises:
            TimeoutException if element not visible within timeout
        """
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element not visible with locator: {locator}")
            raise
    
    def wait_for_element_invisible(self, locator, timeout=None):
        """
        Wait for an element to be invisible.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            timeout: Wait timeout in seconds
            
        Returns:
            True if element is invisible
            
        Raises:
            TimeoutException if element still visible within timeout
        """
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"Element still visible with locator: {locator}")
            raise
    
    def scroll_to_element(self, locator, timeout=None):
        """
        Scroll to an element.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            timeout: Wait timeout in seconds
            
        Returns:
            Self for method chaining
        """
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            return self
        except TimeoutException:
            logger.error(f"Element not found with locator: {locator}")
            raise
    
    def take_screenshot(self, filename=None):
        """
        Take a screenshot of the current page.
        
        Args:
            filename: Name of the screenshot file
            
        Returns:
            Path to the screenshot file
        """
        if filename is None:
            timestamp = int(time.time())
            filename = f"screenshot_{timestamp}.png"
        
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up two levels to the project root
        project_root = os.path.dirname(os.path.dirname(current_dir))
        # Screenshot directory
        screenshot_dir = os.path.join(project_root, 'reports', 'screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)
        
        # Take screenshot
        screenshot_path = os.path.join(screenshot_dir, filename)
        self.driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved to {screenshot_path}")
        
        return screenshot_path
    
    def get_current_url(self):
        """
        Get the current URL.
        
        Returns:
            Current URL
        """
        return self.driver.current_url
    
    def get_title(self):
        """
        Get the page title.
        
        Returns:
            Page title
        """
        return self.driver.title
    
    def refresh_page(self):
        """
        Refresh the current page.
        
        Returns:
            Self for method chaining
        """
        self.driver.refresh()
        return self
    
    def go_back(self):
        """
        Navigate back to the previous page.
        
        Returns:
            Self for method chaining
        """
        self.driver.back()
        return self
    
    def go_forward(self):
        """
        Navigate forward to the next page.
        
        Returns:
            Self for method chaining
        """
        self.driver.forward()
        return self
