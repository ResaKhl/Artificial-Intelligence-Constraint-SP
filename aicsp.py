import copy
def findNext():
    with open('input10.txt', 'r') as f:
        bed = f.readline()
        parkinglotSpace = f.readline()
        lahsaListAlready = [] #list of applicants already assigned to lahsa
        splaListAlready = [] #list of applicants already assigned to lahsa
        lahsaApplicantsNum = f.readline()
        for i in range(int(lahsaApplicantsNum)):
            lahsaListAlready.append(f.readline()[:5])
        splaApplicantsNum = f.readline()
        for i in range(int(splaApplicantsNum)):
            splaListAlready.append(f.readline()[:5])

        totalNumAppl = f.readline()
        applsInfosAdded = []
        applsInfosAvail = []
        splaSpace = [] #splaSpace is the list of all of the information of already added applicants to the spla list.
        lahsaSpace = [] #lahsaSpace is the list of all of the information of already added applicants to the lahsa list.
        for i in range(int(totalNumAppl)):
            tempInfo = f.readline()
            if (tempInfo[:5] in splaListAlready):
                applsInfosAdded.append([tempInfo, 's'])
                splaSpace.append(tempInfo)
            elif(tempInfo[:5] in lahsaListAlready):
                applsInfosAdded.append([tempInfo, 'l'])
                lahsaSpace.append(tempInfo)
            else:
                applsInfosAdded.append([tempInfo, 'n'])
                applsInfosAvail.append(tempInfo)


    potentialSPLAApplicants = []
    potentialLAHSAApplicants = []
    sharedApplicantsBetween2Org = []
    for x in range(len(applsInfosAvail)):
        isShared = 0
        if(applsInfosAvail[x][11]=='Y' and applsInfosAvail[x][12]=='Y' and applsInfosAvail[x][10]=='N' and applsInfosAvail[x][:5] not in splaListAlready):
            potentialSPLAApplicants.append(applsInfosAvail[x])
            isShared +=1
        if (applsInfosAvail[x][5] == 'F' and int(applsInfosAvail[x][6:9])>17 and applsInfosAvail[x][9] == 'N' and applsInfosAvail[x][:5] not in lahsaListAlready):
            potentialLAHSAApplicants.append(applsInfosAvail[x])
            isShared +=1
        if(isShared==2 and applsInfosAvail[x][:5] not in lahsaListAlready and applsInfosAvail[x][:5] not in splaListAlready):
            sharedApplicantsBetween2Org.append(applsInfosAvail[x])
        pass
    justInSPLAPotentialApplicants = []
    for x in range(len(potentialSPLAApplicants)):
        if (potentialSPLAApplicants[x] not in sharedApplicantsBetween2Org):
            justInSPLAPotentialApplicants.append(potentialSPLAApplicants[x])
    justInSPLAPotentialApplicantsSORTED = find_max_days_stays(justInSPLAPotentialApplicants)
    if(len(sharedApplicantsBetween2Org)==0):
        if (int(parkinglotSpace) > len(splaSpace)):
            return justInSPLAPotentialApplicantsSORTED[0]
        if (int(parkinglotSpace) == len(splaSpace)):
            for i in range(len(justInSPLAPotentialApplicantsSORTED)):
                if (not isThereCollision(justInSPLAPotentialApplicantsSORTED[i], splaSpace)):
                    return justInSPLAPotentialApplicantsSORTED[i]
        return justInSPLAPotentialApplicantsSORTED[0]

    if (int(parkinglotSpace) - len(splaListAlready) >= len(potentialSPLAApplicants)):
        return find_max_days_stays(sharedApplicantsBetween2Org)[0] #choosing the person with max days from shared applicants when we have room (space)
        # for more people than all of the ones eligible to get into SPLA
    #finding the applicants not assigned already and who can just go to SPLA

    #TODO
    #another condition: room is less than total eligible, enough to get all of the not shared, but not for all of the shared, take the one with most nights
    #out of the one in the shared, for this condition we get the max of the whole. But First, for output, we traverse the shared, find max, if not collision wih others
    #we take it, if not, go for next, until we find a one.
    #WHEN parkinglotSpace IS LESS THAN total number of applicants and we fisrt search if we can find one in sharedApplicantsBetween2Org
    potentialSPLAApplicantsSORTED = find_max_days_stays(potentialSPLAApplicants)
    if (len(potentialSPLAApplicants) <= int(parkinglotSpace)):
        for i in range(int(parkinglotSpace)):
            if(potentialSPLAApplicantsSORTED[i][0] in sharedApplicantsBetween2Org):
                return potentialSPLAApplicantsSORTED[i]
    sharedApplicantsBetween2OrgSORTED = find_max_days_stays(sharedApplicantsBetween2Org)

    #right here we should write the forloop to see if we can find an appl who's in shared and it doesn't have collision with already chosen and has more days than a
    #one who is in the list of justspla.
    startOfCheckingTheCollision = int(parkinglotSpace)
    if(len(justInSPLAPotentialApplicants) >=  int(parkinglotSpace) and int(parkinglotSpace) != len(splaSpace)):
        for i in range(len(sharedApplicantsBetween2OrgSORTED)):
            for j in range(len(justInSPLAPotentialApplicants)):
                if(sum_days(sharedApplicantsBetween2OrgSORTED[i][0]) >= sum_days(justInSPLAPotentialApplicantsSORTED[j][0])
                        and not isThereCollision(sharedApplicantsBetween2OrgSORTED[i],
                                             justInSPLAPotentialApplicantsSORTED[j])):
                    return sharedApplicantsBetween2OrgSORTED[i]

    if(int(parkinglotSpace)>len(splaSpace)):
        return justInSPLAPotentialApplicantsSORTED[0]

    splaSpacedeepcopy = copy.deepcopy(splaSpace)
    #TODO starting very special case, inspecting collision between 3 queue, already in spla, justinspla, shared
    if(int(parkinglotSpace)==len(splaSpace) and len(sharedApplicantsBetween2OrgSORTED)!=0):
        for i in range(len(sharedApplicantsBetween2OrgSORTED)):
            collisionforcurrentshared = False
            for j in range(len(justInSPLAPotentialApplicantsSORTED)):
                if(sharedApplicantsBetween2OrgSORTED[i][1]>justInSPLAPotentialApplicantsSORTED[j][1]
                    and not isThereCollisionwitharray(sharedApplicantsBetween2OrgSORTED[i],splaSpacedeepcopy)):
                        return sharedApplicantsBetween2OrgSORTED[i]
                elif(not isThereCollisionwitharray(justInSPLAPotentialApplicantsSORTED[j][0], splaSpacedeepcopy)):
                    splaSpacedeepcopy.append(justInSPLAPotentialApplicantsSORTED[j][0])
                if(isThereCollisionwitharray(sharedApplicantsBetween2OrgSORTED[i][0],splaSpacedeepcopy)):
                    collisionforcurrentshared = True
                    break
            if(collisionforcurrentshared): continue
            pass

    # TODO
    # not tested here
    # TODO
    if (int(parkinglotSpace) == len(splaSpace)):
        for i in range(len(potentialSPLAApplicantsSORTED)):
            if (not isThereCollisionwitharray(potentialSPLAApplicantsSORTED[i][0], splaSpace)):
                return potentialSPLAApplicantsSORTED[i]

    return potentialSPLAApplicantsSORTED[0]

    #TODO
    #another condition: room is less enough for not shared, but not for a single shared

    #TODO
    #another condition: room is NOT even enough for the not shared

    #TODO
    #another condition: not any room for newcomers, have to fit newcomers to the already filled spots, but care for collision

    #we can see 2 cond not handled yet: one: room enough for all not shared, but not enough for all shared
    #cond2: is that the room, is not enough for the not shared, not for shared, so, we sort all out, if we have a shared, no worries, but if not, we go to
    #first shared (first of the max heap) compare with all already there and all up in the stack , if no collision, we take it, if not, we go to the next
    #shared until we find a one.


