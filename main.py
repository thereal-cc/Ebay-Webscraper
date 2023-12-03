from bs4 import BeautifulSoup
import requests

def extract_price_average(price_str):
    # Extracts the average value from a range or returns the single value
    prices = [float(part.replace('$', '')) for part in price_str.split(' to ')]
    return sum(prices) / len(prices)

# Scrape Ebay for listings
def scrape_ebay(search_term):
    url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={search_term}&_sacat=0"

    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    div = doc.find(class_="srp-results srp-list clearfix")
    items = div.find_all(class_="s-item s-item__pl-on-bottom")
    items_found = {}

    # Loop through each listing found
    for item in items:
        name = item.find(class_="s-item__title").text
        price = item.find(class_="s-item__price").text
        link = item.find('a').get('href')

        items_found[name] = {"price": price, "link": link}

    # Sort items_found based on price (low to high)
    sorted_items = dict(sorted(items_found.items(), key=lambda x: extract_price_average(x[1]['price'])))

    # Print out results
    for item_name, item_details in sorted_items.items():
        print(f"{item_name}")
        print(f"Price: {item_details['price']}")
        print(f"Link: {item_details['link']}")
        print("\n")

def main():
    search_term = input("Enter what you'd like to search for: ")
    scrape_ebay(search_term=search_term)

main()