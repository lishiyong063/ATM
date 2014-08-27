#coding:utf8
import login,time,shopping,pickle,sys,datetime,re
while True:
    info=['信用卡登陆','商城','后台管理']
    for i in range(len(info)):
        print str(i+1).center(16),info[i]
    which=raw_input("请选择相应的操作:")
    if which=='1':
       b=0
       log_user=login.login()#登陆验证并获取操作用户 
       lu_banlance=login.serach_ban(log_user,'banlance')#获取当前用户的余额 
       log_account=login.get_account(log_user)#登陆用户的账户信息
       now=int(time.strftime( "%m"))#获取本月的月份
       lst_fist = [datetime.date.today().year,datetime.date.today().month]#今年上月份
       today=int(time.strftime("%Y%m%d"))#日期
       #print today,type(today)
       if len(str(lst_fist[1]))==1:
            b='%s0%s'%(lst_fist[0],lst_fist[1])
       else:
            b='%s%s'%(lst_fist[0],lst_fist[1])
       if int(time.strftime("%d"))==30:
           print "您本月的账单为详情如下，请下月10号前按时还款！"
           a=login.query(log_user,b)
           raw_input("\033[1;32;10m 您下月需要还款%s,按确认键继续!\033[0m"%str(a))
       credit=login.credit(log_user,'credit')#登陆用户的额度
       get_laccount=login.get_account(log_user)#获取登陆用户的账号信息
      # u_con=login.query(log_user,time.strftime( "%Y%m"))#用户这个月用的钱
       if int(credit)-int(lu_banlance)>0 and today>10:#欠款
            with open('time.pkl','rb') as f:
                a=int(pickle.load(f))
           # print "pickle-a %s"%a,type(a)   
            if  a!=today:#如果记录的时间不等于当前的时间
                znj=int((int(credit)-int(lu_banlance))*0.05)
                user_ban=int(lu_banlance)-znj #余额-滞纳金
                log_account[4]=user_ban
                if user_ban>=0:
                    with open('bought.pkl','wb') as f:#刷新账户信息
                         pickle.dump(get_laccount,f)
                    login.record_amount('znj',log_user)
                    login.loger(log_user,time.strftime( "%Y/%m/%d-%X"),\
                    '滞纳金',str(-znj),str(-znj))#写入日志
                    tday=time.strftime("%Y%m%d")  #重写日期标记今天的已经扣除
                    with open('time.pkl','wb') as f:
                         pickle.dump(tday,f)
                else:
                   print "\033[5;35;10m您的信用卡已经刷爆！请立即还款!\033[0m"
       while True: 
            log_account=login.get_account(log_user)#登陆用户的账户信息
            list_l=['转账','取款','还款','查询历史账单','退出ATM']
            for i,k in enumerate(list_l):
                print i+1,k
                print '------------------------'
            what_A=raw_input("请输入您的操作:")
            if what_A == '1':
              s_user=raw_input("收款人账户:")
              if s_user!=log_user:  
                 get_account=login.get_account(s_user) #获取账户信息
                 if get_account==False:
                    continue
                 else:   
                    how_money=input('请输入转账金额:')
                    get_account[4]=int(get_account[4])+how_money
                    user_ban=int(lu_banlance)-how_money#支出账户后，还剩下的余额
                    log_account[4]=user_ban
                    if user_ban>=0:#转账
                        with open('bought.pkl','wb') as f:#刷新账户信息
                            pickle.dump(get_account,f)
                        login.record_amount('transfer',s_user)
                        print '转账成功!!!'
                        login.loger(s_user,time.strftime( "%Y/%m/%d-%X"),\
                        '转入',str(+how_money),'0')
                        with open('bought.pkl','wb') as f:
                            pickle.dump(log_account,f)
                        login.record_amount('transfer',log_user)#扣款
                        login.loger(log_user,time.strftime( "%Y/%m/%d-%X"),\
                        '支出',str(-how_money),'0')
                        raw_input("\033[5;35;10m请按确认键继续\033[0m")
                    else:
                         print"余额不够！"
                         sys.exit()
              else:print "操作错误！"       
            elif what_A=='2':#取款
              while True:  
                s_money=input("请输入您要取款的金额:")
                lixi=int(s_money*0.05)
                kk=s_money+lixi#取款数加上利息
                if kk<=int(lu_banlance):
                    user_ban=int(lu_banlance)-kk#利息加上取款
                    log_account[4]=user_ban
                    with open('bought.pkl','wb') as f:
                        pickle.dump(log_account,f)
                    login.record_amount('transfer',log_user)#扣款
                    login.loger(log_user,time.strftime( "%Y/%m/%d-%X"),\
                    '取款',str(-kk),lixi)
                    print "取款成功！快去泡妹子吧！"
                    raw_input("\033[5;35;10m请按确认键继续\033[0m")
                else:
                    print "余额不够！"
                    continue
                break    
            elif what_A=='3':#还款
              while True:
                money=raw_input("请输入还款金额:")
                if  money.isdigit() and len(money)!=0: 
                    user_ban=int(lu_banlance)+int(money)
                    if user_ban>=0:
                        log_account[4]=user_ban
                        with open('bought.pkl','wb') as f:
                            pickle.dump(log_account,f)
                        login.record_amount('transfer',log_user)#扣款
                        login.loger(log_user,time.strftime( "%Y/%m/%d-%X"),\
                        '还款','+%s'%money,0)
                        print "还款成功"
                        raw_input("\033[5;35;10m请按确认键继续\033[0m")
                else:
                    print  "输入错误!"
                    continue
                break       
            elif what_A=='4':#查询
              while True:
                mouth=['1','2','3','4','5','6','7','8','9','10','11','12']
                what_mounth=raw_input('请输入您要查询月份:')
                if what_mounth in mouth:
                    print "\033[1;35;10m 现在是%s月,您的信用额度是%s,您的余额为：%s\033[0m"\
                    %(time.strftime("%m"),credit,lu_banlance)
                    print "-------------------------------------------------------------------------"
                    if len(str(lst_fist[1]))==1:
                         b='0%s'%(what_mounth)
                    else:
                         b=what_mounth
                    which_query=str(lst_fist[0])+b
                    con=login.query(log_user,which_query)
                    if con>=0:
                        print "这月没有欠款."
                    else:print "这月欠费%s"%con    
                    raw_input("\033[5;35;10m请按确认键继续\033[0m")
                else:
                    print "只能输入1-12月份的日期哦！"
                    continue
                break    
            elif what_A=='5':#退出ATM
                sys.exit()
    elif which=='2':
        total=shopping.shop()#结束后返回一个消费总额
        who=login.login()#获得当前登陆用户
        money=login.serach_ban(who,'banlance')#获取登陆用户余额
        user_ban=int(money)-int(total) #账户消费后的余额
        if user_ban>=0:
            get_account=login.get_account(who)    #获取当前账户信息     
            user_ban=int(money)-int(total) #账户消费后的余额
            get_account[4]=user_ban
            with open('bought.pkl','wb') as f:
                pickle.dump(get_account,f)
            login.record_amount('con',who)#扣款
            print "您这次消费了%s元，余额还有%s元"%(total,user_ban)
            login.loger(who,time.strftime( "%Y/%m/%d-%X"),'购物',str(-total),'0')
            sys.exit()
        else:
            print "您的余额不够"
            sys.exit()
    elif which == '3':
            login.manager()
            sys.exit()
    else:
        print "没有这个选项，请重新输入！"
