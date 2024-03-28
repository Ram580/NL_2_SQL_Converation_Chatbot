examples = [
  {
      "input": "List all customers in France with a credit limit over 20,000.",
      "query": "SELECT * FROM customers WHERE country = 'France' AND creditLimit > 20000;"
  },
  {
      "input": "Get the highest payment amount made by any customer.",
      "query": "SELECT MAX(amount) FROM payments;"
  },
  {
      "input": "Show product details for products in the 'Motorcycles' product line.",
      "query": "SELECT * FROM products WHERE productLine = 'Motorcycles';"
  },
  {
      "input": "Retrieve the names of employees who report to employee number 1002.",
      "query": "SELECT firstName, lastName FROM employees WHERE reportsTo = 1002;"
  },
  {
      "input": "List all products with a stock quantity less than 7000.",
      "query": "SELECT productName, quantityInStock FROM products WHERE quantityInStock < 7000;"
  },
  {
    'input':"what is price of `1968 Ford Mustang`",
    "query": "SELECT `buyPrice`, `MSRP` FROM products  WHERE `productName` = '1968 Ford Mustang' LIMIT 1;"   
  }, 
  {
    "input": "List products sold by order date.",
    "query": "SELECT productName , orderDate , DAYNAME(orderDate) AS 'DayName' FROM products INNER JOIN orderdetails ON products.productCode = orderdetails.productCode INNER JOIN Orders ON orderdetails.orderNumber = orders.orderNumber WHERE DAYNAME(Orders.orderDate) = 'MONDAY';"
  },
  {
    "input": "List the order dates in descending order for orders for the 1940 Ford Pickup Truck.",
    "query": "SELECT DISTINCT(products.productName), orders.orderDate FROM orders JOIN orderdetails ON orderdetails.orderNumber = orders.orderNumber JOIN products ON orderdetails.productCode = products.productCode WHERE productName = '1940 Ford Pickup Truck' ORDER BY orderDate DESC;"
  },
  {
    "input": "List the names of customers and their corresponding order number where a particular order from that customer has a value greater than $25,000.",
    "query": "SELECT customers.customerName, orders.orderNumber, SUM(orderdetails.priceEach * orderdetails.quantityOrdered) AS tot_value FROM customers JOIN orders ON customers.customerNumber = orders.customerNumber JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber GROUP BY customers.customerName, orders.orderNumber HAVING tot_value > 25000 ORDER BY customers.customerName;"
  },
  {
    "input": "For orders containing more than two products, report those products that constitute more than 50% of the value of the order.",
    "query": "SELECT orderNumber, productName, ProductsCount ,contribution FROM (SELECT orderNumber, productCode, (SELECT Count(*) FROM orderdetails WHERE OrderNumber = Main.orderNumber) As 'ProductsCount', quantityOrdered*priceEach As 'Product Value', (quantityOrdered*priceEach / (SELECT SUM(quantityOrdered*priceEach) FROM orderdetails WHERE orderNumber = Main.orderNumber ))*100 As 'Contribution' FROM orderdetails Main ORDER BY orderNumber) DataTable INNER JOIN Products ON Products.productCode = DataTable.productCode WHERE ProductsCount > 2 AND Contribution > 50;"
  },
  {
    "input": "List all the products purchased by Herkku Gifts.",
    "query": "SELECT productName FROM products INNER JOIN orderdetails od on products.productCode = od.productCode INNER JOIN orders o on od.orderNumber = o.orderNumber INNER JOIN customers c on o.customerNumber = c.customerNumber WHERE c.customerName = 'Herkku Gifts';"
  },
  {
    "input": "Find products containing the name 'Ford'.",
    "query": "SELECT productName AS 'Products' FROM Products WHERE productName LIKE '%Ford%';"
  },
  {
    "input": "List products ending in 'ship'.",
    "query": "SELECT productName FROM products WHERE productName LIKE '%ship';"
  },
  {
    "input": "Report the number of customers in Denmark, Norway, and Sweden.",
    "query": "SELECT customerName FROM Customers WHERE country IN ('Denmark','Norway','Sweden');"
  },
  {
    "input": "What are the products with a product code in the range S700_1000 to S700_1499",
    "query": "SELECT productCode,productName FROM Products WHERE RIGHT(productCode,4) BETWEEN 1000 AND 1499 ORDER BY RIGHT(productCode,4);"
  },
  {
    "input": "Which customers have a digit in their name?",
    "query": "SELECT customerName FROM Customers WHERE customerName RLIKE '[0-9]';"
  },
  {
    "input": "List the names of employees called Dianne or Diane.",
    "query": "SELECT CONCAT(firstName,' ',lastName) AS 'Employee Name' FROM Employees WHERE lastName RLIKE 'Dianne|Diane' OR firstName RLIKE 'Dianne|Diane';"
  },
  {
    "input": "List the products containing ship or boat in their product name.",
    "query": "SELECT productName FROM Products WHERE productName RLIKE 'ship|boat';"
  },
  {
    "input": "List the products with a product code beginning with S700.",
    "query": "SELECT productCode, productName FROM Products WHERE productCode LIKE 'S700%';"
  },
  {
    "input": "Find products containing the name 'Ford'.",
    "query": "SELECT productName As 'Products' FROM Products WHERE productName LIKE '%Ford%';"
  },
  {
    "input": "List products ending in 'ship'.",
    "query": "SELECT productName FROM products WHERE productName LIKE '%ship';"
  },
  {
    "input": "Report the number of customers in Denmark, Norway, and Sweden.",
    "query": "SELECT customerName FROM Customers WHERE country IN ('Denmark','Norway','Sweden');"
  },
  {
    "input": "what is the minimum payment received ?",
    "query": "SELECT min(amount) As 'Minimum Payment' FROM payments;"
  }
]

from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
# Access the value of Huggingface_API_KEY
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
embeddings = HuggingFaceEmbeddings(huggingfacehub_api_token=HF_API_TOKEN,model_name="sentence-transformers/all-MiniLM-L6-v2")

@st.cache_resource
def get_example_selector():
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        embeddings,
        Chroma,
        k=2,
        input_keys=["input"],
    )
    return example_selector