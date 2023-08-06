import numpy as np
import datetime as dt
import inspect

__version__ = "0.0.2"
__author__ = "toby.devlin@bmtglobal.com, jonah.chorley@bmtglobal.com"
__aus_date__ = "%d/%m/%Y %H:%M:%S"


def dump(obj):
    """
    A function for printing the methods and properties (instance variables) of an object:

        dump(obj)

    :param obj: Any python object
    """
    methods = []
    properties = []

    for attr in dir(obj):
        if hasattr(obj, attr) and '__' not in attr:
            if callable(getattr(obj, attr)):
                methods.append(attr)
            else:
                properties.append(attr)

    print('Methods:')
    for attr in methods:
        print("obj.{}".format(attr))
    print('\nProperties:')
    for attr in properties:
        print("obj.{}".format(attr))


def get_main():
    frames = [stack[0] for stack in inspect.stack()]
    for frame in frames:
        module = inspect.getmodule(frame)
        if module.__name__ == '__main__':
            return module

    return None


def get_object(name):
    module = get_main()
    if hasattr(module, name):
        return getattr(module, name)
    else:
        return None


def get_date_time(in_array, fmt='%d/%m/%Y %H:%M:%S'):
    # Basic input parameters
    in_array = np.array(in_array, ndmin=1)
    arr_type = in_array.dtype.type
    arr_shape = in_array.shape

    # Initialize conversion logic
    from_str = False
    from_num = False

    # Determine conversion logic
    if arr_type is np.str_:
        from_str = True
    else:
        from_num = True

    # Initialize output array
    out_array = np.empty(arr_shape, dtype=np.object)

    # If from string -> datetime
    if from_str:
        for ii in range(in_array.size):
            out_array[ii] = dt.datetime.strptime(in_array[ii], fmt)

    # If from number -> datetime
    if from_num:
        epoch = dt.datetime(1970, 1, 1)
        in_array = in_array.astype(np.float64)
        for ii in range(in_array.size):
            delta = dt.timedelta(seconds=in_array[ii])
            out_array[ii] = epoch + delta

    return out_array


def get_date_str(in_array, fmt='%d/%m/%Y %H:%M:%S'):
    # Basic input parameters
    in_array = np.array(in_array, ndmin=1)
    arr_type = in_array.dtype.type
    arr_shape = in_array.shape

    # Convert any numbers to datetime
    if arr_type is not np.object_:
        in_array = get_date_time(in_array)

    # Initialize output array
    str_check = in_array[0].strftime(fmt)
    d_type = '<U{:d}'.format(len(str_check))
    out_array = np.empty(arr_shape, dtype=d_type)

    # Convert datetime to string
    for ii in range(in_array.size):
        out_array[ii] = in_array[ii].strftime(fmt)

    return out_array


def get_date_num(in_array, fmt='%d/%m/%Y %H:%M:%S'):
    # Basic input parameters
    in_array = np.array(in_array, ndmin=1)
    arr_type = in_array.dtype.type
    arr_shape = in_array.shape

    # Convert any numbers to datetime
    if arr_type is not np.object_:
        in_array = get_date_time(in_array, fmt)

    # Initialize output array
    out_array = np.empty(arr_shape, dtype=np.float64)

    # Convert datetime to number
    epoch = dt.datetime(1970, 1, 1)
    for ii in range(in_array.size):
        delta = in_array[ii] - epoch
        out_array[ii] = delta.total_seconds()

    return out_array


class Expression:

    @classmethod
    def decorator(cls, function_call):

        def wrapper(*args, **kwargs):
            # Basic preparation
            args = list(args)
            expression = None
            index = None

            # Find expressions in input arguments
            for ii, arg in enumerate(args):
                if type(arg).__name__ == cls.__name__:
                    expression = arg
                    index = ii

            # Evaluate output based on expression
            if expression is None:
                output = function_call(*args, **kwargs)
            else:
                eval_args = list()
                for ii in range(len(expression.variables)):
                    args[index] = expression.variables[ii]
                    if expression.is_defined[ii]:
                        eval_args.append(get_object(args[index]))
                    else:
                        eval_args.append(function_call(*args, **kwargs))
                output = expression.evaluate(*eval_args)

            return output

        return wrapper

    def __init__(self, expression):
        self.expression = expression
        self.__interpret__()

    def __interpret__(self):
        # Define legal operations, functions and characters
        ops = ['**', '*', '/', '+', '-']
        chars = ['[', ']', '(', ')', ' ', "'", ':']
        funcs = ['hyp', 'dot', 'vec', 'sum']
        calls = ['np.hypot', 'np.dot', 'np.column_stack', 'np.sum']

        # Determine variables that exist in expression string
        string = self.expression
        for op in ops:
            string = string.replace(op, ',')
        for other in funcs + chars:
            string = string.replace(other, '')
        self.variables = string.split(',')

        # Remove constants
        for string in self.variables:
            try:
                float(string)
                is_num = True
            except ValueError:
                is_num = False
            if is_num:
                self.variables.remove(string)

        # Find if any variables that are defined in main name space
        self.is_defined = list()
        for variable in self.variables:
            handle = get_object(variable)
            if handle is None:
                self.is_defined.append(False)
            else:
                self.is_defined.append(True)

        # Determine the evaluation string
        argument_fmt = 'args[{}]'
        self.string = self.expression
        for aa, variable in enumerate(self.variables):
            place_holder = variable
            replace_with = argument_fmt.format(aa)
            self.string = self.string.replace(place_holder, replace_with)
        for aa, func in enumerate(funcs):
            place_holder = func
            replace_with = calls[aa]
            self.string = self.string.replace(place_holder, replace_with)

    def evaluate(self, *args):
        return eval(self.string)


def unsupported_decorator(function_call):

    def wrapper(*args):
        name = function_call.__name__
        message = '{} is currently not supported'.format(name)
        print(message)

    return wrapper


def timer_decorator(function_call):

    name = function_call.__name__
    message = '{} took {}s to execute'

    def wrapper(*args, **kwargs):
        ts = dt.datetime.now().timestamp()
        output = function_call(*args, **kwargs)
        te = dt.datetime.now().timestamp()
        print(message.format(name, te - ts))

        return output

    return wrapper
