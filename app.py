import streamlit as st
import requests

def getAllBookstore():
    url = "https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=M"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    res = response.json()
    return res

def getCountyOption(data):
    optlist = []
    for d in data:
        cn = d["cityName"].split()
        if cn[0] in optlist:
            continue
        optlist.append(cn[0])
    return optlist

def getDistrictOption(data, county):
    optlist = []
    for d in data:
        if d["cityName"].strip()[:3] == county:
            dis = d["cityName"].strip()[5:]
            if len(dis) == 0:
                continue
            if dis in optlist:
                continue
            optlist.append(dis)
    return optlist

def getSpecificBookstore(data, county, district):
    sbs = []
    for d in data:
        if d["cityName"].strip()[:3] != county:
            continue
        if d["cityName"].strip()[5:] in district:
            if d in sbs:
                continue
            sbs.append(d)
    return sbs

def getBookstoreInfo(data):
    elist = []
    for d in data:
        expander = st.expander(d["name"])
        expander.image(d["representImage"])
        expander.metric("hitRate", d["hitRate"])
        expander.subheader("Introduction")
        st.write(d["Introduction"])
        expander.subheader("Address")
        st.write(d["Address"])
        expander.subheader("Open Time")
        st.write(d["Open Time"])
        expander.subheader("Email")
        st.write(d["Email"])
        elist.append(expander)
    return elist

def app():
    bookstorelist = getAllBookstore()
    st.header("特色書店地圖")
    st.metric("Total bookstore", len(bookstorelist))
    county = st.selectbox("請選擇縣市", getCountyOption(bookstorelist))
    district = st.multiselect("請選擇區域", getDistrictOption(bookstorelist, county))
    specificbookstore = getSpecificBookstore(bookstorelist, county, district)
    num = len(specificbookstore)
    st.write(f"總共有{num}項結果", num)
    specificbookstore.sort(key = lambda x:x["hitRate"])
    bookstoreinfo = getBookstoreInfo(specificbookstore)


if __name__ == "__main__":
    app()