#this function is to figure out if there is a collision of a single entry with an array based on the days were given.
def isThereCollisionwitharray(toBeChecked, arraygiven):
    for x in arraygiven:
        if(isThereCollisionv2(toBeChecked, x)): return True
    return False

def isThereCollisionv2(toBeChecked, arraygiven):
    hasCollision = False
    for j in range(13,20):
        if(int(toBeChecked[j])== int(arraygiven[j]) == 1):
                hasCollision = True
                break
    return hasCollision

def isThereCollision(toBeChecked, arraygiven):
    hasCollision = False
    for j in range(13,20):
        if(int(toBeChecked[0][j])== int(arraygiven[0][j]) == 1):
                hasCollision = True
                break
    return hasCollision


def find_max_days_stays(applicantsInfo):
    applicantsInfoListwithsumOfdays = []
    for i in range(len(applicantsInfo)):
        applicantsInfoListwithsumOfdays.append(sum_days(applicantsInfo[i]))
    applicantsInfoListwithsumOfdays= sorted(applicantsInfoListwithsumOfdays, key=lambda x:(x[1]), reverse=True)
    return applicantsInfoListwithsumOfdays

def sum_days(applicantInfo):
    sum=0
    for i in range(13,20):
        sum+=int(applicantInfo[i])
    tempList = [applicantInfo,sum]
    return tempList

# find_max_days_stays(['00001F020NNYY1001000\n', '00003M040NNYY1000110\n', '00004M033NNYY1000000\n'])
with open('output.txt', 'w') as f2:
    nextSplaAccepted = findNext()
    towritestr = nextSplaAccepted[0][:5]
    f2.write(str(towritestr))
