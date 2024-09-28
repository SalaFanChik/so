from playwright.async_api import async_playwright
import asyncio

async def run_playwright(kztin):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"https://omarket.kz/search/?q={kztin}&send=Y&r=Y")
        # Выполните нужные действия, например, получение данных
        await browser.close()
