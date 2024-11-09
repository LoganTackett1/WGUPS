import math

# Point class
class Point:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def tostring(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

# Main program
# Read in x and y for Point P
p = Point()
p.x = int(input())
p.y = int(input())

dx = int(input())
dy = int(input())
dd = int(input())

curr = Point()
iteration = 0

best = curr
best_dist = ((best.x-p.x)**2+(best.y-p.y)**2)**0.5
best_iteration = 0
best_unchanged_streak = 0
while best_unchanged_streak < 3:
    if (iteration + 1) % 3 == 0:
        vect = Point(dx-dd,dy-dd)
    else:
        vect = Point(dx,dy)
    new = Point(curr.x + vect.x, curr.y + vect.y)
    new_dist = ((new.x-p.x)**2+(new.y-p.y)**2)**0.5
    curr = new
    iteration += 1
    if best_dist > new_dist:
        best = new
        best_dist = new_dist
        best_iteration = iteration
        best_unchanged_streak = 0
    else:
        best_unchanged_streak += 1
    

print("Point P: " + p.tostring())
print("Arrival Point: " + best.tostring())
print("Distance between P and arrival: " + str(best_dist))
print("Number of iterations: " + str(best_iteration))
