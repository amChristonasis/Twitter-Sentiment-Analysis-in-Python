import pandas as pd
from pymongo import MongoClient
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()

def create_header(some_string):
    header_style = {
        'background-color' : '#1B95E0',
        'padding' : '1.5rem',
        'color': 'white',
        'font-family': 'Verdana, Geneva, sans-serif'
    }
    header = html.Header(html.H1(children=some_string, style=header_style))
    return header

app.layout = html.Div(children=[
    html.Div(create_header('Energie Transitie Sentiment Inspector')),
    html.Div([
        html.Div(
            dcc.Graph(
                id='recent-tweets-table',
                    ), style={'display': 'inline-block', 'width' : '60%'}),
        html.Div(
            dcc.Graph(
                id='most-active-users',
                    ), style={'display': 'inline-block','width':'40%'}),
        html.Div(
            dcc.Interval(
                id='interval-component',
                interval=5*1000, # in milliseconds
                n_intervals=0
                    ))]
, style={'width': '100%', 'display': 'inline-block'}
            ),
    html.Div([
        html.Div(
            dcc.Graph(
                id='tweets-per-day',
                    ), style={'display': 'inline-block', 'vertical-align':'top','width':'50%'}),
        html.Div(
            dcc.Graph(
                id='donut-sentiment',
                    ), style={'display': 'inline-block','width':'50%'})]
    , style={'width': '100%', 'display': 'inline-block'}
            )
    ])

@app.callback(Output('recent-tweets-table', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    # connect to mongo and store in pandas dataframe
    client = MongoClient('localhost',27017)
    db = client.twitter_nl
    collection = db.tweet_info
    df = pd.DataFrame(list(collection.find()))

    # sort tweets by descending follower count
    df['creation_datetime'] = pd.to_datetime(df['creation_datetime'])
    df.sort_values(by='creation_datetime', ascending=False, inplace=True)
    
    values = [[date for date in df.head(5)['creation_datetime']],
                [text for text in df.head(5)['text']],
                [senti_val for senti_val in df.head(5)['senti_val']],
                [subjectivity for subjectivity in df.head(5)['subjectivity']]]
    
    trace0 = go.Table(
      columnorder = [1,2,3,4],
      columnwidth = [15,60,15,15],
      header = dict(
        values = [['<b>Date</b>'],['<b>Text</b>'],
                      ['<b>Sentiment Score</b>'],['<b>Subjectivity Score</b>']],
        line = dict(color = 'blue'),
        fill = dict(color = '#1B95E0'),
        align = ['left','center'],
        font = dict(color = 'white', size = 16),
        height = 40
      ),
      cells = dict(
        values = values,
        line = dict(color = 'blue'),
        fill = dict(color = ['white']),
        align = ['left', 'center'],
        font = dict(color = 'black', size = 14),
        height = 30
        ))
      
    data = [trace0]
    layout = dict(title='<b>Most Recent Tweets on Energy</b>', height=700,
                  titlefont=dict(size=20))
    
    fig = dict(data=data, layout=layout)

    return fig

@app.callback(Output('tweets-per-day', 'figure'),
              [Input('interval-component', 'n_intervals')])
def tweets_per_day(n):
    # connect to mongo and store in pandas dataframe
    client = MongoClient('localhost',27017)
    db = client.twitter_nl
    collection = db.tweet_info
    df = pd.DataFrame(list(collection.find()))

    # sort tweets by descending follower count
    df['creation_date'] = pd.to_datetime(df['creation_datetime'])
    df['tweet_date'] = pd.DatetimeIndex(df['creation_date']).date
    df2 = df.groupby(['tweet_date']).username.count().reset_index()
    df2.rename(columns={'username': 'users_count'})

    trace1 = go.Bar(
        x=df2['tweet_date'],  
        y=df2['username'],
        name = 'Tweets per Day',
        marker=dict(color='#1B95E0') # set the marker color to gold
    )
    
    data = [trace1]
    
    layout = go.Layout(
        title='<b>Tweets per day</b>',
        barmode='group',
        titlefont=dict(size=20)
        #'stack', 'group', 'overlay', 'relative'
    )
    
    fig = go.Figure(data=data, layout=layout)

    return fig

@app.callback(Output('most-active-users', 'figure'),
              [Input('interval-component', 'n_intervals')])
def most_active_users(n):
    # connect to mongo and store in pandas dataframe
    client2 = MongoClient('localhost',27017)
    db2 = client2.twitter_nl
    collection2 = db2.tweet_info
    df2 = pd.DataFrame(list(collection2.find()))

    df2['user_description'] = df2['user_description'].fillna('')
    df2['user'] = df2['username'] + df2['user_description']
    df2['usercount'] = df2.groupby('user')['user'].transform('count')
    df2.usercount = df2.usercount.astype('int64') 
    result = df2[['username','user_description','usercount']].drop_duplicates()
    result = result.sort_values(by=['usercount'],ascending=False).head(10)
    result = result.sort_values(by=['usercount'])
    
    data = [go.Bar(
                x=result['usercount'],
                y=result['username'],
                marker = {'color':['rgb(26, 118, 255)','rgb(26, 118, 255)',
                                   'rgb(26, 118, 255)','rgb(26, 118, 255)','rgb(26, 118, 255)',
                                   'rgb(26, 118, 255)','rgb(26, 118, 255)','rgb(26, 118, 255)','blue','red']},
                text = result['user_description'],
                orientation = 'h',
                )]
    
    layout = dict(title='<b>Most Active Users Tweeting</b>', height=700,
                  titlefont=dict(size=20))
    
    fig = dict(data=data, layout=layout)

    return fig

@app.callback(Output('donut-sentiment', 'figure'),
              [Input('interval-component', 'n_intervals')])
def donut_sentiment(n):
    # connect to mongo and store in pandas dataframe
    client = MongoClient('localhost',27017)
    db = client.twitter_nl
    collection = db.tweet_info
    tweets = pd.DataFrame(list(collection.find()))
    
    # bucket the sentimental scores
    cat_senti = []
    for row in tweets.senti_val:
       if float(row) > 0.3:
           cat_senti.append('Positive')
       elif float(row) <-0.3:
           cat_senti.append('Negative')
       else:
           cat_senti.append('Neutral')
    tweets['cat_senti'] = cat_senti
    
    
    def cal_percent(senti):
       count_net = len(tweets[tweets['cat_senti'] == senti])
    #   #cent_net = round((count_net/len(tweets)*100), 2)
       return(count_net)
    
    data = [cal_percent('Neutral'),cal_percent('Positive'),cal_percent('Negative')]
    #data.append(cal_percent('Neutral'),cal_percent('Positive'),cal_percent('Negative'))
    #data.append(cal_percent('Positive'))
    #data.append(cal_percent('Negative'))
    
    ## Plotting the donut
    trace1 = {"hole": 0.5, "type": "pie", "labels": ["Neutral","Positive","Negative"], "values": data,
             "showlegend": True, "marker.line.width": 10 , "marker.line.color" : 'white', 'marker': {'colors': ['grey','green','red']}}
    
    
    layout = go.Layout(
           title = "<b>Sentimental analysis</b>",
           titlefont=dict(size=20),
           height=600)
    
    fig = go.Figure(data=[trace1], layout=layout)

    return fig

if __name__ == '__main__':
    app.run_server()
