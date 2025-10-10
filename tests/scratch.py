import asyncio
from pydoll.browser import Chrome

async def element_finding_examples():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://www.seloger.com/classified-search?distributionTypes=Rent&estateTypes=Apartment&locations=AD08FR31096&numberOfBedroomsMin=1&numberOfRoomsMin=1&priceMax=1200&spaceMin=30')

        specific_items = await tab.query("//div[@class='css-1kfguso']", find_all=True, timeout=10)
        print(specific_items)

asyncio.run(element_finding_examples())

# Examples of finding elements
# # Find by attributes (most intuitive)
# submit_btn = await tab.find(
#     tag_name='button',
#     class_name='btn-primary',
#     text='Submit'
# )
# # Find by ID
# username_field = await tab.find(id='username')
# # Find multiple elements
# all_links = await tab.find(tag_name='a', find_all=True)
# # CSS selectors and XPath
# nav_menu = await tab.query('nav.main-menu')
# specific_item = await tab.query('//div[@data-testid="item-123"]')
# # With timeout and error handling
# delayed_element = await tab.find(
#     class_name='dynamic-content',
#     timeout=10,
#     raise_exc=False  # Returns None if not found
# )
# # Advanced: Custom attributes
# custom_element = await tab.find(
#     data_testid='submit-button',
#     aria_label='Submit form'
# )
#specific_items = await tab.find(tag_name='div', class_name='css-1kfguso', find_all=True)