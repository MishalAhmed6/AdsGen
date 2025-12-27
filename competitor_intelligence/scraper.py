"""
Competitor intelligence scraper.
Scrapes information from websites, social media, and search engines.
"""
import os
import re
import json
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse, urljoin
import logging

logger = logging.getLogger(__name__)

# Optional imports for web scraping
try:
    import requests
    from bs4 import BeautifulSoup
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("requests/beautifulsoup4 not installed. Web scraping will be limited.")

try:
    from googlesearch import search as google_search
    GOOGLE_SEARCH_AVAILABLE = True
except ImportError:
    GOOGLE_SEARCH_AVAILABLE = False
    logger.warning("googlesearch-python not installed. Google search will be unavailable.")


class CompetitorIntelligence:
    """Scrape competitor information from various sources."""
    
    def __init__(self):
        self.session = None
        if REQUESTS_AVAILABLE:
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
    
    def gather_intelligence(self, competitor_name: str, website_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Gather comprehensive competitor intelligence.
        
        Args:
            competitor_name: Name of the competitor business
            website_url: Optional website URL if known
        
        Returns:
            Dictionary with scraped information:
            {
                'business_name': str,
                'website': str,
                'description': str,
                'services': List[str],
                'key_features': List[str],
                'pricing_info': str,
                'contact_info': Dict,
                'social_media': Dict,
                'reviews_summary': str,
                'competitive_advantages': List[str],
                'source': str  # 'website', 'social_media', 'google', 'none'
            }
        """
        intelligence = {
            'business_name': competitor_name,
            'website': website_url or '',
            'description': '',
            'services': [],
            'key_features': [],
            'pricing_info': '',
            'contact_info': {},
            'social_media': {},
            'reviews_summary': '',
            'competitive_advantages': [],
            'source': 'none'
        }
        
        # Try to find website if not provided
        if not website_url:
            website_url = self._find_website(competitor_name)
            intelligence['website'] = website_url or ''
        
        # 1. Try scraping website first
        if website_url:
            website_data = self._scrape_website(website_url)
            if website_data and website_data.get('description'):
                intelligence.update(website_data)
                intelligence['source'] = 'website'
                logger.info(f"Successfully scraped website data for {competitor_name}")
                return intelligence
        
        # 2. Try social media if website fails
        social_data = self._scrape_social_media(competitor_name)
        if social_data and social_data.get('description'):
            intelligence.update(social_data)
            intelligence['source'] = 'social_media'
            logger.info(f"Successfully scraped social media data for {competitor_name}")
            return intelligence
        
        # 3. Try Google search as fallback
        google_data = self._search_google(competitor_name)
        if google_data and google_data.get('description'):
            intelligence.update(google_data)
            intelligence['source'] = 'google'
            logger.info(f"Found data from Google search for {competitor_name}")
            return intelligence
        
        # If all fail, return minimal data
        logger.warning(f"Could not scrape data for {competitor_name}, using fallback")
        return intelligence
    
    def _find_website(self, business_name: str) -> Optional[str]:
        """Try to find business website URL using Google search."""
        if not GOOGLE_SEARCH_AVAILABLE:
            return None
        
        try:
            # Search for business website
            query = f"{business_name} official website"
            results = list(google_search(query, num_results=3))
            
            for url in results:
                # Filter out social media and directories
                if not any(domain in url.lower() for domain in ['facebook.com', 'instagram.com', 'linkedin.com', 'yelp.com', 'yellowpages.com']):
                    return url
        except Exception as e:
            logger.warning(f"Error finding website: {e}")
        
        return None
    
    def _scrape_website(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape business website for information."""
        if not REQUESTS_AVAILABLE or not self.session:
            return None
        
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '') if meta_desc else ''
            
            # Extract title
            title_tag = soup.find('title')
            title = title_tag.get_text(strip=True) if title_tag else ''
            
            # Try to find main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|body', re.I))
            if main_content:
                paragraphs = main_content.find_all('p')
                text_content = ' '.join([p.get_text(strip=True) for p in paragraphs[:5]])
                if not description and text_content:
                    description = text_content[:500]  # First 500 chars
            
            # Extract services/features from common sections
            services = []
            key_features = []
            
            # Look for service lists
            for section in soup.find_all(['section', 'div'], class_=re.compile(r'service|feature|offer|product', re.I)):
                items = section.find_all(['li', 'div', 'p'])
                for item in items[:10]:
                    text = item.get_text(strip=True)
                    if text and len(text) > 10 and len(text) < 200:
                        if 'service' in section.get('class', []):
                            services.append(text)
                        else:
                            key_features.append(text)
            
            # Extract contact info
            contact_info = {}
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            phone_pattern = r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}'
            
            page_text = soup.get_text()
            emails = re.findall(email_pattern, page_text)
            phones = re.findall(phone_pattern, page_text)
            
            if emails:
                contact_info['email'] = emails[0]
            if phones:
                contact_info['phone'] = phones[0]
            
            # Extract address
            address_tags = soup.find_all(['address', 'div'], class_=re.compile(r'address|location|contact', re.I))
            if address_tags:
                contact_info['address'] = address_tags[0].get_text(strip=True)[:200]
            
            return {
                'description': description or title,
                'services': list(set(services[:10])),  # Remove duplicates, limit to 10
                'key_features': list(set(key_features[:10])),
                'contact_info': contact_info
            }
        
        except Exception as e:
            logger.warning(f"Error scraping website {url}: {e}")
            return None
    
    def _scrape_social_media(self, business_name: str) -> Optional[Dict[str, Any]]:
        """Scrape information from social media platforms."""
        # Note: Full social media scraping requires APIs (Facebook Graph API, Instagram Basic Display, etc.)
        # For now, we'll try to find social media pages and scrape basic info
        
        if not REQUESTS_AVAILABLE:
            return None
        
        intelligence = {
            'description': '',
            'services': [],
            'key_features': []
        }
        
        # Try to find Facebook page
        try:
            # Search for Facebook page URL
            if GOOGLE_SEARCH_AVAILABLE:
                query = f"{business_name} facebook page"
                results = list(google_search(query, num_results=2))
                
                for url in results:
                    if 'facebook.com' in url.lower():
                        fb_data = self._scrape_facebook_page(url)
                        if fb_data:
                            intelligence.update(fb_data)
                            intelligence['social_media'] = {'facebook': url}
                            return intelligence
        except Exception as e:
            logger.warning(f"Error searching for social media: {e}")
        
        return None
    
    def _scrape_facebook_page(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape Facebook business page (basic info only, no login required)."""
        if not REQUESTS_AVAILABLE or not self.session:
            return None
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Facebook pages have meta tags with business info
            description = ''
            meta_og_desc = soup.find('meta', property='og:description')
            if meta_og_desc:
                description = meta_og_desc.get('content', '')
            
            return {
                'description': description
            }
        except Exception as e:
            logger.warning(f"Error scraping Facebook page: {e}")
            return None
    
    def _search_google(self, business_name: str) -> Optional[Dict[str, Any]]:
        """Search Google for business information."""
        if not GOOGLE_SEARCH_AVAILABLE:
            return None
        
        try:
            # Search for business information
            query = f"{business_name} business services reviews"
            results = list(google_search(query, num_results=5))
            
            descriptions = []
            for url in results[:3]:  # Check first 3 results
                if REQUESTS_AVAILABLE and self.session:
                    try:
                        response = self.session.get(url, timeout=5)
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.text, 'html.parser')
                            
                            # Extract meta description or first paragraph
                            meta_desc = soup.find('meta', attrs={'name': 'description'})
                            if meta_desc:
                                desc = meta_desc.get('content', '')
                                if desc and len(desc) > 50:
                                    descriptions.append(desc)
                            
                            # Try to get title
                            title = soup.find('title')
                            if title:
                                title_text = title.get_text(strip=True)
                                if business_name.lower() in title_text.lower():
                                    descriptions.append(title_text)
                    except:
                        continue  # Skip if can't scrape this URL
            
            if descriptions:
                return {
                    'description': ' '.join(descriptions[:2])[:500],  # Combine first 2 descriptions
                    'source': 'google'
                }
        except Exception as e:
            logger.warning(f"Error searching Google: {e}")
        
        return None
    
    def enhance_competitor_data(self, competitor_name: str, existing_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance existing competitor data with scraped intelligence.
        
        Args:
            competitor_name: Name of competitor
            existing_data: Existing competitor data dict
        
        Returns:
            Enhanced competitor data
        """
        website_url = existing_data.get('website') or existing_data.get('url')
        
        # Gather intelligence
        intelligence = self.gather_intelligence(competitor_name, website_url)
        
        # Merge with existing data (scraped data takes priority)
        enhanced = existing_data.copy()
        
        if intelligence.get('description'):
            enhanced['description'] = intelligence['description']
        
        if intelligence.get('services'):
            existing_services = enhanced.get('services', [])
            enhanced['services'] = list(set(existing_services + intelligence['services']))
        
        if intelligence.get('key_features'):
            existing_features = enhanced.get('key_features', [])
            enhanced['key_features'] = list(set(existing_features + intelligence['key_features']))
        
        if intelligence.get('contact_info'):
            enhanced['contact_info'] = {**enhanced.get('contact_info', {}), **intelligence['contact_info']}
        
        enhanced['scraped_source'] = intelligence.get('source', 'none')
        enhanced['website'] = intelligence.get('website') or enhanced.get('website', '')
        
        return enhanced

