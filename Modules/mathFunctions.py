from pygame.math import Vector2
import math

class MathFunctions:

    def __init__(self):
        pass

    def linear(self,a,b,t):
        return float((float(b) - float(a)) * float(t) + float(a))

    def sawTooth(self, a, b, t):
        # a = 32   b = 64
        # 32 - 64  - 64 - 32
        if t <= 0.5:
            return self.map(float(t),0,0.5,float(a),float(b))
        else:
            return self.map(float(t),0.5,1,float(b),float(a))

    def map(self,x,in_min,in_max,out_min,out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

    @staticmethod
    def limitVector(vector, max):
        if (vector.magnitude_squared() > max*max):
            result = vector.normalize()
            result.scale_to_length(max)
            return result
        return vector