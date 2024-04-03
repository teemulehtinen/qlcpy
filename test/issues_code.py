def array_to_power(a, p, index=None):
  if index is None:
    for i in range(len(a)):
      a[i] **= p
  else:
    a[index] = a[index] ** p
