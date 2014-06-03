import numpy and np

class RandomSurvivalForest:


  def __init__(self, ntrees=1000, min_deaths=3, split_rule='logrank'
                percent_vars=.75, boot_size=.75, seed=NULL ):
    # TODO: check if all params are correct
    self.ntrees = ntrees
    self.trees = None
    self.min_deaths = min_deaths
    self.split_rule = split_rule
    self.percent_vars = percent_vars
    self.boot_size = boot_size
    
    # Generate random random seed if null
    if seed is NULL:
      seed = np.random.randint(0, 1000000) 
    self.seed = seed
    # Create a local random generator
    self.rgen = np.random.RandomState(self.seed)
   

  def fit(self, X, Y, split_fn_gens):
    # Should fit only be able to be called once?
    if not self.trees is None:
     raise AlreadyFit()
  
    self.X, self.Y = X, Y
    self.nd, self.np = X.shape
    self.B = np.ceil(self.nd * self.boot_size)
    self.p = np.ceil(self.np * self.percent_vars)

    # If only one generator then assume that it's the generator for all vars
    if not isinstance(split_fn_gens, list):
      split_fn_gens = [split_fn_gens]*self.np
    self.split_fn_gens = split_fn_gens

    # TODO: check if X,Y and split_fn_gens valid
    

    bs_inds = self.bootstrap_inds()
    self.trees = [self.build_tree(inds) for inds in bs_inds]

    # TODO: delete data after for space?

  def predict(self, X):
    pass

  def bootstrap_inds(self):
    return self.rgen.randint(0, self.nd, (self.ntrees, self.B))


  def build_tree(self, inds):
    #evaluate fns
    # get p candidate vars
    # generate fns for them
    # calculate split  
    # choose best

    # Randomly select candidate predictors
    preds = self.rgen.choice(self.np, size=self.p, replace=False) 
    max_val = float('-inf')
    max_fn = None
    for i in preds:
      (n_gen, fn_gen) = self.split_fn_gens[i]
      for _ in xrange(n_gen):
        fn = fn_gen()
        split_val = self.split_val_fn(fn(self.X(inds, preds)), self.Y(inds,:))
        if split_val > max_val:
          max_val = split_val
          max_fn = fn
    

  
class Node:

  # range of split_fn is domain of child_map
  # TODO: throw errors when input incorrect
  def __init__(self, split_fn=None, child_map=None, chf=None):
    if split_fn is None:
      self.terminal = True
      self.chf = chf
    else: 
      self.split_fn = split_fn
      self.child_map = child_map

  def prop_down(self, x):
    if self.terminal:
      return self
    else: 
      return self.child_map[self.split_fn(x)].prop_down(x)

  def chf(self):
    return self.chf
