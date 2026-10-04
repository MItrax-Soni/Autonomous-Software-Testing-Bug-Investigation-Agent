import asyncio
import os
import uuid
from typing import List, Dict, Any, Set
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.services.ssrf_validator import SSRFValidator, SSRFSecurityError
from app.models.session import TestSession
from app.models.page import DiscoveredPage
from app.models.element import DiscoveredElement

class WebCrawlerService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def crawl_target(self, session_id: str) -> Dict[str, Any]:
        """
        Crawls the target URL up to session.max_depth and session.max_pages.
        Extracts pages and interactive DOM elements and saves them to the database.
        """
        # 1. Fetch Session from DB
        stmt = select(TestSession).where(TestSession.id == session_id)
        result = await self.db.execute(stmt)
        session = result.scalar_one_or_none()
        if not session:
            raise ValueError(f"Session with ID {session_id} not found.")

        target_url = session.target_url

        # 2. SSRF Validation
        SSRFValidator.validate_url(target_url)

        # Update session status to SCANNING
        session.status = "SCANNING"
        await self.db.commit()

        parsed_base = urlparse(target_url)
        base_origin = f"{parsed_base.scheme}://{parsed_base.netloc}"

        visited_urls: Set[str] = set()
        queue: List[Dict[str, Any]] = [{"url": target_url, "depth": 0}]

        discovered_pages_count = 0
        discovered_elements_count = 0

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=settings.PLAYWRIGHT_HEADLESS,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
            )
            context = await browser.new_context(
                viewport={"width": settings.BROWSER_VIEWPORT_WIDTH, "height": settings.BROWSER_VIEWPORT_HEIGHT},
                user_agent="AntigravityAutonomousTestingAgent/0.1.0"
            )

            # Ensure screenshot folder exists for session
            session_artifacts_dir = os.path.join(settings.ARTIFACTS_DIR, session_id)
            os.makedirs(session_artifacts_dir, exist_ok=True)

            page = await context.new_page()

            try:
                while queue and discovered_pages_count < session.max_pages:
                    item = queue.pop(0)
                    curr_url = item["url"]
                    curr_depth = item["depth"]

                    # Normalize URL (strip fragment)
                    clean_url = curr_url.split("#")[0].rstrip("/")
                    if clean_url in visited_urls:
                        continue
                    visited_urls.add(clean_url)

                    # SSRF Re-validation before navigation
                    try:
                        SSRFValidator.validate_url(curr_url)
                    except SSRFSecurityError:
                        continue

                    # Navigate to page
                    http_status = None
                    try:
                        response = await page.goto(
                            curr_url,
                            wait_until="domcontentloaded",
                            timeout=settings.PLAYWRIGHT_ACTION_TIMEOUT_MS * 2
                        )
                        http_status = response.status if response else 200
                        # Brief wait for client-side hydration
                        await asyncio.sleep(0.5)
                    except Exception as nav_err:
                        print(f"Navigation warning for {curr_url}: {nav_err}")
                        http_status = 500

                    page_title = await page.title() or curr_url

                    # Capture page screenshot
                    screenshot_filename = f"page_{discovered_pages_count + 1}.png"
                    screenshot_full_path = os.path.join(session_artifacts_dir, screenshot_filename)
                    try:
                        await page.screenshot(path=screenshot_full_path, full_page=False)
                        rel_screenshot_path = f"/artifacts/{session_id}/{screenshot_filename}"
                    except Exception:
                        rel_screenshot_path = None

                    # Persist DiscoveredPage
                    db_page = DiscoveredPage(
                        session_id=session.id,
                        url=curr_url,
                        title=page_title,
                        http_status=http_status,
                        depth=curr_depth,
                        screenshot_path=rel_screenshot_path
                    )
                    self.db.add(db_page)
                    await self.db.flush() # Populate db_page.id
                    discovered_pages_count += 1

                    # Extract Interactive Elements via DOM evaluation
                    raw_elements = await page.evaluate("""() => {
                        const results = [];
                        const interactiveSelectors = [
                            'button',
                            'a[href]',
                            'input',
                            'select',
                            'textarea',
                            '[role="button"]',
                            '[role="link"]',
                            '[role="dialog"]'
                        ];

                        const nodes = document.querySelectorAll(interactiveSelectors.join(','));
                        nodes.forEach((el, index) => {
                            // Filter out hidden or collapsed elements
                            const style = window.getComputedStyle(el);
                            if (style.display === 'none' || style.visibility === 'hidden') return;

                            const tag = el.tagName.toLowerCase();
                            let type = el.getAttribute('type') || tag;
                            if (tag === 'a') type = 'link';
                            if (el.getAttribute('role') === 'button') type = 'button';

                            // Compute a unique/robust selector
                            let selector = '';
                            if (el.id) {
                                selector = `#${CSS.escape(el.id)}`;
                            } else if (el.name) {
                                selector = `${tag}[name="${CSS.escape(el.name)}"]`;
                            } else if (el.getAttribute('data-testid')) {
                                selector = `[data-testid="${CSS.escape(el.getAttribute('data-testid'))}"]`;
                            } else if (el.getAttribute('aria-label')) {
                                selector = `[aria-label="${CSS.escape(el.getAttribute('aria-label'))}"]`;
                            } else {
                                // Fallback CSS nth selector
                                selector = `${tag}:nth-of-type(${index + 1})`;
                            }

                            // Semantic label derivation
                            const text = (el.innerText || el.value || el.placeholder || el.getAttribute('aria-label') || el.name || '').trim();
                            const label = text.length > 50 ? text.substring(0, 47) + '...' : text;

                            // Collect essential attributes
                            const attrs = {};
                            for (let attr of el.attributes) {
                                if (['id', 'name', 'type', 'class', 'placeholder', 'role', 'href'].includes(attr.name)) {
                                    attrs[attr.name] = attr.value;
                                }
                            }

                            results.push({
                                tag_name: tag,
                                element_type: type,
                                selector: selector,
                                semantic_label: label || `${type} element`,
                                attributes_json: attrs,
                                is_interactive: true
                            });
                        });
                        return results;
                    }""")

                    # Persist Elements
                    for raw_el in raw_elements:
                        db_element = DiscoveredElement(
                            page_id=db_page.id,
                            tag_name=raw_el["tag_name"],
                            element_type=raw_el["element_type"],
                            selector=raw_el["selector"],
                            semantic_label=raw_el["semantic_label"],
                            attributes_json=raw_el["attributes_json"],
                            is_interactive=raw_el["is_interactive"]
                        )
                        self.db.add(db_element)
                        discovered_elements_count += 1

                    # Queue child same-origin links if depth allows
                    if curr_depth < session.max_depth:
                        links = await page.eval_on_selector_all("a[href]", "els => els.map(e => e.href)")
                        for link in links:
                            if not link:
                                continue
                            abs_link = urljoin(curr_url, link).split("#")[0].rstrip("/")
                            parsed_link = urlparse(abs_link)
                            if f"{parsed_link.scheme}://{parsed_link.netloc}" == base_origin:
                                if abs_link not in visited_urls and not any(q["url"] == abs_link for q in queue):
                                    queue.append({"url": abs_link, "depth": curr_depth + 1})

            finally:
                await context.close()
                await browser.close()

        # Update Session state to SCANNED
        session.status = "SCANNED"
        await self.db.commit()

        return {
            "session_id": session_id,
            "status": "SCANNED",
            "pages_discovered": discovered_pages_count,
            "elements_discovered": discovered_elements_count
        }
