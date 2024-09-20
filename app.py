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
    # Add trace with enhanced styling
    fig1.add_trace(go.Scatter(
    x=year_data.index, 
    y=year_data.values, 
    mode='lines+markers',  # Add markers
    name='Crashes',
    line=dict(color='royalblue', width=2),  # Set line color and width
    marker=dict(size=6, color='red')  # Set marker size and color
    ))

# Update layout with enhanced styling
    fig1.update_layout(
    title={
        'text': 'Yearly Trends of Airplane Crashes',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title='Year',
    yaxis_title='Number of Crashes',
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),  # Add grid lines
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    plot_bgcolor='white'  # Set background color
    )

    # Convert the figure to HTML
    graph1_html = pio.to_html(fig1, full_html=False)
    return graph1_html

def create_fatalities_time_series():
    # Ensure we are only summing numeric columns
    df_grouped_year = df.groupby('Year').sum(numeric_only=True)

    fig5 = go.Figure()

# Add the line plot for total fatalities
    fig5.add_trace(go.Scatter(
        x=df_grouped_year.index,  # X-axis: Year
        y=df_grouped_year['Fatalities'],  # Y-axis: Total Fatalities
        mode='lines+markers',  # Line and markers
        marker=dict(color='darkred', size=8),  # Marker customization
        line=dict(color='darkred', width=2),  # Line customization
        name='Total Fatalities'
    ))

# Customize the layout
    fig5.update_layout(
        title='Total Fatalities in Airplane Crashes Over Time',
        xaxis_title='Year',
        yaxis_title='Total Fatalities',
        template='plotly_white',  # Set a light theme
        hovermode='x unified',  # Hover effect showing x-axis value across all traces
        xaxis=dict(showgrid=True),  # Enable x-axis gridlines
        yaxis=dict(showgrid=True),  # Enable y-axis gridlines
        height=500,  # Set the figure height
        width=900  # Set the figure width
    )

    # Convert the figure to HTML
    graph5_html = pio.to_html(fig5, full_html=False)
    return graph5_html

# Function to create the second Plotly graph (Crashes per month)
def create_monthly_crashes():
    df['Month'] = pd.to_datetime(df['Date'], errors='coerce').dt.month
    month_data = df['Month'].value_counts().sort_index()

    fig2 = go.Figure()
    # Add trace with enhanced styling and color gradient
    fig2.add_trace(go.Bar(
    x=month_data.index, 
    y=month_data.values, 
    marker=dict(
        color=month_data.values,
        colorscale='Viridis',  # Set color gradient
        showscale=True  # Show color scale
    ),
    name='Crashes by Month'
    ))

# Update layout with enhanced styling
    fig2.update_layout(
    title={
        'text': 'Number of Airplane Crashes per Month',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title='Month',
    yaxis_title='Number of Crashes',
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),  # Add grid lines
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    plot_bgcolor='white'  # Set background color
    )

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

# Function to Visualization a Relationship between number of people aboard and fatalities
def create_trends_analysis():
# Assuming df is your DataFrame
    fig = px.scatter(
    df,
    x='Aboard',
    y='Fatalities',
    opacity=0.6,
    title='Number of Fatalities vs. Number of People Aboard'
)

