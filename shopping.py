#coding=utf8
import sys,pickle,time
#将商品和价格从文件中读出到列表，
def shop():
    print "欢迎来到老男孩大商城!"
    bought_list=[]
    su_list=[]
    while True:
        shop_list=[]
        shop_pice=[]
        with open('shoplist.txt') as f:
            for i in f.readlines():
                shop_list.append(i.strip().split()[0])
                shop_pice.append(i.strip().split()[1])
        f=len(shop_list)
        for i in range(f):
            print '-------------------------------------------------------'
            print i+1,"\033[1;32;10m %s \033[0m"%shop_list[i].ljust(20),"\033[1;32;10m %s \033[0m"%shop_pice[i]
        print '-------------------------------------------------------'    
        #选择要购买的商品 判断余额是否足够，若足够则加入到购物车列表，不足确认是否继续购买
        which=raw_input('选一个您想买的商品:')
        if which in shop_list:
            index=shop_list.index(which) #得到商品的索引取得对应的价格
            print shop_list[index],shop_pice[index]
            raw_input("确认按Eter,退出按Ctrl+C:")
            bought_list.append(which)#将商品添加到购物车
            while True:
                opr=raw_input("您是要继续购买还是退出？(Y/N):")
                if opr=='Y' or opr == 'y':
                    break
                elif opr=='N' or opr == 'n':
                    print '------------------------------------------------'
                    print "你买了这些:"
                    total_money=0
                    for i in bought_list:
                        pice=shop_pice[shop_list.index(i)]
                        print "\033[1;32;10m %s \033[0m"%i ,'花了%s元' % pice
                        print '------------------------------------------------'
                        total_money=int(total_money)+int(pice)
                    return total_money    #返回这些商品一共花费的钱
                print "对不起，您只能选择：Y/N!"
                continue
            continue               
        else:
            print "\033[1;32;10m没有这个商品，你丫眼睛有问题吧\033[0m！"
            continue
        break
