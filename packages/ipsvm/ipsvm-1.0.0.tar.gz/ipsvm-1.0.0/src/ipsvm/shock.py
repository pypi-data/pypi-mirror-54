import numpy as np
from sklearn.linear_model import RANSACRegressor
from sklearn.tree import DecisionTreeRegressor


class Jump:
    def __init__(self, data, config):
        self._config = config
        self._data = data
        self._dtr = None
        self._timestamp = None
        self._before = None
        self._after = None
        self._jump = None
        self._sharpness = None

    @property
    def data(self):
        return self._data

    @property
    def dtr(self):
        if self._dtr is None and self.data.size >= self._config["MIN_POINTS"]:
            self._dtr = DecisionTreeRegressor(max_depth=1)
            self._dtr.fit(np.transpose([self.data.index]), self.data)
        return self._dtr

    @property
    def timestamp(self):
        if self._timestamp is None and self.dtr is not None:
            self._timestamp = self.dtr.tree_.threshold[0]
        return self._timestamp

    @property
    def before(self):
        if self._before is None:
            self._before = self.data.index <= self.timestamp
        return self._before

    @property
    def after(self):
        if self._after is None:
            self._after = self.data.index >= self.timestamp
        return self._after

    def is_up(self):
        data_before = self.dtr.predict([[self.data.index[0]]])[0]
        data_after = self.dtr.predict([[self.data.index[-1]]])[0]
        return data_after >= data_before

    def is_down(self):
        return not self.is_up()

    @property
    def jump(self):
        if self._jump is None and self.dtr is not None:
            data_before = self.dtr.predict([[self.data.index[0]]])[0]
            data_after = self.dtr.predict([[self.data.index[-1]]])[0]
            self._jump = np.log10(max([data_before, data_after]) / min([data_before, data_after]))
        return self._jump

    @property
    def sharpness(self):
        if (
            self._sharpness is None
            and self.dtr is not None
            and self.data.loc[self.data.index <= self.timestamp].size >= self._config["MIN_POINTS"] // 2
            and self.data.loc[self.data.index >= self.timestamp].size >= self._config["MIN_POINTS"] // 2
        ):
            area_ratio_before = (
                np.trapz(self.data[self.before] - self.data.min(), self.data.index[self.before])
                / (self.data.max() - self.data.min())
                / (self.data.index[self.before][-1] - self.data.index[self.before][0])
            )
            area_ratio_after = (
                np.trapz(self.data[self.after] - self.data.min(), self.data.index[self.after])
                / (self.data.max() - self.data.min())
                / (self.data.index[self.after][-1] - self.data.index[self.after][0])
            )
            if self.is_up():
                self._sharpness = ((1 - area_ratio_before) + area_ratio_after) / 2
            else:
                self._sharpness = ((1 - area_ratio_after) + area_ratio_before) / 2
        return self._sharpness


class FieldJump(Jump):
    def __init__(self, data, config):
        self._jitter = None
        super().__init__(data, config)

    @property
    def dtr(self):
        if self._dtr is None and self.data.size >= self._config["MIN_POINTS"]:
            self._dtr = RANSACRegressor(DecisionTreeRegressor(max_depth=1), min_samples=self.data.size - 1)
            self._dtr.fit(np.transpose([self.data.index]), self.data)
        return self._dtr

    @property
    def timestamp(self):
        if self._timestamp is None and self.dtr is not None:
            self._timestamp = self.dtr.estimator_.tree_.threshold[0]
        return self._timestamp

    @property
    def jitter(self):
        if (
            self._jitter is None
            and self.dtr is not None
            and self.data.loc[self.data.index <= self.timestamp].size >= self._config["MIN_POINTS"] // 2
            and self.data.loc[self.data.index >= self.timestamp].size >= self._config["MIN_POINTS"] // 2
        ):
            if self.is_up():
                self._jitter = 1 - (
                    np.median(self.data[self.before].diff()[1:].abs() / np.diff(self.data.index[self.before]))
                    / np.mean(self.data[self.after].diff()[1:].abs() / np.diff(self.data.index[self.after]))
                )
            else:
                self._jitter = 1 - (
                    np.median(self.data[self.after].diff()[1:].abs() / np.diff(self.data.index[self.after]))
                    / np.mean(self.data[self.before].diff()[1:].abs() / np.diff(self.data.index[self.before]))
                )
        return self._jitter


class DensityJump(Jump):
    pass


class SpeedJump(Jump):
    @property
    def jump(self):
        if self._jump is None and self.dtr is not None:
            data_before = self.dtr.predict([[self.data.index[0]]])[0]
            data_after = self.dtr.predict([[self.data.index[-1]]])[0]
            self._jump = max([data_before, data_after]) / min([data_before, data_after]) - 1
        return self._jump


class Shock:
    def __init__(self, timestamp, data, config):
        self._timestamp = timestamp
        self._field_jump = FieldJump(data.field, config)
        self._density_jump = DensityJump(data.density, config)
        self._speed_jump = SpeedJump(data.speed, config)

    @property
    def field_jump(self):
        return self._field_jump

    @property
    def density_jump(self):
        return self._density_jump

    @property
    def speed_jump(self):
        return self._speed_jump

    @property
    def features(self):
        return (
            self.field_jump.jump,
            self.field_jump.sharpness,
            self.field_jump.jitter,
            (self._timestamp - self.field_jump.timestamp) / 60 if self.field_jump.timestamp is not None else None,
            self.density_jump.jump,
            self.density_jump.sharpness,
            self.speed_jump.jump,
            self.speed_jump.sharpness,
            (self.field_jump.timestamp - self.density_jump.timestamp) / 60
            if self.field_jump.timestamp is not None and self.density_jump.timestamp is not None
            else None,
            (self.field_jump.timestamp - self.speed_jump.timestamp) / 60
            if self.field_jump.timestamp is not None and self.speed_jump.timestamp is not None
            else None,
        )
