from django.shortcuts import render
from django.http import HttpResponse
import time
import sys,math

# ----------------------- Global Variables --------------------------

rows,cols = (10,5)
r1 = r2 = r3 = r4 = r5 = 0
nop = 0
nor = 0
INT_MAX = 9999999
original_time = 0
optimised_time = 0

alloc = [[0 for i in range(cols)] for j in range(rows)]
maxneed = [[0 for i in range(cols)] for j in range(rows)]
needed = [[0 for i in range(cols)] for j in range(rows)]
initialavailable = [0]*cols
original_result = [] 
optimised_result = []

 
#  ----------------------------- Front Page ------------------------------------------------------------------------
def index(request):
    return render(request,'index.html')
# ------------------------------------------------------------------------------------------------------------------

# --------------------------- Taking Input from the user -----------------------------------------------------------
def input(request):
    global r1,r2,r3,r4,r5  
    global nop
    global nor
    global alloc
    global maxneed
    nop = 0
    nor = 0
    r1 = r2 = r3 = r4 = r5 = 0
    for i in range(nop):
        for j in range(nor):
            alloc[i][j] = 0
            maxneed[i][j] = 0
    context = {
        "nop" : nop,
        "nor" : nor,
        "r1" : r1,
        "r2" :r2,
        "r3" : r3,
        "r4" :r4,
        "r5" : r5,
        "alloc" : alloc,
        "maxneed":maxneed
    }
    response = request.method
    if response == "POST":
        nop = (int)(request.POST['nop'])
        nor = (int)(request.POST['nor'])
        r1 = (int)(request.POST['r1'])
        r2 = (int)(request.POST['r2'])
        r3 = (int)(request.POST['r3'])
        r4 = (int)(request.POST['r4'])
        r5 = (int)(request.POST['r5'])

        for i in range(10):
            for j in range(5):
                val = i*10 + j
                x = str(val)
                numalloc = (int)(request.POST[x])
                nummax = (int)(request.POST['m'+x])
                alloc[i][j] = numalloc
                maxneed[i][j] = nummax

        context = {
            "nop" : nop,
            "nor" : nor,
            "r1" : r1,
            "r2" :r2,
            "r3" : r3,
            "r4" :r4,
            "r5" : r5,
            "alloc" : alloc,
            "maxneed": maxneed
        }

    return render(request,'input.html',context)
# ------------------------------------------------------------------------------------------------------------------

