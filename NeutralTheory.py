import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import bernoulli 

def Variation_Reproduction(Distribution,FSr):    
    #Distribution of reproduction-based population augmentation    
    #each array element is the index of the population increased by one
    reproduction = np.random.choice(
         a=[q for q in range(len(Distribution))],size=FSr,  
         p=[q/np.sum(Distribution) for q in Distribution])     
    #variation of the distribution caused by reproduction
    Dr = [np.sum(reproduction==q) for q in range(len(Distribution))]   
    return Dr

def Variation_Migration(Distribution,FSm,D_mainland):  
    #Distribution of migration-based population augmentation  
    #each array element is the index of the population increased by one
    migration = np.random.choice(
         a=[q for q in range(len(D_mainland))],size=FSm,  
         p=[q/np.sum(D_mainland) for q in D_mainland]) 
    #variation of the distribution caused by migration
    Dm = [np.sum(migration==q) for q in range(len(Distribution))] 
    return Dm
def FillingProcesses_Distribution(Distribution,TotalSlots,m,k):
    #determination of the probabilities of filling processes
    FS = TotalSlots-np.sum(Distribution) #Free slots
    data = np.random.choice( #migration, reproduction,speciation 
         a=[0, 1, 2],size=FS,  
         p=[m*(1-k), (1-m)*(1-k),k] ) 
    FSm = len([q for q in data if q==0]) #places filled by migration
    FSr = len([q for q in data if q==1]) #places filled by reproduction
    FSs = len([q for q in data if q==2]) #places filled by speciation
    if FSm+FSr+FSs!=FS: #check of the good categorical distribution
        print("Issue with the distribution of filling procedures")
    #output : migration,reproduction,speciation
    return FSm,FSr,FSs
def Variation_Death(Distribution,Pd):
    #death process at the population level
    Dd = [0]*len(Distribution)
    for i in range(len(Distribution)):
        Dd[i] = np.sum(bernoulli.rvs(Pd, 1-Pd,Distribution[i]))
    return np.asarray(Dd)
#%%
Pb = 0.1 #birth rate
Pd = 0.01 #death rate
Pm = 0.1 #migration rate
Ps = 0.1 #speciation rate
m=0.2 #migration-filling probability
k=0.00 #speciation-filling probability
D_mainland = [1000,1000,1000,1000,1000,
              1000,1000,1000,1000,0] #mainland species distribution probability
T = 1000 #number of timesteps
rv = bernoulli.rvs(Pd, 1-Pd) 

N=10*100 #total number of individuals on an island

Distribution = [50,50,50,150,150,150,100,100,100,100]
DH = [[0]*len(Distribution)]*T
DH[0] = Distribution

for i in range(1,T):
    #Variation with death
    Dd = Variation_Death(Distribution,Pd)
    Distribution = Distribution-Dd
    #Variation with birth,migration,speciation
    FS = FillingProcesses_Distribution(Distribution,N,m,k)
    Dr = Variation_Reproduction(Distribution,FS[1])
    Dm = Variation_Migration(Distribution,FS[0],D_mainland)
    #Lacking : speciation
    Distribution = Distribution + Dr + Dm
    DH[i] = np.asarray(Distribution)
    
DH = np.asarray(DH)


fig=plt.figure(figsize=(12,8))
for ii in range(10):
    plt.plot(DH[:,ii])
    
plt.show()