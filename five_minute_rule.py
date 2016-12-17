import math
import matplotlib
import matplotlib.pyplot as plt

B  = float(1  )
KB = float(1e3)
MB = float(1e6)

LINEWIDTH = 4

"""
page_size     : bytes / page
ram_price     : dollars / byte
access_price  : dollars / (page/s)
mem_size      : bytes
access_period : second
"""
class Disk(object):
    def __init__(self, page_size=4*KB, ram_price=5/KB, access_price=2000):
        self.page_size    = float(page_size)
        self.ram_price    = float(ram_price)
        self.access_price = float(access_price)

    def __str__(self):
        page_size = "${}\\frac{{KB}}{{page}}$".format(self.page_size / KB)
        ram_price = "$\\frac{{\\${}}}{{KB\\ RAM}}$".format(self.ram_price * KB)
        access_price = "$\\frac{{\\${}}}{{(page/second)}}$".format(self.access_price)
        return "{}; {}; {}".format(page_size, ram_price, access_price)

def disk_cost(disk, mem_size, access_period):
    num_pages = math.ceil(mem_size / disk.page_size)
    return num_pages / access_period * disk.access_price

def ram_cost(disk, mem_size):
    return mem_size * disk.ram_price

def break_even(disk, mem_size):
    num_pages = math.ceil(mem_size / disk.page_size)
    return num_pages * disk.access_price / (ram_cost(disk, mem_size))

def plot_costs(disk, mem_size, filename):
    access_periods = range(60, 60 * 15)
    disk_costs = [disk_cost(disk, mem_size, ap) for ap in access_periods]
    ram_costs = [ram_cost(disk, mem_size) for _ in access_periods]

    plt.figure()
    plt.plot(access_periods, disk_costs, linewidth=LINEWIDTH, label="disk costs")
    plt.plot(access_periods, ram_costs, linewidth=LINEWIDTH, label="RAM costs")
    plt.gca().set_ylim([0, 60])
    plt.legend()
    plt.grid()
    plt.xlabel("Access Period (seconds)")
    plt.ylabel("Cost (dollars)")
    plt.savefig(filename)

def plot_break_even(disks):
    plt.figure()
    mem_sizes = [i * KB for i in range(1, 21)]

    for disk in disks:
        break_evens = [break_even(disk, mem_size) for mem_size in mem_sizes]
        plt.plot(mem_sizes, break_evens, linewidth=LINEWIDTH, label=str(disk))

    plt.grid()
    plt.legend()
    plt.xlabel("Memory Size (bytes)")
    plt.ylabel("Break Even (seconds)")
    plt.savefig("break-even.pdf")

def main():
    matplotlib.rcParams.update({'font.size': 20})
    disk = Disk()
    for i in range(1, 9):
        plot_costs(disk, i * KB,  "costs-{:02d}KB.pdf".format(i))

    matplotlib.rcParams.update({'font.size': 16})
    plot_break_even([
        Disk(),
        Disk(page_size=6*KB),
        Disk(ram_price=4/KB),
        Disk(access_price=1500),
    ])

if __name__ == "__main__":
    main()
