import numpy as np

def logrank(T_inds, death_inds, Y):
  # This assumes that Y is sorted by survival time (0th column of Y)
  # TODO: Could we get a signigicant speed up if we do all candidate 
  # variables at once?

  numerator = 0.0
  denom = 0.0

  nsamples, _ = Y.shape

  T_deaths_before_i = 0.0
  T_tot = T_alive_before_i = float(len(T_inds))
  deaths_tot_before_i = 0.0
  deaths_tot = float(len(death_inds))
  alive_tot_before_i = float(nsamples )

  T_d_i = 0
  d_i = 0
  i = 0

  while d_i < deaths_tot:
    # Check if current event is a death
    print T_deaths_before_i, T_alive_before_i, deaths_tot_before_i, alive_tot_before_i
    if i == death_inds[d_i]:
      numerator += T_deaths_before_i - \
                  (T_alive_before_i) * (deaths_tot_before_i/alive_tot_before_i)

      prop_alive_T = T_alive_before_i/alive_tot_before_i

      denom +=  (prop_alive_T) * (1 - prop_alive_T) \
              * ( (alive_tot_before_i - deaths_tot_before_i) \
                  /(alive_tot_before_i - 1) \
                ) \
              * deaths_tot_before_i

      d_i += 1
      deaths_tot_before_i += 1
      alive_tot_before_i -= 1
      
      # Check if death is a True case
      if T_d_i < T_tot and i == T_inds[T_d_i]:
        T_d_i += 1
        T_deaths_before_i += 1
        T_alive_before_i -= 1

    else:
      if T_d_i < T_tot and i == T_inds[T_d_i]:
        T_d_i += 1
  
    print numerator, denom
    i += 1
    print

  return numerator, denom
     
