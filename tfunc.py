#!/usr/bin/env python 

from csv import reader
from bisect import bisect_right

class TFunc():
    def __init__(self, datafile):
        self.fd_x = []
        self.fd_y = []
        try: 
            df = reader(open(datafile,'rb'),delimiter=',',quotechar='|')
        except IOError:
            print "Could not find",datafile
            exit (1)
        for line in df:
            if len(line) > 0 and len(line) < 3:
                try: 
                    x = float(line[0])
                except ValueError:
                    print "Failed to parse", line[0], "as a float in", line
                    exit(1)
                try: 
                    y = float(line[1])
                except ValueError:
                    print "Failed to parse", line[1], "as a float in", line
                    exit(1)
                self.fd_x.append(x)
                self.fd_y.append(y) 
            elif len(line) >= 3:
                print "cannot parse",line, len(line)
                exit (1)
    def lookup(self, x): 
        if x <= self.fd_x[0]:
            return self.fd_y[0]
        elif x >= self.fd_x[len(self.fd_x)-1]:
            return self.fd_y[len(self.fd_y)-1]
        else:
            i = bisect_right(self.fd_x,x) - 1
            return self.linear_interpolation(x,(self.fd_x[i],self.fd_y[i]),(self.fd_x[i+1],self.fd_y[i+1]))

    def linear_interpolation(self, x, p0, p1):
        x0 = p0[0]
        y0 = p0[1]
        x1 = p1[0]
        y1 = p1[1]
        return y0 + ((((x-x0)*y1) - ((x-x0)*y0))/(x1-x0))

if __name__ == '__main__':
    tf = TFunc('df.csv')
    print tf.lookup(-1.245)
