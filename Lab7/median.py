def median(numberlist):
    sortedlist = sorted(numberlist)
    return sortedlist[len(numberlist)//2] if (len(numberlist)%2 == 1)\
        else (sortedlist[len(numberlist)//2] + sortedlist[len(numberlist)//2 - 1])/2

if __name__ == '__main__':
    print(median([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))