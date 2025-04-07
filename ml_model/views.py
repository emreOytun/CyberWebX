import os
import pefile
import pandas as pd
import numpy as np
from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadedFile
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
import joblib
from django.conf import settings
import magic

# Function to extract features from files based on their type
def extract_features(file_path):
    try:
        file_type = magic.from_file(file_path, mime=True)
        features = {'file_size': os.path.getsize(file_path)}

        if 'exe' in file_type or 'dll' in file_type:  # PE files
            pe = pefile.PE(file_path)
            features['num_sections'] = len(pe.sections)
            features['entry_point'] = pe.OPTIONAL_HEADER.AddressOfEntryPoint
            features['image_base'] = pe.OPTIONAL_HEADER.ImageBase
            features['section_entropy'] = sum(section.get_entropy() for section in pe.sections) / len(pe.sections)
            features['import_count'] = len(pe.DIRECTORY_ENTRY_IMPORT)
            features['export_count'] = len(pe.DIRECTORY_ENTRY_EXPORT.symbols) if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT') else 0
        else:
            # Add more feature extraction methods for other file types here
            features['num_sections'] = 0
            features['entry_point'] = 0
            features['image_base'] = 0
            features['section_entropy'] = 0
            features['import_count'] = 0
            features['export_count'] = 0

        return pd.DataFrame([features])
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Function to classify the uploaded file
def classify_file(file_path):
    model_path = os.path.join(settings.BASE_DIR, 'Classifier.pkl')
    
    # Check if the model exists
    if not os.path.exists(model_path):
        generate_model(None)  # Generate the model if it doesn't exist
        if not os.path.exists(model_path):
            return None, "Model generation failed. Please try again."

    model = joblib.load(model_path)
    features = extract_features(file_path)
    
    if features is not None:
        prediction = model.predict(features)
        return prediction[0]  # Return the first prediction
    else:
        return None, "Feature extraction failed."

# Function to generate and train the model
def generate_model(request):
    malware_dir = './datasets/malware'
    benign_dir = './datasets/benign'
    
    features_list = []
    labels = []

    # Process malware files
    for filename in os.listdir(malware_dir):
        file_path = os.path.join(malware_dir, filename)
        features = extract_features(file_path)
        if features is not None:
            features_list.append(features.iloc[0].to_dict())
            labels.append(1)  # Malware label

    # Process benign files
    for filename in os.listdir(benign_dir):
        file_path = os.path.join(benign_dir, filename)
        features = extract_features(file_path)
        if features is not None:
            features_list.append(features.iloc[0].to_dict())
            labels.append(0)  # Benign label

    # Prepare data for training
    features_df = pd.DataFrame(features_list)
    X = features_df
    y = np.array(labels)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize Random Forest Classifier
    rfc = RandomForestClassifier()

    # Hyperparameter tuning using Grid Search
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
    }
    grid_search = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=5, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # Save the best model
    best_model = grid_search.best_estimator_
    model_path = os.path.join(settings.BASE_DIR, 'Classifier.pkl')
    joblib.dump(best_model, model_path)

    # return render(request, 'ml_model/model_generated.html', {'message': 'Model generated successfully!'})

# View to handle file uploads
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            file_path = uploaded_file.file.path
            prediction = classify_file(file_path)
            print(prediction)
            if prediction is not None:
                result = "Malware" if prediction == 1 else "Benign"
                return render(request, 'ml_model/result.html', {'prediction': result})
            else:
                return render(request, 'ml_model/result.html', {'prediction': "Error in classification."})
    else:
        form = UploadFileForm()
    return render(request, 'ml_model/upload.html', {'form': form})