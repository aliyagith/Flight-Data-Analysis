from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt

# Use Agg backend for non-interactive environments
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('Airplane_Crashes_and_Fatalities_Since_1908.csv')

# Example: Create visualizations for each analysis
def create_operator_analysis():
    operator_data = df['Operator'].value_counts().head(10)
    operator_data.plot(kind='bar', figsize=(10, 6))
    plt.title('Top 10 Operators with Most Crashes')
    plt.xlabel('Operator')
    plt.ylabel('Number of Crashes')
    plt.savefig('static/images/operator_analysis.png')
    plt.clf()  # Clear the figure after saving

def create_causes_analysis():
    cause_data = df['Summary'].dropna().str.split().explode().value_counts().head(10)
    cause_data.plot(kind='bar', figsize=(10, 6))
    plt.title('Top Words in Crash Summary (Causes)')
    plt.xlabel('Word')
    plt.ylabel('Frequency')
    plt.savefig('static/images/causes_analysis.png')
    plt.clf()  # Clear the figure after saving

def create_trends_analysis():
    df['Year'] = pd.to_datetime(df['Date'], errors='coerce').dt.year
    year_data = df['Year'].value_counts().sort_index()
    year_data.plot(kind='line', figsize=(10, 6))
    plt.title('Yearly Trends of Airplane Crashes')
    plt.xlabel('Year')
    plt.ylabel('Number of Crashes')
    plt.savefig('static/images/trends_analysis.png')
    plt.clf()  # Clear the figure after saving

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/operators-analysis')
def operators_analysis():
    create_operator_analysis()
    return render_template('operators_analysis.html')

@app.route('/causes-analysis')
def causes_analysis():
    create_causes_analysis()
    return render_template('causes_analysis.html')

@app.route('/trends-analysis')
def trends_analysis():
    create_trends_analysis()
    return render_template('trends_analysis.html')

if __name__ == '__main__':
    app.run(debug=True)
