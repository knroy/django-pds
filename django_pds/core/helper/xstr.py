class xstr(str):

    """
    xstr is a subclass of string (str)
    converts string to any other types
    """

    def isbool(self):
        return self == 'True' or self == 'true' or self == 'False' or self == 'false'

    def convert_to_bool(self):
        if self == 'True' or self == 'true':
            return True
        return False

    def isint(self):
        try:
            item = int(self)
            return True
        except ValueError:
            return False

    def isfloat(self):
        try:
            item = float(self)
            return True
        except ValueError:
            return False

    def get(self):

        if self.isbool():
            return self.convert_to_bool()

        if self.isint():
            return int(self)

        if self.isfloat():
            return float(self)

        if self.startswith('\'') and self.endswith('\''):
            return self[1:len(self) - 1]

        return self.strip()
