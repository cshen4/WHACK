# MeetingtheDemand
Handles requests via SMS for Partners in Health

Due to the lack of technological infrastructure in many countries that Partners in Health support, there is an inaccurate flow of information regarding the demand os medical supplies

The purpose of this program is to determine the true demand to avoid stocks outs and under ordering.

How it works:
1. Clients (locations with little access to internet) texts the product SKU and the quantity of the product needed to a Twilio number
2. List of all products that a client requests is visible through a website that the Admin can use to determine which items are in demand
3. Admin (Partners in Health) confirms the shipment of the product by entering on the website the amount of product sent
4. Twilio responds back to client to confirm the order

Utilizes Vertica database and the twilio api to enable the client and admin to have direct, organized contact regarding the demand of different medical products.
