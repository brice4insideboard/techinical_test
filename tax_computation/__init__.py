# coding: utf-8

import os
import sys
from abc import ABCMeta
import math
from re import findall, sub
from copy import deepcopy
import unicodedata


class PayStation(object):
    def __init__(self, *args):
        self.total_price = 0.0
        self.total_tax = 0.0
        self.original_list_of_products = args[0]

    def clean_product_description(self):
        """

        :return: None
        """
        list_of_product = deepcopy(self.original_list_of_products)
        for i in range(0, len(self.original_list_of_products)):
            i = 0
            try:
                item = self.original_list_of_products[i]
            except IndexError:
                break
            number_of_occurrence = self.original_list_of_products.count(item)
            total_price = 0
            if number_of_occurrence > 1:
                same_product_list = []
                for duplicate_item in list_of_product:
                    if duplicate_item.product_description == item.product_description:
                        total_price += duplicate_item.price
                        same_product_list.append(duplicate_item)
                total_price = round(total_price, 2)
                remaining_item = same_product_list[0]
                list(map(lambda x: self.original_list_of_products.remove(x), same_product_list))
                list(map(lambda x: list_of_product.remove(x), same_product_list))
            else:
                remaining_item = deepcopy(item)
                total_price += remaining_item.price
                list(map(lambda x: self.original_list_of_products.remove(x), [remaining_item]))
                list(map(lambda x: list_of_product.remove(x), [remaining_item]))
            remaining_item.product_description = remaining_item.product_description[:-1]
            remaining_item.product_description = remaining_item.product_description.replace(findall(r"-?\d+", remaining_item.product_description)[0],
                                                                                            str(number_of_occurrence))
            remaining_item.product_description = sub(pattern="\d+\.\d+",
                                                     repl='',
                                                     string=remaining_item.product_description)
            remaining_item.product_description = remaining_item.product_description[:-2]
            remaining_item.product_description = '{}: {}'.format(remaining_item.product_description,
                                                                 total_price)
            list_of_product.append(remaining_item)

        self.original_list_of_products = list_of_product

    def create_bill(self):
        """Create the final output

        :return: Nothing
        """
        self.clean_product_description()
        list(map(lambda x: print(x.product_description), self.original_list_of_products))  # Print each product description in the given list
        print('Montant des taxes : {}'.format(round(self.total_tax, 2)))
        print('Total : {}'.format(round(self.total_price, 2)))

    def compute_total_price(self):
        """Compute the total price for the given shopping cart

        :return: Nothing
        """
        for item in self.original_list_of_products:
            self.total_price += item.price
        self.total_price = round(self.total_price, 2)

    def compute_taxes(self):
        """Compute taxes for each item in the shopping cart

        :return: Nothing
        """
        for item in self.original_list_of_products:
            final_tax = item.price * round(item.tax, 2)
            fraction, integer = math.modf(final_tax)
            if fraction != 0:
                fraction = fraction + (0.05 - fraction % 0.05)
            fraction = round(fraction, 2)
            final_tax = integer + fraction
            self.total_tax += final_tax
            item.price = item.price + final_tax
            fraction, integer = math.modf(item.price)
            fraction = round(fraction, 2)
            item.price = integer + fraction


class ProductFactory(metaclass=ABCMeta):
    __slots__ = ['price', 'imported', 'tax', 'specials', 'product_description']

    def __init__(self, imported=False, price=0.0, product_line=''):
        self.price = price
        self.imported = imported
        self.tax = 0.05 if imported else 0.0
        self.specials = dict()
        self.product_description = product_line
        file_directory = os.listdir('./specials')
        for files in file_directory:
            with open(file='./specials/{}'.format(files)) as current_file:
                self.specials[files[:-4]] = list(map(lambda s: s.strip(), [word for word in current_file]))  # Remove \n at the end of each word in the file

    def __eq__(self, other):
        """Overrides the basic EQ implementation

        :param other: (object) The object we want self to be compared with
        :return: (bool) True if it's the same object, False otherwise
        """
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__ and self.imported == other.imported
        return False

    @staticmethod
    def create_product(product_class, imported=False, price=0.0, product_description=''):
        """Factory's product creation

        :param product_class: (str) The classname of the desired product
        :param imported: (bool) Is this product is imported
        :param price: (float) Product's price
        :param product_description: (str) Product description
        :return: (object) A new product
        """
        try:
            return globals()[product_class.capitalize()](imported, price, product_description)  # Call the constructor with it's parameters
        except KeyError:
            return globals()['Product'](imported, price, product_description)


