from io import BytesIO
import base64
import matplotlib.pyplot as plt

# Create image from plot
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png).decode('utf-8')
    return graph

# Generate chart based on user input
def get_chart(chart_type, data, labels=None):
    plt.switch_backend('AGG')
    plt.figure(figsize=(6, 4))

    if chart_type == 'bar':
        plt.bar(labels, data['cooking_time'])  # use plain labels
        plt.ylabel('Cooking Time (mins)')
        plt.xticks(rotation=45, ha='right')
        plt.title('Cooking Time by Recipe')

    elif chart_type == 'pie':
        plt.pie(data['cooking_time'], labels=labels, autopct='%1.1f%%')
        plt.title('Cooking Time Distribution')

    elif chart_type == 'line':
        plt.plot(labels, data['cooking_time'], marker='o')  # use plain labels
        plt.xticks(rotation=45, ha='right')
        plt.title('Cooking Time Trend')

    else:
        plt.text(0.5, 0.5, 'Invalid chart type', ha='center')

    plt.tight_layout()
    return get_graph()
