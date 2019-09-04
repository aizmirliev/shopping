## Documentation



shopping basket class. 
It provides the caller with the ability to calculate the metrics (total, subtotal and discount) for the current state of it (based pn the input parameters (catalogue and special offers) and the ability to change its internal state by adding to or removing from the basket. For simplicity  are amalgamated into add/remove basket sets. 
the main function is a test driver for creation of basket objects and demonstration of some of the basket functionality and the examples in the description.

The internal calculation of the metrics
The coder has viewed the special offers into two categories - per product and per combination of products, naming the latter 'multiple' for the lack of a better choice at the time.

The former is straightforward, applying the discount in the sub-total loop. The processing logic is in the _productdiscount() member function. 

The latter is also implemented into a separate method, _multiplediscount(). It constructs a subset of the actual basket comprising the items relevant for that offer and the to determine how many of these should be free, starting from the cheapest ones first progressively working towards the more expensive.    
 

Further improvement suggestions: 
1. Change the catalogue dictionary from the current product_name:price which is limited to key/value pairs which are more informative and extensible in terms of adding more properties. 
2. The offers are coded in a way to retain their meaning and still easier to process, without loss of generality. If however natural language wording is required, then additional parsing should be implemented.
3, try/except block is a simplistic view intended to catch all exeptions. These could be re-raised to inform calling modules and exceptions could be more specialized.    

