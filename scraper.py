import random
import re
import brotli
from typing import List, Tuple, Dict
from bs4 import BeautifulSoup
import cloudscraper
from tqdm import tqdm
from logger import get_logger

logger = get_logger(__name__)


class WebScraper:
    def __init__(self):
        self.scraper = self._create_scraper()
        self.headers = {
            "User-Agent": self._get_random_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
            "DNT": "1",
        }

    def _get_random_user_agent(self) -> str:
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
        ]
        return random.choice(user_agents)

    def _create_scraper(self):
        logger.info("Creating scraper...")
        return cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "windows", "mobile": False}
        )

    def _extract_email_components(self, img_src: str) -> Tuple[str, str]:
        """Extract email components from the image source URL."""
        domain_match = re.search(r"strT1=([^&]+)", img_src)
        username_match = re.search(r"strT2=([^&]+)", img_src)

        domain = domain_match.group(1) if domain_match else None
        username = username_match.group(1) if username_match else None

        return username, domain

    def _extract_emails_from_html(self, soup: BeautifulSoup) -> List[Tuple[str, str]]:
        """Extract roles and email addresses from the HTML."""
        results = []
        email_rows = soup.find_all("div", class_="row")
        current_role = None

        for row in email_rows:
            heading = row.find("h5")
            if heading:
                current_role = heading.get_text(strip=True)
                continue

            email_imgs = row.find_all("img", src=lambda x: x and "text2img.aspx" in x)
            if email_imgs and current_role and current_role.startswith("Entraîneur/e"):
                for img in email_imgs:
                    username, domain = self._extract_email_components(img["src"])
                    if username and domain:
                        email = f"{username}@{domain}"
                        results.append((current_role, email))

        seen = set()
        unique_results = []
        for role, email in results:
            if (role, email) not in seen:
                seen.add((role, email))
                unique_results.append((role, email))

        return unique_results[1:]

    def fetch_and_extract_emails(
        self, teams: Dict[str, str]
    ) -> Dict[str, Dict[str, str]]:
        my_dict = {}
        for team, url in tqdm(teams.items(), desc="Scraping teams"):
            try:
                my_dict[team] = {}
                logger.info(f"Fetching webpage: {url}")
                response = self.scraper.get(url, headers=self.headers)
                response.raise_for_status()

                content = response.content
                if (
                    "content-encoding" in response.headers
                    and "br" in response.headers["content-encoding"].lower()
                ):
                    logger.info("Decompressing Brotli response...")
                    try:
                        content = brotli.decompress(content)
                    except brotli.error as e:
                        logger.error(f"Brotli decompression failed: {e}")

                try:
                    decoded_content = content.decode("utf-8")
                except UnicodeDecodeError:
                    logger.warning("Failed to decode as UTF-8, trying ISO-8859-1...")
                    decoded_content = content.decode("iso-8859-1")

                logger.info("Extracting email addresses for Entraîneurs...")
                soup = BeautifulSoup(decoded_content, "html.parser")
                results = self._extract_emails_from_html(soup)

                if results:
                    logger.info(
                        f"Found {len(results)} email addresses for Entraîneurs."
                    )
                    for role, email in results:
                        my_dict[team][role] = email
                else:
                    logger.info("No email addresses found for Entraîneurs.")

            except Exception as e:
                logger.error(f"An error occurred: {e}", exc_info=True)
        return my_dict
