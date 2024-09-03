from log import logger
import get_pos
import detail
import classify
import cdir
import save_excel
import os
import sys 
import clear_dir






def pi():
    # console = sys.stdout                		# 得到当前输出方向， 也就是控制台
    file = open(r".\givenchy_data.txt", 'w',encoding='utf-8')
    sys.stdout = file                   				# 重定向到文件
  


def deleteSameNum(num):
    last = num[-1]
    for i in range(len(num)-2, -1, -1): #len(num)-2是倒数第二个数，第一个-1为了生成到0下标
        if last == num[i]:
            del num[i] #删除后位置i处的元素后，其后一个相同的元素又补到了i位置
        else:
            last = num[i]
    return num

def d_du(du):
    path = du[0] + '/'+du[0][7:].replace('/','_')+'_givenchy.xlsx'
    logger.info(du[0]+' part capturing')
    pos = get_pos.out(du[1])
    lss = [['货号','价格','大小','网上是否有货','有货店量','货名',"MATERIAL","COLOR", "SIZE CHART TYPE",'DESCRIPTION','img_url']]
    for po in pos:
    #for po in pos[:6]:
        logger.info(po+' capturing---')
        lss = lss + detail.out(po)  
        pass
    lss=deleteSameNum(lss)
    if len(lss) == 1:
        return du
    save_excel.out(path,lss)
    logger.info(path+' saved successfully')
    return None

def deal_err(ers):
    keep = True
    max_t = 5
    cu = 1 
    fin_ers = []
    while cu < max_t and keep:
        ers_in = []
        logger.info('错误尝试 >>>' + str(cu))
        for i in ers:
            er = d_du(i)
            # er = i
            if er != None:
                ers_in.append(er)
            pass
        
        if ers_in == []:
            keep = False
        else:
            ers = ers_in
            cu = cu+1
        
        fin_ers = ers_in   
    logger.info('错误重试结束')
    logger.info(fin_ers)

def main():
    
    pi()
    logger.info(' 自动清空  res   文件夹 \n勿关闭窗口  输出信息已转入  data.txt\n运行完毕会自动关闭')
    clear_dir.clean_folder('../res')
    clss = classify.out()
    dus = cdir.out(clss)
    

    ers = []  #  收集失败分类
    for i in dus[41:]:
        # i = dus[15]
        if i[1] != None:
            er = d_du(i)
            # er = i
            if er != None:
                ers.append(er)
        pass
    pass

    # 失败分类重新请求
    if len(ers) != 0:
        deal_err(ers)
    print('运行完成')
if __name__ == '__main__':
    main()
    exit()



