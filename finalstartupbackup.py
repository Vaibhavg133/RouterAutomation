import pexpect
import getpass
user=raw_input('Enter Username:')
ip=raw_input('Enter IP:')
port=raw_input('Enter Port:')
password=getpass.getpass('Password:')
command='/usr/bin/ssh'+" "+user+"@"+ip+" -p "+port
child=pexpect.spawn(command)
child.expect('password:')
child.sendline(password)
child.expect(':~#')
child.sendline('cli')
child.expect('#')
child.sendline('show running-config | nomore')
child.expect("#")
showrun=child.before
filename='root.txt'
file=open(filename,'wb')
file.write(showrun)
file.close()
child.close()
