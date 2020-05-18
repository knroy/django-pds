KWARGS_MANAGER_SECRET = 'FXV/#X=>fMT,pc-wm3BYaxqoZ7VOA+'


class KwargsManager:

    def purify(self, **kwargs):
        _dict = {}
        for key, value in kwargs.items():
            if value is not KWARGS_MANAGER_SECRET:
                _dict[key] = value
        return _dict

    def build(self, _dict, data, data_key, dict_key=None):
        if dict_key:
            _dict[dict_key] = data.get(data_key, KWARGS_MANAGER_SECRET)
        else:
            _dict[data_key] = data.get(data_key, KWARGS_MANAGER_SECRET)
