import sys

from numpy import linalg as la

from gauss import *
from utils import formatting, str_to_row, get_step_and_master_count

inp = open('input.txt', 'r')
out = open('output.txt', 'w')

comm = MPI.COMM_WORLD
master = 0
A, b, rows = [], [], []

if comm.rank == master:
    n = int(inp.readline())

    for line in inp:
        A.append(str_to_row(line[:-2]))
        b.append(int(line[-2:-1]))

    det = la.det(np.array(A))

    if not det:
        print formatting(comm.rank, 'ERROR! det A = {} - there is no inversion'.format(det))
        comm.bcast(0, root=master)
        sys.exit()

    comm.bcast(n, root=master)

    step, master_count = get_step_and_master_count(n, comm.size)

    rows = [A[i] + [i] for i in range(master_count)]

    cur = master_count
    for proc in range(1, comm.size):
        for i in range(step):
            comm.send(A[cur + i] + [cur + i], dest=proc)  # send row with index as last element
        cur += step

else:
    n = comm.bcast(None, root=master)
    step = n / comm.size

    if not step:
        sys.exit()

    for i in range(step):
        rows.append(comm.recv(source=master))
