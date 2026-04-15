# Hungry-Burger

- In order to get started, install every package which is needed in the project, go to the terminal and paste the following:\
 `pip install -r requirements.txt`

- If anyone installs a package which will be used to run the website, paste the following in the terminal:\
  `pip freeze > requirements.txt`

- Two commands to share data
`./manage.py dumpdata`

1. Essential Operational Models
These are the most important for the day-to-day running of the restaurant:

Order: This is where the manager will see incoming requests, total amounts, and which customer placed the order.

OrderStatus: You need this registered so you can define the different stages of an order (e.g., "Received", "In Kitchen", "Ready for Pickup") as suggested by your professor.

RestaurantTable: Register this so the manager can manage the physical tables where customers sit.

2. Menu Management Models
These allow the manager to fulfill the "admin side" requirement of adding, removing, and editing items:

Product: To manage individual burgers, sides, and drinks.

Category: To organize the menu (e.g., Burgers, Drinks, Desserts).

OptionGroup: To manage sets of choices like "Choose your sauce" or "Select your bun".

Option: To manage the actual items within those groups, such as "Ketchup," "Mayonnaise," or "Gluten-free bun".

3. Record-Keeping Models (Secondary)
These are useful for the manager to review what was actually sold, including the price "snapshots":

OrderItem: To see exactly which products were part of which order.

OrderItemOption: To see the specific customizations (like "Extra Bacon") and the price charged at that moment.