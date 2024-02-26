import plotly.graph_objs as go
import pandas as pd

# Sample data (replace this with your own stock data)
data = pd.DataFrame({
    'Date': pd.date_range(start='2024-01-01', end='2024-01-10'),
    'Open': [100, 105, 110, 108, 115, 118, 120, 122, 125, 130],
    'High': [102, 108, 112, 115, 120, 122, 124, 128, 132, 135],
    'Low': [98, 103, 108, 105, 112, 115, 118, 120, 122, 125],
    'Close': [101, 107, 111, 113, 118, 120, 122, 126, 129, 133]
})

# Create figure
fig = go.Figure()

# Add traces
fig.add_trace(go.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close']))

# Update layout
fig.update_layout(title='Interactive Stock Chart',
                  xaxis_title='Date',
                  yaxis_title='Price')

# Show plot
fig.show()