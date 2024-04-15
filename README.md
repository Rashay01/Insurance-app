# Sanlam Platinum Plus Insurance

# Setup

1. One can run the `create_tables.sql` file to create the tables in the database as well as get some dummy data.
2. Run `pip install -r requirements.txt` to get all the dependencies installed
3. In the `.env` add the database connection with the variable name `AZURE_CONNECTION_URL` and the secret key with `FORM_SECRET_KEY`
4. Run `flask run` to run the app

## Sanlam Platinum Plus Insurance
On conducting desktop insurance research it was identified that there is very limited insurance cover for luxury, top-end, valuable, rare, antique and sentimental-valued products and possessions. If this type of insurance was available, it is not well publicized and generally falls under the specified items insurance for home contents or personal insurance.

Thus, we identified a gap in the market for a company to focus pre-dominantly only on insurance for these type of luxury, rare products, antiques and highly expensive products.
So, the idea of Sanlam Platinum Plus was born. The idea to link this to a well-known brand such a Sanlam to provide the trust, reliability and good reputation, that focusses predominantly only on these luxury products was initiated.
We had to clarify and define what the luxury/antique/rare/high-valued insurable product was focussed upon. In this regard, we choose to focus on items that are not necessary for living but are deemed as highly desirable within a culture or society. We further decided that a luxury item insurance policy may cover high-value items like jewelry, art, including high-end automobiles and yachts but also services, such as full-time or live-in chefs and housekeepers.

Luxury items are considered elite in a particular society and are typically high-quality, rare, and require more resources to produce than non-luxury items. Examples of luxury items include:

- High-end watches and jewelry
- Designer clothing and shoes
- High-end cars
- Yachts
- Private jets
- Country club memberships
- Landscaping services
- Expensive real estate

We decided to develop a web-based Insurance Policy Management System (IPMS) application that will form part of the Sanlam Insurance offerings. It was decided to call it Sanlam Platinum Plus as we wanted to show the relationship with Sanlam but to differentiate it to focus on top-end products as defined above.

This web-based application had to be user friendly, intuitive for all users or people looking to ensure these high-end products and had to have a Premium ‘look and feel’.

We also wanted to have the core features of :

- User Registration and authentication
- Policy management (able to Create, Read, Update, and when the client wants to delete a policy then the status of the policy will change as we intend to keep all transaction history)
- Customer management (able to Add, Update, and prevented a customer from deleting their information because we wanted to store all historical information)
- Claim processing (able to create a claim for an existing policy and track the status of the claim, which can be Received, under Investigation, Declined or Approved)
- Although specific reporting and analytics has not been catered for, a user/customer can list all quotations, policies and claims made.

As a Proof Of Concept (POC) and to develop a Minimum Viable Product (MVP) we decided to focus upon developing the functionality for the luxury product categories of Classic Cars and Jewelry as a point of departure. When the POC and MVP have been approved past the User Acceptance Test (UAT) and complete testing, all the other luxury product categories will be added on.

As further enhancements the intention is to include a module to the web-application to cater for reporting and analytics, and to provide for the approval workflow for claims processing. API Authentication and Authorization will also be catered for going forward.

With regards to the choice of the technology stack, we used Python as the programming language, together with Flask (including Flask-WTF, Flask-Login, Flask-SQLAlchemy) to showcase a full-stack developer approach from server-side logic with Flask to database interactions and RESTful API services. We used Jinja2 templates to render responsive HTML pages. CSS was used to style the HTML pages using Bootstrap which contained the JavaScript to enhance the user interface.

## REST API's documentation

[documentation](https://documenter.getpostman.com/view/33636476/2sA3Bj7tKf)

It is also in the postman collection file with the name `Insurance App (IPMS).postman_collection.json`






Note: The test users password is `password` and the ID number is `0101165412342`

## Design process:

- a basic wire frame was conducted in [figma basic wire frame](https://www.figma.com/file/o1jrudMDK24V6NuATfFBB1/Untitled?type=design&node-id=0%3A1&mode=design&t=LiqwcPvkY29EzjV5-1)
- Designed a ERD :
![ERD Diagram](./ERD%20diagram.png "ERD Diagram")
