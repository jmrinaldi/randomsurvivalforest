import numpy as np

def binary_gen():
  fn_gen = lambda _: lambda data: data == 1
  return (1, fn_gen)

def discrete_gen(vals):
  fn_gen = lambda n: lambda data: data == vals[n]
  return (len(vals), fn_gen)

def real_range_gen(ngen, low, high, random_gen=None):
  if random_gen is None:
    random_gen = np.random

  val_gen = lambda : low + (high-low) * random_gen.rand()
  fn_gen = lambda n: lambda data: data < val_gen()

  return (ngen, fn_gen)
