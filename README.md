# Banker's-Algorithm-Project
![frontpage](/first.PNG)
## Code For Original Banker's Algorithm (Python)
      global rows,cols,alloc,maxneed,r1,r2,r3,r4,r5,needed,initialavailable,original_result
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
                      print(s)
                      s = "Now Available Resources : "
                      for j in range(nor):
                          available[j] += alloc[i][j]
                          s += str(available[j]) + ", "

                      f[i] = 1
                      ac = 1
                      print(s)    
                  else:
                      s = f"Denied for P{i+1} ❌"
                      print(s)    
          if(ac == 0):
              for i in range(nop):
                  if(f[i] == 0):
                      isDeadLock = 1
                      break
              break   
          cnt = cnt + 1

      print("Analyzing")
      if(isDeadLock):
          s = " 💀💀 DeadLock has Occured 💀💀"
          print(s)
          if(ind == 0):
              s =  "No Process can be terminated"
              print(s)

          else:
              s = ""
              for i in range(ind-1):
                  s += f"P{ans[i]+1} , "
              s += f"P{ans[ind-1]+1} can be terminated but rest cannot be terminated. Hence DeadLock"
              print(s) 
      else:
          print("✅ System is Safe ✅")
          s = "Safe Sequence ▶ "
          for i in range(nop-1):
              s += f"P{ans[i]+1}   ↣   "  
          s += f"P{ans[nop-1]+1}"
          print(s)

### --------------------------------------------------------------------------------------------------------

### Helper Functions for Optimised Algorithm
    def count_sort(a,n,pos,idx):
        # pos signify the pos(taking 0 as rightmost digit) of digit into consideration
        div = pow(10, pos)
        # count sort lgana hai on the basis of num
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
        
### --------------------------------------------------------------------------------------------------------

## Code For (Proposed) Optimised Banker's Algorithm (Python)
    global rows,cols,alloc,maxneed,r1,r2,r3,r4,r5,needed,initialavailable,print
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

        for i in range(nop) :
            if (maximum_needed_allocation[i] <= minimum_available and completed_process[process[i]] == 0) :
                completed_process[process[i]] = 1
                safe_sequence(process[i])
                s = f"Granted for P{process[i]+1} ✅"
                print(s)
                s = "Now Available Resources : "
                for j in range(nor) :
                    available_resource[j] = available_resource[j] + alloc[process[i]][j]
                    s += str(available_resource[j]) + ", "
                print(s)
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
                    safe_sequence(process[i])
                    s = f"Granted for P{process[i]+1} ✅"
                    print(s)
                    s = "Now Available Resources : "
                    for j in range(nor):
                        available_resource[j] = available_resource[j] + alloc[process[i]][j]
                        s += str(available_resource[j]) + ", "
                    print(s)

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

        print("Analyzing")
        if(isDeadLock):
            s = " 💀 DeadLock has Occured 💀"
            print(s)
            if(len(safe_sequence) == 0):
                s =  "No Process can be terminated"
                print(s)
            else:
                s = ""
                for i in range(len(safe_sequence)-1):
                    s += f"P{safe_sequence[i]+1} , "
                s += f"and P{safe_sequence[len(safe_sequence)-1]+1} can be terminated but rest cannot be terminated. Hence DeadLock"
                print(s)
        else:
            print("✅ System is Safe ✅")
            s = "Safe Sequence ▶ "
            for i in range(len(safe_sequence)-1):
                s += f"P{safe_sequence[i]+1}   ↣   "  
            s += f"P{safe_sequence[len(safe_sequence)-1]+1}"
            print(s)

## Taking Input From The User
![input1](/input1.PNG)

![input2](/input2.PNG)

## Simulation Result 
![sim1](/sim1.PNG)

![sim2](/sim2.PNG)

![sim3](/sim3.PNG)

## Graphical Analysis
![graph](/graph.PNG)
