

import logging

CATALOGUE = {
    'Baked Beans':  0.99, 
    'Biscuits' : 1.20,
    'Sardines' : 1.89,
    'Shampoo (Small)' : 2.00,
    'Shampoo (Medium)' : 2.50,
    'Shampoo (Large)' : 3.50,
}

SPECIAL_OFFERS = {
    'Baked Beans': {'buy' :2, 'free' :1 }, 
    'Sardines': {'discount': 25 },
    'Multiple': {'buy' :3, 'from': ['Shampoo (Small)', 'Shampoo (Medium)','Shampoo (Large)'] , 'free' :1 },
    }

class ShoppingBasket(object):
    def __init__(self, basket={}, catalogue=CATALOGUE, specialoffers=SPECIAL_OFFERS):
        self.basket = basket
        self.catalogue = catalogue 
        self.specialoffers = specialoffers
        self._reset()
        
    def _reset(self):
        self._subtotal = 0.0
        self._discount = 0.0
        self._total = 0.0
        
    def currentvalue(self):
        self._calculate()

        return { 'SubTotal': float(format(self._subtotal , '.2f')),
                 'Discount': float(format(self._discount , '.2f')),
                 'Total':float(format(self._total, '.2f'))}

    def _ordercheapestfirst(self, productlist):
        data = {}
        for product_name in productlist:
            price = self.catalogue[product_name]
            data[price] = data.get(price, []) + [product_name]

        prices = list(data.keys())
        prices.sort()
        result = []
        for price in prices:
            result.extend(data[price])
        return result
    
    def _productdiscount(self, product_name, items, price):
        discount = 0.0 
        if product_name in self.specialoffers:
            offer = self.specialoffers[product_name]
            if 'discount' in offer:
                discount =  price * (offer['discount'] / 100.0) * items
            elif 'free' in offer and 'buy' in offer:
                buy = offer[ 'buy']
                free = offer[ 'free']

                temp = items // (buy + free)
                discount =  price * temp
        return discount
    
    def _multiplediscount(self):
        offer = self.specialoffers['Multiple']
        buy = offer[ 'buy']
        free = offer[ 'free']
        fromset = offer[ 'from']
        subbasket = {product_name: self.basket.get(product_name, 0) for product_name in fromset}
        
        items = sum(list(subbasket.values()))
        temp = items // (buy)

        discount = 0.0
        # order by lowest price first
        applicable_names = self._ordercheapestfirst(fromset)
        while temp > 0: 
            for product_name in applicable_names:
                if subbasket[product_name]:
                   a = subbasket[product_name] - temp
                   price = self.catalogue.get(product_name, 0)
                   if a <= 0: #insufficient at this level
                       discount +=  subbasket[product_name]*price
                       temp -= subbasket[product_name]
                       print('Multiproduct Offer: Free %s x %s' %(product_name, subbasket[product_name]))
                       subbasket[product_name] = 0
                   else:
                       print('Multiproduct Offer: Free %s x %s' %(product_name, temp))
                       discount += temp*price
                       temp = 0
                if not temp:
                    break
        return discount 
        
    def _calculate(self):
        try: 
            #individual products
            for product_name, items in list(self.basket.items()):
                price = self.catalogue.get(product_name, 0)
                self._subtotal += price * items
                # check for special offers specific to product
                discount = self._productdiscount(product_name, items, price)
                self._discount += discount

            # multiple offer products
            if 'Multiple' in self.specialoffers:
                discount = self._multiplediscount()
                self._discount += discount    
            self._discount += 0.00005 # to help with rounding
            
	    #total
            self._total = self._subtotal - self._discount
        except Exception as e:
            logging.exception('Exception caught in  _calculate %s' %(e))
            self._reset()
            raise
            
    
    def additems(self, add_basket={}):
        self._reset()
        for product_name, items in list(add_basket.items()):
            new_items = self.basket.get(product_name, 0) + items
            self.basket[product_name] = new_items

    def removeitems(self, remove_basket={}):
        self._reset()
        for product_name, items in list(remove_basket.items()):
            new_items = self.basket.get(product_name, 0) - items
            if new_items < 0:
                logging.warning(
                    'Request to subtract more than actually is available. Actual: %s Requested: %s' %(self.basket.get(product_name, 0), items)) 
                new_items = 0 
            self.basket[product_name] = new_items   
          
def main():

    ## should be empty 
    sb = ShoppingBasket()
    print(sb.currentvalue())

    ## testing order 
    a = sb._ordercheapestfirst(['Shampoo (Small)', 'Shampoo (Medium)','Shampoo (Large)'])
    print (a)
    a = sb._ordercheapestfirst(['Shampoo (Large)', 'Shampoo (Medium)','Shampoo (Small)'])
    print (a)
    
    ## special order baskets (basket, expected result) 
    test_data = [
        ({'Baked Beans': 4,'Biscuits' : 1}, {'SubTotal': 5.16, 'Discount': 0.99, 'Total': 4.17}),
        ({'Baked Beans': 2,'Biscuits' : 1, 'Sardines': 2}, {'SubTotal': 6.96, 'Discount': 0.95, 'Total': 6.01}),
        ({'Shampoo (Small)':2, 'Shampoo (Medium)':1,'Shampoo (Large)':3}, {'SubTotal': 17.0, 'Discount': 4.0, 'Total': 13.0} ),
        ({'Shampoo (Small)':1, 'Shampoo (Medium)':2,'Shampoo (Large)':3}, {'SubTotal': 17.5, 'Discount': 4.5, 'Total': 13.0})
        ]

    for basket, expected in list(test_data):
        print('Start: Basket: %s Expected: %s' %(basket, expected))
        sb.additems(basket)
        result = sb.currentvalue()
        if result != expected:
            logging.warning('iNCORRECT')
        print('End: Result: %s Expected: %s' %(result, expected))
        sb.removeitems(basket)

# additional work
# do the catalog dictionary in the form {'product_name':'', 'price':222...} so it is more extensible 
# note
# I think the example is wrong for multiproduct offer

if __name__ == '__main__':
    main()