# Update layout to customize the appearance
    fig.update_layout(
    title={
        'text': 'Number of Fatalities vs. Number of People Aboard',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title='Number of People Aboard',
    yaxis_title='Number of Fatalities',
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    plot_bgcolor='white'  # Set background color
)
# Function to Distribution of the number of fatalities
def create_trends_analysis():
    fig = px.histogram(
        df,
        x='Fatalities',
        nbins=50,
        title='Distribution of Fatalities in Airplane Crashes',
        opacity=0.6,
        color_discrete_sequence=['red'],
        marginal='kde'  # Add KDE curve
)

# Update layout to customize the appearance
    fig.update_layout(
        title={
        'text': 'Distribution of Fatalities in Airplane Crashes',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title='Number of Fatalities',
    yaxis_title='Frequency',
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    plot_bgcolor='white'  # Set background color
)
# Function of total fatalities over time
fig = go.Figure()

# Add a line plot
fig.add_trace(go.Scatter(
    x=df_grouped_year.index, 
    y=df_grouped_year['Fatalities'], 
    mode='lines+markers',
    marker=dict(color='darkred'), 
    line=dict(color='darkred'),
    name='Fatalities'
))

# Add title and labels
fig.update_layout(
    title='Total Fatalities in Airplane Crashes Over Time',
    xaxis_title='Year',
    yaxis_title='Total Fatalities',
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True),
    plot_bgcolor='white',
    width=800, height=400
)

# Function of Top 10 types of aircraft involved in crashes
def create_causes_analysis():
top_types = df['Type'].value_counts().nlargest(10)

# Create the bar plot using Plotly
fig = go.Figure()

# Add bars to the figure
fig.add_trace(go.Bar(
    x=top_types.values,
    y=top_types.index,
    orientation='h',  # Horizontal bar plot
    marker=dict(color=top_types.values, colorscale='coolwarm'),  # Color palette
    name='Aircraft Types'
))

# Customize the layout
fig.update_layout(
    title={
        'text': 'Top 10 Types of Aircraft Involved in Crashes',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title='Number of Crashes',
    yaxis_title='Type of Aircraft',
    plot_bgcolor='white',
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    height=600,
    width=1000
)
# Function of Top 10 locations with the most crashes
def create_causes_analysis():
    # Get the top 10 locations with the most crashes
top_locations = df['Location'].value_counts().nlargest(10)

# Create the bar plot using Plotly
fig = go.Figure()

# Add bars to the figure
fig.add_trace(go.Bar(
    x=top_locations.values,
    y=top_locations.index,
    orientation='h',  # Horizontal bar plot
    marker=dict(color=top_locations.values, colorscale='copper'),  # Apply the copper color palette
    name='Locations'
))

# Customize the layout
fig.update_layout(
    title={
        'text': 'Top 10 Locations with the Most Crashes',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title='Number of Crashes',
    yaxis_title='Location',
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    plot_bgcolor='white',
    height=600,
    width=1000
)
# Function of top 10 routes with the most crashes
def create_causes_analysis():
# Get the top 10 routes with the most crashes
top_routes = df['Route'].value_counts().nlargest(10)

# Create the bar plot using Plotly
fig = go.Figure()

# Add bars to the figure
fig.add_trace(go.Bar(
    x=top_routes.values,
    y=top_routes.index,
    orientation='h',  # Horizontal bar plot
    marker=dict(color=top_routes.values, colorscale='rocket'),  # Apply 'rocket' color palette
    name='Routes'
))

# Customize the layout
fig.update_layout(
    title={
        'text': 'Top 10 Routes with the Most Crashes',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title='Number of Crashes',
    yaxis_title='Route',
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    plot_bgcolor='white',
    height=600,
    width=1000
)
# Function of distribution of crashes with ground fatalities
def create_causes_analysis():
# Filter the dataframe for crashes involving ground fatalities
ground_fatalities = df[df['Ground'] > 0]

# Create the histogram with KDE using Plotly
fig = ff.create_distplot(
    [ground_fatalities['Ground']],  # Data for ground fatalities
    group_labels=['Ground Fatalities'],  # Label for the data
    bin_size=5,  # You can adjust the bin size to match the seaborn histogram
    colors=['purple']  # Set color to purple
)

# Customize the layout for titles and labels
fig.update_layout(
    title={
        'text': 'Distribution of Crashes Involving Ground Fatalities',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title='Number of Ground Fatalities',
    yaxis_title='Frequency',
    plot_bgcolor='white',
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    height=600,
    width=1000
)

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
    graph5 = create_fatalities_time_series()
    graph2 = create_monthly_crashes()
    graph3 = create_operator_analysis()
    graph6 = create_trends_analysis()
    graph7 = create_trends_analysis()
    graph8 = create_causes_analysis()
    graph9 = create_causes_analysis()
    graph4 = create_operator_analysis()
    graph10 = create_causes_analysis()


    # Pass the generated graphs to the HTML template
    return render_template('trends_analysis.html', graph1=graph1, graph2=graph2, graph5=graph5, graph3=graph3, graph6=graph6, graph7=graph7, graph8=graph8, graph9=graph9, graph4=graph4, graph10=graph10)

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
