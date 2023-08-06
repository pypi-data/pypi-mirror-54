#2018, jaroslaw.jankun@gmail.com
#v1.4
import re


#if ip is in good format it returns True, e.g.: verify('126.23.120.224') 
#pass second argument to verify format with mask like /24, e.g.: verify('126.23.120.224/24','ip/mask')
#pass second argument to verify format with mask like 255.255.255.240, e.g.: verify('126.23.120.224/24','ip/mask255')
def verify(ip, *args):
    regex_ip='^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$'
    regex_ipmask='^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\/([0-9]|[1-2][0-9]|3[0-2])$'    
    regex_ipmask255='^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\/(((255|254|252|240|224|192|128)\.0\.0\.0)|(255\.(255|254|252|240|224|192|128)\.0\.0)|(255\.255\.(255|254|252|240|224|192|128)\.0)|(255\.255\.255\.(255|254|252|240|224|192|128)))$'

    expression=regex_ip
    if "".join(args)=='ip/mask': expression=regex_ipmask
    if "".join(args)=='ip/mask255': expression=regex_ipmask255

    if re.search(expression,ip): return True
    else: return False


#gives mask in format x.x.x.x from mask in decimal format like 24 or 16 or 23...
def dec_to_mask255(mask_dec,**kwargs):    
    
    #gives partial octet of mask, which is not 255 and not 0, for example if number of '1s' is N=7, then we have 128, for 6 : 192, for 5 : 224
    #this is necessary for 'is_in_subnet' and 'dec_to_mask255' methods
    def _not_full_octet(N,base,P):           
        if N == 1 : return str(base)             # base is 128 , P is 64 ( needs to be so :) )       
        else:
            base+=P
            P=P//2                              # added double slash // for python 3 !
            return _not_full_octet(N-1,base,P)
    	
    mask255=""                                  
    for x in range(0,4):                        # 4 times because there are 4 octets of mask
        if mask_dec >= 8:
            mask255+="255"
            mask_dec-=8
        elif mask_dec > 0:
             mask255+=_not_full_octet(mask_dec,128,64)
             mask_dec=0
        else: mask255+="0"
            
        if x!=3 : mask255+="." 
    mask_octets = mask255.split('.')            #puts MASK into array of octets
    
    if kwargs.get('output') == 'string':
        return ".".join(mask_octets)
    else:
        return mask_octets

#changes mask in format: 255.255.255.128 to format: 25
def mask255_to_dec(mask255):

    # counts one octet of mask : for example for 128 it gives 1, for 192 it gives 2, for 224 gives 3
    #necessary for method mask255_to_dec
    def _one_octet(octet,base=128,increment=64,l=1):
        if octet == 0: return 0
        if base == octet : return l
        base+=increment
        increment=increment//2
        l+=1
        return _one_octet(octet,base,increment,l)
    
        return(mask_dec+l)

    mask_dec=0
    mask255_octets=mask255.split(".")
    for octet in mask255_octets:
        mask_dec+=_one_octet(int(octet))
    return mask_dec
 
#If provided mask(string) is real, returns True
def is_mask(mask):
	MASKS=["0.0.0.0", "128.0.0.0", "192.0.0.0", "224.0.0.0", "240.0.0.0", "248.0.0.0", "252.0.0.0", "254.0.0.0", "255.0.0.0",
		"255.128.0.0", "255.192.0.0", "255.224.0.0", "255.240.0.0", "255.248.0.0", "255.252.0.0", "255.254.0.0", "255.255.0.0",
		"255.255.128.0", "255.255.192.0", "255.255.224.0", "255.255.240.0", "255.255.248.0", "255.255.252.0", "255.255.254.0",
		"255.255.255.0", "255.255.255.128", "255.255.255.192", "255.255.255.224", "255.255.255.240", "255.255.255.248",
		"255.255.255.252", "255.255.255.254", "255.255.255.255"]
	if mask in MASKS: return True
	else: return False
          
#if 'ip' belongs to subnet 'net', it gives True, otherwise - false
def is_in_subnet(ip,net):                               
   
    if "/" in ip: ip=ip.split("/")[0]   # if 'ip' is also subnet (implicitly smaller, than 'net')
   
   
    if len(net.split('/')) == 2:
        mask_dec = int(net.split('/')[1])  #this is decimal mask
    net_octet = net.split('.')            #puts subnet ip into array with octets
    net_octet[3]=net_octet[3].split("/")[0]

    ip_octet = ip.split('.')              #puts host ip into array with octets

    mask_octets=dec_to_mask255(mask_dec)
    
    net_AND=""                                  #AND of subnet with mask and ip with mask, comparison gives final decision
    for s in range(len(net_octet)): net_AND+= str(int(net_octet[s]) & int(mask_octets[s]))+'.'
    ip_AND=""
    for s in range(len(ip_octet)): ip_AND+= str(int(ip_octet[s]) & int(mask_octets[s]))+'.'

    if net_AND == ip_AND: return True           
    else : return False        

#returns subnet ip e.g.: get_subnet_ip("192.168.1.10/24) returns 192.168.1.0  
def get_subnet_ip(address):                                      
    ip = address.split("/")[0]  #ip
    mask_dec = int(address.split('/')[1])  #this is decimal mask
    ip_octet = ip.split('.')              #puts host ip into array with octets

    mask_octets=dec_to_mask255(mask_dec) #get mask in other format
                                           
    ip_AND=[]                                      #AND of ip with mask
    for s in range(len(ip_octet)): ip_AND.append( str(int(ip_octet[s]) & int(mask_octets[s])) )

    return ".".join(ip_AND)

#method returns True if ip is between ip_start and ip_end range
def is_in_range(ip_start, ip_end,ip):
	ip_start_tab=ip_start.split('.')
	ip_end_tab=ip_end.split('.')
	ip_tab=ip.split('.')
	
	#below, for example 1.16.100.99 becomes 001016100099, so I can compare them later
	ip_start_number= "".join([str('{:03}'.format(int(number))) for number in ip_start_tab])  
	ip_end_number= "".join([str('{:03}'.format(int(number))) for number in ip_end_tab])
	ip_number= "".join([str('{:03}'.format(int(number))) for number in ip_tab])
	
	if int(ip_number) >= int(ip_start_number) and int(ip_number) <= int(ip_end_number):
		return True
	else:
		return False