# ------------------------ Helper function for Optimized Algorithm -------------------------------------------------
def count_sort(a,n,pos,idx):
	# // pos signify the pos(taking 0 as rightmost digit) of digit into consideration
    div = pow(10, pos)
    # // count sort lgana hai on the basis of num
    freq = [0]*10
    position = [0]*10

    for i in range(n):
        x = (a[idx[i]] // div) % 10
        freq[x] += 1

    final = [0]*(n)

    position[0] = 0
    for i in range(1,10):
        position[i] = position[i - 1] + freq[i - 1]

    for i in range(n):
        final[position[(a[idx[i]] // div) % 10]] = idx[i]
        position[(a[idx[i]] // div) % 10] += 1

    for i in range(n):
        idx[i] = final[i]
def radiax_sort(a ,n):
    maxele = 1
    for i in range(n):
        maxele = max(maxele, a[i])

    maxdig = (int)(math.log10(maxele))
    # // log10(999)=3
    idx = [0]*(n)
    for i in range(n):
        idx[i] = i

    for i in range(maxdig+1):
        count_sort(a, n, i, idx)

    return idx
def compute(available_resource,m):
    ans = INT_MAX
    for i in range(m):
        ans = min(ans, available_resource[i])

    return ans
# ------------------------------------------------------------------------------------------------------------------

# ------------------------- Function for Original Bankers Algorithm ------------------------------------------------
def originalBanker():
    global rows,cols,alloc,maxneed,r1,r2,r3,r4,r5,needed,initialavailable,original_result
    original_result.clear()
    available = [0]*nor
    for i in range(nor):
        available[i] = initialavailable[i]

    f = [0]*(nop+1) # number of processes completed
    ans = [0]*(nop+1) # safe sequence if exist
    isDeadLock = 0 # to check if the deadlock exist or not
    cnt = 0 
    ind = 0 # index for the safe sequence
    
    while(cnt < nop-1):
        ac = 0 # to check if there is any change or not 
        for i in range(nop):
            if(f[i] == 0):
                cangive = 1
                for j in range(nor):
                    if(needed[i][j] > available[j]):
                        cangive = 0
                        break  
                if(cangive == 1):
                    ans[ind] = i
                    ind = ind + 1
                    s = f"Granted for P{i+1} ✅"
                    original_result.append(s)
                    s = "Now Available Resources : "
                    for j in range(nor):
                        available[j] += alloc[i][j]
                        s += str(available[j]) + ", "

                    f[i] = 1
                    ac = 1
                    original_result.append(s)    
                else:
                    s = f"Denied for P{i+1} ❌"
                    original_result.append(s)    
        if(ac == 0):
            for i in range(nop):
                if(f[i] == 0):
                    isDeadLock = 1
                    break
            break   
        cnt = cnt + 1

    original_result.append("Analyzing")
    if(isDeadLock):
        s = " 💀💀 DeadLock has Occured 💀💀"
        original_result.append(s)
        if(ind == 0):
            s =  "No Process can be terminated"
            original_result.append(s)

        else:
            s = ""
            for i in range(ind-1):
                s += f"P{ans[i]+1} , "
            s += f"P{ans[ind-1]+1} can be terminated but rest cannot be terminated. Hence DeadLock"
            original_result.append(s) 
    else:
        original_result.append("✅ System is Safe ✅")
        s = "Safe Sequence ▶ "
        for i in range(nop-1):
            s += f"P{ans[i]+1}   ↣   "  
        s += f"P{ans[nop-1]+1}"
        original_result.append(s)

    pass
# ------------------------------------------------------------------------------------------------------------------

# ------------------------  Function for Proposed Optimized Bankers Algorithm --------------------------------------
def optimizedBanker():
    global rows,cols,alloc,maxneed,r1,r2,r3,r4,r5,needed,initialavailable,optimised_result
    optimised_result.clear()
    available_resource = [0]*nor
    for i in range(nor):
        available_resource[i] = initialavailable[i]

    safe_sequence = []
    completed_process = [0]*(nop)
    maximum_needed_allocation = [0]*(nop)
    minimum_available = INT_MAX
    for i in range(nop):
        imax = 0
        for j in range(nor):
            imax = max(imax, needed[i][j])
        maximum_needed_allocation[i] = imax
    process = radiax_sort(maximum_needed_allocation, nop)
    isDeadLock = False

    # -------------- Main Algorithm -------------------
    for i in range(nop) :
        if (maximum_needed_allocation[i] <= minimum_available and completed_process[process[i]] == 0) :
            completed_process[process[i]] = 1
            safe_sequence.append(process[i])
            s = f"Granted for P{process[i]+1} ✅"
            optimised_result.append(s)
            s = "Now Available Resources : "
            for j in range(nor) :
                available_resource[j] = available_resource[j] + alloc[process[i]][j]
                s += str(available_resource[j]) + ", "
            optimised_result.append(s)
            minimum_available = compute(available_resource,nor)
        else:
            j = 0
            while(j<nor):
                if (needed[process[i]][j] <= available_resource[j]):
                    j += 1
                    continue 
                else:
                    break
            if (j == nor):
                completed_process[process[i]] = 1
                safe_sequence.append(process[i])
                s = f"Granted for P{process[i]+1} ✅"
                optimised_result.append(s)
                s = "Now Available Resources : "
                for j in range(nor):
                    available_resource[j] = available_resource[j] + alloc[process[i]][j]
                    s += str(available_resource[j]) + ", "
                optimised_result.append(s)
                
                minimum_available = compute(available_resource,nor)
            else:
                isDeadLock = True
                break        
    # -------------------------------------------------

    #  --- Checking if there is any process left ------
    for i in range(nop):
        # // If anyone of them remains incomplete then deadlock
        if (completed_process[i] == 0):
            isDeadLock = True
            break
    #  ------------------------------------------------

    optimised_result.append("Analyzing")
    if(isDeadLock):
        s = " 💀 DeadLock has Occured 💀"
        optimised_result.append(s)
        if(len(safe_sequence) == 0):
            s =  "No Process can be terminated"
            optimised_result.append(s)
        else:
            s = ""
            for i in range(len(safe_sequence)-1):
                s += f"P{safe_sequence[i]+1} , "
            s += f"and P{safe_sequence[len(safe_sequence)-1]+1} can be terminated but rest cannot be terminated. Hence DeadLock"
            optimised_result.append(s)
    else:
        optimised_result.append("✅ System is Safe ✅")
        s = "Safe Sequence ▶ "
        for i in range(len(safe_sequence)-1):
            s += f"P{safe_sequence[i]+1}   ↣   "  
        s += f"P{safe_sequence[len(safe_sequence)-1]+1}"
        optimised_result.append(s)
    pass
# ------------------------------------------------------------------------------------------------------------------

# ------------------------------ Simulator to Simulate both the algorithms -----------------------------------------
def simulator(request):
    global rows,cols,alloc,maxneed,r1,r2,r3,r4,r5,needed,initialavailable,original_result,optimised_result
    global original_time,optimised_time
    nres = []
    for i in range(cols):
        nres.append(i+1)
    
    pval = {}

    # -------- Calculating the Needed Matrix ----------------------
    for i in range(nop):
        for j in range(nor):
            needed[i][j] = maxneed[i][j] - alloc[i][j]
    # --------------------------------------------------------------
    
    for i in range(nop):
        pval[i] = {
            'pid' : i+1,
            'array' : needed[i]
        }

    # ------ calculating the available Resources --------------------
    for i in range(nor):
        sum = 0
        for j in range(nop):
            sum = sum + alloc[j][i]
        if(i == 0):
            initialavailable[i] = r1 - sum
        elif(i == 1):
            initialavailable[i] = r2 - sum
        elif(i == 2):
            initialavailable[i] = r3 - sum
        elif(i == 3):
            initialavailable[i] = r4 - sum
        elif(i == 4):
            initialavailable[i] = r5 - sum
    # ---------------------------------------------------------------

    # --------------- Original Bankers Algorithm --------------------
    import timeit
    x = 0
    for i in range(100):
        start = timeit.default_timer()
        originalBanker()
        # y = 0
        # while(y<10000000):
        #     y += 1
        # time.sleep(0.01)
        end = timeit.default_timer()
        x += (end - start)*1000
    original_time = x / 100
    #  ---------------------------------------------------------------

    # ------------- optimised bankers algorithm ----------------------
    x = 0
    for i in range(100):
        start = timeit.default_timer()
        optimizedBanker()
        # time.sleep(0.01)
        end = timeit.default_timer()
        x += (end - start)*1000
    optimised_time = x / 100

    # ----------------------------------------------------------------
    context = {
        "nres" : nres,
        "alloc" : alloc,
        'pval' : pval,
        "avail" : initialavailable,
        "original": original_result,
        "original_time":original_time,
        "optimised":optimised_result,
        "optimised_time":optimised_time
    }

    return render(request,'simulator.html',context)


def graph(request):

    context = {
        "optimised_time": optimised_time,
        "original_time":original_time,
        "input": (nor*nop)
    }
    return render(request,'graph.html',context)