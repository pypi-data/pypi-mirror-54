import calendar
import math
import os.path
import random
from datetime import datetime, timedelta

import joblib
import numpy as np
import pyprind
from astropy.io import ascii
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt
from sklearn.metrics import precision_recall_curve
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from .config import Config
from .data import Data
from .shock import Shock


DEFAULT_PREDICTOR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "predictor.pkl")


def get_random_datetime(start, end):
    start_ts = calendar.timegm(start.timetuple())
    end_ts = calendar.timegm(end.timetuple())
    return datetime.fromtimestamp(random.random() * (end_ts - start_ts) + start_ts)


def dt2ts(dt):
    return calendar.timegm(dt.timetuple())


class IPSVM:
    def __init__(self, config=Config(), load_default_predictor=True):
        self._config = config
        if load_default_predictor:
            self._predictor = joblib.load(DEFAULT_PREDICTOR_PATH)
        else:
            self._predictor = None

    def load(self):
        self._predictor = joblib.load(self.config["PREDICTOR"])

    @property
    def config(self):
        return self._config

    @property
    def predictor(self):
        return self._predictor

    def get_adaptive_features(self, shock_datetime, data):
        shock_timestamp = calendar.timegm(shock_datetime.timetuple())
        features = []
        for step in range(
            self.config["MIN_SCAN_WINDOW"],
            self.config["MAX_SCAN_WINDOW"] + self.config["SCAN_STEP"],
            self.config["SCAN_STEP"],
        ):
            shock = Shock(
                shock_timestamp, data.range(shock_timestamp - step * 60, shock_timestamp + step * 60), self.config
            )
            features = shock.features
            if None not in features:
                break
        return features

    def collect_true_positives(self, spacecraft, monthly=True):
        spacecraft = self.config.spacecraft_from_alias(spacecraft)
        shocks = ascii.read(self.config["SPACECRAFT"][spacecraft]["TRUE_POSITIVES_LIST"])
        shock_datetimes = np.array(
            [datetime(row["col1"], row["col2"], row["col3"], row["col4"], row["col5"], row["col6"]) for row in shocks]
        )
        shock_datetimes.sort()
        features_set = []
        classes_set = []
        bar = pyprind.ProgPercent(shock_datetimes.size * self.config["TRUE_POSITIVES_SHIFT_NUMBER"], track_time=True)
        prev_year = 0
        prev_month = 0
        data = None
        for shock_datetime in shock_datetimes:
            if monthly:
                if shock_datetime.year != prev_year or shock_datetime.month != prev_month:
                    start = datetime(shock_datetime.year, shock_datetime.month, 1)
                    end = start + relativedelta(months=1)
                    data = Data.get_spacecraft_data(
                        spacecraft,
                        start - timedelta(minutes=self.config["MAX_SCAN_WINDOW"] + self.config["SCAN_STEP"]),
                        end + timedelta(minutes=self.config["MAX_SCAN_WINDOW"] + self.config["SCAN_STEP"]),
                        self.config,
                    )
                    data.filter(self.config)
                    prev_year = shock_datetime.year
                    prev_month = shock_datetime.month

            count_shifts = 0
            while count_shifts < self.config["TRUE_POSITIVES_SHIFT_NUMBER"]:
                shift = random.uniform(
                    -self.config["TRUE_POSITIVES_SHIFT_RANGE"], self.config["TRUE_POSITIVES_SHIFT_RANGE"]
                )
                if monthly:
                    range_data = data.range(
                        dt2ts(
                            shock_datetime
                            + timedelta(minutes=shift)
                            - timedelta(minutes=self.config["MAX_SCAN_WINDOW"])
                        ),
                        dt2ts(
                            shock_datetime
                            + timedelta(minutes=shift)
                            + timedelta(minutes=self.config["MAX_SCAN_WINDOW"])
                        ),
                    )
                else:
                    range_data = Data.get_spacecraft_data(
                        spacecraft,
                        shock_datetime + timedelta(minutes=shift) - timedelta(minutes=self.config["MAX_SCAN_WINDOW"]),
                        shock_datetime + timedelta(minutes=shift) + timedelta(minutes=self.config["MAX_SCAN_WINDOW"]),
                        self.config,
                    )
                    range_data.filter(self.config)
                features = self.get_adaptive_features(shock_datetime, range_data)
                if None not in features:
                    features_set.append(features)
                    classes_set.append(True)
                count_shifts += 1
                bar.update()
        joblib.dump(
            {"features": features_set, "classes": classes_set},
            self.config["SPACECRAFT"][spacecraft]["TRUE_POSITIVES_FEATURES_SET"],
        )

    def collect_false_positives(self, spacecraft, start=None, step=timedelta(hours=1)):
        spacecraft = self.config.spacecraft_from_alias(spacecraft)
        shocks = ascii.read(self.config["SPACECRAFT"][spacecraft]["TRUE_POSITIVES_LIST"])
        shock_datetimes = np.array(
            [datetime(row["col1"], row["col2"], row["col3"], row["col4"], row["col5"], row["col6"]) for row in shocks]
        )
        shock_datetimes.sort()
        first_shock_datetime = np.amin(shock_datetimes)
        last_shock_datetime = np.amax(shock_datetimes)

        if start is None:
            start = datetime(first_shock_datetime.year, first_shock_datetime.month, 1)
            features_set = []
            classes_set = []
        else:
            start = datetime(start.year, start.month, 1)
            data = joblib.load(self.config["SPACECRAFT"][spacecraft]["FALSE_POSITIVES_FEATURES_SET"])
            features_set = data["features"]
            classes_set = data["classes"]

        end = start + relativedelta(months=1)

        while (
            start - timedelta(minutes=self.config["MAX_SCAN_WINDOW"] + self.config["SCAN_STEP"]) < last_shock_datetime
        ):
            print(start.year, start.month)
            data = Data.get_spacecraft_data(
                spacecraft,
                start - timedelta(minutes=self.config["MAX_SCAN_WINDOW"] + self.config["SCAN_STEP"]),
                end + timedelta(minutes=self.config["MAX_SCAN_WINDOW"] + self.config["SCAN_STEP"]),
                self.config,
            )
            data.filter(self.config)

            test_datetime = start
            while test_datetime <= end:
                delta = min([np.abs(td.total_seconds()) for td in shock_datetimes - test_datetime]) / 60
                if delta < self.config["MAX_SCAN_WINDOW"] * 2:
                    test_datetime += step
                    continue
                range_data = data.range(
                    dt2ts(test_datetime - timedelta(minutes=self.config["MAX_SCAN_WINDOW"])),
                    dt2ts(test_datetime + timedelta(minutes=self.config["MAX_SCAN_WINDOW"])),
                )
                features = self.get_adaptive_features(test_datetime, range_data)

                if None not in features:
                    predicted_class = self.predictor.predict(np.array([np.hstack(features)]))[0]
                    if predicted_class == True:
                        predicted_prob = self.predictor.predict_proba(np.array([np.hstack(features)]))[0][
                            int(predicted_class)
                        ]
                        print(test_datetime, predicted_prob)
                        features_set.append(features)
                        classes_set.append(False)
                test_datetime += step

            start += relativedelta(months=1)
            end += relativedelta(months=1)

            joblib.dump(
                {"features": features_set, "classes": classes_set},
                self.config["SPACECRAFT"][spacecraft]["FALSE_POSITIVES_FEATURES_SET"],
            )

    def collect_true_negatives(self, spacecraft, monthly=True):
        spacecraft = self.config.spacecraft_from_alias(spacecraft)
        shocks = ascii.read(self.config["SPACECRAFT"][spacecraft]["TRUE_POSITIVES_LIST"])
        shock_datetimes = np.array(
            [datetime(row["col1"], row["col2"], row["col3"], row["col4"], row["col5"], row["col6"]) for row in shocks]
        )
        shock_datetimes.sort()
        first_shock_datetime = np.amin(shock_datetimes)

        features_set = []
        classes_set = []

        count = 0

        prev_year = 0
        prev_month = 0

        start = datetime(first_shock_datetime.year, first_shock_datetime.month, 1)
        end = start + relativedelta(months=1)

        bar = pyprind.ProgPercent(
            self.config["TRUE_NEGATIVES_PER_TRUE_POSITIVES"] * shock_datetimes.size, track_time=True
        )
        for shock_datetime in shock_datetimes:
            if monthly:
                if shock_datetime.year != prev_year or shock_datetime.month != prev_month:
                    start = datetime(shock_datetime.year, shock_datetime.month, 1)
                    end = start + relativedelta(months=1)
                    data = Data.get_spacecraft_data(
                        spacecraft,
                        start - timedelta(minutes=self.config["MAX_SCAN_WINDOW"] + self.config["SCAN_STEP"]),
                        end + timedelta(minutes=self.config["MAX_SCAN_WINDOW"] + self.config["SCAN_STEP"]),
                        self.config,
                    )
                    data.filter(self.config)
                    prev_year = shock_datetime.year
                    prev_month = shock_datetime.month

            count_per_shock = 0

            while count_per_shock < self.config["TRUE_NEGATIVES_PER_TRUE_POSITIVES"]:
                random_datetime = get_random_datetime(start, end)
                delta = min([np.abs(td.total_seconds()) for td in shock_datetimes - random_datetime]) / 60
                if delta < self.config["MAX_SCAN_WINDOW"] * 2:
                    continue
                if monthly:
                    range_data = data.range(
                        dt2ts(random_datetime - timedelta(minutes=self.config["MAX_SCAN_WINDOW"])),
                        dt2ts(random_datetime + timedelta(minutes=self.config["MAX_SCAN_WINDOW"])),
                    )
                else:
                    range_data = Data.get_spacecraft_data(
                        spacecraft,
                        random_datetime - timedelta(minutes=self.config["MAX_SCAN_WINDOW"]),
                        random_datetime + timedelta(minutes=self.config["MAX_SCAN_WINDOW"]),
                        self.config,
                    )
                    range_data.filter(self.config)
                features = self.get_adaptive_features(random_datetime, range_data)
                if None not in features:
                    features_set.append(features)
                    classes_set.append(False)
                    count += 1
                    count_per_shock += 1
                    bar.update()

        joblib.dump(
            {"features": features_set, "classes": classes_set},
            self.config["SPACECRAFT"][spacecraft]["TRUE_NEGATIVES_FEATURES_SET"],
        )

    def fit(self, true_positives=["ACE"], false_positives=[], true_negatives=["ACE"], save=True):
        train_features_set = []
        train_classes_set = []
        test_features_set = []
        test_classes_set = []

        if true_positives is not None:
            true_positives_features_set = []
            true_positives_classes_set = []
            for spacecraft in true_positives:
                spacecraft = self.config.spacecraft_from_alias(spacecraft)
                data = joblib.load(self.config["SPACECRAFT"][spacecraft]["TRUE_POSITIVES_FEATURES_SET"])
                true_positives_features_set += data["features"]
                true_positives_classes_set += data["classes"]
            n_true_positives = len(true_positives_features_set)
            i_train_true_positives = np.random.choice(
                np.arange(n_true_positives), int(self.config["TRAIN_RATIO"] * n_true_positives), replace=False
            )
            i_test_true_positives = np.random.choice(
                np.delete(np.arange(n_true_positives), i_train_true_positives),
                int(self.config["TEST_RATIO"] * n_true_positives),
                replace=False,
            )
            for i in i_train_true_positives:
                train_features_set.append(true_positives_features_set[i])
                train_classes_set.append(true_positives_classes_set[i])
            for i in i_test_true_positives:
                test_features_set.append(true_positives_features_set[i])
                test_classes_set.append(true_positives_classes_set[i])

        if false_positives is not None:
            false_positives_features_set = []
            false_positives_classes_set = []
            for spacecraft in false_positives:
                spacecraft = self.config.spacecraft_from_alias(spacecraft)
                data = joblib.load(self.config["SPACECRAFT"][spacecraft]["FALSE_POSITIVES_FEATURES_SET"])
                false_positives_features_set += data["features"]
                false_positives_classes_set += data["classes"]
            n_false_positives = len(false_positives_features_set)
            i_train_false_positives = np.random.choice(
                np.arange(n_false_positives), int(self.config["TRAIN_RATIO"] * n_false_positives), replace=False
            )
            i_test_false_positives = np.random.choice(
                np.delete(np.arange(n_false_positives), i_train_false_positives),
                int(self.config["TEST_RATIO"] * n_false_positives),
                replace=False,
            )
            for i in i_train_false_positives:
                train_features_set.append(false_positives_features_set[i])
                train_classes_set.append(false_positives_classes_set[i])
            for i in i_test_false_positives:
                test_features_set.append(false_positives_features_set[i])
                test_classes_set.append(false_positives_classes_set[i])

        if true_negatives is not None:
            true_negatives_features_set = []
            true_negatives_classes_set = []
            for spacecraft in true_negatives:
                spacecraft = self.config.spacecraft_from_alias(spacecraft)
                data = joblib.load(self.config["SPACECRAFT"][spacecraft]["TRUE_NEGATIVES_FEATURES_SET"])
                true_negatives_features_set += data["features"]
                true_negatives_classes_set += data["classes"]
            n_true_negatives = len(true_negatives_features_set)
            i_train_true_negatives = np.random.choice(
                np.arange(n_true_negatives), int(self.config["TRAIN_RATIO"] * n_true_negatives), replace=False
            )
            i_test_true_negatives = np.random.choice(
                np.delete(np.arange(n_true_negatives), i_train_true_negatives),
                int(self.config["TEST_RATIO"] * n_true_negatives),
                replace=False,
            )
            for i in i_train_true_negatives:
                train_features_set.append(true_negatives_features_set[i])
                train_classes_set.append(true_negatives_classes_set[i])
            for i in i_test_true_negatives:
                test_features_set.append(true_negatives_features_set[i])
                test_classes_set.append(true_negatives_classes_set[i])

        train_features_set = np.vstack(train_features_set)
        train_classes_set = np.hstack(train_classes_set)
        test_features_set = np.vstack(test_features_set)
        test_classes_set = np.hstack(test_classes_set)

        param_grid = [{"svc__C": np.logspace(0, 2, 10), "svc__gamma": np.logspace(-2, 0, 10)}]

        self._predictor = GridSearchCV(
            make_pipeline(StandardScaler().fit(train_features_set), SVC(class_weight="balanced", probability=True)),
            param_grid=param_grid,
            scoring=self.config["SCORING"],
            n_jobs=-1,
            cv=self.config["CROSS_VALIDATION"],
        )
        self.predictor.fit(train_features_set, train_classes_set)

        if save:
            joblib.dump(self.predictor, self.config["PREDICTOR"])

        if self.config["TEST_RATIO"] > 0.0:
            print("All test set score: ", self.predictor.score(test_features_set, test_classes_set))
            print(
                "Only shocks score: ",
                self.predictor.score(
                    test_features_set[test_classes_set == True], test_classes_set[test_classes_set == True]
                ),
            )
        precision, recall, _ = precision_recall_curve(
            test_classes_set, self.predictor.decision_function(test_features_set)
        )
        plt.plot(recall, precision, label="Precision-Recall curve")
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.show()

    def predict(self, spacecraft, dt):
        spacecraft = self.config.spacecraft_from_alias(spacecraft)
        data = Data.get_spacecraft_data(
            spacecraft,
            dt - timedelta(minutes=self.config["MAX_SCAN_WINDOW"]),
            dt + timedelta(minutes=self.config["MAX_SCAN_WINDOW"]),
            self.config,
        )
        data.filter(self.config)
        features = self.get_adaptive_features(dt, data)
        if None in features:
            return [False, 1.0]
        else:
            predicted_class = self.predictor.predict(np.array([np.hstack(features)]))[0]
            predicted_probability = self.predictor.predict_proba(np.array([np.hstack(features)]))[0][
                int(predicted_class)
            ]
            return [predicted_class, predicted_probability]
