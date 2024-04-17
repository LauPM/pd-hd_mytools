import pandas as pd
import random
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

df = pd.read_csv('linear_fit_values.txt', sep='\t')
df['Label'] = df['IP'].apply(lambda x: str(x))+"_ch"+df['Filename'].apply(lambda x: x.split(".")[0].split("_")[-1].zfill(2))
df['Slope (V/DAC)'] = df['Slope'].apply(lambda x: 1/x)
df['Intercept (V)'] = -1*(df['Slope'].apply(lambda x: 1/x)*df['Intercept'])
# print(df)
labels = ["104", "107", "109", "111", "112", "113"]
marker_symbols = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up']*8
marker_colors = px.colors.qualitative.Plotly + px.colors.qualitative.Alphabet + px.colors.qualitative.D3 + px.colors.qualitative.Dark24 + px.colors.qualitative.G10 + px.colors.qualitative.T10 + px.colors.qualitative.Vivid + px.colors.qualitative.Safe
channel_counts = df['Label'].value_counts()

for label in labels:
    print(f'IP: {label}')
    for plot in ["Slope (V/DAC)", "Intercept (V)"]:
        fig_hist = go.Figure()
        for file in sorted(df['Label'][df['IP'] ==  int(label)].unique()):
            hist, bin_edges = np.histogram(df[df['Label'] == file][plot])
            color = df[df['Label'] == file]['AFE'].values[0]
            fig_hist.add_trace(go.Bar(x=bin_edges[:-1], y=hist, name=file, opacity=0.75,width=np.diff(bin_edges),marker=dict(color=marker_colors[int(color)])))
            fig_hist.update_xaxes(matches="x",showline=True,mirror="ticks",zeroline=False,showgrid=True,minor_ticks="inside",tickformat='.3f',)
            fig_hist.update_yaxes(matches="y",showline=True,mirror="ticks",zeroline=False,showgrid=True,minor_ticks="inside",tickformat='.s',)
            fig_hist.update_layout(template="presentation", yaxis_title='Counts', xaxis_title=plot,
                                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, itemsizing='constant'),
                                    # xaxis=dict(tickangle=45),
                                    font=dict(size=18),
                                    bargap=0)

            fig_hist.write_image(f'../../images/iv_curves/ip_{label}_{plot.split(" ")[0].lower()}_hist.png')
            fig_hist.write_html(f'../../images/iv_curves/ip_{label}_{plot.split(" ")[0].lower()}_hist.html')