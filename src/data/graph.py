import matplotlib.pyplot as plt
import csv

def main():
  ys = []
  xs = []
  markers_on = []
  with open('data-0.csv', 'r') as f:
    for i, line in enumerate(f):
      vals = line.split()
      y = vals[2]
      if y is not None:
        try:
          y = float(y)
          ys.append(y)
        except ValueError:
          msg = vals[len(vals) - 1]

          if msg == 'pre':
            markers_on.append(i)

          ys.append(ys[len(ys) - 1])
        xs.append(vals[1])

  plt.plot(xs, ys, marker='o', markevery=markers_on, markersize=50)
  plt.show()

if __name__ == '__main__':
  main()

