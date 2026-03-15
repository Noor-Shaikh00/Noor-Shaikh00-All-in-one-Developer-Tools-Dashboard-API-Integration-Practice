import streamlit as st
import requests
import json

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Developer Tools Dashboard", page_icon="🛠️", layout="wide")

# -------------------------------
# Dark / Light Mode Toggle
# -------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False  # default light

st.sidebar.subheader("🌙 Dark / Light Mode")
mode = st.sidebar.checkbox("Dark Mode", value=st.session_state.dark_mode, key="dark_mode_checkbox")
st.session_state.dark_mode = mode  # update session state

# Apply CSS based on mode
if st.session_state.dark_mode:
    st.markdown("""
        <style>
        body {background-color:#0E1117; color:white;}
        .stTextInput>div>div>input {background-color:#1c1c1c; color:white;}
        .stButton>button {background-color:#333333; color:white;}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body {background-color:white; color:black;}
        .stTextInput>div>div>input {background-color:white; color:black;}
        .stButton>button {background-color:#f0f2f6; color:black;}
        </style>
    """, unsafe_allow_html=True)

# -------------------------------
# Title
# -------------------------------
st.title("🛠️ Developer Tools Dashboard")
st.write("Multiple APIs in one dashboard")

# -------------------------------
# Session State
# -------------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# -------------------------------
# Search Bar
# -------------------------------
search = st.text_input("🔎 Search Tool")

if mode:
    st.markdown("""
        <style>
        body {background-color:#0E1117;color:white;}
        </style>
    """, unsafe_allow_html=True)


# -------------------------------
# TOOL 1: JSON Formatter
# -------------------------------
if search == "" or "json" in search.lower():

    st.subheader("📊 JSON Formatter")

    json_input = st.text_area("Paste JSON here")

    if st.button("Format JSON"):

        try:
            parsed = json.loads(json_input)
            formatted = json.dumps(parsed, indent=4)

            st.code(formatted, language="json")

        except:
            st.error("Invalid JSON format")

            if st.button("⭐ Add JSON Formatter to Favorites", key="fav_json"):
             if "JSON Formatter" not in st.session_state.favorites:
              st.session_state.favorites.append("JSON Formatter")


# -------------------------------
# TOOL 2: Crypto Price Tracker
# -------------------------------
if search == "" or "crypto" in search.lower():

    st.subheader("💰 Crypto Price Tracker")

    coin = st.text_input("Enter Coin Name (bitcoin, ethereum)")

    if st.button("Check Crypto Price"):

        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
            data = requests.get(url).json()

            price = data[coin]["usd"]

            st.success(f"{coin.upper()} Price: ${price}")

        except:
            st.error("Crypto not found")


# # -------------------------------
# # TOOL 3: Stock Tracker
# # -------------------------------
# if search == "" or "stock" in search.lower():

#     st.subheader("📈 Stock Price Tracker")

#     symbol = st.text_input("Enter Stock Symbol (AAPL, TSLA)")

#     if st.button("Get Stock Price"):

#         try:
#             url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey=demo"
#             data = requests.get(url).json()

#             price = data[0]["price"]

#             st.success(f"{symbol.upper()} Price: ${price}")

#         except:
#             st.error("Stock not found")


# -------------------------------
# TOOL 4: IP Lookup
# -------------------------------
if search == "" or "ip" in search.lower():

    st.subheader("🌐 IP Lookup")

    ip = st.text_input("Enter IP Address")

    if st.button("Check IP Info"):

        try:
            url = f"http://ip-api.com/json/{ip}"
            data = requests.get(url).json()

            st.write("Country:", data["country"])
            st.write("City:", data["city"])
            st.write("ISP:", data["isp"])

            st.code(json.dumps(data, indent=2), language="json")

        except:
            st.error("Invalid IP Address")



# -------------------------------
# TOOL 5: Programming Joke
# -------------------------------
if search == "" or "joke" in search.lower():

    st.subheader("😂 Programming Joke")

    if st.button("Get Joke"):
        url = "https://official-joke-api.appspot.com/jokes/programming/random"
        data = requests.get(url).json()[0]

        st.info(data["setup"])
        st.success(data["punchline"])

        if st.button("⭐ Add Joke Tool to Favorites"):
            st.session_state.favorites.append("Joke Generator")

        st.code(json.dumps(data, indent=2), language="json")


# -------------------------------
# TOOL 6: GitHub User Search
# -------------------------------
if search == "" or "github" in search.lower():

    st.subheader("👨‍💻 GitHub User Info")

    username = st.text_input("Enter GitHub Username")

    if st.button("Search GitHub"):

        url = f"https://api.github.com/users/{username}"
        data = requests.get(url).json()

        if "login" in data:

            st.image(data["avatar_url"], width=120)

            st.write("Name:", data["name"])
            st.write("Followers:", data["followers"])
            st.write("Public Repos:", data["public_repos"])

            if st.button("⭐ Add GitHub Tool to Favorites"):
                st.session_state.favorites.append("GitHub Search")

            st.code(json.dumps(data, indent=2), language="json")

        else:
            st.error("User not found")


# -------------------------------
# TOOL 7: Weather
# -------------------------------
if search == "" or "weather" in search.lower():

    st.subheader("🌦️ Weather Info")

    city = st.text_input("Enter City")

    if st.button("Check Weather"):

        api = f"https://wttr.in/{city}?format=j1"
        data = requests.get(api).json()

        temp = data["current_condition"][0]["temp_C"]
        desc = data["current_condition"][0]["weatherDesc"][0]["value"]

        st.success(f"Temperature: {temp}°C")
        st.write("Condition:", desc)

        if st.button("⭐ Add Weather Tool to Favorites"):
            st.session_state.favorites.append("Weather Tool")

        st.code(json.dumps(data, indent=2), language="json")


# -------------------------------
# TOOL 8: Tech News
# -------------------------------
if search == "" or "news" in search.lower():

    st.subheader("📰 Tech News")

    url = "https://hn.algolia.com/api/v1/search?query=technology"
    data = requests.get(url).json()

    for news in data["hits"][:5]:
        st.write("🔹", news["title"])


# -------------------------------
# Favorites Section
# -------------------------------
st.sidebar.subheader("⭐ Favorite Tools")

for tool in st.session_state.favorites:
    st.sidebar.write("⭐", tool)


# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("### 🚀 Developed by Noor Shaikh")