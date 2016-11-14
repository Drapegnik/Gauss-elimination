import time


def str_to_row(s):
    return [int(x) for x in s.split()]


def get_step_and_master_count(n, size):
    """
    Count number of rows per process
    :param n: matrix dimension
    :param size: number of process
    :return: number of rows for slave and for master
    """
    step = n / size
    return step, step + n % size


def rank_from_row(n, size, i):
    """
    Count rank of process that work with row
    :param n: matrix dimension
    :param size: number of process
    :param i: row index
    :return: process rank
    """
    step, master_count = get_step_and_master_count(n, size)

    if i < master_count:
        return 0

    i -= master_count
    return 1 + i // step


class Colors:
    HEADER = '\033[1;95m'
    OKBLUE = '\033[1;94m'
    OKGREEN = '\033[1;92m'
    WARNING = '\033[1;93m'
    FAIL = '\033[1;91m'
    CYAN = '\033[1;96m'
    ENDC = '\033[0m'


def formatting(rank, message):
    template = '${color} {name}{end_color}: {message}'

    return template.format(
        color=(Colors.FAIL if rank == 0 else Colors.OKGREEN),
        name=('master' if rank == 0 else 'proc{}'.format(rank)),
        end_color=Colors.ENDC,
        message=message
    )


def format_action(action, rows):
    if len(rows) < 4 and len(rows[0]) < 10:
        return '\t*{0}*\t{1} rows: {2}'.format(action, len(rows), [x[:-1] for x in rows])
    else:
        return '\t*{0}*\t{1} rows'.format(action, len(rows))


class Timer:
    def __init__(self, message):
        self.message = message
        self.start = time.time()

    def finish(self):
        print "\n{0}: {1:.3f} s\n".format(self.message, (time.time() - self.start)) + "-" * 50
