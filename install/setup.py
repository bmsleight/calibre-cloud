import getopt, sys
import pexpect


def pexpect_simple(cmd):
    child = pexpect.spawn(cmd)
    child.logfile = sys.stdout
    child.expect(pexpect.EOF, timeout=600)
    child.close()


def add_user_cloud(password):
    child = pexpect.spawn('/usr/sbin/adduser cloud')
    child.logfile = sys.stdout
    child.expect('Enter new UNIX password:')
    child.sendline(password)
    child.expect('Retype new UNIX password:')
    child.sendline(password)
    child.expect('Full Name \[\]:')
    child.sendline('')
    child.expect('Room Number \[\]:')
    child.sendline('')
    child.expect('Work Phone \[\]:')
    child.sendline('')
    child.expect('Home Phone \[\]:')
    child.sendline('')
    child.expect('Other \[\]:')
    child.sendline('')
    child.expect('Is the information correct\? \[Y\/n\] ')
    child.sendline('y')
    child.read()
    child.close()


def install_calibre():
    child = pexpect.spawn('python -c "import urllib2; exec urllib2.urlopen(\'http://status.calibre-ebook.com/linux_installer\').read(); main()"')
    child.logfile = sys.stdout
    child.expect('Enter the installation directory for calibre \[/opt\]: ')
    child.sendline('')
    child.expect(pexpect.EOF, timeout=600)
    child.close()


def install_django_app(password):
    pexpect_simple('rm -R /home/cloud/*')
    pexpect_simple('su cloud -c "cd /home/cloud/ ; svn checkout http://calibre-cloud.googlecode.com/svn/trunk/ calibre-cloud-read-only"')
    pexpect_simple('su cloud -c "mv /home/cloud/calibre-cloud-read-only/calibreupload /home/cloud/"')

    child = pexpect.spawn('su cloud -c "cd /home/cloud/calibreupload/ ; ./manage.py syncdb "')
    child.logfile = sys.stdout 
    child.expect('Would you like to create one now\? \(yes\/no\): ')
    child.sendline('yes')
    #Username (Leave blank to use 'bms'): 
    child.expect('\): ')
    child.sendline('y')
    child.expect('E-mail address: ')
    child.sendline('cloud@example.com')
    child.expect('Password: ')
    child.sendline(password)
    child.expect('Password \(again\): ')
    child.sendline(password)
    child.expect(pexpect.EOF, timeout=600)
    child.close()
    pexpect_simple('cp /home/cloud/calibre-cloud-read-only/apache/cloud /etc/apache2/sites-available/default')
    pexpect_simple('cp /home/cloud/calibre-cloud-read-only/apache/calibre /etc/apache2/sites-available/calibre')
    pexpect_simple('a2ensite calibre')
    pexpect_simple('a2enmod proxy proxy_html proxy_http headers')
    pexpect_simple('/etc/init.d/apache2 restart')


def setup_x11vnc(password):
    pexpect_simple('rm -R /root/.vnc/certs')
    child = pexpect.spawn('x11vnc -sslGenCA')
    child.logfile = sys.stdout 
    child.expect('Enter PEM pass phrase:')
    child.sendline(password)
    child.expect('Verifying - Enter PEM pass phrase:')
    child.sendline(password)
    child.expect('Country Name \(2 letter code\) \[AU\]:')
    child.sendline('UK')
    child.expect('State or Province Name \(full name\) \[mystate\]:')
    child.sendline('')
    child.expect('Locality Name \(eg\, city\) \[\]:')
    child.sendline('')
    child.expect('Organization Name \(eg\, company\) \[x11vnc server CA\]')
    child.sendline('Cloud Calibre')
    child.expect('Organizational Unit Name \(eg\, section\) \[\]')
    child.sendline('Cloud Calibre Unit')
    child.expect('Common Name \(eg\, YOUR name\) \[root x11vnc server CA\]:')
    child.sendline('root Cloud Calibre CA')
    child.expect('Email Address \[x11vnc\@CA.nowhere\]:')
    child.sendline('cloud@example.com')
    child.expect('Press Enter to print the cacert\.pem certificate to the screen: ')
    child.sendline('')
    child.expect(pexpect.EOF, timeout=600)
    child.close()

    child = pexpect.spawn('x11vnc -sslGenCert server')
    child.logfile = sys.stdout 
    child.expect('Country Name \(2 letter code\) \[AU\]:')
    child.sendline('UK')
    child.expect('State or Province Name \(full name\) \[mystate\]:')
    child.sendline('')
    child.expect('Locality Name \(eg\, city\) \[\]:')
    child.sendline('')
    child.expect('Organization Name \(eg\, company\) \[x11vnc server\]')
    child.sendline('Cloud Calibre')
    child.expect('Organizational Unit Name \(eg\, section\) \[\]')
    child.sendline('Cloud Calibre Unit')
    child.expect('Common Name \(eg\, YOUR name\) \[x11vnc server\]:')
    child.sendline('root Cloud Calibre CA')
    child.expect('Email Address \[x11vnc\@server\.nowhere\]:') 
    child.sendline('cloud@example.com')
    child.expect('A challenge password \[\]:')
    child.sendline('')
    child.expect('An optional company name \[\]:')
    child.sendline('')
    child.expect('Protect key with a passphrase\?  y/n ')
    child.sendline('n')
    child.expect('Enter pass phrase for \.\/CA\/private\/cakey\.pem:')
    child.sendline(password)
    child.expect('Sign the certificate\? \[y\/n\]:')
    child.sendline('y')
    child.expect('1 out of 1 certificate requests certified\, commit\? \[y\/n\]')
    child.sendline('y')
    child.expect('Press Enter to print the server\.crt certificate to the screen: ')
    child.sendline('')
    child.expect(pexpect.EOF, timeout=600)
    child.close()


def setup_rc():
    pexpect_simple('cp /home/cloud/calibre-cloud-read-only/install/startvnc.sh /root/startvnc.sh')
    pexpect_simple('echo "/bin/bash /root/startvnc.sh &" > /etc/rc.local')

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:c:", ["password=", "clear="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        print "Invalid option"
        sys.exit(2)
    output = None
    verbose = False
    password_user = False
    for o, a in opts:
        if o in ("-p", "--password"):
            password_user = a
        elif o in ("-c", "--clear"):
            password_clear = a
        else:
            assert False, "unhandled option"
    if password_user:
        # set up stuff
        add_user_cloud(password_user)
        install_calibre()
        install_django_app(password_clear)
        setup_x11vnc(password_user)
        setup_rc()
        print "**** SETUP Ran with no errors ****"

if __name__ == "__main__":
    main()

