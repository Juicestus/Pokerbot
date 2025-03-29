def graph_results(fn = 'gamelog.txt'):

    note = "Winning counts at the end of the round: , "

    totals = {}
    with open(fn, 'r') as f:
        for l in f:
            if l.startswith(note):
                p = l.replace(note, '').replace('\n', '').replace(')', '').split(', ')
                for a in p:
                    b = a.split('(')
                    k = b[0].strip()
                    v = b[1].strip()
                    if k not in totals.keys():
                        totals[k] = []
                    totals[k].append(int(v))
                   

    import matplotlib.pyplot as plt

    for k, v in totals.items():
        plt.plot(list(range(len(v))), v, '-', label=k)
       
    plt.xlabel("rounds")
    plt.ylabel("$")
    plt.legend()
    plt.title("earnings")
    #plt.show()
    plt.savefig("earnings.png")
    
if __name__ == '__main__':
    graph_results()
                    