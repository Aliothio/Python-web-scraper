#!/usr/bin/env python3 
#   If needed run
#       sudo apt install python3-pip
#       pip3 install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
import functions
import sys

def scraper():
    URL = "https://finance.yahoo.com/markets/world-indices/"
    page = requests.get(URL)
    #print(results.prettify())
    soup = BeautifulSoup(page.content, "html.parser")
    body = soup.find(class_="body")
    stock_rows = body.find_all(class_="row")

    # Run the loops if there is even any arguments to check
    if len(sys.argv) > 1:
        # Loop per argument
        for arg in sys.argv[1:]:
            # Loop per row in the body of website
            for row in stock_rows:
                # Find the symbol to be compared against argument and get rid of the ^ since the argument doesn't have that
                tempSymbol = row.find("span", class_="symbol")
                tempSymbol = tempSymbol.text.strip()
                tempSymbol = tempSymbol.replace("^", "")
                
                if arg.upper() != tempSymbol:
                    # Continue on the next row if the symbol isn't the one that matches the argument
                    continue
                else:
                    # Rename the symbol since it matches with the one in argument
                    symbol = tempSymbol

                    # Find and print the title of the symbol
                    title = row.find("a", class_="ticker", target="_parent")
                    title = title['title']
                    print(title)

                    # Find, output, and prepare the value of the stock to be compared to potential old value
                    value = row.find("fin-streamer", attrs={"data-field": "regularMarketPrice"}) # <--- Have to use dictionary since data-field has a '-' in it
                    value = value.text.strip()
                    value_num = float(value.replace(",", ""))
                    print("Current price is $"+value)

                    # See if an old file for the stock exists and if it does get the name
                    file_status, file_name = functions.doesFileExist(symbol)
                    if file_status:
                        # Open the old file to get the old value
                        file = open('.finance/'+file_name, 'r')
                        old_value = file.read()
                        old_value_num = float(old_value.replace(",", ""))
                        file.close()
                        print("The old price was $"+old_value)

                        # Separate file name into individual parts
                        tokens_file = file_name.split('_')

                        # Find difference in values and output accordingly
                        value_diff = value_num-old_value_num
                        value_diff = round(value_diff, 2)
                        if value_diff > 0.0:
                            print("Price increased by $"+str(value_diff)+" since your last check on "+tokens_file[1]+" "+tokens_file[2])
                        elif value_diff < 0.0:
                            print("Price decreased by $"+str(value_diff)+" since your last check on "+tokens_file[1]+" "+tokens_file[2])
                        else:
                            print("Price has not changed since you last checked on "+tokens_file[1]+" "+tokens_file[2])

                        # Delete the old file
                        functions.deleteFile('.finance/'+file_name)

                    # Open new file in function then write the value to it
                    new_File = functions.makeFile('.finance/'+symbol)
                    new_File.write(value)
                    new_File.close()
                    print("")
                    break


if __name__ == "__main__":
    # Make the .finance directory if it doesn't already exist then run the scraper
    functions.makeFinance()
    scraper()
    