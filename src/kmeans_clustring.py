import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.cluster import KMeans
from sklearn.preprocessing import FunctionTransformer
from sklearn.metrics import silhouette_score, davies_bouldin_score
import mlflow
import mlflow.sklearn
import pickle

# Assuming cleaning_utils is a module that contains the fix_outliers function

def clustering_pipeline(n_clusters, columns, df, model_save_path=None):
    # Define the outlier fixing function
    def fix_outliers(X):
        # Implement your outlier handling logic here
        # For example, using your provided fix_outliers function
        return X

    # Define the steps in the pipeline
    preprocessing_steps = [
        ('outlier_fix', FunctionTransformer(func=fix_outliers)),
        ('scaling', StandardScaler()),
        ('normalization', FunctionTransformer(func=normalize)),
    ]

    # Create a ColumnTransformer if you have specific preprocessing for different column types
    preprocessor = ColumnTransformer(
        transformers=[('all', Pipeline(preprocessing_steps), columns)]
    )

    # Define the final steps including clustering
    final_steps = [
        ('clustering', KMeans(n_clusters=n_clusters, random_state=1))
    ]

    # Create the full pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('cluster_model', Pipeline(final_steps))
    ])

    # Fit the pipeline on your data
    pipeline.fit(df)

    # Access the KMeans model
    kmeans_model = pipeline.named_steps['cluster_model'].named_steps['clustering']

    # Log metrics with MLflow
    mlflow.start_run()
    mlflow.log_param("outlier_fix", "fix_outliers")
    mlflow.log_param("scaling", "StandardScaler")
    mlflow.log_param("normalization", "normalize")
    mlflow.log_param("n_clusters", n_clusters)

    # Log clustering metrics
    mlflow.log_metric('inertia', kmeans_model.inertia_)
    mlflow.log_metric('silhouette_score', silhouette_score(df, kmeans_model.labels_))
    mlflow.log_metric('davies_bouldin_index', davies_bouldin_score(df, kmeans_model.labels_))

    # Log the model with MLflow
    mlflow.sklearn.log_model(pipeline, "model")

    # Save the model as a .pkl file if a save path is provided
    if model_save_path:
        with open(model_save_path, 'wb') as model_file:
            pickle.dump(kmeans_model, model_file)
        mlflow.log_artifact(model_save_path, "model.pkl")

    mlflow.end_run()

    return kmeans_model

# Example Usage:
# Assuming df_user_engagement is your DataFrame and ['xdr_sessions', 'dur_ms', 'total_data_bytes'] are columns
# result_kmeans_model = clustering_pipeline(n_clusters=3, columns=['xdr_sessions', 'dur_ms', 'total_data_bytes'], df=df_user_engagement, model_save_path='path/to/save/model.pkl')
