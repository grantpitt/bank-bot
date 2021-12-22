from playwright.async_api import async_playwright
import asyncio
from auth import username, password


async def fetch(page, doc):
    # set the download attribute to avoid opening preview
    await doc.evaluate("(node) => node.setAttribute('download', 'download')")

    # capture the download
    async with page.expect_download() as download_info:
        await doc.click()
    download = await download_info.value

    # get title from child node and save to documents folder
    title = await doc.locator(".edoc-row-name").inner_text()
    await download.save_as(f"documents/{title}.pdf")

async def run(playwright):
    # connect to browser and open page
    browser = await playwright.webkit.launch(headless=False, slow_mo=50)
    page = await browser.new_page(accept_downloads=True)
    # go to macu and login
    await page.goto("https://www.macu.com/")
    await page.fill("[name='username']", username)
    await page.fill("[name='password']", password)
    await page.click("#ctl00_plcMain_plcLeft_lt_zoneBanner_MACUSite_HomepageBannerForm_loginButton")
    # navigate to the page with documents
    await page.click("#e_docs_navigation_item")
    await page.click("[filtertab='eStatements']")
    docs = page.locator('.edoc-row')
    count = await docs.count()

    # setup fetch task for each document
    tasks = []
    for i in range(count):
        doc = docs.nth(i)
        work = fetch(page, doc)
        task = asyncio.create_task(work)
        tasks.append(task)

    # run all the tasks (awaitable objects) concurrently
    await asyncio.gather(*tasks)

    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())
