
import streamlit as st
from abc import ABC, abstractmethod

st.set_page_config(
    page_title="Food Delivery Management",
    layout="wide"
)


class Food:

    def __init__(self, food_id, name, price):
        self.food_id = food_id
        self.name = name
        self.price = price


class Order:

    def __init__(self, customer, food, quantity):
        self.customer = customer
        self.food = food
        self.quantity = quantity
        self.total = food.price * quantity


class Person:

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone


class Customer(Person):

    def __init__(self, name, phone, balance):
        super().__init__(name, phone)
        self.__balance = balance

    def get_balance(self):
        return self.__balance

    def add_money(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False

    def make_payment(self, amount):
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
            return True
        return False


class DeliveryPartner(Person):

    def __init__(self, name, phone, vehicle):
        super().__init__(name, phone)
        self.vehicle = vehicle


class Payment(ABC):

    @abstractmethod
    def pay(self, amount):
        pass


class UpiPayment(Payment):

    def pay(self, amount):
        return f"Rs. {amount} paid successfully using UPI"


class CardPayment(Payment):

    def pay(self, amount):
        return f"Rs. {amount} paid successfully using Card"


class CashPayment(Payment):

    def pay(self, amount):
        return f"Rs. {amount} will be paid using Cash on Delivery"


foods = [
    Food(1, "Pizza", 199),
    Food(2, "Burger", 99),
    Food(3, "Biryani", 249),
    Food(4, "Sandwich", 120),
    Food(5, "Fried Rice", 180)
]


if "customer" not in st.session_state:
    st.session_state.customer = Customer("Gokul", "9876543210", 1000)

if "delivery_partner" not in st.session_state:
    st.session_state.delivery_partner = DeliveryPartner(
        "Ravi", "9876543211", "Bike"
    )

if "orders" not in st.session_state:
    st.session_state.orders = []

if "payments" not in st.session_state:
    st.session_state.payments = []

customer = st.session_state.customer
delivery_partner = st.session_state.delivery_partner


st.title("Food Delivery Management System")
st.write(f"Welcome, {customer.name}")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a page",
    [
        "Dashboard",
        "Food Menu",
        "Customers",
        "Orders",
        "Payments",
        "Delivery"
    ]
)


if page == "Dashboard":

    st.header("Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Food Items", len(foods))
    col2.metric("Total Orders", len(st.session_state.orders))
    col3.metric("Wallet Balance", f"Rs. {customer.get_balance()}")

    st.subheader("Welcome to Food Delivery Management")


elif page == "Food Menu":

    st.header("Available Food")

    for food in foods:
        with st.container(border=True):
            st.subheader(food.name)
            st.write(f"Price: Rs. {food.price}")


elif page == "Customers":

    st.header("Customer Management")

    st.write("Customer Name:", customer.name)
    st.write("Phone Number:", customer.phone)

    st.subheader("Wallet Management")

    st.metric("Wallet Balance", f"Rs. {customer.get_balance()}")

    amount = st.number_input(
        "Enter amount to add",
        min_value=0,
        step=100,
        key="wallet_add"
    )

    if st.button("Add Money"):
        if customer.add_money(amount):
            st.success("Money added successfully!")
            st.rerun()
        else:
            st.warning("Enter an amount greater than zero.")


elif page == "Orders":

    st.header("Order Management")

    selected_food = st.selectbox(
        "Select Food",
        foods,
        format_func=lambda food: f"{food.name} - Rs. {food.price}"
    )

    quantity = st.number_input(
        "Enter Quantity",
        min_value=1,
        step=1
    )

    total = selected_food.price * quantity

    st.write(f"Total Amount: Rs. {total}")

    if st.button("Place Order"):

        order = Order(customer, selected_food, quantity)

        st.session_state.orders.append(order)

        st.success("Order placed successfully!")

    st.subheader("Order History")

    for index, order in enumerate(st.session_state.orders, start=1):
        st.write(
            f"{index}. {order.food.name} | "
            f"Quantity: {order.quantity} | "
            f"Total: Rs. {order.total}"
        )


elif page == "Payments":

    st.header("Payment Management")

    if not st.session_state.orders:
        st.info("Please place an order first.")

    else:

        order_options = [
            f"Order {i + 1} - {order.food.name} - Rs. {order.total}"
            for i, order in enumerate(st.session_state.orders)
        ]

        selected_index = st.selectbox(
            "Select Order",
            range(len(order_options)),
            format_func=lambda index: order_options[index]
        )

        order = st.session_state.orders[selected_index]

        payment_type = st.selectbox(
            "Select Payment Method",
            ["UPI", "Card", "Cash on Delivery"]
        )

        if st.button("Make Payment"):

            if payment_type == "UPI":
                payment = UpiPayment()

            elif payment_type == "Card":
                payment = CardPayment()

            else:
                payment = CashPayment()

            if payment_type == "Cash on Delivery":
                result = payment.pay(order.total)
                st.session_state.payments.append(result)
                st.success(result)

            elif customer.make_payment(order.total):
                result = payment.pay(order.total)
                st.session_state.payments.append(result)
                st.success(result)
                st.rerun()

            else:
                st.error("Insufficient wallet balance. Please add money.")

    st.subheader("Payment History")

    for payment in st.session_state.payments:
        st.write(payment)


elif page == "Delivery":

    st.header("Delivery Management")

    st.write("Delivery Partner:", delivery_partner.name)
    st.write("Phone:", delivery_partner.phone)
    st.write("Vehicle:", delivery_partner.vehicle)

    st.success("Delivery Partner Available")
