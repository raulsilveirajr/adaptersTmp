class BaseEntity:
    def __str__(self):
        str = "\n"
        for property in self.__annotations__.items():
            property_name = f"{property[0]}"
            if hasattr(self, property_name):
                property_value = getattr(self, property_name)
                str += f"{property_name}: {property_value}\n\n"
        return str
