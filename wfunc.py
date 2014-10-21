#!/usr/bin/env python 

from csv import reader
from bisect import bisect_right

class WFunc():
    def __init__(self, datafile):
        self.time = []
        self.mag = []
        try: 
            df = reader(open(datafile,'rb'),delimiter=',',quotechar='|')
        except IOError:
            print "Could not find",datafile
            exit (1)
        for line in df:
            if len(line) > 0 and len(line) < 3:
                try: 
                    self.time.append(float(line[0]))
                    self.mag.append(float(line[1]))
                except ValueError:
                    print "Failed to parse float in", line
                    exit(1)
            elif len(line) >= 3:
                print "cannot parse",line, len(line)
                exit (1)

    def lookup(self, t): 
        if t <= self.time[0]:
            return self.mag[0]
        elif t >= self.time[len(self.time)-1]:
            return self.mag[len(self.mag)-1]
        else:
            i = bisect_right(self.time,t) - 1
            return self.linear_interpolation(t,(self.time[i],self.mag[i]),(self.time[i+1],self.mag[i+1]))

    def linear_interpolation(self, t, p0, p1):
        x0 = p0[0]
        y0 = p0[1]
        x1 = p1[0]
        y1 = p1[1]
        return y0 + ((((t-x0)*y1) - ((t-x0)*y0))/(x1-x0))

if __name__ == '__main__':
    w = WFunc('wave.csv')
    print w.lookup(.00000000195)


