class VersionConverter:
    regex = "v[0-9]+"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