class Book(ProductFactory):
    def __init__(self, imported=False, price=0.0, product_description=''):
        super().__init__(imported, price, product_description)


class Food(ProductFactory):
    def __init__(self, imported=False, price=0.0, product_description=''):
        super().__init__(imported, price, product_description)


class Medication(ProductFactory):
    def __init__(self, imported=False, price=0.0, product_description=''):
        super().__init__(imported, price, product_description)


class Product(ProductFactory):
    def __init__(self, imported=False, price=0.0, product_description=''):
        super().__init__(imported, price, product_description)
        self.tax += 0.10


def is_imported(product):
    """Check if the product is imported or not

    :param product: (str) Line containing the product's informations
    :return: (bool) True if imported, False otherwise
    """
    return True if 'import' in product else False


def get_product_category(product, factory_specials):
    """Check for word inside each category in order to create the corresponding object

    :param product: (str) The product description
    :param factory_specials: (dict) Contains names of product per category (key: product, values: names)
    :return: (str) The product category
    """
    for key in factory_specials:
        for item in factory_specials[key]:
            if item in product:
                return key.capitalize()
    return 'Product'


def get_price(product_description):
    """Search float inside a line and return the converted value

    :param product_description: (str)
    :return: (float) The seeked price
    """
    price = findall("\d+\.\d+", product_description)  # Regex: match positive float
    try:
        return float(price[0])
    except IndexError:
        raise ValueError('You need to put a price')


def ascii_uniformization(string):
    """Remove non ascii character in a string and replace them with the most accurate correspondence

    :param string: (str) The string we want to uniformize
    :return: (byte) Byte string without accent
    """
    nfkd_form = unicodedata.normalize('NFKD', string)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii


def context_analysis(text_input):
    """Create list of object depending on the text input (aka shopping cart)

    :param text_input: (TextIOWrapper) The content of the basic shopping cart
    :return: A list which contains all the bought objects (aka shopping cart)
    """

    factory = ProductFactory()
    shopping_cart = []
    for line in text_input:
        if line == '\n' or line == '':
            continue
        try:
            occurrence = int(findall(pattern=r"-?\d+",  # Regex: match positive and negative integer
                                     string=line)[0])
        except IndexError:
            print('{} MUST have number of item'.format(line[:-1]))
        try:
            item_price = float(findall(pattern="[-+]?[0-9]*\.?[0-9]+",  # Regex: match positive and negative float
                                       string=line)[-1])
        except IndexError:
            print('{} MUST have a price'.format(line[:-1]))
            continue
        try:
            if occurrence <= 0 or item_price <= 0:
                raise ValueError
            line = ascii_uniformization(line).decode('utf-8')
            for i in range(0, occurrence):
                shopping_cart.append(factory.create_product(product_class=get_product_category(product=line,
                                                                                               factory_specials=factory.specials),
                                                            imported=is_imported(line),
                                                            price=get_price(line),
                                                            product_description=line))
        except ValueError:
            print("Prices and number of object can't be 0, negative or non-existent")
    return shopping_cart

file_path = os.path.dirname('./files')

if __name__ == '__main__':
    for file in sys.argv[1:]:
        if file.endswith('.txt'):
            try:
                if os.stat('{}/{}'.format(file_path, file)).st_size == 0:
                    print('{} is empty'.format(file))
                with open(file) as current_file:
                    shopping_cart = context_analysis(text_input=current_file)
                pay_station = PayStation(shopping_cart)
                pay_station.compute_taxes()
                pay_station.compute_total_price()
                pay_station.create_bill()
            except FileNotFoundError:
                print("{} doesn't exists.".format(file))
        else:
            print('Your file(s) needs to ends with .txt')
