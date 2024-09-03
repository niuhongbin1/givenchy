import get_pos
import detail
import classify
import cdir
import save_excel
'''
ERROR
/short-jacket-in-wool-and-cashmere/S359Y02X40-8100.html?cgid=women&p=228
'''

def deleteSameNum(num):
    last = num[-1]
    for i in range(len(num)-2, -1, -1): #len(num)-2是倒数第二个数，第一个-1为了生成到0下标
        if last == num[i]:
            del num[i] #删除后位置i处的元素后，其后一个相同的元素又补到了i位置
        else:
            last = num[i]
    return num




if __name__ == '__main__':
    path = './test.xlsx'
    pos = get_pos.out('https://www.givenchy.com/fr/fr/homme/sacs/cut-out/')
    lss = [['货号','价格','大小','l3','剩余有货店量','名称','img url']]
    for po in pos:
        print(po,'采集中---')
        lss = lss + detail.out(po)  
        # print(po[35:],'已采集')
        pass
    lss=deleteSameNum(lss)
    save_excel.out(path,lss)
    print(path,'已储存')

