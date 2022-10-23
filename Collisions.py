class DNode:
    def __init__(self):
        self.mass=0
        self.velocity=0
        self.poslast=0      # Position until last collision
        self.timelast=0     # Time until last collision
    def retnode(self):
        return [self.mass,self.velocity,self.poslast,self.timelast]

class HeapNode:
    # A Node class is defined
    def __init__(self):
        self.index=None       # Index to the time of collision of a pair of particles
        self.timenumber=None  # Used to denote which the pair number whose index is being stored
        self.time=0           # Used to denote the time for collision of a particular pair of particles

class heaplist:
    def __init__(self,sizelimit):
        self.sizelimit = sizelimit      # Max size of heap
        self.cur_size = 0               # Current size of heap
        self.list = [HeapNode()]*(self.sizelimit + 1)   # List comprising of tuples
        self.root = 1       # Index to root of heap
    
    def min_heapify(self, i):
        # Does heap down operation and heapifies a particular node
        if i > (self.cur_size//2):
            return

        k1=2*i
        k2=2*i+1
        a=self.list[i].time
        b=self.list[k1].time
        c=0
        if k2>self.cur_size:
            c=None
        else:
            c=self.list[k2].time

        if a==-1:
            if b!=-1 and c!=-1:
                if c!=None and b<=c:
                    self.swap(i,k1)
                    self.min_heapify(k1)
                if c!=None and c<=b:
                    self.swap(i,k2)
                    self.min_heapify(k2)
                if c==None:
                    self.swap(i,k1)
                    self.min_heapify(k1)
            if b!=-1 and c==-1:
                self.swap(i,k1)
                self.min_heapify(k1)
            if b==-1 and c!=None and c!=-1:
                self.swap(i,k2) 
                self.min_heapify(k2)
            if b==-1 and c==-1:
                self.min_heapify(k1)
                self.min_heapify(k2)
            
        if a!=-1:
            if b!=-1 and c!=-1:
                if c!=None and b<=c and a>b:
                    self.swap(i,k1)
                    self.min_heapify(k1)
                if c!=None and c<=b and a>c:
                    self.swap(i,k2)
                    self.min_heapify(k2)
                if c==None and b<a:
                    self.swap(i,k1)
                    self.min_heapify(k1)
            if b!=-1 and c==-1:
                if a>b:
                    self.swap(i,k1)
                    self.min_heapify(k1)
            if b==-1 and c!=None and c!=-1:
                if a>c:
                    self.swap(i,k2)
                    self.min_heapify(k2)
        
                    
    def swap(self,i,j):
        # Swaps any two given nodes of the heap and simultaneously maintains the index properly
        
        n1=self.list[i]
        n2=self.list[j]
        c1=n1.timenumber
        c2=n2.timenumber
        n1.timenumber,n2.timenumber=n2.timenumber,n1.timenumber
        n1.time,n2.time=n2.time,n1.time

        if c1==i and c2==j:
            n1.index,n2.index=n2.index,n1.index
        elif c1==i and c2!=j:
            self.list[n1.timenumber].index=i
            n1.index=j
        elif c1!=i and c2==j:
            self.list[n2.timenumber].index=j
            n2.index=i
        else:
            self.list[n1.timenumber].index=i
            self.list[n2.timenumber].index=j
        self.list[i]=n1
        self.list[j]=n2
        return list

    def heapup(self,i):
        k=i
        r=k//2
        while r>0:
            r=k//2
            c=self.list[r].time
            if self.list[k].time!=-1 and (c==-1 or (c!=-1 and c>self.list[k].time)):
                self.swap(k,r)
            else:
                break
            k=r
            r=r//2

    def build_heap(self): 
        for i in range(self.cur_size//2, 0, -1):
            self.min_heapify(i)

def timeforcollision(x1,x2,v1,v2):
    # Calculates time for collision of two particles
    if v1-v2<=0:
        return -1
    t=(x2-x1)/(v1-v2)
    if t<0:
        return t*-1
    return t

def velocityaftercollision(m1,m2,v1,v2):
    # Calculates velocity after a particular collision between two particles

    k1=(m1-m2)/(m1+m2)
    k2=2*m1/(m1+m2)
    k3=2*m2/(m1+m2)
    v_1=k1*v1+k3*v2
    v_2=k2*v1-k1*v2
    return [v_1,v_2]


def listCollisions(M,x,v,m,t):
    result=[]
    dic=[]
    l=len(M)
    h=heaplist(l)    
    
    # Creating dictionary list for storing the details of each particle
    for i in range(0,l+1):
        tem=DNode()
        if i==0:
            dic.append(tem)
            continue
        tem.mass=M[i-1]
        tem.velocity=v[i-1]
        tem.poslast=x[i-1]
        tem.timelast=0
        dic.append(tem)

    for i in range(1,l):        # Adding elements into a list comprising the times of collisions
        o=HeapNode()
        o.index=i
        o.timenumber=i
        o.time=timeforcollision(x[i-1],x[i],v[i-1],v[i])    # Needs to be reviewed
        h.cur_size+=1
        h.list[h.cur_size]=o
    
    h.build_heap()
        
    if h.cur_size==0 or h.list[1].time==-1:     # Checking a trivial condition
        return []
    count=0
    tim=0
    
    while True:
        
        node=h.list[1]          # Extracting most preferred node
        x=node.timenumber
        tim=node.time
        
        if tim==-1:     # Condition when there are no collisions
            break

        count+=1
        if count>m or tim>t:        # Given limits are checked
            break
        
        
        templist=velocityaftercollision(dic[x].mass,dic[x+1].mass,dic[x].velocity,dic[x+1].velocity)    # Velocities after collision b/w two masses

        # Updating the positins of the current
        dic[x].poslast=dic[x].poslast+dic[x].velocity*(tim-dic[x].timelast)
        dic[x+1].poslast=dic[x+1].poslast+dic[x+1].velocity*(tim-(dic[x+1].timelast))

        tuple=(round(tim,4),x-1,round(dic[x].poslast,4))
        result.append(tuple)        # Appending details of a particular collision to a tuple
        
        # Updating velocities of the two colliding particles
        dic[x].velocity=templist[0]
        dic[x+1].velocity=templist[1]
        
        # Updating the times of the neighbourhood collisions
        dic[x].timelast=tim
        dic[x+1].timelast=tim
        u=h.list[x].index
        h.list[u].time=-1
        h.heapup(u)
        h.min_heapify(h.list[x].index)
        
        if x>1:     # Updating time of collision for previous pair if it exits
            d=dic[x-1].poslast+dic[x-1].velocity*(tim-(dic[x-1].timelast))
            tt=timeforcollision(d,dic[x].poslast,dic[x-1].velocity,dic[x].velocity)
            if tt!=-1:
                tt+=tim
            u=h.list[x-1].index
            h.list[u].time=tt
            h.heapup(u)
            h.min_heapify(h.list[x-1].index)
        
        if x<l-1:   # Updating time of collision for next pair if it exits
            tt=timeforcollision(dic[x+1].poslast,dic[x+2].poslast+(dic[x+2].velocity)*(tim-(dic[x+2].timelast)),dic[x+1].velocity,dic[x+2].velocity)
            u=h.list[x+1].index
            if tt!=-1:
                tt+=tim
            h.list[u].time=tt
            h.heapup(u)
            h.min_heapify(h.list[x+1].index)
    return result

