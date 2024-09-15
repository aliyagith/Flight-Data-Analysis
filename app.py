from flask import Flask, render_template
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('Airplane_Crashes_and_Fatalities_Since_1908.csv')

# Function to create the first Plotly graph (Yearly trends of airplane crashes)
def create_trends_analysis():
    df['Year'] = pd.to_datetime(df['Date'], errors='coerce').dt.year
    year_data = df['Year'].value_counts().sort_index()

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=year_data.index, y=year_data.values, mode='lines', name='Crashes'))
    fig1.update_layout(title='Yearly Trends of Airplane Crashes', xaxis_title='Year', yaxis_title='Number of Crashes')

    # Convert the figure to HTML
    graph1_html = pio.to_html(fig1, full_html=False)
    return graph1_html

# Function to create the second Plotly graph (Crashes per month)
def create_monthly_crashes():
    df['Month'] = pd.to_datetime(df['Date'], errors='coerce').dt.month
    month_data = df['Month'].value_counts().sort_index()

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=month_data.index, y=month_data.values, marker_color='yellow', name='Crashes by Month'))
    fig2.update_layout(title='Number of Airplane Crashes per Month', xaxis_title='Month', yaxis_title='Number of Crashes')

    # Convert the figure to HTML
    graph2_html = pio.to_html(fig2, full_html=False)
    return graph2_html

# Function to create the third Plotly graph (Crashes by Operator)
def create_operator_analysis():
    operator_data = df['Operator'].value_counts().head(10)

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=operator_data.index, y=operator_data.values, marker_color='blue', name='Crashes by Operator'))
    fig3.update_layout(title='Top 10 Operators with Most Crashes', xaxis_title='Operator', yaxis_title='Number of Crashes')

    # Convert the figure to HTML
    graph3_html = pio.to_html(fig3, full_html=False)
    return graph3_html

# Function to create the fourth Plotly graph (Crash Causes - top words in summaries)
def create_causes_analysis():
    cause_data = df['Summary'].dropna().str.split().explode().value_counts().head(10)

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=cause_data.index, y=cause_data.values, marker_color='red', name='Top Words in Crash Summary'))
    fig4.update_layout(title='Top Words in Crash Summary (Causes)', xaxis_title='Word', yaxis_title='Frequency')

    # Convert the figure to HTML
    graph4_html = pio.to_html(fig4, full_html=False)
    return graph4_html

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/trends-analysis')
def trends_analysis():
    # Generate the graphs for the trends analysis page
    graph1 = create_trends_analysis()
    graph2 = create_monthly_crashes()

    # Pass the generated graphs to the HTML template
    return render_template('trends_analysis.html', graph1=graph1, graph2=graph2)

@app.route('/operators-analysis')
def operators_analysis():
    # Generate the graphs for the operators analysis page
    graph3 = create_operator_analysis()
    # Pass the generated graphs to the HTML template
    return render_template('operators_analysis.html', graph3=graph3)

@app.route('/causes-analysis')
def causes_analysis():
    # Generate the graphs for the causes analysis page
    graph4 = create_causes_analysis()

    # Pass the generated graphs to the HTML template
    return render_template('causes_analysis.html', graph4=graph4)

if __name__ == '__main__':
    app.run(debug=True)
