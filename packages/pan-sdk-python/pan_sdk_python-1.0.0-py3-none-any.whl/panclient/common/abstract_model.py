import json
import sys


class AbstractModel(object):
    """Base class for all models."""

    def _serialize(self, allow_none=False):
        """Get all params which are not None if None is not allowed."""
        def dfs(obj):
            if isinstance(obj, AbstractModel):
                d = vars(obj)
                ret = {}
                for k in d:
                    r = dfs(d[k])
                    if allow_none or r is not None:
                        ret[k[0] + k[1:]] = r
                return ret
            elif isinstance(obj, list):
                return [dfs(o) for o in obj if allow_none or dfs(o) is not None]
            else:
                return obj.encode("UTF-8") if isinstance(obj, type(u"")) and sys.version_info[0] == 2 else obj

        return dfs(self)

    def _deserialize(self, params):
        return None

    def to_json_string(self, *args, **kwargs):
        """Serialize obj to a JSON formatted str, ensure_ascii is False by default"""
        if "ensure_ascii" not in kwargs:
            kwargs["ensure_ascii"] = False
        return json.dumps(self._serialize(allow_none=False), *args, **kwargs).encode('utf-8')

    def from_json_string(self, json_str):
        """Deserialize a JSON formatted str to a Python object"""
        params = json.loads(json_str)
        self._deserialize(params)

    def __repr__(self):
        return "%s" % self.to_json_string()
