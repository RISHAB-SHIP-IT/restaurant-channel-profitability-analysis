import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("restaurant_data.csv")

df["InStoreRevenue"] = df["InStoreOrdersCount"] * df["AOV"]
df["UberEatsRevenue"] = df["UberEatsOrdersCount"] * df["AOV"]
df["DoorDashRevenue"] = df["DoorDashOrdersCount"] * df["AOV"]
df["SelfDeliveryRevenue"] = df["SelfDeliveryOrdersCount"] * df["AOV"]

df["SD_DeliveryTotalCost"] = df["SelfDeliveryOrdersCount"] * df["DeliveryCostOrder"]

df["InStoreNetProfit"] = df["InStoreRevenue"] * (1 - df["COGSRate"] - df["OPEXRate"])

df["UberEatsNetProfit"] = df["UberEatsRevenue"] * (1 - df["COGSRate"] - df["OPEXRate"] - df["CommissionRate"])

df["DoorDashNetProfit"] = df["DoorDashRevenue"] * (1 - df["COGSRate"] - df["OPEXRate"] - df["CommissionRate"])

df["SelfDeliveryNetProfit"] = (df["SelfDeliveryRevenue"] * (1 - df["COGSRate"] - df["OPEXRate"]) - df["SD_DeliveryTotalCost"])

st.title("Restaurant Channel Profitability Analysis")

st.write("This dashboard analyzes profitability across InStore, UberEats, DoorDash and SelfDelivery channels")

st.subheader("Dataset Preview")
st.dataframe(df)

st.subheader("Channel-wise Net Profit Comparison")

profit_data = df[["InStoreNetProfit","UberEatsNetProfit","DoorDashNetProfit","SelfDeliveryNetProfit"]].sum()

fig1 = px.bar(x=profit_data.index,y=profit_data.values,labels={"x":"Channel","y":"Net Profit"},title="Total Profit by Channel")

st.plotly_chart(fig1)

st.subheader("Channel Margin Efficiency")

df["InStoreMargin"] = df["InStoreNetProfit"] / df["InStoreRevenue"]
df["UberMargin"] = df["UberEatsNetProfit"] / df["UberEatsRevenue"]
df["DoorDashMargin"] = df["DoorDashNetProfit"] / df["DoorDashRevenue"]
df["SelfDeliveryMargin"] = df["SelfDeliveryNetProfit"] / df["SelfDeliveryRevenue"]

margin_values = [
df["InStoreMargin"].mean(),
df["UberMargin"].mean(),
df["DoorDashMargin"].mean(),
df["SelfDeliveryMargin"].mean()
]

channels = ["InStore","UberEats","DoorDash","SelfDelivery"]

fig2 = px.bar(x=channels,y=margin_values,title="Average Margin by Channel")

st.plotly_chart(fig2)

st.subheader("Cost Structure Breakdown")

costs = {
"COGS":df["COGSRate"].mean(),
"OPEX":df["OPEXRate"].mean(),
"Commission":df["CommissionRate"].mean(),
"Delivery Cost":df["DeliveryCostOrder"].mean()
}

fig3 = px.pie(names=list(costs.keys()),values=list(costs.values()),title="Average Cost Distribution")

st.plotly_chart(fig3)

st.subheader("Cuisine Profitability Heatmap")

pivot = df.pivot_table(values="InStoreNetProfit",index="CuisineType",columns="Segment",aggfunc="mean")

fig, ax = plt.subplots()

sns.heatmap(pivot,annot=True,cmap="coolwarm",ax=ax)

st.pyplot(fig)
