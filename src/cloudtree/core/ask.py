


def ask(question, default=None, required=True):

    if default is not None:
        question += ' [%s]' % (str(default))
    if not question.endswith(' '):
        question += ' '

    while True:
        answ = input(question).strip()
        if len(answ) == 0:
            if required:
                print("Answer required")
            else:
                return default
        else:
            return answ


def ask_yn(question, default=None, required=True):

    if default is not None:
        if default:
            default = 'yes'
        else:
            default = 'no'

    while True:

        answ = ask(question, default, required)

        if answ is None:
            return None
        elif answ.lower() in ('y', 'yes'):
            return True
        elif answ.lower() in ('n', 'no'):
            return False

        print("Answer must be yes or no")


def ask_choose(question, options, default=None, required=True):

    question = question + "\n"
    for i, option in enumerate(options):
        question += " %d) %s\n" % (i+1, option)
    question += "\n"

    while True:
        answ = ask(question, default, required)

        # First, try direct match
        if answ in options:
            return answ

        # Second, try by index
        try:
            return options[int(answ)-1]
        except:
            pass

        print ("Not a valid option")


