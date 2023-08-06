def pop_argument(args, index=0):
    if index >= len(args):
        return None
    
    return args.pop(index)


def pop_option(args, option, short=None, default=None, vtype=str):
    if type(option) == list:
        selectors = ['--' + opt for opt in option]
    else:
        selectors = ['--' + option]

    if short is not None:
        selectors.append('-' + short)

    index = next((i for i in xrange(len(args)) if args[i] in selectors), None)
    if index is None or index == len(args) - 1:
        return default

    value = args.pop(index + 1)
    selector = args.pop(index)
    
    return vtype(value)


def pop_flag(args, flag, short=None):
    selectors = ['--' + flag]
    if short is not None:
        selectors.append('-' + short)

    index = next((i for i in xrange(len(args)) if args[i] in selectors), None)
    if index is None:
        return False

    args.pop(index)
    return True


