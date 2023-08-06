import pandas as pd
import json
import logging
import os
import joblib
import gitlab

from typing import List, Dict

from abc import ABC, abstractproperty

from hypermodel.utilities.file_hash import file_md5
from hypermodel.features import (
    get_unique_feature_values,
    one_hot_encode,
    describe_features
)
from hypermodel.platform.abstract.services import PlatformServicesBase


class ModelContainer:
    """
    The `ModelContainer` class provides a wrapper for a Machine Learning model,
    detailing information about Features (numeric & categorical), information about
    the distributions of feature columns and potentially a reference to the current
    version of the model's `.joblib` file. 
    """
    config: PlatformServicesBase
    all_features: List[str]
    features_categorical: List[str]
    target: str

    unique_values: Dict[str, List[str]]

    def __init__(
        self,
        name: str,
        project_name: str,
        features_numeric: List[str],
        features_categorical: List[str],
        target: str,
        services: PlatformServicesBase,
    ):
        self.project_name = project_name
        self.name = name
        self.services = services
        self.features_numeric = features_numeric
        self.features_categorical = features_categorical
        self.features_all = features_numeric+features_categorical
        self.target = target

        # File name helpers
        self.filename_distributions = f"{self.name}-distributions.json"
        self.filename_model = f"{self.name}.joblib"
        self.filename_reference = f"{self.name}-reference.json"

        self.is_loaded = False

    def analyze_distributions(self, data_frame: pd.DataFrame):
        """
        Given a dataframe, find all the unique values for categorical features
        and the distribution of all the numerical features and store them within
        this object.

        Args:
            data_frame (pd.DataFrame): The dataframe to analyze

        Returns:
            A reference to self
        """
        logging.info(f"ModelContainer {self.name}: analyze_distributions")
        self.feature_uniques = get_unique_feature_values(
            data_frame, self.features_categorical
        )
        self.feature_summaries = describe_features(data_frame, self.features_numeric)

        return self

    def dump_distributions(self):
        """
        Write information about the distributions of features to the local filesystem

        Returns:
            The path to the file that was written
        """
        file_path = self.get_local_path(self.filename_distributions)

        with open(file_path, "w") as f:
            json_obj = {
                "feature_uniques": self.feature_uniques,
                "feature_summaries": self.feature_summaries,
            }
            json.dump(json_obj, f)
        return file_path

    def build_training_matrix(self, data_frame: pd.DataFrame):
        """
        Convert the provided `data_frame` to a matrix after one-hot encoding
        all the categorical features, using the currently cached `feature_uniques`

        Args:
            data_frame (pd.DataFrame): The pandas dataframe to encode

        Returns:
            A numpy array of the encoded data
        """
        logging.info(f"ModelContainer {self.name}: build_training_matrix")

        # Now lets do the encoding thing...
        encoded_df = one_hot_encode(data_frame, self.feature_uniques)

        for nf in self.features_numeric:
            encoded_df[nf] = data_frame[nf]

        matrix = encoded_df.values
        return matrix

    def load(self, reference_file=None):
        """
        Given the provided reference file, look up the location of the model
        in the DataLake and load it into memory.  This will load the .joblib
        file, as well as any distributions / unique values associeated with this
        model reference

        Args:
            reference_file (str): The path of the reference json file

        Returns:
            None
        """
        lake = self.services.lake

        if reference_file is None:
            reference_file = self.get_local_path(self.filename_reference)

        logging.info(
            f"ModelContainer {self.name} loading container from {reference_file}"
        )
        with open(reference_file) as f:
            reference = json.load(f)

            # Load the distributions
            dist_ref = reference["distributions"]
            dist_path = self.get_local_path(self.filename_distributions)

            lake.download(dist_ref["path"], dist_path)
            self.load_distributions(dist_path)

            # Load the model
            model_ref = reference["model"]
            model_path = self.get_local_path(self.filename_model)
            lake.download(model_ref["path"], model_path)
            self.load_model()

    def load_distributions(self, file_path: str):
        logging.info(f"ModelContainer {self.name}: load_distributions")
        with open(file_path, "r") as f:
            json_obj = json.load(f)
            self.feature_uniques = json_obj["feature_uniques"]
            self.feature_summaries = json_obj["feature_summaries"]
        return self

    def publish(self):
        """
        Publish the model (as a Joblib)
        """
        # Write the models locally
        local_path_dist = self.dump_distributions()
        local_path_model = self.dump_model()

        # Write them to cloud storage
        bucket_path_dist = self.get_bucket_path(self.filename_distributions)
        bucket_path_model = self.get_bucket_path(self.filename_model)

        config = self.services.config
        lake = self.services.lake

        lake.upload(bucket_path_dist, local_path_dist, bucket_name=config.lake_bucket)
        lake.upload(bucket_path_model, local_path_model, bucket_name=config.lake_bucket)

        # Now finally we want to write our reference file to our repository and build a merge request
        reference = {
            "model": {
                "bucket": config.lake_bucket,
                "path": bucket_path_model,
                "md5": file_md5(local_path_model),
            },
            "distributions": {
                "bucket": config.lake_bucket,
                "path": bucket_path_dist,
                "md5": file_md5(local_path_dist),
            },
        }

        return reference

    def dump_reference(self, reference):
        file_path = self.get_local_path(self.filename_reference)
        with open(file_path, "w") as f:
            json.dump(reference, f, indent=2)


    def create_merge_request(self, reference, description="New models!"):
        self.services.git.create_merge_request(
            reference=reference,
            reference_path=self.filename_reference,
            description="New models!",
            target_branch="master",
            labels=["model-bot"],
        )


    def bind_model(self, model):
        self.model = model
        return self

    def dump_model(self):
        model_path = self.get_local_path(self.filename_model)
        joblib.dump(self.model, model_path)
        return model_path

    def load_model(self):
        model_path = self.get_local_path(self.filename_model)
        self.model = joblib.load(model_path)
        return self.model

    def get_local_path(self, filename):
        path = f"{self.services.config.kfp_artifact_path}"
        # If the path does not exist, then create it.

        if not os.path.exists(path):
            os.makedirs(path)
        return f"{self.services.config.kfp_artifact_path}/{filename}"

    def get_bucket_path(self, filename):
        config = self.services.config
        workflow_id = (
            os.environ["KF_WORKFLOW_ID"] if "KF_WORKFLOW_ID" in os.environ else "local"
        )
        path = f"models/{self.project_name}/{config.ci_commit}/{workflow_id}/{filename}"
        return path
