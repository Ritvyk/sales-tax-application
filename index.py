
# Terminal program to calculate sales tax for various goods and print a receipt

import re

# class to define taxations for multiple edge cases


class Taxations:
    basicSalesTax = 10
    importSalesTax = 5
    exemptedGoods = ["book", "chocolate", "pills", "medicine"]

    def __init__(self):
        pass

    def __isExempted(self, productName):
        isExempted = False
        for exemptGood in self.exemptedGoods:
            if(productName.find(exemptGood) >= 0):
                isExempted = True
                break
        return isExempted

    # calculate taxation based on the parameters
    def calculateTaxForProduct(self, product):
        if product:
            totalTaxation = 0
            if(not self.__isExempted(product["name"])):
                totalTaxation += (((product["price"] *
                                    product["quantity"]) * self.basicSalesTax)/100)
                if product["isImported"]:
                    totalTaxation += ((product["price"] *
                                       product["quantity"]) * self.importSalesTax)/100
            else:
                if product["isImported"]:
                    totalTaxation += ((product["price"] * product["quantity"])
                                      * self.importSalesTax)/100
            finalCost = round(
                (product["price"] + totalTaxation) * product["quantity"], 2)
            return {"salesTax": totalTaxation, "finalCost": finalCost}
        else:
            return None


class Shop:
    cart = []
    receiptItems = []

    def __init__(self):
        self.cart = []
        self.receiptItems = []

    def buyItems(self):
        numInputLines = int(input("Enter number of input lines : "))
        lineInputs = []
        for i in range(0, numInputLines):
            lineInputs.append(input(f"Enter Line {i + 1} : "))
        self.cart = lineInputs

    def __decodeLine(self, inputSentence):
        productsDetail = []

        def decodeProductDetails(product):
            try:
                price = inputSentence.lower().split(
                    f"{product['name']} at ")[1].split(" ")[0]
                quantity = re.findall(
                    "[0-9]+", inputSentence.lower().partition(f"{product['name']}")[0])[-1]
            except:
                print(
                    "Cannot find price or quantity for the product, problem in input string.")
                return None

            return {
                "name": product["name"],
                "price": float(price),
                "quantity": int(quantity),
                "isImported": False
            }

        if inputSentence.lower().count("of") > 0:
            for word in inputSentence.lower().split("of"):
                if word.find("at") != -1:
                    name = word.lower().lstrip().split(" at ")[0].strip()
                    if name.find("imported") >= 0:
                        name = name.replace("imported", "").strip()
                    productsDetail.append({
                        "name": name
                    })
        else:
            name = " ".join(re.findall(
                "[a-z]+", inputSentence.lower().split(" at ")[0]))
            productsDetail.append({
                "name": name
            })
        productsDetail = list(map(decodeProductDetails, productsDetail))
        if productsDetail:
            for i in range(0, inputSentence.lower().count("imported")):
                productsDetail[i].update({"isImported": True})

        return productsDetail

    def fetchDetailsForLineItems(self):
        for line in self.cart:
            self.receiptItems.append(self.__decodeLine(line))

    def printCart(self):
        for lineItem in self.cart:
            print(lineItem)

    def printReceipt(self):
        if self.receiptItems[0] != None and self.receiptItems[0][0] != None:
            taxation = Taxations()
            total = 0
            totalSalesTax = 0
            receiptStrings = []
            for listItem in self.receiptItems:
                for item in listItem:
                    taxDetails = taxation.calculateTaxForProduct(item)
                    total += taxDetails["finalCost"]
                    totalSalesTax += taxDetails["salesTax"]
            for cartItem in self.cart:
                tempStr = cartItem
                for listItem in self.receiptItems:
                    for item in listItem:
                        taxDetails = taxation.calculateTaxForProduct(item)
                        tempStr = tempStr.replace(
                            f"{item['price']}", f"{taxDetails['finalCost']}")
                receiptStrings.append(tempStr.strip())
            print("\n\n")
            for receiptString in receiptStrings:
                print(receiptString)

            print(f"Total Sales Tax : {round(totalSalesTax,2)}")
            print(f"Total : {total}")
            print("____________________________________________________")
            print("Your final receipt, Thanks for shopping with US !!")
            print("\n")
        else:
            print(
                "There has been an error , probably input strings format aren't correct!")


def __init__():
    shop = Shop()
    shop.buyItems()
    shop.fetchDetailsForLineItems()
    shop.printReceipt()


__init__()
