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
  
    # TODO: check if X,Y and split_fn_gens valid 
    
    # TODO: sorting might be irrelevant since bootstrap sample
    #  ...  bootstrap is now sorted, but make sure sorting isn't messed up elsewhere  
    # Sort data by survival time
    sorted_inds = np.argsort(Y(:,0))
    self.X, self.Y = X(sorted_inds, :), Y(sorted_inds, :)

    self.nd, self.np = X.shape
    self.B = np.ceil(self.nd * self.boot_size)
    self.p = np.ceil(self.np * self.percent_vars)

    
    # If only one generator then assume that it's the generator for all vars
    if not isinstance(split_fn_gens, list):
      split_fn_gens = [split_fn_gens]*self.np
    self.split_fn_gens = split_fn_gens


    bs_inds = self.bootstrap_inds()
    self.trees = [self.build_tree(inds) for inds in bs_inds]
    self.bs_inds = bs_inds

    # TODO: delete data after for space?

  def predict(self, X):
    pass

  def bootstrap_inds(self):
    return np.sort(self.rgen.randint(0, self.nd, (self.ntrees, self.B)), axis=1)


  def build_tree(self, inds):
    curr_X = self.X(inds,:)
    curr_Y = self.Y(inds, :)

    # Check if terminating condition is met 
    death_inds = np.nonzero(curr_Y)
    if len(death_inds) < self.min_deaths:
      return None

    # Randomly select candidate predictors
    preds = self.rgen.choice(self.np, size=self.p, replace=False) 

    # Generate split functions and search for max split
    max_val = float('-inf')
    max_fn = None
    max_pred_split = None
    max_T_inds = None
    max_F_inds = None
    for p in preds:
      (n_gen, fn_gen) = self.split_fn_gens[p]
      for _ in xrange(n_gen):
        fn = fn_gen()
        # map predictor given function
        pred_split = fn(curr_X(:, p))
        T_inds = np.nonzero(pred_split)
        F_inds = np.nonzero(pred_split==False)
        split_val = self.split_val_fn(T_inds, death_inds, curr_Y)
        if split_val > max_val:
          max_val = split_val
          max_fn = fn
          max_T_inds = T_inds
          max_F_inds = F_inds
          max_pred_split = pred_split


    T_node = build_tree(max_T_inds)
    F_node = build_tree(max_F_inds)

    # Check if this is a terminal node
    if None in [T_node, F_node]:
      # TODO: calculate chf
      chf = True
      return Node(chf=chf) 
    else: 
      return Node(split_fn=max_fn, child_map={True: T_node, False:F_node})
    

  
class Node:

  # range of split_fn is domain of child_map
  # TODO: throw exception when input incorrect
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
