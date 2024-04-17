import pandas as pd
import random
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv('output.txt', sep='\t')
df['Label'] = df['IP'].apply(lambda x: x.split(".")[-1])+"_ch"+df['File'].apply(lambda x: x.split(".")[0].split("_")[-1].zfill(2))
# df['Label'] = "Ch"+df['File'].apply(lambda x: x.split(".")[0].split("_")[-1])
df['Folder'] = df['Folder'].apply(lambda x: x.replace('Apr', '04').replace('Mar', '03'))
df['Folder'] = df['Folder'].apply(lambda x: x.split('-')[2] +"_"+ x.split('-')[0] +"_"+ x.split('-')[1] +"_"+ x.split('-')[3])
df['Folder'] = df['Folder'].apply(lambda x: x.replace('run', ''))
df = df.sort_values('Folder')
df = df[df['Vdb(Suggested)'] != 0]
print(df)
labels = ["104", "107", "109", "111", "112", "113"]
marker_symbols = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up']*8
marker_colors = px.colors.qualitative.Plotly + px.colors.qualitative.Alphabet + px.colors.qualitative.D3 + px.colors.qualitative.Dark24 + px.colors.qualitative.G10 + px.colors.qualitative.T10 + px.colors.qualitative.Vivid + px.colors.qualitative.Safe
channel_counts = df['Label'].value_counts()

for label in labels:
    fig_scatter = go.Figure()
    fig_hist = go. Figure()
    i = 0
    for file in sorted(df['Label'][df['IP'] ==  f"10.73.137.{label}"].unique()):
        file_data = pd.DataFrame()
        file_data = df[(df['Label'] == file)]
        # print(file_data)
        fig_scatter.add_trace(go.Scatter(x=file_data['Folder'], y=file_data['Vdb(Suggested)'],
                                    mode='markers', name=file,
                                    marker=dict(symbol=marker_symbols[i], color=marker_colors[i])))
        fig_scatter.update_xaxes(matches="x",showline=True,mirror="ticks",zeroline=False,showgrid=True,minor_ticks="inside",tickformat='.s',)
        fig_scatter.update_yaxes(matches="y",showline=True,mirror="ticks",zeroline=False,showgrid=True,minor_ticks="inside",tickformat='.s',)
        fig_scatter.update_layout(template="presentation", yaxis_title='Vdb(Suggested)', #title='Plot of Vdb(Suggested) vs Time'
                             legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, itemsizing='constant'),
                             xaxis=dict(tickangle=45),
                             font=dict(size=10))
        i += 1

        fig_hist.add_trace(go.Bar(x=channel_counts[(channel_counts.index == file)].index, 
                                  y=channel_counts[(channel_counts.index == file)].values,
                                  marker=dict(color='teal')))
        fig_hist.update_xaxes(matches="x",showline=True,mirror="ticks",zeroline=False,showgrid=True,minor_ticks="inside",tickformat='.s',)
        fig_hist.update_yaxes(matches="y",showline=True,mirror="ticks",zeroline=False,showgrid=True,minor_ticks="inside",tickformat='.s',)
        fig_hist.update_layout(template="presentation", yaxis_title='Counts', xaxis_title='Channels', #title='Plot of Vdb(Suggested) vs Time'
                               showlegend=False, xaxis=dict(tickangle=45), font=dict(size=10))
        
    fig_scatter.write_image(f'../../images/iv_curves/ip_{label}_evolution.png')
    fig_scatter.write_html(f'../../images/iv_curves/ip_{label}_evolution.html')

    fig_hist.write_image(f'../../images/iv_curves/ip_{label}_ch_hist.png')
    fig_hist.write_html(f'../../images/iv_curves/ip_{label}_ch_hist.html')


# plt.scatter(df['Folder'], df['Vdb(Suggested)'])
# plt.xlabel('File')
# plt.ylabel('Vdb(Suggested)')
# # plt.title('Plot of Column 1 vs Column 2')
# plt.savefig('images/plot.png')
# plt.show()