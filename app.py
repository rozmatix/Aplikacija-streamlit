import streamlit as st
import statistics
import matplotlib.pyplot as plt
import numpy as np
from csv import DictReader
from statistics import mean
from datetime import datetime
import collections

st.set_page_config(layout="wide")

np.set_printoptions(suppress=True)
ocene = np.loadtxt('./podatki/ml-latest-small/ratings.csv', delimiter=',',skiprows=1)
reader = DictReader(open('./podatki/ml-latest-small/movies.csv','rt',encoding='utf-8'))
i=0
filmi=[]
for row in reader:
    filmi.append([row["movieId"],row["title"],row["genres"]])

filmi = np.array(filmi)

naj10 = []


for film in filmi:
    m = ocene[ (np.float64(film[0])==ocene[:,1]) ]
    if len(m)>=100:
        naj10.append(np.append(film,[mean(m[:,2]),len(m)]))
        

naj10 = np.array(naj10)
naj10 = naj10[naj10[:, 3].argsort()[::-1]][:10]

st.markdown("## 10 najbolj ocenjenih filmov")
st.dataframe(naj10)


st.markdown("## Prikaz filmov")


st.markdown("### izberi minimalno stevilo ocen")
minOcen = st.number_input(label="",step=1,min_value=1)



st.markdown("### izberi zanr")

zanrcheck = st.checkbox("Ne uporabljaj zanra")

zanr  = st.selectbox(
    "",
    ("Action","Adventure","Animation","Children\'s","Comedy","Crime","Documentary","Drama","Fantasy","Film-Noir","Horror","Musical","Mystery","Romance","Sci-Fi","Thriller","War","Western","(no genres listed)")
)

st.markdown("### izberi leto")
letocheck = st.checkbox("Ne uporabljaj leta")
leto = st.number_input(label="",step=1,min_value=1900,max_value=2025)

filmFilter = []

def represents_int(s):
    try: 
        int(s)
    except ValueError:
        return False
    else:
        return True
if st.button("prikazi filme", type="tertiary"):
    for film in filmi:
        m = ocene[ (np.float64(film[0])==ocene[:,1]) ]
        z = set(film[2].split('|'))
        l = film[1].split('(')[-1].split(')')[0].replace("-", "")
        if represents_int(l):
            l = int(l)
        else:
            l = 0

        if len(m)>=minOcen and (zanrcheck or zanr in z) and (letocheck or l==leto):
            filmFilter.append(np.append(film,[mean(m[:,2]),len(m)]))

    filmFilter = np.array(filmFilter)
    filmFilter = filmFilter[filmFilter[:, 3].argsort()[::-1]]
    st.dataframe(filmFilter)

st.markdown("## Primerjalnik filmov")

film1  = st.selectbox(
    "izberi 1. film za primerjavo",
    (filmi[:,1])
)
film2  = st.selectbox(
    "izberi 2. film za primerjavo",
    (filmi[:,1])
)

