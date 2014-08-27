#coding:utf8
import time,pickle,sys,re,getpass
def accoun():
    accoun={}
    with open('userlist.txt','r+') as f:
        for i in f.readlines():
            accoun[i.strip().split()[0]]=i.strip().split()[1:]
    return accoun
def login():#登陆模块登陆3次锁定账号，24小时候自动解锁
  while True:
    account=accoun()
    name=raw_input("请输入您的用户名：").strip()
    for k,v in account.items():
        if name in account.keys():
          if name==k:
            if v[0]!= '0':
              print "时间差%s"%(int(time.time())-int(v[0]))
              if int(time.time())-int(v[0])<=36920:
                print "您的账户已经被锁定"
                sys.exit()
              else:
                   v[0]='0'
                   modify(k,v,account)
              if int(time.time())-int(v[0])<=36920:
                 print "您的账户已经被锁定"
                 sys.exit()
              else:
                   v[0]='0'
                   modify(k,v,account)
            for i in range(4):
                if i<=2:
                    password=getpass.getpass('请输入您的密码: ')
                    if v[2]!=password:
                        print "密码错误，请重新输入您的密码！"
                        continue
                    else:
                        print '登陆成功，欢迎来到老男孩信用卡中心！'
                        return name
                else:
                    print "您的信用卡已经被锁定，请24小时后重新登陆！"
                    v[0]=str(int(time.time()))
                    modify(k,v,account)
                    sys.exit()
          else:continue
    else:
        print "没有这个用户，请重新输入！"
def modify(k,v,account):#解除锁定账户
    with open('userlist.txt','w') as f:
        for t,y in account.items():
            if t==k:
                list_s='\t'.join([k]+v)
                f.writelines(list_s)
                f.write('\n')
            else:
                list_y='\t'.join([t]+y)
                f.writelines(list_y)
                f.write('\n')
def serach_ban(name,what):#取得登陆用户的余额
    account=accoun()
    for v,k in account.items():
        if what=='banlance':
            if v==name:
                return k[4]
def credit(name,what):#取得登陆用户的余额
    account=accoun()
    for v,k in account.items():
        if what=='credit':
            if v==name:
                return k[3]               
def record_amount(tran_type,s_user):#消费功能
    if tran_type!='drawl':#取款-drawl 转账-transfer 消费-consume
        with open('bought.pkl','r+') as f:
            c=pickle.load(f)
        account=accoun()
        with open('userlist.txt','w') as f:            
          for k,v in account.items():
            if k==s_user:
               v[4]=str(c[4])
               list_s='\t'.join([k]+v)
               f.writelines(list_s)
               f.write('\n')
            else:
               list_e='\t'.join([k]+v)
               f.writelines(list_e)
               f.write('\n')
def loger(account,tran_date,tran_type,amount,interest):#记录操作日志
    f = file('log.txt','a+')
    msg="%s %s %s %s %s" %(account,tran_date,tran_type,amount,interest)
    f.writelines(msg)
    f.write('\n')
    f.close()
def get_account(name):#获取用户的信息
    account=accoun()
    if name in account.keys():
        return account[name]
    else:
        print "账号信息错误！"
        return False
def query(name,time=time.strftime( "%Y%m")):#匹配出年月
    with open('log.txt') as f:
       mon_con=0 
       print "账户\t\t时间\t\t    操作\t    明细      \t    利息"
       for i in f.readlines():
            list_q=i.strip().split()
            b=list_q[1]
            a=re.compile(r'(\d+)/(\d+)')
            c=a.match(b)
            now=''.join(c.groups()) #获取日志中的年月
            if list_q[0]==name and int(time)==int(now):
              if list_q[2]=='还款':
                 print list_q[0].ljust(10),list_q[1].ljust(25),\
                 ("\033[1;32;10m%s\033[0m"%list_q[2]).ljust(30) ,\
                 ("\033[1;31;10m%s\033[0m"%list_q[3]).ljust(31),list_q[4] 
                 mon_con=mon_con+int(list_q[3])
              else:
                 print list_q[0].ljust(10),list_q[1].ljust(25),\
                 ("\033[1;32;10m%s\033[0m"%list_q[2]).ljust(30) ,list_q[3].ljust(17),list_q[4]
                 mon_con=mon_con+int(list_q[3])
       return mon_con 
def manager():
    account=accoun()
    m_list=["解锁",'增加用户','删除用户']
    for e,l in enumerate(m_list):
        print (e+1),'\t',l
    which=raw_input("请选择您的操作:")
    if which=='1':
      while True:
        t=0  
        name=raw_input("您要解锁哪个个账户?>>")
        for k,v in account.items():
            if k==name:
                v[0]='0'
                modify(k,v,account)
                print "用户%s，解锁成功!"%name
                t=1
            sys.exit()
        if t==0:    
            print "没有这个用户请重新输入!"
            continue
        continue
    elif which=='2':
      while True:  
        print "请输入您要增加用户的账户信息!"
        name=raw_input("用户>>")
        if name not in account.keys():
            passwd=raw_input("密码>>")
            ed=raw_input("信用额度>>")
            yu=ed
            a_list=[name,'0','0',passwd,ed,yu]
            s_list='\t'.join(a_list)
            if len(name)!=0 and ed.isdigit() and len(passwd)!=0 and len(ed)!=0:
                with open('userlist.txt','a+') as f:
                    f.writelines(s_list)
                    f.write('\n')
                print "%s,增加成功，额度是%s"%(name,ed)
            else:
                print "用户名，密码不能为空且额度只能是数字"
                continue
        else:
            print "这个用户名已经存在"
            continue
        break
    elif which=='3':
        name=raw_input("请输入您要删除的用户:>>")
        with open('userlist.txt','w') as f:
            for t,y in account.items():
                if t!=name:
                    list_s='\t'.join([t]+y)
                    f.writelines(list_s)
                    f.write('\n')
            print "用户%s,删除成功!"%name



    








