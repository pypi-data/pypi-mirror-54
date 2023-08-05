from ..frontend import jit
import numpy as np

def CND(x):
  """
  Simpler approximation of the cumulative normal density. 
  """
  a1 = 0.31938153
  a2 = -0.356563782
  a3 = 1.781477937
  a4 = -1.821255978
  a5 = 1.330274429
  L = abs(x)
  K = 1.0 / (1.0 + 0.2316419 * L)
  w = 1.0 - 1.0/np.sqrt(2*3.141592653589793)* np.exp(-1*L*L/2.) * (a1*K +
      a2*K*K + a3*K*K*K + a4*K*K*K*K + a5*K*K*K*K*K)
  if x<0:
    w = 1.0-w
  return w

def erf(x):
  return 2 * CND(x * 1.4142135623730951) - 1

def erfc(x):
  return 2 * (1 - CND(x * 1.4142135623730951)) 

"""
P = np.asarray([
  2.46196981473530512524E-10,
  5.64189564831068821977E-1,
  7.46321056442269912687E0,
  4.86371970985681366614E1,
  1.96520832956077098242E2,
  5.26445194995477358631E2,
  9.34528527171957607540E2,
  1.02755188689515710272E3,
  5.57535335369399327526E2
])

Q = np.asarray([
  1.32281951154744992508E1,
  8.67072140885989742329E1,
  3.54937778887819891062E2,
  9.75708501743205489753E2,
  1.82390916687909736289E3,
  2.24633760818710981792E3,
  1.65666309194161350182E3,
  5.57535340817727675546E2
])

R = np.asarray([
  5.64189583547755073984E-1,
  1.27536670759978104416E0,
  5.01905042251180477414E0,
  6.16021097993053585195E0,
  7.40974269950448939160E0,
  2.97886665372100240670E0
])

S = np.asarray([
  2.26052863220117276590E0,
  9.39603524938001434673E0,
  1.20489539808096656605E1,
  1.70814450747565897222E1,
  9.60896809063285878198E0,
  3.36907645100081516050E0
])

T = np.asarray([
  9.60497373987051638749E0,
  9.00260197203842689217E1,
  2.23200534594684319226E3,
  7.00332514112805075473E3,
  5.55923013010394962768E4
])

U = np.asarray([
  3.35617141647503099647E1,
  5.21357949780152679795E2,
  4.59432382970980127987E3,
  2.26290000613890934246E4,
  4.92673942608635921086E4
])

MAXLOG = 7.09782712893383996732E2


@jit
def polevl(x, coef):
  ans = coef[0]
  for i in range(len(coef) - 1, 1, -1):
    ans = ans * x + coef[i]
  return ans


@jit
def p1evl(x, coef):
  ans = x + coef[0]
  for i in range(len(coef) - 1, 1, -1):
    ans = ans * x + coef[i]
  return ans

@jit
def ndtr(a):
  x = a * np.sqrt(2)
  z = np.abs(x)

  if z < np.sqrt(2):
    y = 0.5 + 0.5 * erf(x)
  else:
    y = 0.5 * erfc(z)

  if x > 0:
    y = 1.0 - y
  return y



def erfc(a):
  if a < 0.0:
    x = -a
  else:
    x = a

  if x < 1.0:
    return 1.0 - erf(a)

  z = -a * a
  if z < -MAXLOG:
    if a < 0:
      return 2.0
    else:
      return 0.0

  z = np.exp(z)

  if x < 8.0:
    p = polevl(x, P)
    q = p1evl(x, Q)
  else:
    p = polevl(x, R)
    q = p1evl(x, S)

  y = (z * p) / q

  if a < 0:
    y = 2.0 - y

  return y


def erf(x):
  if np.abs(x) > 1.0:
    return 1.0 - erfc(x)
  z = x * x

  y = x * polevl(z, T, 4) / p1evl(z, U, 5)
  return (y)
"""