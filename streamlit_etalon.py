import pandas as pd
import streamlit as st
#import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots



st.set_option('deprecation.showfileUploaderEncoding', False)
st.title("Etalon Checker LI-7700")
uploaded_file = st.file_uploader("Choose LI-7700 file")
uploaded_ref  = st.file_uploader("Choose Referece LI-7700 file")
column_name = ["DATAH","MSEC","SECONDS","NANOSECONDS","DIAG","CH4D","CH4","TEMP","PRESSURE","RSSI","DROPRATE","AUX1","AUX2","AUX3",	"AUX4","AUX5","AUX6","AUX7","AUX8","AUXTC1","AUXTC2","AUXTC3","CHK"]
rthld = st.slider("Filter Data Below RSSI:",min_value=20,max_value=90,value=60)
result = st.button("Plot Figure")



if uploaded_file is not None:
  # this is the actual data file
  df = pd.read_csv(uploaded_file,sep='\t',header=9,low_memory=False)
  df1 = df.loc[df["DATASTATH"] == "DATA" ]
  df2 = df.loc[df["DATASTATH"]== "DATASTAT"]
  df1 = df1[1:]          #  remove bad header
  df1 = df1.iloc[:,:-3]  # remove extra columns
  df1.columns = column_name # insert new header
  ch41 = df1['CH4'].values
  sec1 = df1['SECONDS'].values
  rss1 = df1['RSSI'].values
  tcham = df1['TEMP'].values
  setpt = df2['BCTSETPT']
  secpt = df2['SECONDS']
  


if uploaded_ref is not None:
    # this is the reference file
  dfr = pd.read_csv(uploaded_ref,sep='\t',header=9,low_memory=False)
  df3 = dfr.loc[dfr["DATASTATH"] == "DATA" ]
  df4 = dfr.loc[dfr["DATASTATH"]== "DATASTAT"]
  df3 = df3[1:]          #  remove bad header
  df3 = df3.iloc[:,:-3]  # remove extra columns
  df3.columns = column_name # insert new header
  ch4r = df3['CH4'].values
  secr = df3['SECONDS'].values
  rssr = df3['RSSI'].values
  
  xy,x_ind,y_ind = np.intersect1d(sec1,secr,return_indices=True)
  ch4del  = ch41[x_ind] - ch4r[y_ind]
  xsec    = sec1[x_ind]
  chambt  = tcham[x_ind]
  rss1    = rss1[x_ind]
  idx = [i for i,v in enumerate(rss1) if v < rthld]
  ch4del[idx] = np.nan



if result:
    
    # Create figure with secondary y-axis
    fig =go.Figure()
    
    fig.add_trace(
    go.Scatter(x=xsec, y=ch4del, name="Delta CH4")
    )
    
    
    fig.add_trace(
    go.Scatter(x=xsec, y=chambt, name="Tchamber (°C",
    yaxis="y3")
    )
    

    fig.add_trace(
    go.Scatter(x=secpt, y=setpt, name="Set Point (°C)",
    yaxis="y4")
    )

    # Create axis objects
    fig.update_layout(
        xaxis=dict(
            domain=[0.0, 0.85]
        ),
        yaxis=dict(
            title="<b>Delta CH4 </b>",
            titlefont=dict(
                color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            )
        ),
        yaxis3=dict(
            title="<b>T Chamber (°C) </b>",
            titlefont=dict(
                color="#d62728"
            ),
            tickfont=dict(
                color="#d62728"
            ),
            anchor="x",
            overlaying="y",
            side="right",   
        ),
        yaxis4=dict(
            title="<b>Set Point (°C) </b>",
            titlefont=dict(
                color="#9467bd"
            ),
            tickfont=dict(
                color="#9467bd"
            ),
            anchor="free",
            overlaying="y",
            side="right",
            position=0.95
        )
    )

    # Add figure title
    fig.update_layout(
    title_text="Delta CH4 and Temperature",
    width=800,
    height=400
    )   
    # Set x-axis title
    fig.update_xaxes(title_text="Seconds")
    fig.update_yaxes(automargin=True)
    # Set y-axes titles
    #fig.update_yaxes(title_text="<b>Delta CH4 </b>", secondary_y=False)
    #fig.update_yaxes(title_text="<b>Tchamber (°C)</b>", secondary_y=True)
    st.plotly_chart(fig, use_container_width=False)
