from flask import Flask, render_template, request
from utils1 import get_healthai_response,extract_text_from_image
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from flask import jsonify

app = Flask(__name__)

@app.route('/disease')
def disease_form():
    return render_template("disease.html")

@app.route('/treatment')
def treatment_form():
    return render_template("treatment.html")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    query = request.form.get("query")
    prompt = f"""
As a healthcare AI assistant, provide a helpful, accurate, and evidence-based response to the following patient question:

PATIENT QUESTION: {query}

Provide a clear, empathetic response that includes facts, avoids diagnoses, and uses simple language.
"""
    print("Received query:", query)
    result = get_healthai_response(prompt)
    print("AI Response:", result)
    return jsonify({"result": result})



@app.route('/disease', methods=['POST','GET'])
def disease():
    data = request.form
    prompt = f"""
As a medical AI assistant, predict potential conditions based on the following:

Symptoms: {data.get('symptoms')}
Age: {data.get('age')}
Gender: {data.get('gender')}
History: {data.get('history')}
Heart Rate: {data.get('hr')} bpm
Blood Pressure: {data.get('bp_sys')}/{data.get('bp_dia')} mmHg
Glucose: {data.get('glucose')} mg/dL
Recent Symptoms: {data.get('recent')}

Respond with top 3 likely conditions, likelihood, explanation, and next steps.
"""
    result = get_healthai_response(prompt)
    return render_template("result.html", query=data.get('symptoms'), response=result)

@app.route('/treatment', methods=['POST','GET'])
def treatment():
    data = request.form
    prompt = f"""
Generate a treatment plan for:

Condition: {data.get('condition')}
Age: {data.get('age')}
Gender: {data.get('gender')}
Medical History: {data.get('history')}

Include: medications, lifestyle, diet, physical activity, follow-up care, and mental health tips.
"""
    result = get_healthai_response(prompt)
    return render_template("result.html", query=data.get('condition'), response=result)

@app.route('/analytics', methods=['GET', 'POST'])
def analytics():
    if request.method == 'POST':
        hr = int(request.form.get('hr'))
        bp_sys = int(request.form.get('bp_sys'))
        bp_dia = int(request.form.get('bp_dia'))
        glucose = int(request.form.get('glucose'))

        # === Create a combined chart ===
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle("Patient Health Analytics", fontsize=16)

        labels = ['Heart Rate', 'BP Systolic', 'BP Diastolic', 'Glucose']
        values = [hr, bp_sys, bp_dia, glucose]
        colors = ['#ff6384', '#36a2eb', '#ffcd56', '#4bc0c0']

        # 📊 Bar Chart
        axs[0, 0].bar(labels, values, color=colors)
        axs[0, 0].set_title('Vitals Bar Chart')
        axs[0, 0].set_ylabel('Values')
        axs[0, 0].set_ylim(0, max(values) + 50)
        for i, val in enumerate(values):
            axs[0, 0].text(i, val + 3, str(val), ha='center')

        # 🕸 Radar Chart
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        values_normalized = [v / (max(values)+20) * 100 for v in values]
        values_looped = values_normalized + values_normalized[:1]
        angles += angles[:1]
        ax_radar = plt.subplot(2, 2, 2, polar=True)
        ax_radar.plot(angles, values_looped, color='teal', linewidth=2)
        ax_radar.fill(angles, values_looped, color='skyblue', alpha=0.4)
        ax_radar.set_title("Vitals Radar Chart")
        ax_radar.set_xticks(angles[:-1])
        ax_radar.set_xticklabels(labels)

        # 🍩 Donut Chart
        wedges, texts = axs[1, 0].pie(values, colors=colors, startangle=90)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        axs[1, 0].add_artist(centre_circle)
        axs[1, 0].axis('equal')
        axs[1, 0].set_title("Vitals Donut Chart")
        axs[1, 0].legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        # 🔥 Heatmap
        df = pd.DataFrame({'Vitals': labels, 'Values': values}).set_index('Vitals')
        sns.heatmap(df, annot=True, cmap="YlGnBu", fmt=".0f", cbar=False, ax=axs[1, 1])
        axs[1, 1].set_title("Vitals Heatmap")

        # ✅ Save the combined image
        image_path = os.path.join('static', 'analytics_chart.png')
        plt.tight_layout()
        plt.savefig(image_path)
        plt.close()

        return render_template("result.html", query="Patient Analytics", chart_image=image_path)

    return render_template("analytics.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files.get("report")
        if uploaded_file:
            extracted_text = extract_text_from_image(uploaded_file)
            prompt = f"""
Analyze this medical report:
{extracted_text}
Highlight issues, explain simply, and suggest next steps.
"""
            result = get_healthai_response(prompt)
            return render_template("report_result.html", extracted_text=extracted_text, response=result)
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)