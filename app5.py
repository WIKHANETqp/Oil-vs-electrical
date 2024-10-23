import streamlit as st
import base64
import requests

# Function to add background image from URL
def add_bg_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = base64.b64encode(response.content).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{image_data}");
                background-size: cover;
            }}
            .stTextInput, .stNumberInput, .stSelectbox {{
                background-color: rgba(255, 255, 255, 0.8);
                padding: 10px;
                border-radius: 10px;
            }}
            .result-box {{
                background-color: rgba(255, 255, 255, 0.8);
                padding: 10px;
                border-radius: 10px;
                margin: 10px 0;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("Failed to load the background image.")

# Main app logic
def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'

    if st.session_state['page'] == 'home':
        home_page()
    elif st.session_state['page'] == 'comparison':
        comparison_page()

# Function to get fuel prices (mockup example)
def get_fuel_prices(fuel_type):
    prices = {
        "Gasohol 91": 40.50,
        "Gasohol 95": 41.00,
        "E20": 35.00,
        "E85": 30.00,
        "Benzene": 45.00,
        "Diesel": 32.00
    }
    return prices.get(fuel_type, 0)

# Home page: Button to start comparison between electric and gasoline vehicles
def home_page():
    st.title("รถที่ใช้น้ำมัน vs รถใช้ไฟฟ้า")
    st.write("เปรียบเทียบประสิทธิภาพและค่าใช้จ่ายระหว่าง รถไฟฟ้า และ รถใช้น้ำมัน")

    if st.button('คำนวณรถที่ใช้น้ำมัน vs รถใช้ไฟฟ้า'):
        st.session_state['page'] = 'comparison'

# Comparison page: Car selection and input for both electric and gasoline vehicles
def comparison_page():
    st.title("เปรียบเทียบ รถไฟฟ้า vs รถใช้น้ำมัน")

    col1, col2 = st.columns(2)

    # Select EV Car Brand and Model
    with col1:
        st.header("รถใช้ไฟฟ้า")
        ev_car_brand = st.selectbox("เลือกยี่ห้อรถไฟฟ้า", ["BYD", "Tesla", "MG", "ORA"])
        ev_car_model = st.selectbox("เลือกรุ่นรถไฟฟ้า", ["Atto 3", "Model Y", "MG ZS EV", "Good Cat"])

        ev_speed = st.number_input("กรอกความเร็วปกติของรถ (กม./ชม.)", min_value=0.0, key="ev_speed")
        ev_distance = st.number_input("กรอกระยะทางที่เดินทาง (กม.)", min_value=0.0, key="ev_distance")
        electricity_price = st.number_input("กรอกราคาค่าไฟฟ้า (บาท/kWh)", min_value=0.0, key="electricity_price")

    # Select Gasoline Car Brand and Model
    with col2:
        st.header("รถใช้น้ำมัน")
        gas_car_brand = st.selectbox("เลือกยี่ห้อรถน้ำมัน", ["Honda", "Mazda", "Isuzu"])
        gas_car_model = st.selectbox("เลือกรุ่นรถน้ำมัน", ["Civic", "Mazda 2", "D-Max"])

        fuel_type = st.selectbox("เลือกประเภทน้ำมัน", ["Gasohol 91", "Gasohol 95", "E20", "E85", "Benzene", "Diesel"])
        fuel_price = get_fuel_prices(fuel_type)
        st.write(f"ราคาน้ำมันที่เลือก: {fuel_price:.2f} บาท/ลิตร")

        gas_speed = st.number_input("กรอกความเร็วปกติของรถ (กม./ชม.)", min_value=0.0, key="gas_speed")
        gas_distance = st.number_input("กรอกระยะทางที่เดินทาง (กม.)", min_value=0.0, key="gas_distance")

    # Perform calculation and comparison
    if st.button("คำนวณ"):
        # EV calculation
        ev_efficiency = ev_distance / 420 if ev_distance > 0 else 0  # Example
        ev_total_cost = ev_efficiency * ev_distance * electricity_price if ev_distance > 0 else 0

        # Gasoline calculation
        gas_efficiency = gas_distance / 15 if gas_distance > 0 else 0  # Example
        gas_total_cost = gas_efficiency * fuel_price if gas_distance > 0 else 0

        # Display results side by side
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("ผลลัพธ์รถไฟฟ้า")
            st.markdown(
                f"<div class='result-box'>ประสิทธิภาพ: {ev_efficiency:.2f} kWh/กม.<br>ค่าใช้จ่ายรวม: {ev_total_cost:.2f} บาท</div>", 
                unsafe_allow_html=True
            )

        with col2:
            st.subheader("ผลลัพธ์รถใช้น้ำมัน")
            st.markdown(
                f"<div class='result-box'>ประสิทธิภาพ: 15 กม./ลิตร<br>ค่าใช้จ่ายรวม: {gas_total_cost:.2f} บาท</div>", 
                unsafe_allow_html=True
            )

    # Go back button
    if st.button("กลับไปหน้าหลัก"):
        st.session_state['page'] = 'home'

# Run the app
if __name__ == '__main__':
    add_bg_from_url('https://images-storage.thaiware.site/tips/2020_11/images/1433_20111714250002_67.png')  # Set background from URL
    main()
