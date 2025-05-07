@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Retrieve uploaded CSV file
        file = request.files['file']
        df = pd.read_csv(file)

        # Expected feature columns
        features = [
            "Torque(Nm)",
            "Hydraulic_Pressure(bar)",
            "Cutting(kN)",
            "Coolant_Pressure(bar)",
            "Spindle_Speed(RPM)",
            "Coolant_Temperature"
        ]

        # Check all required columns exist
        missing_cols = [col for col in features if col not in df.columns]
        if missing_cols:
            return jsonify({'error': f'Missing columns: {missing_cols}'}), 400

        # Preprocess and predict
        input_data = df[features]
        processed_data = preprocessing_pipeline.transform(input_data)
        prediction = model.predict(processed_data)

        # Return prediction results
        results = ['Yes' if pred == 1 else 'No' for pred in prediction]
        df['Downtime_Prediction'] = results

        # Optional: return full table
        return jsonify({'predictions': df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
