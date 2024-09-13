import plotly.express as px

def visualize_pii_distribution(classified_pii):
    categories = list(classified_pii.keys())
    values = [len(v) for v in classified_pii.values()]
    fig = px.pie(values=values, names=categories, title='PII Distribution')
    fig.show()
