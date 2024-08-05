
class Subset:
    '''
    Subset represents some subset on datacube
    '''
    def __init__(self, operation: str, *values):
        formatted_values = []
        for value in values:
            if isinstance(value, str):
                formatted_values.append(f'"{value}"')
            else:
                formatted_values.append(str(value))

        count = len(formatted_values)

        self.query = ""

        if count == 1:
            self.query = f'{operation}({formatted_values[0]})'
        elif count > 1:
            self.query = f'{operation}({':'.join(formatted_values)})'
        else:
            raise ValueError("No values were provided")
            