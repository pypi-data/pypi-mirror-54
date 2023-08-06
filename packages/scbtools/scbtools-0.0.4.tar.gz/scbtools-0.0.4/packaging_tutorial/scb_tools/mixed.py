import random
#-------------num 返回的数字个数 start 起始 end 终止---------
def create_random(num:int,star=-100,end=100)->list:
    raw_list=range(star,end)
    result=random.sample(raw_list,num)