if st.button("primerjaj filma", type="tertiary"):

    film1id = filmi[ (film1==filmi[:,1]) ][0][0]
    film2id = filmi[ (film2==filmi[:,1]) ][0][0]

    ocenefilm1 = ocene[ (np.float64(film1id)==ocene[:,1]) ]
    ocenefilm2 = ocene[ (np.float64(film2id)==ocene[:,1]) ]

    stOcen1 = len(ocenefilm1)
    avgOcen1 = mean(ocenefilm1[:,2])
    divOcen1 = statistics.stdev(ocenefilm1[:,2])
    stOcen2 = len(ocenefilm2)
    avgOcen2 = mean(ocenefilm2[:,2])
    divOcen2 = statistics.stdev(ocenefilm2[:,2])

    ocenePoLetih1 = dict()
    for ocena in ocenefilm1:
        letoOc = datetime.strftime(datetime.fromtimestamp(ocena[3]), '%Y')
        if not ocenePoLetih1.get(letoOc):
            ocenePoLetih1[letoOc]=[]
        ocenePoLetih1[letoOc].append(ocena[2])

    stOcenPoLetih1 = dict()
    avgOcenPoLetih1 = dict()

    for letoOc in ocenePoLetih1:
        stOcenPoLetih1[letoOc]= len(ocenePoLetih1[letoOc])
        avgOcenPoLetih1[letoOc]= mean(ocenePoLetih1[letoOc])
    
    oceneNames1, oceneCount1 = np.unique(ocenefilm1[:,2], return_counts=True)

    ocenePoLetih2 = dict()
    for ocena in ocenefilm2:
        letoOc = datetime.strftime(datetime.fromtimestamp(ocena[3]), '%Y')
        if not ocenePoLetih2.get(letoOc):
            ocenePoLetih2[letoOc]=[]
        ocenePoLetih2[letoOc].append(ocena[2])

    stOcenPoLetih2 = dict()
    avgOcenPoLetih2 = dict()

    for letoOc in ocenePoLetih2:
        stOcenPoLetih2[letoOc]= len(ocenePoLetih2[letoOc])
        avgOcenPoLetih2[letoOc]= mean(ocenePoLetih2[letoOc])
    
    oceneNames2, oceneCount2 = np.unique(ocenefilm2[:,2], return_counts=True)

    col1,col2 = st.columns(2)
    with col1:
        st.write("podatki za: ",film1)
        st.write("povprecna ocena: ",avgOcen1,"stevilo ocen: ",stOcen1,"standardni odklon ocen: ",divOcen1)
        plt.figure(figsize=(18, 4))
        ax = plt.gca()
        ax.set_xticks(np.arange(1,5.5,step=0.5))
        plt.title("histogram ocen")
        plt.xlabel("ocene")
        plt.ylabel("Stevilo ocen")
        plt.bar(oceneNames1, oceneCount1,width=0.5)
        st.pyplot(plt.gcf())
        plt.figure(figsize=(18, 4))
        plt.title("Stevilo ocen vsako leto")
        plt.xlabel("leto")
        plt.ylabel("Stevilo ocen")
        plt.bar(collections.OrderedDict(sorted(stOcenPoLetih1.items())).keys(), collections.OrderedDict(sorted(stOcenPoLetih1.items())).values())
        st.pyplot(plt.gcf())
        plt.figure(figsize=(18, 4))
        plt.title("Popvrecna ocena vsako leto")
        plt.xlabel("leto")
        plt.ylabel("povprecna ocena")
        plt.bar(collections.OrderedDict(sorted(avgOcenPoLetih1.items())).keys(), collections.OrderedDict(sorted(avgOcenPoLetih1.items())).values())
        st.pyplot(plt.gcf())
    with col2:
        st.write("podatki za: ",film2)
        st.write("povprecna ocena: ",avgOcen2,"stevilo ocen: ",stOcen2,"standardni odklon ocen: ",divOcen2)
        plt.figure(figsize=(18, 4))
        ax = plt.gca()
        ax.set_xticks(np.arange(1,5.5,step=0.5))
        plt.title("histogram ocen")
        plt.xlabel("ocene")
        plt.ylabel("Stevilo ocen")
        plt.bar(oceneNames2, oceneCount2,width=0.5)
        st.pyplot(plt.gcf())
        plt.figure(figsize=(18, 4))
        plt.title("Stevilo ocen vsako leto")
        plt.xlabel("leto")
        plt.ylabel("Stevilo ocen")
        plt.bar(collections.OrderedDict(sorted(stOcenPoLetih2.items())).keys(), collections.OrderedDict(sorted(stOcenPoLetih2.items())).values())
        st.pyplot(plt.gcf())
        plt.figure(figsize=(18, 4))
        plt.title("Popvrecna ocena vsako leto")
        plt.xlabel("leto")
        plt.ylabel("povprecna ocena")
        plt.bar(collections.OrderedDict(sorted(avgOcenPoLetih2.items())).keys(), collections.OrderedDict(sorted(avgOcenPoLetih2.items())).values())
        st.pyplot(plt.gcf())