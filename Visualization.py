import pandas as pd
import plotly.graph_objects as go

# CSV-Datei laden
df = pd.read_csv('survey_responses.csv')

print(f"Number of answers: {len(df)}")

# Frage 1 Daten (blaue Punkte)
trace1 = go.Scatterternary(
    a=df['q1_equality'],
    b=df['q1_technological_progress'],
    c=df['q1_sustainability'],
    mode='markers',
    marker=dict(
        size=10,
        color='rgb(66, 126, 234)',  # Blau
        opacity=0.7,
        line=dict(color='white', width=1),
        symbol='circle'
    ),
    name='2025 Values',
    text=[f"Frage 1<br>Session: {sid}<br>Equality: {a:.1f}%<br>Tech Progress: {b:.1f}%<br>Sustainability: {c:.1f}%"
          for sid, a, b, c in zip(df['session_id'], df['q1_equality'], df['q1_technological_progress'], df['q1_sustainability'])],
    hovertemplate='%{text}<extra></extra>'
)

# Frage 2 Daten (grüne Punkte)
trace2 = go.Scatterternary(
    a=df['q2_equality'],
    b=df['q2_technological_progress'],
    c=df['q2_sustainability'],
    mode='markers',
    marker=dict(
        size=10,
        color='rgb(56, 239, 125)',  # Grün
        opacity=0.7,
        line=dict(color='white', width=1),
        symbol='diamond'
    ),
    name='2075 Values',
    text=[f"Frage 2<br>Session: {sid}<br>Equality: {a:.1f}%<br>Tech Progress: {b:.1f}%<br>Sustainability: {c:.1f}%"
          for sid, a, b, c in zip(df['session_id'], df['q2_equality'], df['q2_technological_progress'], df['q2_sustainability'])],
    hovertemplate='%{text}<extra></extra>'
)

# Figure erstellen
fig = go.Figure(data=[trace1, trace2])

# Layout konfigurieren
fig.update_layout(
    title=dict(
        text=f'Survey Results ({len(df)} Answers)',
        x=0.5,
        xanchor='center',
        font=dict(size=24, color='#333')
    ),
    ternary=dict(
        sum=100,
        aaxis=dict(
            title='Equality',
            min=0,
            linewidth=2,
            ticks='outside',
            ticksuffix='%',
            gridcolor='#ddd'
        ),
        baxis=dict(
            title='Technological Progress',
            min=0,
            linewidth=2,
            ticks='outside',
            ticksuffix='%',
            gridcolor='#ddd'
        ),
        caxis=dict(
            title='Sustainability',
            min=0,
            linewidth=2,
            ticks='outside',
            ticksuffix='%',
            gridcolor='#ddd'
        ),
        bgcolor='#f8f9fa'
    ),
    showlegend=True,
    legend=dict(
        x=0.02,
        y=0.98,
        bgcolor='rgba(255, 255, 255, 0.9)',
        bordercolor='#ddd',
        borderwidth=1
    ),
    width=900,
    height=800,
    paper_bgcolor='white',
    font=dict(family="Arial, sans-serif", size=12),
    margin=dict(t=100, b=50, l=50, r=50)
)

# Plot anzeigen
fig.show()

# Optional: Als HTML-Datei speichern
fig.write_html('survey_visualization.html')
print("\nVisualisierung wurde als 'survey_visualization.html' gespeichert")
