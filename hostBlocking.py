import os
import subprocess

def split_hosts_head_and_tail():
    with open('/etc/hosts', 'rt') as f:
        s = ""
        for i in range(9):
            s += f.readline()
        with open('/tmp/etc_hosts_head.tmp', 'wt') as outf:
            outf.write(s)

        s = ""
        while True:
            currentLine =  f.readline()
            if not currentLine:
                break
            s += currentLine
        with open('/tmp/etc_hosts_tail.tmp', 'wt') as outf:
            outf.write(s)
        
def append_to_hosts(webname):
    lines = subprocess.check_output('cat /tmp/etc_hosts_tail.tmp | grep ' + webname + ' | cat', shell=True)
    if not len(lines):
        lines = subprocess.check_output('echo ' + '0.0.0.1 ' + webname + '.com >> /tmp/etc_hosts_tail.tmp', shell=True)
        lines = subprocess.check_output('echo ' + '0.0.0.1 www.' + webname + '.com >> /tmp/etc_hosts_tail.tmp', shell=True)
    #join head and tail
    lines = subprocess.check_output('cat /tmp/etc_hosts_head.tmp /tmp/etc_hosts_tail.tmp > /tmp/etc_hosts.tmp', shell=True)
    lines = subprocess.check_output('rm /tmp/etc_hosts_head.tmp /tmp/etc_hosts_tail.tmp', shell=True)
    os.system('sudo mv /tmp/etc_hosts.tmp /etc/hosts')


def remove_from_hosts(lineToRemove):
    lines = subprocess.check_output('cat /tmp/etc_hosts_tail.tmp | grep ' + lineToRemove + ' | cat > /tmp/etc_hosts_remover.tmp', shell=True)
    lines = subprocess.check_output('grep -v -f /tmp/etc_hosts_remover.tmp /tmp/etc_hosts_tail.tmp | cat > /tmp/output.tmp', shell=True)
    lines = subprocess.check_output('cat /tmp/output.tmp', shell=True)
    #join head and tail
    lines = subprocess.check_output('cat /tmp/etc_hosts_head.tmp /tmp/output.tmp > /tmp/etc_hosts.tmp', shell=True)
    lines = subprocess.check_output('rm /tmp/output.tmp /tmp/etc_hosts_remover.tmp /tmp/etc_hosts_head.tmp /tmp/etc_hosts_tail.tmp', shell=True)
    os.system('sudo mv /tmp/etc_hosts.tmp /etc/hosts')

    
def block_website(website):
    split_hosts_head_and_tail()
    append_to_hosts(website)

def unblock_website(website):
    split_hosts_head_and_tail()
    remove_from_hosts(website)


unblock_website('youtube') 

print(subprocess.check_output('cat /etc/hosts', shell=True).decode('utf-8'))